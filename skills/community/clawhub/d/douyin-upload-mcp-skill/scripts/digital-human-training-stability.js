#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

const ROOT = new URL('..', import.meta.url).pathname;
const DEFAULT_BASE_DIR = '/tmp/douyin-digital-human-training-stability';

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

function trainingText(round) {
  return [
    `照片：https://example.com/person-${round}.jpg`,
    `数字人名称：测试${round}`,
  ].join('\n');
}

function commandSpec(round) {
  return [
    { text: '训练数字人', expectAction: 'digital_human_training_collect_needed', expectText: /已确认人设|本人照片链接/ },
    { text: '照片：https://example.com/person-only.jpg', expectAction: 'digital_human_training_collect_needed', expectText: /已确认人设/ },
    { text: trainingText(round), expectAction: 'digital_human_training_succeeded', expectText: /跳过 Coze 工作流|默认数字人ID/ },
    { text: '数字人状态', expectAction: 'digital_human_training_status', expectText: /数字人ID：已绑定/ },
  ];
}

function personaState(round) {
  const fields = {
    name: `测试${round}`,
    photo: `https://example.com/person-${round}.jpg`,
    sex: '男',
    age: '35',
    work_year: '8',
    bissiness: '农业棚膜顾问',
    advantage: '熟悉棚膜选型和种植户真实问题',
    segment: '大棚种植农户',
    trials: '朴实、专业、耐心',
    cases: '服务过1000个种植户',
    demand: '通过抖音建立信任并获取咨询',
    taboos: '不夸大效果',
  };
  return {
    version: 1,
    status: 'confirmed',
    fields,
    draft: {
      fields,
      summary: {
        coreIdentity: '8年农业棚膜顾问',
        audience: '大棚种植农户',
        tone: '朴实、专业、耐心',
        value: '帮种植户选对棚膜',
      },
      strategy: '测试人设战略定位方案',
      marketing: '测试IP营销策划方案',
    },
    confirmed: {
      fields,
      summary: {
        coreIdentity: '8年农业棚膜顾问',
        audience: '大棚种植农户',
        tone: '朴实、专业、耐心',
        value: '帮种植户选对棚膜',
      },
      strategy: '测试人设战略定位方案',
      marketing: '测试IP营销策划方案',
      confirmedAt: new Date().toISOString(),
    },
  };
}

function runRoute(text, env, index) {
  const result = spawnSync(process.execPath, [
    'scripts/feishu-reply-watcher.js',
    'route-text',
    '--text',
    text,
    '--dry-run',
    '--chat-id',
    'oc_digital_human_test',
    '--message-id',
    `manual_digital_human_${Date.now()}_${index}`,
  ], {
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

function leakedInternal(text) {
  return /stack|TypeError|ReferenceError|SyntaxError|node:|at\s+\w+|HTTP \d{3}|undefined|null/i.test(text);
}

function validateStep(spec, run, messages) {
  const result = run.payload?.result || {};
  const action = result.payload?.action || result.action;
  const combined = messages.join('\n');
  const issues = [];
  if (!run.ok || !run.payload?.ok) issues.push('route_failed');
  if (action !== spec.expectAction) issues.push(`unexpected_action:${action || 'none'}`);
  if (messages.length !== 1) issues.push(`unexpected_message_count:${messages.length}`);
  if (!spec.expectText.test(combined)) issues.push('unexpected_customer_text');
  if (leakedInternal(combined)) issues.push('internal_detail_leaked');
  return {
    text: spec.text.includes('\n') ? 'training-fields' : spec.text,
    action,
    messages,
    pass: issues.length === 0,
    issues,
  };
}

function validateFinalState(stateDir) {
  const training = readJson(join(stateDir, 'digital-human-state.json'), {});
  const marketing = readJson(join(stateDir, 'automation-marketing-state.json'), {});
  const issues = [];
  if (training.lastJob?.status !== 'succeeded') issues.push(`training_status:${training.lastJob?.status || 'none'}`);
  if (!training.lastJob?.digitalHumanBizId) issues.push('missing_training_model_id');
  if (!training.lastJob?.skippedCoze) issues.push('coze_not_skipped');
  if (!marketing.digitalHuman?.modelId) issues.push('missing_marketing_model_id');
  if (!/^default/.test(String(marketing.digitalHuman?.source || ''))) issues.push(`unexpected_model_source:${marketing.digitalHuman?.source || 'none'}`);
  return { pass: issues.length === 0, issues, training, marketing };
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
    DIGITAL_HUMAN_TRAINING_API_KEY: 'dry-run-key',
    DIGITAL_HUMAN_SKIP_COZE: 'true',
  };
  const personaPath = join(stateDir, 'persona-state.json');
  const steps = [];
  let previousMessages = 0;
  const specs = commandSpec(round);
  for (let i = 0; i < specs.length; i += 1) {
    const spec = specs[i];
    if (i === 2) writeFileSync(personaPath, `${JSON.stringify(personaState(round), null, 2)}\n`);
    const run = runRoute(spec.text, env, i + 1);
    const messages = customerTexts(logPath, previousMessages);
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
  const reportPath = join(baseDir, `digital-human-training-stability-${Date.now()}.json`);
  writeFileSync(reportPath, `${JSON.stringify({ summary, results }, null, 2)}\n`);
  console.log(JSON.stringify({ summary, reportPath }, null, 2));
  if (!summary.ok) process.exit(1);
}

main();
