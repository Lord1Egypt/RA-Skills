#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

const ROOT = new URL('..', import.meta.url).pathname;
const DEFAULT_BASE_DIR = '/tmp/douyin-marketing-confirmation-mode-stability';

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
          // Ignore logs.
        }
        start = -1;
      }
    }
  }
  return objects;
}

function readJson(path, fallback = {}) {
  try {
    if (!existsSync(path)) return fallback;
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return fallback;
  }
}

function runMarketing(args, env) {
  const result = spawnSync(process.execPath, ['scripts/marketing-controller.js', ...args], {
    cwd: ROOT,
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: 240000,
    env,
  });
  const output = `${result.stderr || ''}${result.stdout || ''}`.trim();
  return {
    ok: result.status === 0,
    status: result.status,
    output,
    payload: parseJsonObjects(output).at(-1) || null,
  };
}

function personaState(round) {
  return {
    status: 'confirmed',
    confirmed: {
      summary: {
        coreIdentity: `8年宠物保险顾问${round}`,
      },
      fields: {
        name: `张琳${round}`,
        bissiness: '宠物保险顾问服务',
        segment: '新手养宠家庭',
      },
    },
  };
}

function validateStep(name, run, actionPattern, textPattern) {
  const issues = [];
  const action = run.payload?.action || '';
  const customerMessage = run.payload?.customerMessage || '';
  if (!run.ok || run.payload?.ok === false) issues.push('command_failed');
  if (actionPattern && !actionPattern.test(action)) issues.push(`unexpected_action:${action}`);
  if (textPattern !== null && textPattern !== undefined && !textPattern.test(customerMessage)) issues.push('unexpected_customer_text');
  if (/stack|TypeError|ReferenceError|SyntaxError|node:|at\s+\w+/i.test(customerMessage)) issues.push('internal_detail_leaked');
  return { name, action, customerMessage, pass: issues.length === 0, issues, payload: run.payload };
}

function runRound(round, baseDir) {
  const stateDir = join(baseDir, `round-${round}`);
  rmSync(stateDir, { recursive: true, force: true });
  mkdirSync(stateDir, { recursive: true });
  writeFileSync(join(stateDir, 'persona-state.json'), `${JSON.stringify(personaState(round), null, 2)}\n`);
  writeFileSync(join(stateDir, 'automation-marketing-state.json'), `${JSON.stringify({
    version: 1,
    enabled: false,
    publishMode: 'manual_confirm',
    confirmationMode: 'manual',
    schedule: { dailyTime: '07:30' },
    digitalHuman: {
      modelId: process.env.DOUYIN_DEFAULT_DIGITAL_HUMAN_ID || 'CVHPZJ4LCGBMNIZULS0',
      source: 'customer',
      confirmedAt: new Date().toISOString(),
    },
  }, null, 2)}\n`);
  const env = {
    ...process.env,
    DOUYIN_MONITOR_STATE_DIR: stateDir,
    DOUYIN_PERSONA_STATE_PATH: join(stateDir, 'persona-state.json'),
    DOUYIN_MARKETING_STATE_PATH: join(stateDir, 'automation-marketing-state.json'),
    FEISHU_DRY_RUN: 'true',
    DOUYIN_ROUTE_LIGHT_TEST: 'true',
    DOUYIN_DEFAULT_DIGITAL_HUMAN_ID: process.env.DOUYIN_DEFAULT_DIGITAL_HUMAN_ID || 'CVHPZJ4LCGBMNIZULS0',
  };
  const steps = [];

  steps.push(validateStep(
    'request-enable-manual',
    runMarketing(['route-text', '--text', '开启自动化营销', '--dry-run'], env),
    /^marketing_enable_review_required$/,
    /开启前请核对[\s\S]*确认开启/,
  ));
  steps.push(validateStep(
    'confirm-enable-manual',
    runMarketing(['route-text', '--text', '确认开启', '--dry-run'], env),
    /^marketing_enabled$/,
    /方案.*确认|确认方案/,
  ));
  steps.push(validateStep(
    'daily-manual-stops-at-plan',
    runMarketing(['daily-run', '--dry-run', '--force'], env),
    /^marketing_daily_waiting_plan_confirm$/,
    /老板，您的视频方案已生成，请您审核：[\s\S]*回复【通过】或【不通过】/,
  ));
  const manualState = readJson(join(stateDir, 'automation-marketing-state.json'));
  if (!manualState.pendingPlan?.plan || manualState.pendingReview) {
    steps.push({ name: 'manual-state', pass: false, issues: ['manual_daily_state_wrong'], payload: manualState });
  } else {
    steps.push({ name: 'manual-state', pass: true, issues: [], payload: { hasPendingPlan: true } });
  }
  steps.push(validateStep(
    'confirm-plan-generates-review',
    runMarketing(['route-text', '--text', '确认方案', '--dry-run'], env),
    /^marketing_video_generated$/,
    /老板，您的视频制作完成！请您审核：[\s\S]*回复【确认发布】或【不通过】/,
  ));
  steps.push(validateStep(
    'confirm-publish',
    runMarketing(['route-text', '--text', '确认发布', '--dry-run'], env),
    /^publish_pending_review_dry_run$/,
    /^$/,
  ));
  steps.push(validateStep(
    'set-auto-mode',
    runMarketing(['route-text', '--text', '开启自动确认', '--dry-run'], env),
    /^confirmation_mode_auto$/,
    /已开启自动确认模式/,
  ));
  steps.push(validateStep(
    'daily-auto-publishes',
    runMarketing(['daily-run', '--dry-run', '--force'], env),
    /^marketing_daily_run_started_publish$/,
    /^$/,
  ));

  const failures = steps.filter((step) => !step.pass);
  return { round, ok: failures.length === 0, stateDir, steps, failures };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const rounds = Number(args.rounds || 3);
  const baseDir = args.stateDir || DEFAULT_BASE_DIR;
  rmSync(baseDir, { recursive: true, force: true });
  mkdirSync(baseDir, { recursive: true });
  const results = [];
  for (let round = 1; round <= rounds; round += 1) results.push(runRound(round, baseDir));
  const failed = results.filter((round) => !round.ok);
  const summary = {
    ok: failed.length === 0,
    rounds,
    passed: results.length - failed.length,
    failed: failed.length,
    failures: failed.flatMap((round) => round.failures.map((failure) => ({ round: round.round, name: failure.name, issues: failure.issues, action: failure.action }))),
  };
  const reportPath = join(baseDir, `marketing-confirmation-mode-stability-${Date.now()}.json`);
  writeFileSync(reportPath, `${JSON.stringify({ summary, results }, null, 2)}\n`);
  console.log(JSON.stringify({ summary, reportPath }, null, 2));
  if (!summary.ok) process.exit(1);
}

main();
