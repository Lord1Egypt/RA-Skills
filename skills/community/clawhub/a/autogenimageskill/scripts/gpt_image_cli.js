#!/usr/bin/env node
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');

const DEFAULT_MODEL = 'gpt-5.4';
const DEFAULT_IMAGE_MODEL = 'gpt-image-2';
const DEFAULT_SIZE = '1024x1536';
const DEFAULT_QUALITY = 'high';
const DEFAULT_OUTPUT_FORMAT = 'png';
const DEFAULT_DIRECT_RETRIES = 3;
const DEFAULT_TIMEOUT_MS = 180000;
const DEFAULT_POLL_INTERVAL_MS = 1500;
const DEFAULT_STATE_PATH = path.join(os.homedir(), '.openclaw', 'autoGenImageSkill', 'state.json');

function parseArgs(argv) {
  const args = { _: [] };

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];

    if (!token.startsWith('--')) {
      args._.push(token);
      continue;
    }

    const eqIndex = token.indexOf('=');
    if (eqIndex > 2) {
      args[token.slice(2, eqIndex)] = token.slice(eqIndex + 1);
      continue;
    }

    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }

    args[key] = next;
    i += 1;
  }

  return args;
}

function help() {
  return `autoGenImageSkill CLI

Usage:
  node gpt_image_cli.js generate --mode official --permission-code "$OPENAI_API_KEY" --prompt "..." --output out.png
  node gpt_image_cli.js generate --mode proxy --base-url "$GPT_IMAGE_BASE_URL" --api-key "$GPT_IMAGE_API_KEY" --prompt "..."
  node gpt_image_cli.js generate --mode reserved --service-url "$GPT_IMAGE_RELAY_URL" --purchase-key "$GPT_IMAGE_PURCHASE_KEY" --prompt "..."
  node gpt_image_cli.js session --service-url "$GPT_IMAGE_RELAY_URL" --profile-name "demo" --save-session
  node gpt_image_cli.js redeem --service-url "$GPT_IMAGE_RELAY_URL" --purchase-key "$GPT_IMAGE_PURCHASE_KEY" --user-id "$GPT_IMAGE_USER_ID"
  node gpt_image_cli.js quota --service-url "$GPT_IMAGE_RELAY_URL" --user-id "$GPT_IMAGE_USER_ID"

Common generate options:
  --prompt TEXT
  --image PATH_OR_DATA_URL
  --output PATH                     default: generated-image.png
  --model NAME                      default: gpt-5.4
  --image-model NAME                default: gpt-image-2
  --size WxH                        default: 1024x1536
  --quality VALUE                   default: high
  --output-format VALUE             default: png
  --retries N                       direct official/proxy retries, default: 3
  --timeout-ms N                    reserved job timeout, default: 180000

Secrets are read from arguments or environment variables and are never printed.`;
}

function readState(args = {}) {
  const statePath = String(args['state-path'] || process.env.GPT_IMAGE_STATE_PATH || DEFAULT_STATE_PATH);
  try {
    if (!fs.existsSync(statePath)) return { statePath, state: {} };
    const parsed = JSON.parse(fs.readFileSync(statePath, 'utf8'));
    return { statePath, state: parsed && typeof parsed === 'object' ? parsed : {} };
  } catch {
    return { statePath, state: {} };
  }
}

function saveState(statePath, nextState) {
  fs.mkdirSync(path.dirname(statePath), { recursive: true });
  fs.writeFileSync(statePath, JSON.stringify(nextState, null, 2), 'utf8');
}

function stringValue(...values) {
  for (const value of values) {
    if (typeof value === 'string' && value.trim()) return value.trim();
  }
  return '';
}

function integerValue(value, fallback) {
  const parsed = Number.parseInt(String(value ?? ''), 10);
  return Number.isFinite(parsed) ? parsed : fallback;
}

function boolValue(value) {
  return value === true || ['1', 'true', 'yes', 'on'].includes(String(value || '').toLowerCase());
}

function requireValue(name, value) {
  if (!value) {
    throw new Error(`Missing required value: ${name}`);
  }
  return value;
}

function unique(values) {
  const seen = new Set();
  const output = [];
  for (const value of values) {
    if (!value || seen.has(value)) continue;
    seen.add(value);
    output.push(value);
  }
  return output;
}

function normalizeDirectEndpointCandidates(baseUrl) {
  const normalized = String(baseUrl || '').trim().replace(/\/+$/, '');
  if (!normalized) return [];

  const candidates = [];

  if (/\/responses$/i.test(normalized)) {
    candidates.push(normalized);
  } else if (/\/v\d+$/i.test(normalized) || /\/openai\/v\d+$/i.test(normalized)) {
    candidates.push(`${normalized}/responses`);
  } else if (/api\.openai\.com$/i.test(normalized)) {
    candidates.push(`${normalized}/v1/responses`);
  } else {
    candidates.push(`${normalized}/responses`);
    candidates.push(`${normalized}/v1/responses`);
  }

  candidates.push(normalized.replace(/\/openai\/v1\/responses$/i, '/v1/responses'));
  candidates.push(normalized.replace(/\/openai\/v1$/i, '/v1/responses'));
  candidates.push(normalized.replace(/\/v1$/i, '/v1/responses'));

  return unique(candidates);
}

function normalizeServiceRoot(serviceUrl) {
  let root = String(serviceUrl || '').trim().replace(/\/+$/, '');
  root = root.replace(/\/api\/generate\/jobs(?:\/.*)?$/i, '');
  root = root.replace(/\/api\/generate(?:-image)?$/i, '');
  root = root.replace(/\/api\/keys$/i, '');
  root = root.replace(/\/api\/session(?:\/register)?$/i, '');
  return root;
}

function serviceUrl(root, apiPath) {
  const normalizedRoot = normalizeServiceRoot(root);
  return `${normalizedRoot}${apiPath.startsWith('/') ? apiPath : `/${apiPath}`}`;
}

function resolveRelayImageUrl(root, imageUrl) {
  if (/^(data:|https?:\/\/|blob:)/i.test(imageUrl)) {
    return imageUrl;
  }
  if (imageUrl.startsWith('/')) {
    return `${normalizeServiceRoot(root)}${imageUrl}`;
  }
  return `${normalizeServiceRoot(root)}/${imageUrl}`;
}

function mimeFromPath(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  if (ext === '.jpg' || ext === '.jpeg') return 'image/jpeg';
  if (ext === '.webp') return 'image/webp';
  if (ext === '.gif') return 'image/gif';
  return 'image/png';
}

function readImageDataUrl(value) {
  if (!value) return null;
  if (String(value).startsWith('data:image/')) return String(value);

  const absolutePath = path.resolve(String(value));
  const buffer = fs.readFileSync(absolutePath);
  return `data:${mimeFromPath(absolutePath)};base64,${buffer.toString('base64')}`;
}

function buildPayload(args, inputImage) {
  const prompt = requireValue('prompt', stringValue(args.prompt, process.env.PROMPT));
  const imageModel = stringValue(args['image-model'], process.env.GPT_IMAGE_MODEL) || DEFAULT_IMAGE_MODEL;
  const outputFormat = stringValue(args['output-format'], process.env.GPT_IMAGE_OUTPUT_FORMAT) || DEFAULT_OUTPUT_FORMAT;

  return {
    model: stringValue(args.model, process.env.GPT_IMAGE_TEXT_MODEL) || DEFAULT_MODEL,
    input: inputImage
      ? [
          {
            role: 'user',
            content: [
              { type: 'input_text', text: prompt },
              { type: 'input_image', image_url: inputImage },
            ],
          },
        ]
      : prompt,
    tools: [
      {
        type: 'image_generation',
        model: imageModel,
        size: stringValue(args.size, process.env.GPT_IMAGE_SIZE) || DEFAULT_SIZE,
        quality: stringValue(args.quality, process.env.GPT_IMAGE_QUALITY) || DEFAULT_QUALITY,
        output_format: outputFormat,
      },
    ],
    tool_choice: { type: 'image_generation' },
    stream: true,
  };
}

async function readSseResult(response) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  const result = {
    responseId: null,
    createdTool: null,
    finalCall: null,
    outputText: '',
    error: null,
  };

  function captureOutputItem(item) {
    if (!item || typeof item !== 'object') return;

    if (item.type === 'image_generation_call') {
      result.finalCall = item;
      return;
    }

    if (item.type === 'message' && Array.isArray(item.content)) {
      for (const part of item.content) {
        if (part.type === 'output_text' && part.text) {
          result.outputText += part.text;
        }
      }
    }
  }

  function handleEvent(obj) {
    if (obj.response && obj.response.id) {
      result.responseId = obj.response.id;
    }

    if (
      (obj.type === 'response.created' || obj.type === 'response.in_progress') &&
      obj.response &&
      Array.isArray(obj.response.tools) &&
      obj.response.tools[0] &&
      !result.createdTool
    ) {
      result.createdTool = obj.response.tools[0];
    }

    if (obj.type === 'response.output_text.delta' && obj.delta) {
      result.outputText += obj.delta;
    }

    if (obj.type === 'response.output_item.done' && obj.item) {
      captureOutputItem(obj.item);
    }

    if (
      (obj.type === 'response.completed' || obj.type === 'response.incomplete') &&
      obj.response &&
      Array.isArray(obj.response.output)
    ) {
      for (const item of obj.response.output) {
        captureOutputItem(item);
      }
    }

    if (obj.type === 'error' && obj.error) {
      result.error = obj.error;
    }

    if (obj.type === 'response.failed' && obj.response && obj.response.error && !result.error) {
      result.error = obj.response.error;
    }
  }

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    let splitIndex;
    while ((splitIndex = buffer.indexOf('\n\n')) >= 0) {
      const block = buffer.slice(0, splitIndex);
      buffer = buffer.slice(splitIndex + 2);
      const lines = block.split(/\r?\n/);
      const dataLines = [];

      for (const line of lines) {
        if (line.startsWith('data:')) {
          dataLines.push(line.slice(5).trim());
        }
      }

      const dataText = dataLines.join('\n');
      if (!dataText || dataText === '[DONE]') continue;

      try {
        handleEvent(JSON.parse(dataText));
      } catch {
        // Ignore malformed chunks from intermediary relays.
      }
    }
  }

  return result;
}

function findImageGenerationCall(obj) {
  if (!obj || typeof obj !== 'object') return null;
  if (obj.type === 'image_generation_call' && typeof obj.result === 'string') return obj;

  if (Array.isArray(obj)) {
    for (const item of obj) {
      const found = findImageGenerationCall(item);
      if (found) return found;
    }
    return null;
  }

  for (const value of Object.values(obj)) {
    const found = findImageGenerationCall(value);
    if (found) return found;
  }
  return null;
}

function summarizeFailure(failure) {
  if (!failure) return null;
  const copy = { ...failure };
  if (typeof copy.body === 'string' && copy.body.length > 600) {
    copy.body = `${copy.body.slice(0, 600)}...`;
  }
  if (copy.error && typeof copy.error === 'object') {
    copy.error = JSON.stringify(copy.error).slice(0, 600);
  }
  return copy;
}

async function tryDirectEndpoint(endpoint, apiKey, payload) {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      Accept: 'text/event-stream, application/json',
    },
    body: JSON.stringify(payload),
  });

  const contentType = response.headers.get('content-type') || '';

  if (!response.ok) {
    return {
      ok: false,
      endpoint,
      status: response.status,
      contentType,
      body: await response.text(),
      retryable: response.status === 408 || response.status === 409 || response.status === 425 || response.status === 429 || response.status >= 500,
    };
  }

  if (contentType.includes('text/event-stream')) {
    const sse = await readSseResult(response);
    const finalCall = sse.finalCall;
    if (finalCall && finalCall.result) {
      return {
        ok: true,
        endpoint,
        imageBase64: finalCall.result,
        meta: {
          responseId: sse.responseId,
          createdTool: sse.createdTool,
          finalCall,
          outputText: sse.outputText || '',
        },
      };
    }
    return {
      ok: false,
      endpoint,
      status: response.status,
      contentType,
      error: sse.error || 'SSE finished without image_generation_call.result',
      retryable: true,
    };
  }

  const text = await response.text();
  let parsed = null;
  try {
    parsed = JSON.parse(text);
  } catch {
    return {
      ok: false,
      endpoint,
      status: response.status,
      contentType,
      body: text,
      retryable: false,
    };
  }

  const finalCall = findImageGenerationCall(parsed);
  if (finalCall && finalCall.result) {
    return {
      ok: true,
      endpoint,
      imageBase64: finalCall.result,
      meta: {
        responseId: parsed.id || parsed.response?.id || null,
        createdTool: Array.isArray(parsed.tools) ? parsed.tools[0] : null,
        finalCall,
        outputText: '',
      },
    };
  }

  return {
    ok: false,
    endpoint,
    status: response.status,
    contentType,
    body: text,
    retryable: false,
  };
}

async function generateDirect(args, mode) {
  const apiKey =
    mode === 'official'
      ? stringValue(args['permission-code'], args['api-key'], process.env.OPENAI_API_KEY, process.env.GPT_IMAGE_OFFICIAL_PERMISSION_CODE)
      : stringValue(args['api-key'], args['permission-code'], process.env.GPT_IMAGE_API_KEY);
  requireValue(mode === 'official' ? 'permission-code or OPENAI_API_KEY' : 'api-key or GPT_IMAGE_API_KEY', apiKey);

  const baseUrl =
    mode === 'official'
      ? stringValue(args['base-url'], process.env.OPENAI_BASE_URL) || 'https://api.openai.com/v1'
      : requireValue('base-url or GPT_IMAGE_BASE_URL', stringValue(args['base-url'], process.env.GPT_IMAGE_BASE_URL));

  const inputImage = readImageDataUrl(stringValue(args.image, process.env.GPT_IMAGE_INPUT_IMAGE));
  const payload = buildPayload(args, inputImage);
  const endpoints = normalizeDirectEndpointCandidates(baseUrl);
  const retries = Math.max(1, integerValue(args.retries || process.env.GPT_IMAGE_RETRIES, DEFAULT_DIRECT_RETRIES));
  let lastFailure = null;

  for (let attempt = 1; attempt <= retries; attempt += 1) {
    for (const endpoint of endpoints) {
      try {
        const result = await tryDirectEndpoint(endpoint, apiKey, payload);
        if (result.ok) {
          return {
            ...result,
            mode,
            providerName: stringValue(args['provider-name']) || (mode === 'official' ? 'official' : 'proxy'),
            attempt,
          };
        }

        lastFailure = { ...result, attempt };
        if (result.retryable === false) break;
      } catch (error) {
        lastFailure = {
          endpoint,
          attempt,
          error: String(error),
          retryable: true,
        };
      }
    }
  }

  throw new Error(`Generation failed: ${JSON.stringify(summarizeFailure(lastFailure))}`);
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const text = await response.text();
  let body = null;
  try {
    body = text ? JSON.parse(text) : null;
  } catch {
    body = { text };
  }

  if (!response.ok) {
    const message = body && typeof body.error === 'string' ? body.error : `HTTP ${response.status}`;
    const error = new Error(message);
    error.status = response.status;
    error.body = body;
    throw error;
  }

  return body || {};
}

async function postRelayJson(root, apiPath, body, userId = '') {
  const headers = { 'Content-Type': 'application/json' };
  if (userId) headers['X-User-Id'] = userId;
  return fetchJson(serviceUrl(root, apiPath), {
    method: 'POST',
    headers,
    body: JSON.stringify(body || {}),
  });
}

async function getRelayJson(root, apiPath, userId = '') {
  const headers = {};
  if (userId) headers['X-User-Id'] = userId;
  return fetchJson(serviceUrl(root, apiPath), { headers });
}

async function downloadRelayImage(root, imageUrl, userId = '') {
  const headers = {};
  if (userId) headers['X-User-Id'] = userId;
  const response = await fetch(resolveRelayImageUrl(root, imageUrl), { headers });
  if (!response.ok) {
    throw new Error(`Image download failed: HTTP ${response.status}`);
  }
  return Buffer.from(await response.arrayBuffer());
}

async function ensureRelaySession(args, options = {}) {
  const { statePath, state } = readState(args);
  const serviceRoot = normalizeServiceRoot(
    requireValue(
      'service-url or GPT_IMAGE_RELAY_URL',
      stringValue(args['service-url'], process.env.GPT_IMAGE_RELAY_URL, state.serviceUrl)
    )
  );
  const requestedUserId = stringValue(args['user-id'], process.env.GPT_IMAGE_USER_ID, state.userId);
  const profileName = stringValue(args['profile-name'], process.env.GPT_IMAGE_PROFILE_NAME);

  const session = await postRelayJson(serviceRoot, '/api/session', { userId: requestedUserId });
  let user = session.user || null;

  if (profileName) {
    const registered = await postRelayJson(
      serviceRoot,
      '/api/session/register',
      { userId: user?.id || requestedUserId, profileName },
      user?.id || requestedUserId
    );
    user = registered.user || user;
  }

  if (!user || !user.id) {
    throw new Error('Relay did not return a usable user session');
  }

  if (options.save || boolValue(args['save-session'])) {
    saveState(statePath, {
      ...state,
      serviceUrl: serviceRoot,
      userId: user.id,
      profileName: user.profileName || profileName || state.profileName || null,
    });
  }

  return { serviceRoot, user, statePath };
}

async function redeemPurchaseKey(args, sessionInfo) {
  const purchaseKey = stringValue(args['purchase-key'], process.env.GPT_IMAGE_PURCHASE_KEY);
  if (!purchaseKey) return null;

  const valid = await postRelayJson(
    sessionInfo.serviceRoot,
    '/api/keys',
    { action: 'validate', key: purchaseKey },
    sessionInfo.user.id
  );

  if (!valid.valid) {
    throw new Error('purchase key is invalid or already used');
  }

  await postRelayJson(
    sessionInfo.serviceRoot,
    '/api/keys',
    { action: 'consume', key: purchaseKey },
    sessionInfo.user.id
  );

  const status = await postRelayJson(
    sessionInfo.serviceRoot,
    '/api/keys',
    { action: 'status' },
    sessionInfo.user.id
  );

  return status.user || null;
}

async function consumeRelayQuota(args, sessionInfo, hasInputImage) {
  const quota = stringValue(args.quota, process.env.GPT_IMAGE_QUOTA_MODE) || 'auto';
  if (quota === 'none') return { quota: 'none' };

  if (quota === 'free') {
    await postRelayJson(sessionInfo.serviceRoot, '/api/keys', { action: 'consume_free' }, sessionInfo.user.id);
    return { quota: 'free' };
  }

  if (quota === 'credit') {
    const result = await postRelayJson(sessionInfo.serviceRoot, '/api/keys', { action: 'consume_credit' }, sessionInfo.user.id);
    return { quota: 'credit', credits: result.credits };
  }

  if (quota !== 'auto') {
    throw new Error(`Unsupported quota mode: ${quota}`);
  }

  if (!hasInputImage) {
    const free = await postRelayJson(sessionInfo.serviceRoot, '/api/keys', { action: 'check_free' }, sessionInfo.user.id);
    if (free.free) {
      await postRelayJson(sessionInfo.serviceRoot, '/api/keys', { action: 'consume_free' }, sessionInfo.user.id);
      return { quota: 'free' };
    }
  }

  const result = await postRelayJson(sessionInfo.serviceRoot, '/api/keys', { action: 'consume_credit' }, sessionInfo.user.id);
  return { quota: 'credit', credits: result.credits };
}

async function waitForRelayJob(root, jobId, userId, timeoutMs, pollIntervalMs) {
  const startedAt = Date.now();

  while (Date.now() - startedAt <= timeoutMs) {
    const job = await getRelayJson(root, `/api/generate/jobs/${encodeURIComponent(jobId)}`, userId);
    if (job.status === 'queued' || job.status === 'running') {
      await new Promise((resolve) => setTimeout(resolve, pollIntervalMs));
      continue;
    }

    if (job.status === 'succeeded' && job.imageUrl) {
      return job;
    }

    throw new Error(job.error || `Relay job failed with status: ${job.status}`);
  }

  throw new Error(`Relay job timed out after ${timeoutMs}ms`);
}

async function generateReserved(args) {
  const prompt = requireValue('prompt', stringValue(args.prompt, process.env.PROMPT));
  const inputImage = readImageDataUrl(stringValue(args.image, process.env.GPT_IMAGE_INPUT_IMAGE));
  const sessionInfo = await ensureRelaySession(args, { save: boolValue(args['save-session']) });
  const redeemedUser = await redeemPurchaseKey(args, sessionInfo);
  if (redeemedUser) {
    sessionInfo.user = redeemedUser;
  }

  const quota = await consumeRelayQuota(args, sessionInfo, !!inputImage);
  if (quota && quota.quota === 'credit' && Number.isFinite(Number(quota.credits))) {
    sessionInfo.user.credits = Number(quota.credits);
  }
  const preferredProviders = stringValue(args['preferred-providers'], process.env.GPT_IMAGE_PREFERRED_PROVIDERS)
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean);

  const created = await postRelayJson(
    sessionInfo.serviceRoot,
    '/api/generate/jobs',
    {
      prompt,
      image: inputImage,
      userId: sessionInfo.user.id,
      preferredProviders,
    },
    sessionInfo.user.id
  );

  const jobId = requireValue('relay jobId', created.jobId);
  const timeoutMs = Math.max(1000, integerValue(args['timeout-ms'] || process.env.GPT_IMAGE_TIMEOUT_MS, DEFAULT_TIMEOUT_MS));
  const pollIntervalMs = Math.max(250, integerValue(args['poll-interval-ms'] || process.env.GPT_IMAGE_POLL_INTERVAL_MS, DEFAULT_POLL_INTERVAL_MS));
  const job = await waitForRelayJob(sessionInfo.serviceRoot, jobId, sessionInfo.user.id, timeoutMs, pollIntervalMs);
  const imageBuffer = await downloadRelayImage(sessionInfo.serviceRoot, job.imageUrl, sessionInfo.user.id);

  return {
    ok: true,
    mode: 'reserved',
    imageBuffer,
    providerName: job.providerName || null,
    jobId,
    quota,
    user: {
      id: sessionInfo.user.id,
      role: sessionInfo.user.role || null,
      credits: Number(sessionInfo.user.credits || 0),
      profileName: sessionInfo.user.profileName || null,
    },
  };
}

function writeOutput(outputPath, buffer) {
  const absoluteOutput = path.resolve(outputPath || 'generated-image.png');
  fs.mkdirSync(path.dirname(absoluteOutput), { recursive: true });
  fs.writeFileSync(absoluteOutput, buffer);
  return {
    output: absoluteOutput,
    bytes: fs.statSync(absoluteOutput).size,
  };
}

function redactedSummary(summary) {
  return JSON.stringify(summary, null, 2);
}

async function commandGenerate(args) {
  const mode = stringValue(args.mode, process.env.GPT_IMAGE_MODE) || 'official';
  let result = null;

  if (mode === 'official' || mode === 'proxy') {
    result = await generateDirect(args, mode);
    result.imageBuffer = Buffer.from(result.imageBase64, 'base64');
    delete result.imageBase64;
  } else if (mode === 'reserved') {
    result = await generateReserved(args);
  } else {
    throw new Error(`Unsupported mode: ${mode}`);
  }

  const outputInfo = writeOutput(stringValue(args.output, process.env.OUTPUT) || 'generated-image.png', result.imageBuffer);
  const finalCall = result.meta?.finalCall || null;

  process.stdout.write(
    redactedSummary({
      ok: true,
      mode: result.mode || mode,
      providerName: result.providerName || null,
      endpoint: result.endpoint || null,
      jobId: result.jobId || null,
      output: outputInfo.output,
      bytes: outputInfo.bytes,
      responseId: result.meta?.responseId || null,
      image: finalCall
        ? {
            type: finalCall.type,
            model: finalCall.model || null,
            quality: finalCall.quality || null,
            size: finalCall.size || null,
            output_format: finalCall.output_format || null,
            revised_prompt: finalCall.revised_prompt || null,
          }
        : null,
      quota: result.quota || null,
      user: result.user || null,
    }) + '\n'
  );
}

async function commandSession(args) {
  const sessionInfo = await ensureRelaySession(args, { save: boolValue(args['save-session']) });
  process.stdout.write(
    redactedSummary({
      ok: true,
      serviceUrl: sessionInfo.serviceRoot,
      statePath: boolValue(args['save-session']) ? sessionInfo.statePath : null,
      user: sessionInfo.user,
    }) + '\n'
  );
}

async function commandRedeem(args) {
  requireValue('purchase-key or GPT_IMAGE_PURCHASE_KEY', stringValue(args['purchase-key'], process.env.GPT_IMAGE_PURCHASE_KEY));
  const sessionInfo = await ensureRelaySession(args, { save: boolValue(args['save-session']) });
  const user = await redeemPurchaseKey(args, sessionInfo);
  process.stdout.write(
    redactedSummary({
      ok: true,
      serviceUrl: sessionInfo.serviceRoot,
      user: user || sessionInfo.user,
    }) + '\n'
  );
}

async function commandQuota(args) {
  const sessionInfo = await ensureRelaySession(args, { save: false });
  const status = await postRelayJson(sessionInfo.serviceRoot, '/api/keys', { action: 'status' }, sessionInfo.user.id);
  const free = await postRelayJson(sessionInfo.serviceRoot, '/api/keys', { action: 'check_free' }, sessionInfo.user.id);
  process.stdout.write(
    redactedSummary({
      ok: true,
      serviceUrl: sessionInfo.serviceRoot,
      free: !!free.free,
      freeQuota: status.freeQuota ?? null,
      user: status.user || sessionInfo.user,
    }) + '\n'
  );
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const command = args._[0] || 'generate';

  if (args.help || args.h || command === 'help') {
    process.stdout.write(`${help()}\n`);
    return;
  }

  if (typeof fetch !== 'function') {
    throw new Error('Node 18+ is required because this script uses global fetch');
  }

  if (command === 'generate') {
    await commandGenerate(args);
    return;
  }

  if (command === 'session') {
    await commandSession(args);
    return;
  }

  if (command === 'redeem') {
    await commandRedeem(args);
    return;
  }

  if (command === 'quota') {
    await commandQuota(args);
    return;
  }

  throw new Error(`Unknown command: ${command}`);
}

main().catch((error) => {
  process.stderr.write(
    redactedSummary({
      ok: false,
      error: String(error && error.message ? error.message : error),
      status: error && error.status ? error.status : null,
      body: error && error.body ? summarizeFailure(error.body) : null,
    }) + '\n'
  );
  process.exit(1);
});
