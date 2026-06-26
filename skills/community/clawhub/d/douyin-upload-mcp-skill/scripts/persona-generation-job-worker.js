#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn, spawnSync } from 'node:child_process';
import { getFeishuMessage, resolveFeishuConfig, sendFeishuTextChunks } from './feishu-client.js';

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
    timeout: Number(opts.timeout || 300000),
    env: { ...process.env, ...(opts.env || {}) },
  });
  return {
    ok: result.status === 0,
    status: result.status,
    signal: result.signal,
    error: result.error?.message,
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

    const timeoutMs = Number(opts.timeout || 300000);
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

function parseLastJson(text) {
  const raw = String(text || '').trim();
  const candidates = [];
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;
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
        candidates.push(raw.slice(start, i + 1));
        start = -1;
      }
    }
  }
  for (let i = candidates.length - 1; i >= 0; i -= 1) {
    try {
      return JSON.parse(candidates[i]);
    } catch {
      // Keep scanning older candidates.
    }
  }
  return null;
}

function compactOutput(text, max = 5000) {
  const raw = String(text || '');
  return raw.length > max ? raw.slice(-max) : raw;
}

async function notifyIfRequested(jobPath, message, patch = {}) {
  const current = existsSync(jobPath) ? loadJob(jobPath) : {};
  if (!current.notify || !message) return null;
  try {
    let target = current.feishuTarget?.receiveId ? current.feishuTarget : null;
    if (!target && current.sourceMessageId) {
      const sourceMessage = await getFeishuMessage(current.sourceMessageId).catch(() => null);
      if (sourceMessage?.chat_id) {
        target = { receiveId: sourceMessage.chat_id, receiveIdType: 'chat_id' };
        saveJob(jobPath, { feishuTarget: target });
      }
    }
    const cfg = target ? resolveFeishuConfig({
      receiveId: target.receiveId,
      receiveIdType: target.receiveIdType || 'chat_id',
    }) : resolveFeishuConfig();
    const result = await sendFeishuTextChunks(message, cfg);
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
    console.error('Usage: node scripts/persona-generation-job-worker.js --job /abs/job.json');
    process.exit(2);
  }

  const jobPath = args.job;
  const job = saveJob(jobPath, { status: 'running', stage: 'generating', startedAt: new Date().toISOString() });
  const inputText = String(job.text || '').trim();
  const routeArgs = [
    'scripts/persona-flow.js',
    'route-text',
    '--text',
    inputText || '生成人设',
  ];
  if (job.dryRun) routeArgs.push('--dry-run');
  const heartbeat = setInterval(() => {
    saveJob(jobPath, {
      status: 'running',
      stage: 'generating',
      heartbeatAt: new Date().toISOString(),
    });
  }, 10_000);
  const result = await runNodeAsync(routeArgs, { timeout: Number(job.timeoutMs || 360000) });
  clearInterval(heartbeat);
  const payload = parseLastJson(result.output);
  const customerMessage = payload?.customerMessage || (payload?.ok ? '人设流程已处理。' : '人设生成暂未完成，请稍后重试。');

  if (result.ok && payload?.ok) {
    saveJob(jobPath, {
      status: 'succeeded',
      stage: payload.action || 'generated',
      result: payload,
      customerMessage,
      finishedAt: new Date().toISOString(),
    });
    await notifyIfRequested(jobPath, customerMessage);
    return;
  }

  saveJob(jobPath, {
    status: 'failed',
    stage: payload?.action || 'generation_failed',
    result: payload || { ok: result.ok, status: result.status, signal: result.signal, error: result.error, output: compactOutput(result.output) },
    customerMessage,
    finishedAt: new Date().toISOString(),
  });
  await notifyIfRequested(jobPath, customerMessage);
  process.exit(1);
}

main().catch(async (err) => {
  const args = parseArgs(process.argv.slice(2));
  if (args.job) {
    const customerMessage = '人设生成暂未完成，请稍后重试。';
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
