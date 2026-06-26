#!/usr/bin/env node

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const token = argv[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      if (args[key] === undefined) {
        args[key] = true;
      } else if (Array.isArray(args[key])) {
        args[key].push(true);
      } else {
        args[key] = [args[key], true];
      }
    } else {
      if (args[key] === undefined) {
        args[key] = next;
      } else if (Array.isArray(args[key])) {
        args[key].push(next);
      } else {
        args[key] = [args[key], next];
      }
      i++;
    }
  }
  return args;
}

function getApiKey() {
  const primary = process.env.ASR_DASHSCOPE_API_KEY;
  if (primary) return primary;
  const fallback = process.env.DASHSCOPE_API_KEY;
  if (fallback) return fallback;
  throw new Error('Missing required environment variable: ASR_DASHSCOPE_API_KEY (or DASHSCOPE_API_KEY)');
}

function asArray(value) {
  if (value === undefined) return [];
  return Array.isArray(value) ? value : [value];
}

function getLanguageHints() {
  const raw = process.env.ALIYUN_SPEECH_LANG_HINTS || 'zh,en';
  return raw.split(',').map((item) => item.trim()).filter(Boolean);
}

async function submitTask({ apiKey, model, fileUrls, languageHints }) {
  const response = await fetch('https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'X-DashScope-Async': 'enable'
    },
    body: JSON.stringify({
      model,
      parameters: {
        language_hints: languageHints
      },
      input: {
        file_urls: fileUrls
      }
    })
  });

  const text = await response.text();
  let payload = {};
  try {
    payload = text ? JSON.parse(text) : {};
  } catch {
    payload = { raw: text };
  }

  if (!response.ok) {
    throw new Error(`DashScope submit failed (${response.status}): ${text}`);
  }

  return payload;
}

async function queryTask({ apiKey, taskId }) {
  const response = await fetch(`https://dashscope.aliyuncs.com/api/v1/tasks/${taskId}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${apiKey}`
    }
  });

  const text = await response.text();
  let payload = {};
  try {
    payload = text ? JSON.parse(text) : {};
  } catch {
    payload = { raw: text };
  }

  if (!response.ok) {
    throw new Error(`DashScope query failed (${response.status}): ${text}`);
  }

  return payload;
}

async function fetchJson(url) {
  const response = await fetch(url);
  const text = await response.text();
  if (!response.ok) {
    throw new Error(`Fetch transcription result failed (${response.status}): ${text}`);
  }
  try {
    return text ? JSON.parse(text) : {};
  } catch {
    return { raw: text };
  }
}

function extractPlainText(raw) {
  if (!raw || typeof raw !== 'object') return '';

  const transcripts = Array.isArray(raw.transcripts) ? raw.transcripts : [];
  const directTexts = transcripts
    .map((item) => (item && typeof item.text === 'string' ? item.text.trim() : ''))
    .filter(Boolean);
  if (directTexts.length > 0) {
    return directTexts.join('\n\n');
  }

  const sentenceTexts = transcripts
    .flatMap((item) => Array.isArray(item?.sentences) ? item.sentences : [])
    .map((sentence) => (sentence && typeof sentence.text === 'string' ? sentence.text.trim() : ''))
    .filter(Boolean);
  if (sentenceTexts.length > 0) {
    return sentenceTexts.join('\n');
  }

  return '';
}

async function waitForCompletion({ apiKey, taskId, pollSeconds, timeoutSeconds }) {
  const startedAt = Date.now();
  while (true) {
    const payload = await queryTask({ apiKey, taskId });
    const status = payload?.output?.task_status || payload?.task_status || payload?.output?.status;

    if (status === 'SUCCEEDED') {
      return payload;
    }
    if (status === 'FAILED' || status === 'CANCELED') {
      throw new Error(`DashScope task ended with status ${status}: ${JSON.stringify(payload)}`);
    }

    if ((Date.now() - startedAt) / 1000 > timeoutSeconds) {
      throw new Error(`DashScope task timeout after ${timeoutSeconds} seconds`);
    }

    await new Promise((resolve) => setTimeout(resolve, pollSeconds * 1000));
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const fileUrls = asArray(args['file-url']);
  if (fileUrls.length === 0) {
    throw new Error('Missing required argument: --file-url');
  }

  const apiKey = getApiKey();
  const model = process.env.ALIYUN_SPEECH_MODEL || 'paraformer-v2';
  const languageHints = getLanguageHints();
  const pollSeconds = Number(process.env.ALIYUN_SPEECH_POLL_SECONDS || 5);
  const timeoutSeconds = Number(process.env.ALIYUN_SPEECH_TIMEOUT_SECONDS || 1800);

  const submitted = await submitTask({ apiKey, model, fileUrls, languageHints });
  const taskId = submitted?.output?.task_id || submitted?.task_id;
  const requestId = submitted?.request_id || submitted?.requestId || null;
  if (!taskId) {
    throw new Error(`DashScope did not return task_id: ${JSON.stringify(submitted)}`);
  }

  const completed = await waitForCompletion({ apiKey, taskId, pollSeconds, timeoutSeconds });
  const taskResults = completed?.output?.results || completed?.results || [];

  const hydratedResults = [];
  for (const item of taskResults) {
    const transcriptionUrl = item?.transcription_url || item?.transcriptionUrl;
    if (!transcriptionUrl) {
      hydratedResults.push({
        ...item,
        raw: null,
        text: ''
      });
      continue;
    }
    const raw = await fetchJson(transcriptionUrl);
    hydratedResults.push({
      ...item,
      raw,
      text: extractPlainText(raw)
    });
  }

  const finalText = hydratedResults.map((item) => item.text).filter(Boolean).join('\n\n');

  const result = {
    success: true,
    provider: 'aliyun',
    engine: 'dashscope',
    model,
    requestId,
    taskId,
    source: fileUrls,
    submitted,
    completed,
    results: hydratedResults,
    text: finalText
  };

  console.log(JSON.stringify(result, null, args.json ? 0 : 2));
}

main().catch((error) => {
  console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
  process.exit(1);
});
