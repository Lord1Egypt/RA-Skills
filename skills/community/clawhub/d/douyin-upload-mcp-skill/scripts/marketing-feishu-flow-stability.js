#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

const ROOT = new URL('..', import.meta.url).pathname;
const DEFAULT_BASE_DIR = '/tmp/douyin-marketing-feishu-flow-stability';

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

function parseJsonObjects(text) {
  const objects = [];
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;
  const raw = String(text || '');
  for (let i = 0; i < raw.length; i += 1) {
    const ch = raw[i];
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
          objects.push(JSON.parse(raw.slice(start, i + 1)));
        } catch {
          // Ignore log fragments.
        }
        start = -1;
      }
    }
  }
  return objects;
}

function readJson(path, fallback = null) {
  try {
    if (!existsSync(path)) return fallback;
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return fallback;
  }
}

function readJsonl(path) {
  if (!existsSync(path)) return [];
  return readFileSync(path, 'utf8')
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

function personaText(round) {
  return [
    `姓名：张琳${round}`,
    `照片：https://example.com/person-${round}.jpg`,
    '性别：女',
    '年龄：34',
    '从业年限：8年',
    '主营业务：宠物保险顾问服务，帮助养宠家庭选择合适保障',
    '核心优势：熟悉理赔流程，能把复杂条款讲清楚，案例经验丰富',
    '目标客户：一二线城市新手养宠家庭，担心宠物看病贵但不知道怎么买保险',
    '个人特质：亲和、专业、说话直接',
    '经验案例：服务过300多个养宠家庭，处理过多类理赔咨询',
    'IP核心诉求：通过抖音建立专业信任，引导客户咨询宠物保险',
    '禁忌与偏好：不夸大收益，不承诺一定理赔，表达要合规清晰',
  ].join('\n');
}

function commandSpec(round, startText = '启动自动化营销') {
  return [
    { text: startText, expectAction: 'persona_initial_collect_needed', expectText: /^老板好~✨ 打造个人IP，最关键的是打造无可替代的差异化人设，坚决❌拒绝千篇一律的流水线包装，绝不盲目跟风。\n为了让您的IP既有“辨识度”又有“信任感”，请您提供姓名\/昵称、性别、照片、从业\/深耕年限、核心业务、核心优势、目标客户、个人特质信息、过往相关经验\/案例、IP核心诉求、禁忌与偏好等信息～$/ },
    { text: personaText(round), expectAction: 'persona_generation_deferred', expectText: /老板，您的专属人设信息已完成[\s\S]*回复【通过】或【不通过】/ },
    { text: '不通过 需要更专业、更有差异化，突出保险避坑专家定位', expectAction: 'persona_generation_deferred', expectText: /老板，您的专属人设信息已完成[\s\S]*回复【通过】或【不通过】/ },
    { text: '通过', expectAction: 'persona_confirmed', expectText: /^老板，我将基于原图照片和人设信息为您定制专属数字人形象，请稍等片刻~\n老板，您的数字人形象已完成定制，正在为您制作视频，请耐心等待～\n老板，您的视频制作完成！请您审核：[\s\S]*回复【确认发布】或【不通过】/, expectMessageCount: 3 },
    { text: '不通过 口播太短，重新生成', expectAction: 'marketing_video_regeneration_started_light_test', expectText: /^老板，收到修改意见，正在重新制作视频，请稍等～$/ },
    { text: '确认发布', expectAction: 'publish_pending_review_dry_run', expectText: /^$/, expectMessageCount: 0 },
    { text: '数据报告', expectAction: 'report_douyin_data_light_test', expectText: /^老板，昨日数据报告如下，请您查收～\n数据报告：已同步近 90 天作品明细 0 条。/ },
    { text: '自动回复', expectAction: 'auto_reply_both_light_test', expectText: /^自动回复完成：评论 0 条，私信 0 条。$/ },
    { text: '自动化营销状态', expectAction: 'marketing_status', expectText: /自动化营销：未开启/ },
  ];
}

function runRoute(text, env, index) {
  const result = spawnSync(process.execPath, [
    'scripts/feishu-reply-watcher.js',
    'route-text',
    '--text',
    text,
    '--dry-run',
    '--chat-id',
    'oc_stability_test',
    '--message-id',
    `manual_stability_${Date.now()}_${index}`,
  ], {
    cwd: ROOT,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: 240000,
    env,
  });
  const output = `${result.stderr || ''}${result.stdout || ''}`.trim();
  return {
    status: result.status,
    ok: result.status === 0,
    output,
    payload: parseJsonObjects(output).at(-1) || null,
    stdoutTail: String(result.stdout || '').slice(-1000),
    stderrTail: String(result.stderr || '').slice(-1000),
  };
}

function writeStaleDigitalHumanState(stateDir) {
  const staleConfirmedAt = '2026-01-01T00:00:00.000Z';
  writeFileSync(join(stateDir, 'digital-human-state.json'), `${JSON.stringify({
    version: 2,
    status: 'succeeded',
    lastJob: {
      bizId: 'stale-training-job',
      status: 'succeeded',
      createdAt: staleConfirmedAt,
      updatedAt: staleConfirmedAt,
      personaSnapshot: {
        confirmed: true,
        confirmedAt: staleConfirmedAt,
        fingerprint: {
          confirmed: true,
          confirmedAt: staleConfirmedAt,
          name: '旧人设',
          photo: 'https://example.com/old.jpg',
        },
      },
      digitalHumanBizId: 'STALE_OLD_MODEL_SHOULD_NOT_REUSE',
      dryRun: true,
    },
  }, null, 2)}\n`);
  writeFileSync(join(stateDir, 'automation-marketing-state.json'), `${JSON.stringify({
    version: 1,
    enabled: false,
    publishMode: 'manual_confirm',
    confirmationMode: 'manual',
    schedule: { dailyTime: '07:30' },
    digitalHuman: {
      modelId: 'STALE_OLD_MODEL_SHOULD_NOT_REUSE',
      source: 'trained',
      trainingTaskBizId: 'stale-training-job',
      personaConfirmedAt: staleConfirmedAt,
      personaFingerprint: {
        confirmed: true,
        confirmedAt: staleConfirmedAt,
        name: '旧人设',
        photo: 'https://example.com/old.jpg',
      },
      confirmedAt: staleConfirmedAt,
      boundAt: staleConfirmedAt,
    },
  }, null, 2)}\n`);
}

function customerTexts(logPath, previousCount) {
  return readJsonl(logPath).slice(previousCount).filter((item) => item.type === 'text').map((item) => item.text);
}

function waitForMessages(logPath, previousCount, minCount = 1, timeoutMs = 30000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const messages = customerTexts(logPath, previousCount);
    if (messages.length >= minCount) return messages;
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 250);
  }
  return customerTexts(logPath, previousCount);
}

function waitForExpectedMessages(logPath, previousCount, spec, timeoutMs = 90000) {
  const minCount = spec.minMessageCount ?? spec.expectMessageCount ?? 1;
  if (minCount === 0) {
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 600);
    return customerTexts(logPath, previousCount);
  }
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const messages = customerTexts(logPath, previousCount);
    const combined = messages.join('\n');
    if (messages.length >= minCount && (!spec.expectText || spec.expectText.test(combined))) return messages;
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 250);
  }
  return waitForMessages(logPath, previousCount, minCount, 1);
}

function leakedInternal(text) {
  return /stack|TypeError|ReferenceError|SyntaxError|node:|at\s+\w+|HTTP \d{3}|undefined|null/i.test(text);
}

function validateStep(spec, run, messages) {
  const issues = [];
  const result = run.payload?.result || {};
  const action = result.video?.payload?.action || result.next?.payload?.action || result.payload?.action || result.action;
  const combined = messages.join('\n');
  const minMessageCount = spec.minMessageCount ?? spec.expectMessageCount ?? 1;
  if (!run.ok || !run.payload?.ok) issues.push('route_failed');
  if (action !== spec.expectAction) issues.push(`unexpected_action:${action || 'none'}`);
  if (messages.length < minMessageCount) issues.push(`unexpected_message_count:${messages.length}`);
  if (spec.expectMessageCount !== undefined && messages.length !== spec.expectMessageCount) issues.push(`unexpected_message_count:${messages.length}`);
  if (!spec.expectText.test(combined)) issues.push('unexpected_customer_text');
  if (/每日自动化营销已设定|定时任务/.test(combined)) issues.push('schedule_text_leaked');
  if (/内容较长，已截断|完整版本已保存在 persona-state\.json/.test(combined)) issues.push('persona_truncated_notice_leaked');
  if (leakedInternal(combined)) issues.push('internal_detail_leaked');
  return {
    text: spec.text.includes('\n') ? 'persona-fields' : spec.text,
    action,
    messages,
    pass: issues.length === 0,
    issues,
    payload: run.payload,
  };
}

function validateFinalState(stateDir) {
  const marketing = readJson(join(stateDir, 'automation-marketing-state.json'), {});
  const persona = readJson(join(stateDir, 'persona-state.json'), {});
  const digitalHuman = readJson(join(stateDir, 'digital-human-state.json'), {});
  const issues = [];
  if (!persona.confirmed) issues.push('persona_not_confirmed');
  if (marketing.enabled) issues.push('marketing_enabled_before_first_publish_success');
  if (!marketing.digitalHuman?.modelId) issues.push('model_not_set');
  if (marketing.digitalHuman?.modelId === 'STALE_OLD_MODEL_SHOULD_NOT_REUSE') issues.push('stale_model_reused');
  if (digitalHuman.lastJob?.bizId === 'stale-training-job') issues.push('stale_training_job_not_replaced');
  if (marketing.digitalHuman?.personaFingerprint?.confirmedAt && persona.confirmed?.confirmedAt && marketing.digitalHuman.personaFingerprint.confirmedAt !== persona.confirmed.confirmedAt) {
    issues.push('model_persona_mismatch');
  }
  if (!/^(default|trained_dry_run)/.test(String(marketing.digitalHuman?.source || ''))) issues.push(`model_source:${marketing.digitalHuman?.source || 'none'}`);
  if (marketing.pendingPlan) issues.push('pending_plan_not_cleared');
  if (marketing.pendingReview) issues.push('pending_review_not_cleared');
  if (marketing.lastRun?.status !== 'submitted') issues.push(`last_run_status:${marketing.lastRun?.status || 'none'}`);
  if (marketing.videoRevisionFeedback !== '口播太短，重新生成') issues.push('video_revision_feedback_not_recorded');
  const reportsDir = join(stateDir, 'reports');
  const reportFiles = existsSync(reportsDir)
    ? spawnSync('find', [reportsDir, '-maxdepth', '1', '-name', 'marketing-*-xiaoice-input.json', '-print'], { encoding: 'utf8' }).stdout.trim().split(/\r?\n/).filter(Boolean)
    : [];
  for (const file of reportFiles) {
    const input = readJson(file, {});
    const visualTitle = input.videoTitle || input.visualTitle || input.digitalHumanInput?.videoTitle || '';
    if (Array.from(String(visualTitle)).length > 8) issues.push(`visual_title_too_long:${visualTitle}`);
    if (/[：:]/.test(String(visualTitle))) issues.push(`visual_title_contains_colon:${visualTitle}`);
  }
  return { pass: issues.length === 0, issues, marketing, persona, digitalHuman, reportFiles };
}

function runRound(round, baseDir) {
  const stateDir = join(baseDir, `round-${round}`);
  rmSync(stateDir, { recursive: true, force: true });
  mkdirSync(stateDir, { recursive: true });
  const logPath = join(stateDir, 'feishu-dry-run.jsonl');
  writeStaleDigitalHumanState(stateDir);
  const env = {
    ...process.env,
    DOUYIN_MONITOR_STATE_DIR: stateDir,
    DOUYIN_PERSONA_STATE_PATH: join(stateDir, 'persona-state.json'),
    DOUYIN_MARKETING_STATE_PATH: join(stateDir, 'automation-marketing-state.json'),
    DOUYIN_DIGITAL_HUMAN_STATE_PATH: join(stateDir, 'digital-human-state.json'),
    DOUYIN_FEISHU_WATCH_STATE: join(stateDir, 'feishu-reply-watcher-state.json'),
    DOUYIN_FEISHU_UPLOAD_DIR: join(stateDir, 'uploads'),
    DOUYIN_FEISHU_UPSTREAM_DIR: join(stateDir, 'upstream-tasks'),
    DOUYIN_NEXT_VIDEO_PLAN_JOB_DIR: join(stateDir, 'next-video-plan-jobs'),
    FEISHU_DRY_RUN: 'true',
    FEISHU_DRY_RUN_LOG: logPath,
    DOUYIN_ROUTE_LIGHT_TEST: 'true',
    DOUYIN_PERSONA_LLM: 'off',
    DIGITAL_HUMAN_TRAINING_API_KEY: process.env.DIGITAL_HUMAN_TRAINING_API_KEY || 'dry-run-key',
    DIGITAL_HUMAN_SKIP_COZE: 'true',
    DOUYIN_DEFAULT_DIGITAL_HUMAN_ID: process.env.DOUYIN_DEFAULT_DIGITAL_HUMAN_ID || 'CVHPZJ4LCGBMNIZULS0',
  };
  const steps = [];
  let previousMessages = 0;
  const specs = commandSpec(round, round % 2 === 0 ? '开启自动化营销' : '启动自动化营销');
  for (let i = 0; i < specs.length; i += 1) {
    const spec = specs[i];
    const run = runRoute(spec.text, env, i + 1);
    const messages = waitForExpectedMessages(logPath, previousMessages, spec);
    previousMessages = readJsonl(logPath).length;
    steps.push(validateStep(spec, run, messages));
  }
  const finalState = validateFinalState(stateDir);
  const failed = steps.filter((step) => !step.pass);
  return {
    round,
    ok: failed.length === 0 && finalState.pass,
    stateDir,
    steps,
    finalState,
    failures: [
      ...failed.map((step) => ({ text: step.text, issues: step.issues, action: step.action, messages: step.messages })),
      ...(finalState.pass ? [] : [{ text: 'final-state', issues: finalState.issues }]),
    ],
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const rounds = Number(args.rounds || 3);
  const baseDir = args.stateDir || DEFAULT_BASE_DIR;
  rmSync(baseDir, { recursive: true, force: true });
  mkdirSync(baseDir, { recursive: true });
  const results = [];
  for (let round = 1; round <= rounds; round += 1) {
    results.push(runRound(round, baseDir));
  }
  const failed = results.filter((round) => !round.ok);
  const summary = {
    ok: failed.length === 0,
    rounds,
    passed: results.length - failed.length,
    failed: failed.length,
    failures: failed.flatMap((round) => round.failures.map((failure) => ({ round: round.round, ...failure }))),
  };
  const reportPath = join(baseDir, `marketing-feishu-flow-stability-${Date.now()}.json`);
  writeFileSync(reportPath, `${JSON.stringify({ summary, results }, null, 2)}\n`);
  console.log(JSON.stringify({ summary, reportPath }, null, 2));
  if (!summary.ok) process.exit(1);
}

main();
