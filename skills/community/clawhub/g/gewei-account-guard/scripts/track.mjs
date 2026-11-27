#!/usr/bin/env node
import { parseArgs, fail, printJson } from './lib/cli.mjs';
import {
  getAnalyticsStatus,
  normalizeChannel,
  normalizeSurface,
  stableEventUuid,
  trackEvent,
} from './lib/analytics.mjs';
import { EVENT_NAMES, PLUGIN_ID } from './lib/identity.mjs';
import { getProduct } from './lib/links.mjs';
import {
  findBlock,
  getRunStateSnapshot,
  normalizeBlockId,
  normalizePlacement,
  readState,
  resolveRun,
  saveState,
  withStateLock,
} from './lib/run.mjs';

const MODES = new Set(['full', 'quick', 'unknown']);
const OUTCOMES = new Set(['success', 'partial', 'aborted', 'unknown']);

function pick(value, allowed, fallback = 'unknown') {
  const normalized = String(value || '').trim().toLowerCase();
  return allowed.has(normalized) ? normalized : fallback;
}

function nowIso() {
  return new Date().toISOString();
}

function gateStatus() {
  const status = getAnalyticsStatus();
  return {
    enabled: status.enabled,
    reason: status.disabled_reason || (status.opted_out ? 'opted_out' : 'not_configured'),
  };
}

// 锁超时/不可用时：去重关键路径宁可漏报一次（稍后可重试），也不无锁双发。
function lockTimeoutResult() {
  return {
    ok: false,
    skipped: true,
    reason: 'lock_timeout',
    state_lock: false,
    lock_timeout: true,
  };
}

function printHelp() {
  process.stdout.write([
    '用法:',
    '  node scripts/track.mjs loaded --agent qoder --mode full',
    '  node scripts/track.mjs complete --outcome success',
    '  node scripts/track.mjs shown --block-id blk_1a2b3c4d --links kh,zhinikefu',
    '  node scripts/track.mjs shown --block-id blk_1a2b3c4d',
    '  node scripts/track.mjs status --json',
    '',
    '说明:',
    `  loaded     记录 ${EVENT_NAMES.loaded}；同一插件同一 run 只记一次`,
    `  complete   记录 ${EVENT_NAMES.completed}；同一插件同一 run 只记一次`,
    `  shown      确认推荐区块已实际展示，按链接逐条记录 ${EVENT_NAMES.referralShown}`,
    '  status     查看统计配置、当前 run 和推荐区块状态',
    '  --mode     full | quick | unknown，默认 unknown',
    '  --outcome  success | partial | aborted | unknown，默认 unknown',
    '  --agent    qoder | claude-code | codex | 其他客户端标识，默认 unknown',
    '  --run-id   关联到指定调用（推荐传会话 ID）；省略时自动使用当前 run',
    '  --new-run  loaded 时强制新建 run；同一会话内不要重复使用',
    '  --block-id shown 必填，推荐区块 ID',
    '  --links    shown 时要确认的链接 ID，逗号分隔；省略表示区块内全部链接',
    '  --placement shown 时可覆盖区块的展示位置',
    '  --channel  来源渠道标识，默认读取 MATRIX_CHANNEL 或 GEWEI_CHANNEL',
    '  --surface  使用界面标识；loaded 默认 agent-skill，shown 默认 agent-response',
    '  --no-track 本次不发送事件；shown 时只做 dry-run，不写去重状态',
    '',
    '去重规则：',
    '  loaded / complete 按插件 + run 去重；重复执行返回 duplicate 跳过。',
    '  shown 按 run_id + block_id + link_id 去重；没有实际插入回答时不要调用。',
    '  并发执行同一条确认时，脚本会用本机锁串行化，只上报一次。',
    '  事件带稳定 uuid，超时重试不会在 PostHog 重复计数。',
    '  recommend.mjs 只生成区块，不发送任何事件。',
    '',
    '隔离规则：',
    '  不同插件互不影响，不会互相触发 duplicate；建议每个会话传稳定的',
    '  --run-id（或设置 MATRIX_SESSION_ID / GEWEI_SESSION_ID）以区分会话。',
    '  所有矩阵插件共用 track_id；PostHog 用 plugin_id 区分单个插件。',
    '  只发送匿名事件，不含聊天内容、微信号、手机号、截图或报告正文。',
    '',
    '开关规则：',
    '  统计默认关闭（opt-in）。发布者在 config/posthog.json 填入有效 Token 并',
    '  设置 "enabled": true 后才会发送；或用户显式设置 MATRIX_TELEMETRY=1。',
    '  设置 MATRIX_TELEMETRY=0、GEWEI_TELEMETRY=0 或 DO_NOT_TRACK=1 强制关闭。',
    '  拿不到本机状态锁时（lock_timeout）跳过本次上报，稍后重试不会重复计数。',
    '',
  ].join('\n'));
}

async function handleLoaded(flags, channel, surface) {
  if (flags['no-track']) return { ok: false, skipped: true, reason: 'no_track' };
  const gate = gateStatus();
  if (!gate.enabled) return { ok: false, skipped: true, reason: gate.reason };

  const mode = pick(flags.mode, MODES);
  const { locked, value } = await withStateLock(async () => {
    const { state, run, created, reused, persisted } = resolveRun({
      purpose: 'load',
      runId: flags['run-id'],
      newRun: flags['new-run'] === true,
      mode,
      pluginId: PLUGIN_ID,
    });

    if (run.loaded_sent) {
      return {
        ok: true,
        skipped: true,
        reason: 'duplicate_loaded',
        event: EVENT_NAMES.loaded,
        run_id: run.run_id,
        created,
        reused,
        state_persisted: persisted,
      };
    }

    const eventMode = mode === 'unknown' ? run.mode : mode;
    const eventUuid = stableEventUuid(PLUGIN_ID, EVENT_NAMES.loaded, run.run_id);
    const result = await trackEvent(EVENT_NAMES.loaded, { mode: eventMode }, {
      channel,
      surface,
      agent: flags.agent,
      runId: run.run_id,
      eventUuid,
    });

    if (result.ok) {
      run.loaded_sent = true;
      if (eventMode !== 'unknown') run.mode = eventMode;
      run.last_seen_at = nowIso();
    }
    const saved = result.ok ? saveState(state) : persisted;
    return {
      ...result,
      run_id: run.run_id,
      created,
      reused,
      duplicate: false,
      state_persisted: saved,
    };
  }, { requireLock: true });
  if (value === null) return lockTimeoutResult();
  return { ...value, state_lock: locked };
}

async function handleComplete(flags, channel, surface) {
  if (flags['no-track']) return { ok: false, skipped: true, reason: 'no_track' };
  const gate = gateStatus();
  if (!gate.enabled) return { ok: false, skipped: true, reason: gate.reason };

  const outcome = pick(flags.outcome, OUTCOMES);
  const { locked, value } = await withStateLock(async () => {
    const { state, run, created, reused, persisted } = resolveRun({
      purpose: 'complete',
      runId: flags['run-id'],
      mode: 'unknown',
      pluginId: PLUGIN_ID,
    });

    if (run.completed_sent) {
      return {
        ok: true,
        skipped: true,
        reason: 'duplicate_completed',
        event: EVENT_NAMES.completed,
        run_id: run.run_id,
        created,
        reused,
        state_persisted: persisted,
      };
    }

    const eventUuid = stableEventUuid(PLUGIN_ID, EVENT_NAMES.completed, run.run_id);
    const result = await trackEvent(EVENT_NAMES.completed, { outcome }, {
      channel,
      surface,
      agent: flags.agent,
      runId: run.run_id,
      eventUuid,
    });

    if (result.ok) {
      run.completed_sent = true;
      run.completed_at = nowIso();
      run.last_seen_at = run.completed_at;
    }
    const saved = result.ok ? saveState(state) : persisted;
    return {
      ...result,
      run_id: run.run_id,
      created,
      reused,
      duplicate: false,
      state_persisted: saved,
    };
  }, { requireLock: true });
  if (value === null) return lockTimeoutResult();
  return { ...value, state_lock: locked };
}

function parseLinkIds(value) {
  if (value === undefined || value === true) return [];
  const out = [];
  for (const raw of String(value).split(',')) {
    const id = raw.trim().toLowerCase();
    if (!id) continue;
    if (!/^[a-z0-9][a-z0-9_-]{0,31}$/.test(id)) return null;
    if (!out.includes(id)) out.push(id);
  }
  return out;
}

function printShownSummary(result) {
  const sent = Array.isArray(result.sent) ? result.sent : [];
  const duplicates = Array.isArray(result.duplicates) ? result.duplicates : [];
  const failed = Array.isArray(result.failed) ? result.failed : [];
  const skippedLinks = Array.isArray(result.skipped_links) ? result.skipped_links : [];
  const wouldSend = Array.isArray(result.would_send) ? result.would_send : [];

  const parts = [];
  if (result.dry_run) {
    parts.push(`dry-run：未发送事件，待确认 ${wouldSend.length} 条`);
  } else if (result.skipped) {
    parts.push(`未发送事件：${result.reason}`);
  } else if (sent.length) {
    parts.push(`已确认并上报 ${sent.length} 条链接展示`);
  } else {
    parts.push('没有新增展示事件');
  }
  if (duplicates.length) parts.push(`跳过已确认 ${duplicates.length} 条`);
  if (failed.length) parts.push(`发送失败 ${failed.length} 条`);
  if (skippedLinks.length) parts.push(`跳过 ${skippedLinks.length} 条`);
  process.stdout.write(`[shown] ${parts.join('；')}\n`);
}

async function handleShown(flags, channel, surface) {
  if (!flags['block-id']) fail('缺少 --block-id；请先运行 recommend.mjs 生成推荐区块');
  const blockId = normalizeBlockId(flags['block-id']);
  if (!blockId) fail('--block-id 格式不合法；只能包含小写字母、数字、下划线和短横线');

  // dry-run 只读状态，不参与锁，也不阻塞其他并发确认。
  if (flags['no-track']) {
    const state = readState();
    const found = findBlock(state, blockId);
    if (!found) {
      fail(`没有找到推荐区块 ${blockId}；请先运行 recommend.mjs，不要手工构造展示事件`);
    }
    const { run, block } = found;
    const validIds = block.links.map((link) => link.id);
    const requested = flags.links === undefined ? validIds.slice() : parseLinkIds(flags.links);
    if (!requested || !requested.length) fail('--links 格式不合法；请传产品/链接 ID 逗号列表');
    const unknown = requested.filter((id) => !validIds.includes(id) || !getProduct(id));
    if (unknown.length) {
      fail(`以下链接不属于该推荐区块：${unknown.join(', ')}；可选：${validIds.join(', ')}`);
    }
    return {
      event: EVENT_NAMES.referralShown,
      run_id: run.run_id,
      block_id: block.block_id,
      placement: block.placement,
      requested_links: requested,
      sent: [],
      duplicates: requested.filter((id) => block.shown_link_ids.includes(id)),
      failed: [],
      skipped_links: [],
      dry_run: true,
      ok: true,
      skipped: false,
      would_send: requested.filter((id) => !block.shown_link_ids.includes(id)),
      events: 0,
      state_persisted: true,
    };
  }

  const { locked, value } = await withStateLock(async () => {
    // 锁内重新读状态：并发进程可能刚刚确认过这些链接。
    const state = readState();
    const found = findBlock(state, blockId);
    if (!found) return { missing: true };
    const { run, block } = found;
    const validIds = block.links.map((link) => link.id);

    let requested;
    if (flags.links === undefined) {
      requested = validIds.slice();
    } else {
      requested = parseLinkIds(flags.links);
      if (!requested || !requested.length) return { invalid: true };
    }

    const unknown = requested.filter((id) => !validIds.includes(id) || !getProduct(id));
    if (unknown.length) return { unknown, validIds };

    let placement = block.placement;
    if (flags.placement !== undefined) {
      placement = normalizePlacement(flags.placement);
      if (placement === 'unknown' && String(flags.placement).trim().toLowerCase() !== 'unknown') {
        return { invalidPlacement: true };
      }
      block.placement = placement;
    }

    const duplicates = requested.filter((id) => block.shown_link_ids.includes(id));
    const pending = requested.filter((id) => !block.shown_link_ids.includes(id));
    const base = {
      event: EVENT_NAMES.referralShown,
      run_id: run.run_id,
      block_id: block.block_id,
      placement,
      requested_links: requested,
      sent: [],
      duplicates,
      failed: [],
      skipped_links: [],
      dry_run: false,
      events: 0,
    };

    if (!pending.length) {
      run.last_seen_at = nowIso();
      const persisted = saveState(state);
      return { done: { ...base, ok: true, state_persisted: persisted } };
    }

    const gate = gateStatus();
    if (!gate.enabled) {
      return {
        done: {
          ...base,
          ok: false,
          skipped: true,
          reason: gate.reason,
          would_send: pending,
          state_persisted: true,
        },
      };
    }

    const linkTotal = block.links.length;
    const needsCount = block.needs.length;
    for (const linkId of pending) {
      const product = getProduct(linkId);
      const link = block.links.find((entry) => entry.id === linkId);
      const eventUuid = stableEventUuid(
        PLUGIN_ID,
        EVENT_NAMES.referralShown,
        run.run_id,
        block.block_id,
        linkId,
      );
      const result = await trackEvent(EVENT_NAMES.referralShown, {
        mode: block.mode,
        placement,
        block_id: block.block_id,
        product_id: product.id,
        product_title: product.title,
        product_kind: product.kind,
        link_id: product.id,
        link_host: new URL(product.target).hostname,
        link_index: link.link_index,
        link_total: linkTotal,
        product_count: linkTotal,
        needs_count: needsCount,
      }, {
        channel,
        surface,
        agent: flags.agent,
        runId: run.run_id,
        eventUuid,
      });

      if (result.ok) {
        block.shown_link_ids.push(linkId);
        base.sent.push(linkId);
      } else if (result.skipped) {
        base.skipped_links.push({ link_id: linkId, reason: result.reason });
      } else {
        base.failed.push({
          link_id: linkId,
          status: result.status,
          error: result.error,
        });
      }
    }

    base.events = base.sent.length;
    base.ok = base.failed.length === 0 && base.skipped_links.length === 0;
    run.last_seen_at = nowIso();
    const persisted = saveState(state);
    return { done: { ...base, state_persisted: persisted } };
  }, { requireLock: true });

  if (value === null) return lockTimeoutResult();
  if (value.missing) {
    fail(`没有找到推荐区块 ${blockId}；请先运行 recommend.mjs，不要手工构造展示事件`);
  }
  if (value.invalid) fail('--links 格式不合法；请传产品/链接 ID 逗号列表');
  if (value.invalidPlacement) fail('--placement 不合法；请使用文档中的展示位置');
  if (value.unknown) {
    fail(`以下链接不属于该推荐区块：${value.unknown.join(', ')}；可选：${value.validIds.join(', ')}`);
  }
  if (!value.done) {
    // 防御：锁内出现未预期的返回值时按跳过处理，避免上层访问字段崩溃。
    return lockTimeoutResult();
  }
  return { ...value.done, state_lock: locked };
}

async function main() {
  const { positionals, flags } = parseArgs(process.argv.slice(2), {
    booleans: ['json', 'help', 'no-track', 'new-run'],
  });
  const command = positionals[0] || 'help';

  if (flags.help || command === 'help') {
    printHelp();
    return;
  }

  if (command === 'status') {
    printJson({
      ...getAnalyticsStatus(),
      run_state: getRunStateSnapshot(),
    });
    return;
  }

  const channel = normalizeChannel(flags.channel);
  const surface = normalizeSurface(
    flags.surface,
    command === 'shown' ? 'agent-response' : 'agent-skill',
  );

  let result = null;
  if (command === 'loaded' || command === 'start') {
    result = await handleLoaded(flags, channel, surface);
  } else if (command === 'complete') {
    result = await handleComplete(flags, channel, surface);
  } else if (command === 'shown' || command === 'confirm-shown') {
    result = await handleShown(flags, channel, surface);
  } else {
    process.stderr.write(`未知命令：${command}\n`);
    process.stderr.write('可用命令：loaded、complete、shown、status（start 兼容旧版）\n');
    process.exitCode = 1;
    return;
  }

  if (flags.json) {
    printJson(result);
  } else if (command === 'shown' || command === 'confirm-shown') {
    printShownSummary(result);
  }
}

main();
