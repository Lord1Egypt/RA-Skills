#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn, spawnSync } from 'node:child_process';
import { getFeishuMessage, resolveFeishuConfig, sendFeishuText } from './feishu-client.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(process.env.HOME || '.', '.openclaw', 'workspace', 'douyin-ops');
const WATCH_STATE_PATH = process.env.DOUYIN_FEISHU_WATCH_STATE || join(STATE_DIR, 'feishu-reply-watcher-state.json');
const MARKETING_STATE_PATH = process.env.DOUYIN_MARKETING_STATE_PATH || join(STATE_DIR, 'automation-marketing-state.json');
const UPSTREAM_CACHE_DIR = process.env.DOUYIN_FEISHU_UPSTREAM_CACHE_DIR || join(STATE_DIR, 'upstream');

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) continue;
    const key = item.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) args[key] = true;
    else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function loadJob(jobPath) {
  return JSON.parse(readFileSync(jobPath, 'utf8'));
}

function saveJob(jobPath, patch) {
  const current = existsSync(jobPath) ? loadJob(jobPath) : {};
  const next = {
    ...current,
    ...patch,
    updatedAt: new Date().toISOString(),
  };
  mkdirSync(dirname(jobPath), { recursive: true });
  writeFileSync(jobPath, `${JSON.stringify(next, null, 2)}\n`);
  return next;
}

function runNode(args, opts = {}) {
  const result = spawnSync(process.execPath, args, {
    cwd: join(__dirname, '..'),
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: Number(opts.timeout || 3_600_000),
  });
  return {
    ok: result.status === 0,
    status: result.status,
    signal: result.signal,
    output: `${result.stderr || ''}${result.stdout || ''}`.trim(),
  };
}

function runNodeAsync(args, opts = {}) {
  return new Promise((resolve) => {
    const child = spawn(process.execPath, args, {
      cwd: join(__dirname, '..'),
      stdio: ['ignore', 'pipe', 'pipe'],
      env: { ...process.env, ...(opts.env || {}) },
    });
    const maxBuffer = Number(opts.maxBuffer || 2_000_000);
    const chunks = [];
    const startedAt = Date.now();
    let settled = false;
    let timedOut = false;
    let timer = null;

    function append(chunk) {
      chunks.push(Buffer.from(chunk));
      let total = chunks.reduce((sum, item) => sum + item.length, 0);
      while (total > maxBuffer && chunks.length > 1) {
        total -= chunks.shift().length;
      }
    }

    function finish(status, signal, error) {
      if (settled) return;
      settled = true;
      if (timer) clearTimeout(timer);
      const output = Buffer.concat(chunks).toString('utf8').trim();
      resolve({
        ok: status === 0 && !timedOut,
        status,
        signal,
        error,
        timedOut,
        elapsedMs: Date.now() - startedAt,
        output,
      });
    }

    child.stdout.on('data', append);
    child.stderr.on('data', append);
    child.on('error', (err) => finish(null, null, err.message));
    child.on('close', (status, signal) => finish(status, signal, null));

    const timeoutMs = Number(opts.timeout || 3_600_000);
    if (timeoutMs > 0) {
      timer = setTimeout(() => {
        timedOut = true;
        child.kill('SIGTERM');
        setTimeout(() => {
          if (!settled) child.kill('SIGKILL');
        }, 5000).unref();
      }, timeoutMs);
      timer.unref();
    }
  });
}

function parseJsonObjects(text) {
  const objects = [];
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;
  for (let i = 0; i < text.length; i += 1) {
    const ch = text[i];
    if (inString) {
      if (escaped) escaped = false;
      else if (ch === '\\') escaped = true;
      else if (ch === '"') inString = false;
      continue;
    }
    if (ch === '"') inString = true;
    else if (ch === '{') {
      if (depth === 0) start = i;
      depth += 1;
    } else if (ch === '}') {
      depth -= 1;
      if (depth === 0 && start >= 0) {
        try {
          objects.push(JSON.parse(text.slice(start, i + 1)));
        } catch {
          // Ignore logger text.
        }
        start = -1;
      }
    }
  }
  return objects;
}

function parseLastJson(text) {
  const items = parseJsonObjects(String(text || ''));
  return items.at(-1) || null;
}

function compactOutput(text, max = 5000) {
  const raw = String(text || '');
  return raw.length > max ? raw.slice(-max) : raw;
}

function readJson(path, fallback = {}) {
  try {
    if (!existsSync(path)) return fallback;
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return fallback;
  }
}

function writeJson(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`);
}

function startPublishHeartbeat(jobPath) {
  return setInterval(() => {
    saveJob(jobPath, {
      status: 'running',
      stage: 'publishing',
      heartbeatAt: new Date().toISOString(),
    });
  }, 10_000);
}

function markWatcherWaitingPublishSms(jobPath, title, taskPath) {
  const current = readJson(WATCH_STATE_PATH, { seen: {}, lastCreateTime: 0, pendingVideo: null, flow: null });
  writeJson(WATCH_STATE_PATH, {
    ...current,
    flow: {
      active: true,
      step: 'waiting_publish_sms',
      startedAt: current.flow?.startedAt || Date.now(),
      updatedAt: Date.now(),
    },
    pendingUpstreamTask: {
      ...(current.pendingUpstreamTask || {}),
      taskPath,
      title,
    },
    pendingPublish: {
      ...(current.pendingPublish || {}),
      title,
      taskPath,
      publishJobPath: jobPath,
    },
    lastSmsCode: null,
    updatedAt: new Date().toISOString(),
  });
}

function markMarketingPublished(title, publishPayload, taskPath) {
  const current = readJson(MARKETING_STATE_PATH, {});
  const dailyTime = current.schedule?.dailyTime || process.env.DOUYIN_DEFAULT_DAILY_TIME || '07:30';
  const scheduleConfigPath = join(STATE_DIR, 'schedule-config.json');
  const scheduleConfig = readJson(scheduleConfigPath, { version: 1, enabled: true, jobs: {} });
  writeJson(scheduleConfigPath, {
    ...scheduleConfig,
    enabled: true,
    jobs: {
      ...(scheduleConfig.jobs || {}),
      autoReply: {
        enabled: true,
        schedule: scheduleConfig.jobs?.autoReply?.schedule || { kind: 'every', every: '30m' },
      },
      dailyReport: {
        enabled: false,
        schedule: scheduleConfig.jobs?.dailyReport?.schedule || { kind: 'daily', time: dailyTime, tz: process.env.DOUYIN_SCHEDULE_TZ || 'Asia/Shanghai' },
      },
      marketingDaily: {
        enabled: true,
        schedule: { kind: 'daily', time: dailyTime, tz: process.env.DOUYIN_SCHEDULE_TZ || 'Asia/Shanghai' },
      },
    },
  });
  writeJson(MARKETING_STATE_PATH, {
    ...current,
    enabled: true,
    enabledAt: current.enabledAt || new Date().toISOString(),
    schedule: { ...(current.schedule || {}), dailyTime },
    pendingReview: null,
    inFlightVideo: null,
    lastRun: {
      ...(current.lastRun || {}),
      status: 'published',
      finishedAt: new Date().toISOString(),
      stage: 'published_verified',
      title,
      taskPath,
      publishPayload,
      checkedAt: new Date().toISOString(),
    },
    updatedAt: new Date().toISOString(),
  });
}

function scheduleStatusMessage() {
  const result = runNode(['scripts/douyin-schedule-manager.js', 'status'], { timeout: 30000 });
  const payload = parseLastJson(result.output);
  return payload?.customerMessage || '定时任务已开启。';
}

function publishSuccessMessage(title) {
  const publishLine = title
    ? `老板，《${title}》视频投放成功，快去抖音查看吧！`
    : '老板，视频投放成功，快去抖音查看吧！';
  return `${publishLine}\n\n${scheduleStatusMessage()}`;
}

function publishLooksSuccessful(publishPayload, title) {
  return Boolean(
    publishPayload?.ok === true
    && publishPayload?.stage === 'verified'
    && publishPayload?.verify?.found === true
    && (!title || publishPayload.verify.title === title || publishPayload.verify.textSample?.includes?.(title))
  );
}

function failMessage(payload) {
  const text = JSON.stringify(payload || {});
  if (/publish_verification_required|publish_sms|发布需要短信验证|为确保是本人操作抖音账号/i.test(text)) {
    return '抖音发布需要短信验证。请直接回复 6 位验证码。';
  }
  if (/ProtocolError|protocolTimeout|Runtime\.callFunctionOn timed out|Network\.enable timed out|Target closed|Session closed|WebSocket/i.test(text)) {
    return '发布页面控制超时，我已保留当前草稿并会尝试恢复。请稍后回复：发布视频';
  }
  if (/upload_timeout|editor_in_progress|upload_page_timeout|hd_publish_btn_not_found|editor_navigation_blocked|publish_editor_not_ready|publish_btn_not_found|publish_btn_obstructed|publish_btn_disabled|publish_submit_unconfirmed|publish_click_returned_to_upload/i.test(text)) {
    return '发布页面未准备好，我已保留素材。请稍后回复：发布视频';
  }
  if (/cover|封面/i.test(text)) return '封面设置失败，请重新发送可用的封面图片。';
  if (/video|upload|file|视频|上传/i.test(text)) return '视频处理失败，请重新发送可用的视频。';
  if (/login|session|登录/i.test(text)) {
    return '抖音需要重新登录。\n请在电脑端打开飞书，用手机抖音 App 准备扫码。\n准备好后回复：发送二维码';
  }
  return '发布失败，请重新发送可用的视频和封面。';
}

async function notifyIfRequested(jobPath, message, patch = {}) {
  const current = existsSync(jobPath) ? loadJob(jobPath) : {};
  if (!current.notify) return null;
  try {
    let target = current.feishuTarget?.receiveId ? current.feishuTarget : null;
    if (!target && current.sourceMessageId) {
      const sourceMessage = await getFeishuMessage(current.sourceMessageId).catch(() => null);
      if (sourceMessage?.chat_id) {
        target = { receiveId: sourceMessage.chat_id, receiveIdType: 'chat_id' };
        saveJob(jobPath, { feishuTarget: target });
      }
    }
    const result = await sendFeishuText(message, target ? resolveFeishuConfig({
      receiveId: target.receiveId,
      receiveIdType: target.receiveIdType || 'chat_id',
    }) : resolveFeishuConfig());
    saveJob(jobPath, {
      ...patch,
      notifyResult: result,
      notifiedAt: new Date().toISOString(),
    });
    return result;
  } catch (err) {
    saveJob(jobPath, {
      ...patch,
      notifyResult: { ok: false, error: err.message },
      notifyFailedAt: new Date().toISOString(),
    });
    return { ok: false, error: err.message };
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.job) {
    console.error('Usage: node scripts/publish-upstream-job-worker.js --job /abs/job.json');
    process.exit(2);
  }

  const jobPath = args.job;
  const job = saveJob(jobPath, { status: 'running', stage: 'prepare', startedAt: new Date().toISOString() });
  const taskPath = job.taskPath;
  const inputPath = job.inputPath;

  let preparedPayload = null;
  if (args.skipPrepare) {
    preparedPayload = { ok: true, skipped: true };
    saveJob(jobPath, { stage: 'prepared', prepared: preparedPayload });
  } else {
    const prepared = runNode([
      'scripts/prepare-upstream-publish-task.js',
      '--input',
      inputPath,
      '--output',
      taskPath,
      '--cache-dir',
      UPSTREAM_CACHE_DIR,
    ], { timeout: 180000 });
    preparedPayload = parseLastJson(prepared.output);
    saveJob(jobPath, {
      stage: 'prepared',
      prepared: preparedPayload || { ok: prepared.ok, output: compactOutput(prepared.output) },
    });
    if (!prepared.ok || !preparedPayload?.ok) {
      const customerMessage = preparedPayload?.customerMessage || '素材处理失败，请重新发送可用的视频和封面。';
      saveJob(jobPath, {
        status: 'failed',
        stage: 'prepare_failed',
        customerMessage,
        error: preparedPayload || compactOutput(prepared.output),
        finishedAt: new Date().toISOString(),
      });
      await notifyIfRequested(jobPath, customerMessage);
      process.exit(1);
    }
  }

  if (process.env.DOUYIN_TEST_FAKE_PUBLISH_SUCCESS === 'true') {
    const title = job.title || preparedPayload?.validation?.normalized?.title || '测试发布成功';
    const publishPayload = {
      ok: true,
      stage: 'verified',
      plan: { title },
      verify: { found: true, title },
      fake: true,
    };
    markMarketingPublished(title, publishPayload, taskPath);
    const customerMessage = publishSuccessMessage(title);
    saveJob(jobPath, {
      status: 'succeeded',
      stage: 'verified',
      customerMessage,
      publish: publishPayload,
      finishedAt: new Date().toISOString(),
    });
    await notifyIfRequested(jobPath, customerMessage);
    return;
  }

  saveJob(jobPath, { stage: 'publishing', publishStartedAt: new Date().toISOString() });
  const publishTimer = startPublishHeartbeat(jobPath);
  const publish = await runNodeAsync([
    'scripts/publish-task.js',
    '--task',
    taskPath,
    '--execute',
  ], { timeout: Number(job.publishTimeoutMs || process.env.DOUYIN_PUBLISH_JOB_TIMEOUT_MS || 3_900_000) });
  clearInterval(publishTimer);
  const publishPayload = parseLastJson(publish.output);
  const title = publishPayload?.plan?.title || preparedPayload?.validation?.normalized?.title || '';
  if (!publish.ok || !publishLooksSuccessful(publishPayload, title)) {
    const text = JSON.stringify(publishPayload || publish.output || {});
    if (/publish_verification_required|publish_sms|为确保是本人操作抖音账号/i.test(text)) {
      const customerMessage = '抖音发布需要短信验证。请直接回复 6 位验证码。';
      markWatcherWaitingPublishSms(jobPath, title, taskPath);
      saveJob(jobPath, {
        status: 'blocked',
        stage: 'waiting_publish_sms',
        customerMessage,
        publish: publishPayload || { ok: publish.ok, output: compactOutput(publish.output) },
        finishedAt: new Date().toISOString(),
      });
      await notifyIfRequested(jobPath, customerMessage);
      process.exit(0);
    }
    const customerMessage = publishPayload?.customerMessage || failMessage(publishPayload || publish.output);
    saveJob(jobPath, {
      status: 'failed',
      stage: publishPayload?.stage || 'publish_failed',
      customerMessage,
      publish: publishPayload || { ok: publish.ok, output: compactOutput(publish.output) },
      finishedAt: new Date().toISOString(),
    });
    await notifyIfRequested(jobPath, customerMessage);
    process.exit(1);
  }

  markMarketingPublished(title, publishPayload, taskPath);
  const customerMessage = publishSuccessMessage(title);
  saveJob(jobPath, {
    status: 'succeeded',
    stage: 'verified',
    customerMessage,
    publish: publishPayload,
    finishedAt: new Date().toISOString(),
  });
  await notifyIfRequested(jobPath, customerMessage);
}

main().catch(async (err) => {
  const args = parseArgs(process.argv.slice(2));
  if (args.job) {
    const customerMessage = '发布失败，请稍后重试。';
    saveJob(args.job, {
      status: 'failed',
      stage: 'crashed',
      customerMessage,
      error: err.message,
      stack: err.stack,
      finishedAt: new Date().toISOString(),
    });
    await notifyIfRequested(args.job, customerMessage).catch(() => null);
  } else {
    console.error(err.stack || err.message);
  }
  process.exit(1);
});
