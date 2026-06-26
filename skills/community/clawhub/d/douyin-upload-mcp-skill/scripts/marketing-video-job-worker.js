#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { getFeishuMessage, resolveFeishuConfig, sendFeishuText } from './feishu-client.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

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
    timeout: Number(opts.timeout || 1_200_000),
    env: { ...process.env, ...(opts.env || {}) },
  });
  return {
    ok: result.status === 0,
    status: result.status,
    signal: result.signal,
    output: `${result.stderr || ''}${result.stdout || ''}`.trim(),
  };
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
          // Ignore logger text.
        }
        start = -1;
      }
    }
  }
  return objects;
}

function parseLastJson(text) {
  return parseJsonObjects(text).at(-1) || null;
}

function compactOutput(text, max = 5000) {
  const raw = String(text || '');
  return raw.length > max ? raw.slice(-max) : raw;
}

function customerMessageForFailure(payload, run) {
  const text = JSON.stringify(payload || run || {});
  if (/generate_video_missing_prerequisites|缺少|人设|数字人还未就绪/.test(text)) {
    return payload?.customerMessage || '视频生成暂未开始，请先完成人设和数字人形象。';
  }
  if (/xiaoice|video_task|create|timeout|ETIMEDOUT|SIGTERM/i.test(text)) {
    return '视频生成失败，请稍后重试。';
  }
  return payload?.customerMessage || '视频生成失败，请稍后重试。';
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
    console.error('Usage: node scripts/marketing-video-job-worker.js --job /abs/job.json');
    process.exit(2);
  }

  const jobPath = args.job;
  const job = saveJob(jobPath, { status: 'running', stage: 'generate_video', startedAt: new Date().toISOString() });
  const routeText = job.routeText || '确认方案';
  const run = runNode([
    'scripts/marketing-controller.js',
    'route-text',
    '--text',
    routeText,
    '--force',
    ...(process.env.FEISHU_DRY_RUN === 'true' ? ['--dry-run'] : []),
  ], { timeout: Number(job.timeoutMs || 1_200_000) });
  const payload = parseLastJson(run.output);
  if (run.ok && payload?.ok) {
    const customerMessage = payload.customerMessage || '老板，您的视频制作完成！请您审核。';
    saveJob(jobPath, {
      status: 'succeeded',
      stage: payload.action || 'video_generated',
      customerMessage,
      result: payload,
      finishedAt: new Date().toISOString(),
    });
    await notifyIfRequested(jobPath, customerMessage);
    return;
  }

  const customerMessage = customerMessageForFailure(payload, run);
  saveJob(jobPath, {
    status: 'failed',
    stage: payload?.action || 'video_failed',
    customerMessage,
    result: payload || { ok: run.ok, output: compactOutput(run.output), status: run.status, signal: run.signal },
    finishedAt: new Date().toISOString(),
  });
  await notifyIfRequested(jobPath, customerMessage);
  process.exit(1);
}

main().catch(async (err) => {
  const args = parseArgs(process.argv.slice(2));
  if (args.job) {
    const customerMessage = '视频生成失败，请稍后重试。';
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
