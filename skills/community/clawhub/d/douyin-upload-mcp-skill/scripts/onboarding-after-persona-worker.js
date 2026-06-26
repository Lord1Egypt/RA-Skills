#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn, spawnSync } from 'node:child_process';
import { getFeishuMessage, resolveFeishuConfig, sendFeishuTextChunks } from './feishu-client.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(process.env.HOME || '.', '.openclaw', 'workspace', 'douyin-ops');
const DIGITAL_HUMAN_STATE_PATH = process.env.DOUYIN_DIGITAL_HUMAN_STATE_PATH || join(STATE_DIR, 'digital-human-state.json');

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
    timedOut: result.error?.code === 'ETIMEDOUT' || result.signal === 'SIGTERM',
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

function parseJsonObjects(text) {
  const objects = [];
  const raw = String(text || '');
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
        try {
          objects.push(JSON.parse(raw.slice(start, i + 1)));
        } catch {
          // Ignore command logs.
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

function readJson(path, fallback = null) {
  try {
    if (!existsSync(path)) return fallback;
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return fallback;
  }
}

async function notify(jobPath, message, patch = {}) {
  const current = existsSync(jobPath) ? loadJob(jobPath) : {};
  if (!current.notify || !message) return null;
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
  let lastError = null;
  for (let attempt = 1; attempt <= 5; attempt += 1) {
    try {
      const result = await sendFeishuTextChunks(message, cfg);
      saveJob(jobPath, {
        ...patch,
        notifyResult: { ...result, attempt },
        notifiedAt: new Date().toISOString(),
      });
      return result;
    } catch (err) {
      lastError = err;
      saveJob(jobPath, {
        ...patch,
        notifyResult: { ok: false, attempt, error: err.message },
        notifyFailedAt: new Date().toISOString(),
      });
      if (attempt < 5) await new Promise((resolve) => setTimeout(resolve, attempt * 1200));
    }
  }
  {
    saveJob(jobPath, {
      ...patch,
      notifyResult: { ok: false, error: lastError?.message || 'send_failed' },
      notifyFailedAt: new Date().toISOString(),
    });
    return { ok: false, error: lastError?.message || 'send_failed' };
  }
}

function digitalHumanReadyAction(action) {
  return /^digital_human_training_succeeded|^digital_human_training_already_succeeded|^bind_model_id|^digital_human_default_model_confirmed/.test(String(action || ''));
}

function terminalDigitalHumanFailure(action) {
  return /^digital_human_training_failed|^digital_human_quality_failed|^digital_human_training_missing_config|^digital_human_training_route_failed|^digital_human_training_failed_to_start/.test(String(action || ''));
}

function progressMessageForDigitalHuman(payload) {
  const action = String(payload?.action || '');
  const job = payload?.job || {};
  if (action === 'digital_human_training_created' || job.status === 'quality_running') {
    return '数字人形象视频已生成，正在质检和训练，请稍等～';
  }
  if (action === 'digital_human_quality_passed' || action === 'digital_human_training_started' || job.status === 'training_running') {
    return '数字人形象已进入训练阶段，请稍等～';
  }
  if (action === 'digital_human_training_status' && payload?.status === 'coze_running') {
    return '正在生成数字人形象训练视频，请稍等～';
  }
  return '';
}

function marketingRouteArgs(text, job) {
  const routeArgs = [
    'scripts/marketing-controller.js',
    'route-text',
    '--text',
    text,
  ];
  if (job.dryRun) routeArgs.push('--dry-run');
  if (job.feishuTarget?.receiveId) {
    routeArgs.push('--receive-id', job.feishuTarget.receiveId, '--receive-id-type', job.feishuTarget.receiveIdType || 'chat_id');
  }
  return routeArgs;
}

function marketingRouteEnv(job) {
  return {
    DOUYIN_FEISHU_RECEIVE_ID: job.feishuTarget?.receiveId || process.env.DOUYIN_FEISHU_RECEIVE_ID || '',
    DOUYIN_FEISHU_RECEIVE_ID_TYPE: job.feishuTarget?.receiveIdType || process.env.DOUYIN_FEISHU_RECEIVE_ID_TYPE || 'chat_id',
  };
}

function runMarketingRoute(text, job, timeout = 1_200_000) {
  return runNode(marketingRouteArgs(text, job), {
    timeout,
    env: marketingRouteEnv(job),
  });
}

function runMarketingRouteAsync(text, job, timeout = 1_200_000) {
  return runNodeAsync(marketingRouteArgs(text, job), {
    timeout,
    env: marketingRouteEnv(job),
  });
}

function digitalHumanStageFromState(state = {}, fallback = 'digital_human_waiting') {
  const status = String(state?.status || state?.lastJob?.status || '').trim();
  if (status === 'coze_running') return 'digital_human_coze_running';
  if (status === 'created' || status === 'quality_running') return 'digital_human_quality_running';
  if (status === 'quality_passed') return 'digital_human_quality_passed';
  if (status === 'training_started' || status === 'training_running') return 'digital_human_training_running';
  if (status === 'succeeded') return 'digital_human_training_succeeded';
  if (status === 'failed') return 'digital_human_training_failed';
  return fallback;
}

function digitalHumanSnapshot(state = {}) {
  return {
    status: state.status || '',
    updatedAt: state.updatedAt || '',
    lastJobStatus: state.lastJob?.status || '',
    bizId: state.lastJob?.bizId || '',
    qualityProgress: state.lastJob?.quality?.progress ?? null,
    trainingProgress: state.lastJob?.training?.progress ?? null,
  };
}

function startDigitalHumanStatusPump(jobPath, attempt, fallbackStage = 'digital_human_waiting') {
  return setInterval(() => {
    const digitalState = readJson(DIGITAL_HUMAN_STATE_PATH, {});
    saveJob(jobPath, {
      stage: digitalHumanStageFromState(digitalState, fallbackStage),
      digitalHumanAttempt: attempt,
      lastDigitalHumanState: digitalHumanSnapshot(digitalState),
    });
  }, 10_000);
}

function startVideoStatusPump(jobPath) {
  return setInterval(() => {
    saveJob(jobPath, {
      stage: 'video_generating',
      lastVideoProgressMessage: '正在生成首条数字人视频',
    });
  }, 10_000);
}

async function waitForDigitalHuman(jobPath, job) {
  const maxAttempts = Number(job.digitalHumanMaxAttempts || 90);
  const intervalMs = Number(job.digitalHumanIntervalMs || 10000);
  let lastPayload = null;
  let lastProgressMessage = '';
  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    const text = attempt === 1 ? '训练数字人' : '查看数字人训练';
    saveJob(jobPath, { stage: attempt === 1 ? 'digital_human_starting' : 'digital_human_waiting', digitalHumanAttempt: attempt });
    if (attempt === 1) {
      saveJob(jobPath, {
        stage: 'digital_human_coze_running',
        digitalHumanAttempt: attempt,
        lastProgressMessage: '正在生成数字人形象训练视频，请稍等～',
      });
    }
    const progressTimer = startDigitalHumanStatusPump(
      jobPath,
      attempt,
      attempt === 1 ? 'digital_human_coze_running' : 'digital_human_waiting',
    );
    const run = await runMarketingRouteAsync(text, job, Number(job.digitalHumanRouteTimeoutMs || 1_500_000));
    clearInterval(progressTimer);
    const payload = parseLastJson(run.output);
    lastPayload = payload;
    saveJob(jobPath, {
      stage: payload?.action || 'digital_human_check',
      digitalHumanAttempt: attempt,
      lastDigitalHuman: payload || {
        ok: run.ok,
        status: run.status,
        signal: run.signal,
        error: run.error,
        output: compactOutput(run.output),
      },
    });
    if (run.ok && digitalHumanReadyAction(payload?.action)) return payload;
    if (payload?.action === 'digital_human_training_collect_needed') return payload;
    if (terminalDigitalHumanFailure(payload?.action) || payload?.ok === false) return payload;
    const progressMessage = progressMessageForDigitalHuman(payload);
    if (job.notifyProgress !== false && progressMessage && progressMessage !== lastProgressMessage) {
      lastProgressMessage = progressMessage;
      await notify(jobPath, progressMessage, { lastProgressMessage });
    }
    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }
  return lastPayload || { ok: false, action: 'digital_human_wait_timeout', customerMessage: '数字人形象生成暂未完成，请稍后重试。' };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.job) {
    console.error('Usage: node scripts/onboarding-after-persona-worker.js --job /abs/job.json');
    process.exit(2);
  }

  const jobPath = args.job;
  const job = saveJob(jobPath, { status: 'running', stage: 'digital_human_starting', startedAt: new Date().toISOString() });
  const digitalHuman = await waitForDigitalHuman(jobPath, job);
  if (!digitalHumanReadyAction(digitalHuman?.action)) {
    const message = digitalHuman?.customerMessage || '数字人形象生成暂未完成，请稍后重试。';
    saveJob(jobPath, {
      status: digitalHuman?.ok === false ? 'failed' : 'waiting',
      stage: digitalHuman?.action || 'digital_human_not_ready',
      result: { digitalHuman },
      customerMessage: message,
      finishedAt: new Date().toISOString(),
    });
    await notify(jobPath, message);
    if (digitalHuman?.ok === false) process.exit(1);
    return;
  }

  const startVideoMessage = '老板，您的数字人形象已完成定制，正在为您制作视频，请耐心等待～';
  saveJob(jobPath, {
    stage: 'video_starting',
    digitalHuman,
    scheduleDeferredUntilFirstPublish: true,
  });
  await notify(jobPath, startVideoMessage);

  const videoTimer = startVideoStatusPump(jobPath);
  const videoRun = await runMarketingRouteAsync('初次生成数字人视频', job, Number(job.videoRouteTimeoutMs || 2_400_000));
  clearInterval(videoTimer);
  const videoPayload = parseLastJson(videoRun.output);
  const videoMessage = videoPayload?.customerMessage || (videoRun.ok ? '老板，您的视频制作完成！请您审核。' : '视频生成失败，请稍后重试。');
  if (videoRun.ok && videoPayload?.ok) {
    saveJob(jobPath, {
      status: 'succeeded',
      stage: videoPayload.action || 'video_generated',
      result: { digitalHuman, video: videoPayload },
      customerMessage: videoMessage,
      finishedAt: new Date().toISOString(),
    });
    await notify(jobPath, videoMessage);
    return;
  }

  saveJob(jobPath, {
    status: 'failed',
    stage: videoPayload?.action || 'video_failed',
    result: {
      digitalHuman,
      video: videoPayload || {
        ok: videoRun.ok,
        status: videoRun.status,
        signal: videoRun.signal,
        error: videoRun.error,
        output: compactOutput(videoRun.output),
      },
    },
    customerMessage: videoMessage,
    finishedAt: new Date().toISOString(),
  });
  await notify(jobPath, videoMessage);
  process.exit(1);
}

main().catch(async (err) => {
  const args = parseArgs(process.argv.slice(2));
  if (args.job) {
    const message = '自动化营销流程暂未完成，请稍后重试。';
    saveJob(args.job, {
      status: 'failed',
      stage: 'crashed',
      customerMessage: message,
      error: err.message,
      stack: err.stack,
      finishedAt: new Date().toISOString(),
    });
    await notify(args.job, message).catch(() => null);
  } else {
    console.error(err.stack || err.message);
  }
  process.exit(1);
});
