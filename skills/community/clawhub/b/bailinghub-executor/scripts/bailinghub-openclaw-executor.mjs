#!/usr/bin/env node

import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdtemp, rm, writeFile } from 'node:fs/promises';
import { hostname, tmpdir } from 'node:os';
import { join } from 'node:path';

const MAX_HTTP_BODY_BYTES = 2 * 1024 * 1024;
const MAX_TASK_BYTES = 4 * 1024 * 1024;
const MAX_STDOUT_BYTES = 4 * 1024 * 1024;
const MAX_STDERR_BYTES = 256 * 1024;
const REPORT_ATTEMPTS = 3;
const CHILD_ENV_BASE_KEYS = [
  'PATH',
  'HOME',
  'USER',
  'LOGNAME',
  'SHELL',
  'TMPDIR',
  'TMP',
  'TEMP',
  'LANG',
  'LC_ALL',
  'LC_CTYPE',
  'XDG_CONFIG_HOME',
  'XDG_DATA_HOME',
  'XDG_CACHE_HOME',
  'SYSTEMROOT',
  'COMSPEC',
  'PATHEXT',
  'APPDATA',
  'LOCALAPPDATA',
  'USERPROFILE',
];
const FORBIDDEN_FORWARDED_ENV = new Set([
  'OPENCLAW_FORWARD_ENV',
  'NODE_OPTIONS',
  'LD_PRELOAD',
  'LD_LIBRARY_PATH',
  'DYLD_INSERT_LIBRARIES',
  'DYLD_LIBRARY_PATH',
  'DYLD_FRAMEWORK_PATH',
  'BASH_ENV',
  'ENV',
  'GIT_SSH_COMMAND',
]);

class ConfigError extends Error {}
class PermanentProtocolError extends Error {}

function env(name, fallback = '') {
  const value = process.env[name];
  return value === undefined ? fallback : String(value).trim();
}

function requiredEnv(name) {
  const value = env(name);
  if (!value) throw new ConfigError(`Missing required environment variable: ${name}`);
  return value;
}

function integerEnv(name, fallback, minimum, maximum) {
  const raw = env(name, String(fallback));
  const value = Number(raw);
  if (!Number.isInteger(value) || value < minimum || value > maximum) {
    throw new ConfigError(`${name} must be an integer from ${minimum} to ${maximum}`);
  }
  return value;
}

function forwardedEnvironmentNames() {
  const raw = env('OPENCLAW_FORWARD_ENV');
  if (!raw) return [];

  const names = [...new Set(raw.split(',').map((value) => value.trim()).filter(Boolean))];
  for (const name of names) {
    if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(name)) {
      throw new ConfigError(`OPENCLAW_FORWARD_ENV contains an invalid variable name: ${name}`);
    }
    if (name.startsWith('BAILING_') || FORBIDDEN_FORWARDED_ENV.has(name)) {
      throw new ConfigError(`OPENCLAW_FORWARD_ENV may not forward protected variable: ${name}`);
    }
    if (process.env[name] === undefined) {
      throw new ConfigError(`OPENCLAW_FORWARD_ENV names an unset variable: ${name}`);
    }
  }
  return names;
}

function safeIdentifier(value, label, maximum = 160) {
  if (!value || value.length > maximum || /[\u0000-\u001f\u007f]/.test(value)) {
    throw new ConfigError(`${label} must be 1-${maximum} characters without control characters`);
  }
  return value;
}

function parseHubUrl(raw) {
  let url;
  try {
    url = new URL(raw);
  } catch {
    throw new ConfigError('BAILING_HUB_URL must be an absolute URL');
  }

  if (url.username || url.password || url.search || url.hash) {
    throw new ConfigError('BAILING_HUB_URL must not contain credentials, query parameters, or a fragment');
  }

  const loopback = url.hostname === 'localhost'
    || url.hostname === '127.0.0.1'
    || url.hostname === '::1';
  if (url.protocol !== 'https:' && !(url.protocol === 'http:' && loopback)) {
    throw new ConfigError('BAILING_HUB_URL must use HTTPS; HTTP is allowed only for loopback tests');
  }
  if (url.pathname !== '/' && url.pathname !== '') {
    throw new ConfigError('BAILING_HUB_URL must be the BailingHub origin without a path');
  }
  url.pathname = '/';
  return url;
}

function buildConfig() {
  const targets = requiredEnv('BAILING_TARGET')
    .split(',')
    .map((value) => value.trim())
    .filter(Boolean)
    .map((value) => safeIdentifier(value, 'BAILING_TARGET'));
  if (!targets.length) throw new ConfigError('BAILING_TARGET must contain at least one target');

  const agentId = env('OPENCLAW_AGENT', 'bailinghub-executor');
  if (!/^[A-Za-z0-9_-]+$/.test(agentId)) {
    throw new ConfigError('OPENCLAW_AGENT may contain only letters, numbers, underscores, and hyphens');
  }

  const openclawBin = env('OPENCLAW_BIN', 'openclaw');
  if (!openclawBin || /[\u0000-\u001f\u007f]/.test(openclawBin)) {
    throw new ConfigError('OPENCLAW_BIN must be a non-empty executable name or path');
  }

  const timeoutSeconds = integerEnv('OPENCLAW_TIMEOUT_SECONDS', 600, 1, 3600);

  return {
    hubUrl: parseHubUrl(requiredEnv('BAILING_HUB_URL')),
    token: requiredEnv('BAILING_EXECUTOR_TOKEN'),
    targets,
    executorId: safeIdentifier(env('BAILING_EXECUTOR_ID', hostname()), 'BAILING_EXECUTOR_ID'),
    waitMs: integerEnv('BAILING_WAIT_MS', 12_000, 1_000, 60_000),
    heartbeatMs: integerEnv('BAILING_HEARTBEAT_MS', 30_000, 5_000, 120_000),
    runOnce: env('BAILING_RUN_ONCE') === '1',
    openclaw: {
      bin: openclawBin,
      agentId,
      model: safeOptionalValue(env('OPENCLAW_MODEL'), 'OPENCLAW_MODEL'),
      thinking: safeOptionalValue(env('OPENCLAW_THINKING'), 'OPENCLAW_THINKING'),
      timeoutSeconds,
      useGateway: env('OPENCLAW_USE_GATEWAY') === '1',
      forwardEnv: forwardedEnvironmentNames(),
    },
  };
}

function safeOptionalValue(value, label) {
  if (value.length > 300 || /[\u0000-\u001f\u007f]/.test(value)) {
    throw new ConfigError(`${label} must be at most 300 characters without control characters`);
  }
  return value;
}

function log(message) {
  process.stdout.write(`[bailinghub-executor] ${new Date().toISOString()} ${message}\n`);
}

function safeLogValue(value, maximum = 180) {
  return String(value ?? '')
    .replace(/[\u0000-\u001f\u007f]+/g, ' ')
    .slice(0, maximum);
}

function sleep(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

async function readBoundedBody(response, maximum = MAX_HTTP_BODY_BYTES) {
  const declaredLength = Number(response.headers.get('content-length'));
  if (Number.isFinite(declaredLength) && declaredLength > maximum) {
    throw new Error(`HTTP response exceeds ${maximum} bytes`);
  }
  if (!response.body) return '';

  const chunks = [];
  let size = 0;
  const reader = response.body.getReader();
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > maximum) throw new Error(`HTTP response exceeds ${maximum} bytes`);
      chunks.push(Buffer.from(value));
    }
  } finally {
    reader.releaseLock();
  }
  return Buffer.concat(chunks).toString('utf8');
}

async function request(config, pathname, body, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  timer.unref?.();
  try {
    const response = await fetch(new URL(pathname, config.hubUrl), {
      method: 'POST',
      headers: {
        authorization: `Bearer ${config.token}`,
        'content-type': 'application/json',
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
    const text = await readBoundedBody(response);
    return { response, text };
  } finally {
    clearTimeout(timer);
  }
}

function parseJson(text, context) {
  if (!text) return {};
  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`${context} returned invalid JSON`);
  }
}

function capabilities() {
  return {
    runtime: 'openclaw',
    labels: ['openclaw', 'agent-governance', 'outbound-executor'],
  };
}

async function claim(config) {
  try {
    const { response, text } = await request(config, '/executor/claim', {
      executor_id: config.executorId,
      targets: config.targets,
      wait_ms: config.waitMs,
      capabilities: capabilities(),
    }, config.waitMs + 8_000);

    if (response.status === 401) {
      throw new PermanentProtocolError('Claim rejected with 401; verify or rotate the executor token');
    }
    if (response.status === 403) {
      throw new PermanentProtocolError(`Claim rejected with 403; token is not authorized for target ${config.targets.join(',')}`);
    }
    if (!response.ok) {
      log(`claim returned HTTP ${response.status}; retrying`);
      return null;
    }
    return parseJson(text, 'Claim endpoint').job ?? null;
  } catch (error) {
    if (error instanceof PermanentProtocolError) throw error;
    const reason = error?.name === 'AbortError' ? 'request timed out' : safeLogValue(error?.message || error);
    log(`claim failed: ${reason}; retrying`);
    return null;
  }
}

async function heartbeat(config) {
  try {
    const { response } = await request(config, '/executor/heartbeat', {
      executor_id: config.executorId,
      targets: config.targets,
      capabilities: capabilities(),
    }, 8_000);
    if (response.status === 401 || response.status === 403) {
      log(`heartbeat rejected with HTTP ${response.status}; stop and verify the token scope`);
    }
  } catch {
    // Heartbeat is best effort; the next scheduled heartbeat retries.
  }
}

async function report(config, jobId, payload) {
  for (let attempt = 1; attempt <= REPORT_ATTEMPTS; attempt += 1) {
    try {
      const { response } = await request(config, '/executor/result', {
        job_id: jobId,
        ...payload,
      }, 12_000);
      if (response.ok) return true;
      if (response.status === 401 || response.status === 403) {
        log(`result rejected with HTTP ${response.status}; token or target authorization changed`);
        return false;
      }
    } catch {
      // Retry below. The claim token prevents a late result from replacing a newer dispatch.
    }
    if (attempt < REPORT_ATTEMPTS) await sleep(attempt * 2_000);
  }
  log(`result reporting failed after ${REPORT_ATTEMPTS} attempts for job=${safeLogValue(jobId)}`);
  return false;
}

function taskText(job) {
  const input = typeof job?.input === 'string'
    ? job.input
    : JSON.stringify(job?.input ?? '');
  const bytes = Buffer.byteLength(input, 'utf8');
  if (!input.trim()) throw new Error('Claimed task input is empty');
  if (bytes > MAX_TASK_BYTES) throw new Error(`Claimed task exceeds ${MAX_TASK_BYTES} bytes`);
  return input;
}

function sessionKey(job) {
  const raw = String(
    job?.session?.sessionId
      || job?.request_id
      || job?.job_id
      || 'task',
  );
  const slug = raw
    .replace(/[^A-Za-z0-9._-]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 48) || 'task';
  const digest = createHash('sha256').update(raw).digest('hex').slice(0, 12);
  return `bailing-${slug}-${digest}`;
}

function extractReply(data) {
  const payloads = Array.isArray(data?.payloads)
    ? data.payloads
    : Array.isArray(data?.result?.payloads)
      ? data.result.payloads
      : [];
  const text = payloads
    .map((item) => typeof item?.text === 'string' ? item.text.trim() : '')
    .filter(Boolean)
    .join('\n\n');
  if (text) return text;
  const status = safeLogValue(data?.status ?? data?.result?.status ?? 'unknown');
  throw new Error(`OpenClaw returned no visible text (status=${status})`);
}

function sanitizedChildEnvironment(config) {
  const childEnv = { NO_COLOR: '1' };
  for (const key of CHILD_ENV_BASE_KEYS) {
    if (process.env[key] !== undefined) childEnv[key] = process.env[key];
  }
  for (const key of config.openclaw.forwardEnv) childEnv[key] = process.env[key];
  return childEnv;
}

async function runOpenClaw(config, job) {
  const directory = await mkdtemp(join(tmpdir(), 'bailinghub-openclaw-'));
  const messageFile = join(directory, 'task.txt');
  try {
    await writeFile(messageFile, taskText(job), { encoding: 'utf8', mode: 0o600 });

    const args = [
      'agent',
      ...(config.openclaw.useGateway ? [] : ['--local']),
      '--agent', config.openclaw.agentId,
      '--session-key', sessionKey(job),
      '--message-file', messageFile,
      '--json',
      '--timeout', String(config.openclaw.timeoutSeconds),
      ...(config.openclaw.model ? ['--model', config.openclaw.model] : []),
      ...(config.openclaw.thinking ? ['--thinking', config.openclaw.thinking] : []),
    ];

    const stdout = await new Promise((resolve, reject) => {
      const child = spawn(config.openclaw.bin, args, {
        env: sanitizedChildEnvironment(config),
        stdio: ['ignore', 'pipe', 'pipe'],
        shell: false,
      });

      let output = '';
      let outputBytes = 0;
      let stderrBytes = 0;
      let settled = false;
      let terminationReason = '';
      const hardTimeoutMs = (config.openclaw.timeoutSeconds + 15) * 1_000;
      const timer = setTimeout(() => {
        terminationReason = `OpenClaw exceeded the ${config.openclaw.timeoutSeconds}s task timeout`;
        child.kill('SIGKILL');
      }, hardTimeoutMs);
      timer.unref?.();

      const finish = (callback) => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        callback();
      };

      child.stdout.on('data', (chunk) => {
        outputBytes += chunk.length;
        if (outputBytes > MAX_STDOUT_BYTES) {
          terminationReason = `OpenClaw stdout exceeded ${MAX_STDOUT_BYTES} bytes`;
          child.kill('SIGKILL');
          return;
        }
        output += chunk.toString('utf8');
      });

      child.stderr.on('data', (chunk) => {
        stderrBytes += chunk.length;
        if (stderrBytes > MAX_STDERR_BYTES && !terminationReason) {
          terminationReason = `OpenClaw stderr exceeded ${MAX_STDERR_BYTES} bytes`;
          child.kill('SIGKILL');
        }
      });

      child.on('error', (error) => finish(() => {
        reject(new Error(`Unable to start OpenClaw: ${safeLogValue(error.message)}`));
      }));

      child.on('close', (code, signal) => finish(() => {
        if (terminationReason) {
          reject(new Error(terminationReason));
          return;
        }
        if (code !== 0) {
          reject(new Error(`OpenClaw failed (code=${code ?? 'null'}, signal=${signal ?? 'none'})`));
          return;
        }
        resolve(output);
      }));
    });

    let data;
    try {
      data = JSON.parse(stdout);
    } catch {
      throw new Error('OpenClaw returned invalid JSON');
    }
    return extractReply(data);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

async function main() {
  const config = buildConfig();
  let stopping = false;
  let heartbeatInFlight = false;

  for (const signal of ['SIGINT', 'SIGTERM']) {
    process.on(signal, () => {
      stopping = true;
      log(`received ${signal}; exiting after the current task`);
    });
  }

  const heartbeatTimer = setInterval(async () => {
    if (heartbeatInFlight || stopping) return;
    heartbeatInFlight = true;
    try {
      await heartbeat(config);
    } finally {
      heartbeatInFlight = false;
    }
  }, config.heartbeatMs);
  heartbeatTimer.unref?.();

  log(`starting hub=${config.hubUrl.origin} executor=${safeLogValue(config.executorId)} targets=${config.targets.map(safeLogValue).join(',')} runtime=openclaw`);

  try {
    while (!stopping) {
      const job = await claim(config);
      if (!job) {
        await sleep(800);
        continue;
      }

      const jobId = safeIdentifier(String(job.job_id ?? ''), 'job_id', 200);
      log(`processing job=${safeLogValue(jobId)} target=${safeLogValue(job.target)}`);
      const startedAt = Date.now();
      let payload;
      try {
        const text = await runOpenClaw(config, job);
        payload = { ok: true, output: { text } };
      } catch (error) {
        payload = {
          ok: false,
          output: {},
          error: safeLogValue(error?.message || error, 500),
        };
      }

      if (job.claim_token) payload.claim_token = job.claim_token;
      const reported = await report(config, jobId, payload);
      log(`finished job=${safeLogValue(jobId)} ok=${payload.ok} reported=${reported} duration_ms=${Date.now() - startedAt}`);

      if (config.runOnce) break;
    }
  } finally {
    clearInterval(heartbeatTimer);
  }
  log('stopped');
}

try {
  await main();
} catch (error) {
  const prefix = error instanceof ConfigError ? 'configuration error' : 'fatal error';
  process.stderr.write(`[bailinghub-executor] ${prefix}: ${safeLogValue(error?.message || error, 500)}\n`);
  process.exitCode = error instanceof ConfigError ? 2 : 1;
}
