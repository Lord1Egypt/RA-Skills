#!/usr/bin/env node
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

const DEFAULT_BASE_URL = 'https://airemovewatermark.net';
const DEFAULT_OUTPUT_DIR = path.resolve(
  process.cwd(),
  '.openclaw-artifacts',
  'remove-watermark',
);

function parseArgs(argv) {
  const args = { _: [] };

  for (let i = 0; i < argv.length; i += 1) {
    const current = argv[i];
    if (!current.startsWith('--')) {
      args._.push(current);
      continue;
    }

    const key = current.slice(2);
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

function printHelp() {
  console.log(`Usage:
  node scripts/remove_watermark.mjs credits [--api-key <key>] [--base-url <url>]
  node scripts/remove_watermark.mjs remove --file <path> [--wait true] [--download true] [--api-key <key>] [--base-url <url>]
  node scripts/remove_watermark.mjs remove --image-url <url> [--wait true] [--download true] [--api-key <key>] [--base-url <url>]
  node scripts/remove_watermark.mjs task --task-id <id> [--download true] [--api-key <key>] [--base-url <url>]

Defaults:
  base URL defaults to ${DEFAULT_BASE_URL}
  remove waits for completion by default
  completed jobs are not downloaded unless --download true is set
  downloaded files are saved to ${DEFAULT_OUTPUT_DIR}
`);
}

function getConfig(args) {
  const baseUrl = String(
    args['base-url'] ||
      process.env.API_BASE_URL ||
      process.env.REMOVE_WATERMARK_BASE_URL ||
      DEFAULT_BASE_URL
  ).trim();
  const apiKey = String(
    args['api-key'] ||
      process.env.API_KEY ||
      process.env.REMOVE_WATERMARK_API_KEY ||
      ''
  ).trim();

  if (!apiKey) {
    throw new Error(
      'Missing API key. Set API_KEY, REMOVE_WATERMARK_API_KEY, or --api-key'
    );
  }

  return {
    apiKey,
    baseUrl: baseUrl.replace(/\/+$/, ''),
  };
}

function getHeaders(apiKey, extra = {}) {
  return {
    authorization: `Bearer ${apiKey}`,
    ...extra,
  };
}

function guessMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();

  switch (ext) {
    case '.jpg':
    case '.jpeg':
      return 'image/jpeg';
    case '.png':
      return 'image/png';
    case '.webp':
      return 'image/webp';
    default:
      return 'application/octet-stream';
  }
}

async function requestJson(url, init) {
  const response = await fetch(url, init);
  const text = await response.text();

  let json;
  try {
    json = JSON.parse(text);
  } catch {
    throw new Error(`API returned an unreadable response (${response.status})`);
  }

  if (!response.ok || json?.code !== 0) {
    throw new Error(
      humanizeApiError(
        json?.message || `Request failed with status ${response.status}`,
        response.status
      )
    );
  }

  return json;
}

function humanizeApiError(message, status = 0) {
  const normalized = String(message || '').trim();
  const lower = normalized.toLowerCase();

  if (
    status === 401 ||
    status === 403 ||
    lower.includes('invalid api key') ||
    lower.includes('invalid key') ||
    lower.includes('unauthorized') ||
    lower.includes('forbidden')
  ) {
    return 'API key is invalid or not authorized. Check API_KEY and try again.';
  }

  if (
    lower.includes('insufficient') &&
    (lower.includes('credit') || lower.includes('balance'))
  ) {
    return 'Insufficient credits. Add credits, then try the request again.';
  }

  if (
    lower.includes('unsupported') ||
    lower.includes('invalid image') ||
    lower.includes('invalid file type') ||
    lower.includes('file type')
  ) {
    return 'The image format is not supported. Use a JPG, PNG, or WebP image.';
  }

  if (status >= 500 || lower.includes('timeout') || lower.includes('timed out')) {
    return 'The remove-watermark service is temporarily unavailable or timed out. Please try again.';
  }

  return normalized || 'The request failed. Please try again.';
}

function getTaskOutputUrl(json) {
  return (
    json?.data?.task?.outputUrl ||
    json?.data?.outputUrl ||
    json?.outputUrl ||
    ''
  );
}

function parseBooleanFlag(value, defaultValue = false) {
  if (value === undefined || value === null || value === '') {
    return defaultValue;
  }

  const normalized = String(value).trim().toLowerCase();
  if (['true', '1', 'yes'].includes(normalized)) {
    return true;
  }

  if (['false', '0', 'no'].includes(normalized)) {
    return false;
  }

  return defaultValue;
}

function getTaskStatus(json) {
  return String(json?.data?.task?.status || json?.data?.status || '').trim();
}

function getTaskId(json) {
  return String(json?.data?.task?.id || json?.data?.id || json?.id || '').trim();
}

function isCompletedStatus(status) {
  const normalized = String(status || '').trim().toLowerCase();
  return ['completed', 'complete', 'succeeded', 'success', 'done'].includes(
    normalized
  );
}

function isFailedStatus(status) {
  const normalized = String(status || '').trim().toLowerCase();
  return ['failed', 'error', 'cancelled', 'canceled'].includes(normalized);
}

function isCompletedResponse(json) {
  if (json?.data?.completed === true || json?.completed === true) {
    return true;
  }

  return isCompletedStatus(getTaskStatus(json));
}

function inferOutputExtension(outputUrl, fallbackName = '') {
  const fromName = path.extname(String(fallbackName || '').trim());
  if (fromName) {
    return fromName.toLowerCase();
  }

  try {
    const parsed = new URL(outputUrl);
    const fromUrl = path.extname(parsed.pathname);
    if (fromUrl) {
      return fromUrl.toLowerCase();
    }
  } catch {
    // ignore URL parsing errors
  }

  return '.png';
}

function sanitizeFileStem(value) {
  const stem = String(value || '')
    .trim()
    .replace(/\.[^.]+$/, '')
    .replace(/[^a-zA-Z0-9._-]+/g, '-')
    .replace(/^-+|-+$/g, '');

  return stem || 'watermark-result';
}

function getDefaultDownloadTarget({ json, sourceFilePath, outputDir }) {
  const taskId = getTaskId(json);
  const outputUrl = String(getTaskOutputUrl(json) || '').trim();
  const fileStem = sanitizeFileStem(
    sourceFilePath ? path.basename(sourceFilePath) : taskId || 'watermark-result'
  );
  const ext = inferOutputExtension(outputUrl, sourceFilePath);
  return path.join(outputDir, `${fileStem}-cleaned${ext}`);
}

function getTrustedDownloadHosts(baseUrl) {
  const hosts = new Set(['assets.airemovewatermark.net']);

  try {
    hosts.add(new URL(baseUrl).host);
  } catch {
    // ignore invalid base URL here; request path validation happens elsewhere
  }

  return hosts;
}

function assertTrustedOutputUrl(outputUrl, baseUrl) {
  let parsed;

  try {
    parsed = new URL(outputUrl);
  } catch {
    throw new Error('The API returned an invalid output URL.');
  }

  if (parsed.protocol !== 'https:') {
    throw new Error('The API returned a non-HTTPS output URL.');
  }

  if (!getTrustedDownloadHosts(baseUrl).has(parsed.host)) {
    throw new Error(
      `The API returned an untrusted output host: ${parsed.host}.`
    );
  }
}

async function maybeDownloadOutput(json, options = {}) {
  const status = getTaskStatus(json);
  const outputUrl = String(getTaskOutputUrl(json) || '').trim();
  const isCompleted = isCompletedResponse(json);
  const shouldDownload = parseBooleanFlag(options.download, false);

  if (!outputUrl || !isCompleted || !shouldDownload) {
    return null;
  }

  if (!outputUrl) {
    throw new Error(
      `No outputUrl found in response${status ? ` (status: ${status})` : ''}`
    );
  }

  assertTrustedOutputUrl(outputUrl, options.baseUrl || DEFAULT_BASE_URL);

  const targetPath = getDefaultDownloadTarget({
    json,
    sourceFilePath: options.sourceFilePath,
    outputDir: DEFAULT_OUTPUT_DIR,
  });
  const response = await fetch(outputUrl);
  if (!response.ok) {
    throw new Error(`Failed to download output: ${response.status}`);
  }

  const arrayBuffer = await response.arrayBuffer();
  const absolutePath = path.resolve(targetPath);
  await mkdir(path.dirname(absolutePath), { recursive: true });
  await writeFile(absolutePath, new Uint8Array(arrayBuffer));
  return absolutePath;
}

function buildCreditsResult(json) {
  const credits =
    json?.data?.remainingCredits ??
    json?.data?.credits ??
    json?.data?.balance ??
    null;

  return {
    status: 'succeeded',
    command: 'credits',
    credits_remaining: credits,
    result_summary:
      credits === null
        ? 'Credits retrieved successfully.'
        : `Credits retrieved successfully. Remaining credits: ${credits}.`,
    raw: json,
  };
}

function buildTaskResult(json, context = {}) {
  const status = getTaskStatus(json) || 'unknown';
  const taskId = getTaskId(json) || null;
  const completed = isCompletedResponse(json);
  const failed = isFailedStatus(status);
  const outputUrl = String(getTaskOutputUrl(json) || '').trim() || null;
  const resultFile = context.resultFile || null;

  let resultSummary = 'Task status retrieved.';
  if (completed && resultFile) {
    resultSummary = `Watermark removed successfully. Result saved to ${resultFile}.`;
  } else if (completed) {
    resultSummary = 'Watermark removed successfully.';
  } else if (failed) {
    resultSummary = 'The watermark removal task failed.';
  } else if (taskId) {
    resultSummary = `Task is still ${status}. Poll again with task --task-id ${taskId}.`;
  }

  return {
    status: failed ? 'failed' : completed ? 'succeeded' : 'processing',
    command: context.command || 'task',
    task_id: taskId,
    completed,
    result_file: resultFile,
    output_url: outputUrl,
    result_summary: resultSummary,
    next_action:
      !completed && !failed && taskId
        ? `Run: node scripts/remove_watermark.mjs task --task-id ${taskId}`
        : null,
    raw: json,
  };
}

async function runCredits(config) {
  const json = await requestJson(`${config.baseUrl}/api/v1/credits`, {
    headers: getHeaders(config.apiKey),
    method: 'GET',
  });

  console.log(JSON.stringify(buildCreditsResult(json), null, 2));
}

async function runTask(config, args) {
  const taskId = String(args['task-id'] || '').trim();
  if (!taskId) {
    throw new Error('Missing --task-id');
  }

  const json = await requestJson(
    `${config.baseUrl}/api/v1/watermark/tasks/${encodeURIComponent(taskId)}`,
    {
      headers: getHeaders(config.apiKey),
      method: 'GET',
    }
  );

  const resultFile = await maybeDownloadOutput(json, {
    download: args.download,
    baseUrl: config.baseUrl,
  });
  console.log(
    JSON.stringify(
      buildTaskResult(json, {
        command: 'task',
        resultFile,
      }),
      null,
      2
    )
  );
}

async function runRemove(config, args) {
  const filePath = String(args.file || '').trim();
  const imageUrl = String(args['image-url'] || '').trim();
  const wait = String(args.wait || 'true')
    .trim()
    .toLowerCase();

  if (!filePath && !imageUrl) {
    throw new Error('Provide --file or --image-url');
  }

  if (filePath && imageUrl) {
    throw new Error('Provide only one of --file or --image-url');
  }

  let json;
  if (filePath) {
    const absolutePath = path.resolve(filePath);
    const bytes = await readFile(absolutePath);
    const formData = new FormData();
    formData.set(
      'file',
      new File([bytes], path.basename(absolutePath), {
        type: guessMimeType(absolutePath),
      })
    );
    formData.set('wait', wait);

    json = await requestJson(`${config.baseUrl}/api/v1/watermark/remove`, {
      body: formData,
      headers: getHeaders(config.apiKey),
      method: 'POST',
    });
  } else {
    json = await requestJson(`${config.baseUrl}/api/v1/watermark/remove`, {
      body: JSON.stringify({
        imageUrl,
        wait,
      }),
      headers: getHeaders(config.apiKey, {
        'content-type': 'application/json',
      }),
      method: 'POST',
    });
  }

  const resultFile = await maybeDownloadOutput(json, {
    download: args.download,
    sourceFilePath: filePath,
    baseUrl: config.baseUrl,
  });
  console.log(
    JSON.stringify(
      buildTaskResult(json, {
        command: 'remove',
        resultFile,
      }),
      null,
      2
    )
  );
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help || args.h) {
    printHelp();
    return;
  }

  const command = args._[0] || 'remove';

  if (command === 'help') {
    printHelp();
    return;
  }

  const config = getConfig(args);

  switch (command) {
    case 'credits':
      await runCredits(config);
      return;
    case 'task':
      await runTask(config, args);
      return;
    case 'remove':
      await runRemove(config, args);
      return;
    default:
      throw new Error(`Unknown command: ${command}`);
  }
}

main().catch((error) => {
  const message = error instanceof Error ? error.message : String(error);
  console.log(
    JSON.stringify(
      {
        status: 'error',
        result_summary: message,
      },
      null,
      2
    )
  );
  process.exitCode = 1;
});
