#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

const ROOT = new URL('..', import.meta.url).pathname;
const DEFAULT_BASE_DIR = '/tmp/douyin-persona-feishu-messy-stability';

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

function commandSpec(round) {
  return [
    {
      text: `我叫老王${round}，做宠物保险，想在抖音做账号。主要想让养猫养狗的人别乱买保险，我比较会讲理赔坑。`,
      expectAction: 'persona_need_more_info',
      expectText: /还缺：本人照片链接、性别、从业年限、个人特质、经验案例、禁忌偏好/,
    },
    {
      text: '男，做了8年。我说话比较专业、直接、亲和，处理过300多个养宠家庭咨询。',
      expectAction: 'persona_need_more_info',
      expectText: /还缺：本人照片链接、禁忌偏好/,
    },
    {
      text: `照片：https://example.com/laowang-${round}.jpg\n不要夸大效果，也不能承诺一定理赔，表达合规清晰就行。`,
      expectAction: 'persona_generation_deferred',
      expectText: /老板，您的专属人设信息已完成[\s\S]*回复【通过】或【不通过】/,
    },
    {
      text: '通过',
      expectAction: 'persona_confirmed',
      expectText: /^老板，我将基于原图照片和人设信息为您定制专属数字人形象，请稍等片刻~\n老板，您的数字人形象已完成定制，正在为您制作视频，请耐心等待～\n老板，您的视频制作完成！请您审核：[\s\S]*回复【确认发布】或【不通过】/,
      expectMessageCount: 3,
    },
  ];
}

function runRoute(text, env, index, reset = false) {
  const args = [
    'scripts/feishu-reply-watcher.js',
    'route-text',
    '--text',
    text,
    '--dry-run',
    '--chat-id',
    'oc_persona_messy_test',
    '--message-id',
    `manual_persona_messy_${Date.now()}_${index}`,
  ];
  if (reset) args.push('--reset');
  const result = spawnSync(process.execPath, args, {
    cwd: ROOT,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: 180000,
    env,
  });
  const output = `${result.stderr || ''}${result.stdout || ''}`.trim();
  return {
    status: result.status,
    ok: result.status === 0,
    output,
    payload: parseJsonObjects(output).at(-1) || null,
  };
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

function waitForExpectedMessages(logPath, previousCount, spec, timeoutMs = 60000) {
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
  if (!run.ok || !run.payload?.ok) issues.push('route_failed');
  if (action !== spec.expectAction) issues.push(`unexpected_action:${action || 'none'}`);
  const minMessageCount = spec.minMessageCount ?? spec.expectMessageCount ?? 1;
  if (messages.length < minMessageCount) issues.push(`unexpected_message_count:${messages.length}`);
  if (spec.expectMessageCount !== undefined && messages.length !== spec.expectMessageCount) issues.push(`unexpected_message_count:${messages.length}`);
  if (!spec.expectText.test(combined)) issues.push('unexpected_customer_text');
  if (/每日自动化营销已设定|定时任务/.test(combined)) issues.push('schedule_text_leaked');
  if (/内容较长，已截断|完整版本已保存在 persona-state\.json/.test(combined)) issues.push('persona_truncated_notice_leaked');
  if (leakedInternal(combined)) issues.push('internal_detail_leaked');
  return {
    text: spec.text,
    action,
    messages,
    pass: issues.length === 0,
    issues,
  };
}

function validateFinalState(stateDir) {
  const persona = readJson(join(stateDir, 'persona-state.json'), {});
  const marketing = readJson(join(stateDir, 'automation-marketing-state.json'), {});
  const fields = persona.fields || {};
  const required = ['name', 'photo', 'sex', 'work_year', 'bissiness', 'advantage', 'segment', 'trials', 'cases', 'demand', 'taboos'];
  const missing = required.filter((key) => !String(fields[key] || '').trim());
  const issues = [];
  if (persona.status !== 'confirmed') issues.push(`status:${persona.status || 'none'}`);
  if (!persona.confirmed) issues.push('persona_not_confirmed');
  if (missing.length) issues.push(`missing_fields:${missing.join(',')}`);
  if (!/宠物保险/.test(String(fields.bissiness || ''))) issues.push(`business_parse:${fields.bissiness || 'none'}`);
  if (!marketing.digitalHuman?.modelId) issues.push('model_not_set');
  if (!marketing.pendingReview?.publishText) issues.push('pending_video_review_missing');
  return { pass: issues.length === 0, issues, persona, marketing };
}

function runRound(round, baseDir) {
  const stateDir = join(baseDir, `round-${round}`);
  rmSync(stateDir, { recursive: true, force: true });
  mkdirSync(stateDir, { recursive: true });
  const logPath = join(stateDir, 'feishu-dry-run.jsonl');
  const env = {
    ...process.env,
    DOUYIN_MONITOR_STATE_DIR: stateDir,
    DOUYIN_PERSONA_STATE_PATH: join(stateDir, 'persona-state.json'),
    DOUYIN_MARKETING_STATE_PATH: join(stateDir, 'automation-marketing-state.json'),
    DOUYIN_DIGITAL_HUMAN_STATE_PATH: join(stateDir, 'digital-human-state.json'),
    DOUYIN_FEISHU_WATCH_STATE: join(stateDir, 'feishu-reply-watcher-state.json'),
    FEISHU_DRY_RUN: 'true',
    FEISHU_DRY_RUN_LOG: logPath,
    DOUYIN_ROUTE_LIGHT_TEST: 'true',
    DOUYIN_PERSONA_LLM: 'off',
    DIGITAL_HUMAN_SKIP_COZE: 'true',
    DOUYIN_DEFAULT_DIGITAL_HUMAN_ID: process.env.DOUYIN_DEFAULT_DIGITAL_HUMAN_ID || 'CVHPZJ4LCGBMNIZULS0',
  };
  const steps = [];
  let previousMessages = 0;
  const specs = commandSpec(round);
  for (let i = 0; i < specs.length; i += 1) {
    const spec = specs[i];
    const run = runRoute(spec.text, env, i + 1, i === 0);
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
  const reportPath = join(baseDir, `persona-feishu-messy-stability-${Date.now()}.json`);
  writeFileSync(reportPath, `${JSON.stringify({ summary, results }, null, 2)}\n`);
  console.log(JSON.stringify({ summary, reportPath }, null, 2));
  if (!summary.ok) process.exit(1);
}

main();
