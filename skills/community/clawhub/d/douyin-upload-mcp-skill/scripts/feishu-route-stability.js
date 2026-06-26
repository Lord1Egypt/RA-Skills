#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { spawnSync } from 'node:child_process';

const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(process.env.HOME || '.', '.openclaw', 'workspace', 'douyin-ops');

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
  for (let i = 0; i < String(text || '').length; i += 1) {
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
          // Ignore non-JSON spans.
        }
        start = -1;
      }
    }
  }
  return objects;
}

function readJsonl(path) {
  if (!existsSync(path)) return [];
  return readFileSync(path, 'utf8')
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

function runRoute(text, round, index) {
  const logPath = join(STATE_DIR, `feishu-dry-run-${Date.now()}-${round}-${index}.jsonl`);
  rmSync(logPath, { force: true });
  const result = spawnSync(process.execPath, [
    'scripts/feishu-reply-watcher.js',
    'route-text',
    '--text',
    text,
    '--dry-run',
    '--reset',
  ], {
    cwd: join(dirname(new URL(import.meta.url).pathname), '..'),
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: 900000,
    env: {
      ...process.env,
      FEISHU_DRY_RUN: 'true',
      DOUYIN_ROUTE_LIGHT_TEST: 'true',
      FEISHU_DRY_RUN_LOG: logPath,
    },
  });
  const output = `${result.stderr || ''}${result.stdout || ''}`.trim();
  return {
    text,
    status: result.status,
    ok: result.status === 0,
    payload: parseJsonObjects(output).at(-1) || null,
    messages: readJsonl(logPath),
    stdoutTail: result.stdout.slice(-1200),
    stderrTail: result.stderr.slice(-1200),
  };
}

function leakedInternal(text) {
  return /stack|Error:|TypeError|ReferenceError|SyntaxError|detector_output_parse_failed|undefined|null|node:|at\s+\w+|执行崩溃|HTTP \d{3}/i.test(text);
}

function expectedMessages(command, run) {
  if (command === '发布抖音') return ['waiting_video', 'waiting_qr_ready'].includes(run.payload?.flow?.step) ? 1 : 0;
  return 1;
}

function isLoginRequiredMessage(text) {
  return text === '抖音需要重新登录。\n请在电脑端打开飞书，用手机抖音 App 准备扫码。\n准备好后回复：发送二维码';
}

function actionWaitingLoginQr(run) {
  return /waiting_login_qr$/.test(run.payload?.result?.action || '')
    || (run.text === '发布抖音' && run.payload?.flow?.step === 'waiting_qr_ready');
}

function validateRun(run) {
  const textMessages = run.messages.filter((item) => item.type === 'text');
  const imageMessages = run.messages.filter((item) => item.type === 'image');
  const combined = textMessages.map((item) => item.text).join('\n');
  const issues = [];
  if (!run.ok || !run.payload?.ok) issues.push('route_failed');
  if (textMessages.length > 1) issues.push('duplicate_text_messages');
  if (imageMessages.length) issues.push('unexpected_image_message');
  if (combined && leakedInternal(combined)) issues.push('internal_detail_leaked');
  if (!combined && expectedMessages(run.text, run) > 0) issues.push('missing_customer_message');
  const loginQr = actionWaitingLoginQr(run) && isLoginRequiredMessage(combined);
  if (/定时任务|任务计划|查看任务|开启定时任务|关闭定时任务|修改定时任务/.test(run.text) && combined) {
    const scheduleOk = /^定时任务：/.test(combined)
      || /^定时任务已开启/.test(combined)
      || /^定时任务已准备/.test(combined)
      || /^定时任务已暂停/.test(combined)
      || /^自动回复定时任务已改为每/.test(combined)
      || /^自动化营销定时任务已改为每天/.test(combined)
      || /^数据报告不单独设置定时/.test(combined);
    if (!scheduleOk) issues.push('schedule_prompt_not_minimal');
  } else {
    if (run.text === '发布抖音' && combined && combined !== '登录成功，请发送视频。' && !loginQr) issues.push('publish_prompt_not_minimal');
    if (/自动回复/.test(run.text) && combined && !/^自动回复完成：评论 \d+ 条，私信 \d+ 条。$/.test(combined) && !loginQr) issues.push('auto_reply_prompt_not_minimal');
    if (run.text === '更新数据' && combined && !/^数据已更新：近 \d+ 天，作品 \d+ 条。/.test(combined) && !loginQr) issues.push('data_sync_prompt_not_minimal');
    if (/数据报告|数据分析|分析数据|查看数据/.test(run.text) && combined && !/^老板，昨日数据报告如下，请您查收～\n数据报告：已同步近 \d+ 天作品明细/.test(combined) && !loginQr) issues.push('data_report_prompt_not_minimal');
  }
  return {
    ...run,
    messageCount: run.messages.length,
    textCount: textMessages.length,
    imageCount: imageMessages.length,
    customerText: combined,
    issues,
    pass: issues.length === 0,
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const rounds = Number(args.rounds || 3);
  const commands = [
    '发布抖音',
    '数据报告',
    '更新数据',
    '自动回复评论',
    '自动回复私信',
    '自动回复',
    '定时任务',
    '修改定时任务 自动回复 30分钟',
    '修改定时任务 自动回复 2小时',
    '修改定时任务 自动化营销 09:30',
    '关闭定时任务',
    '开启定时任务',
  ];
  mkdirSync(STATE_DIR, { recursive: true });
  const results = [];
  for (let round = 1; round <= rounds; round += 1) {
    for (let i = 0; i < commands.length; i += 1) {
      results.push(validateRun(runRoute(commands[i], round, i + 1)));
    }
  }
  const failed = results.filter((item) => !item.pass);
  const summary = {
    ok: failed.length === 0,
    rounds,
    commands: commands.length,
    total: results.length,
    passed: results.length - failed.length,
    failed: failed.length,
    failures: failed.map((item) => ({
      text: item.text,
      issues: item.issues,
      customerText: item.customerText,
      status: item.status,
      action: item.payload?.result?.action,
    })),
  };
  const reportPath = join(STATE_DIR, `feishu-route-stability-${Date.now()}.json`);
  writeFileSync(reportPath, `${JSON.stringify({ summary, results }, null, 2)}\n`);
  console.log(JSON.stringify({ summary, reportPath }, null, 2));
  if (!summary.ok) process.exit(1);
}

main();
