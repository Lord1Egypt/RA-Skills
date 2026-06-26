#!/usr/bin/env node
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { loadModelScopeRuntime } from './load-modelscope-runtime.mjs';

const RETRY_PREFIX = '(young woman, female, same face, same Claw Xiaoai appearance, highly realistic photo, East Asian ethnicity, do not change gender, keep same outfit and same scene)';

function fail(msg, code = 1) { console.error(msg); process.exit(code); }
async function readStdinText() {
  const chunks = [];
  for await (const chunk of process.stdin) chunks.push(chunk);
  return Buffer.concat(chunks.map((chunk) => Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk))).toString('utf8').trim();
}
function parseArgs(argv) {
  const out = { json: false, retry: 1 };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--json') out.json = true;
    else if (a === '--prompt-stdin') out.promptStdin = true;
    else if (a === '--prompt') out.prompt = argv[++i];
    else if (a === '--out') out.out = argv[++i];
    else if (a === '--retry') out.retry = Number(argv[++i] || 1);
  }
  return out;
}
async function fetchJson(url, timeoutMs, options = {}) {
  const res = await fetch(url, { ...options, signal: AbortSignal.timeout(timeoutMs) });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}: ${await res.text()}`);
  return res.json();
}
async function fetchBuffer(url, timeoutMs, options = {}) {
  const res = await fetch(url, { ...options, signal: AbortSignal.timeout(timeoutMs) });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return Buffer.from(await res.arrayBuffer());
}
async function generate(prompt, runtime) {
  const { apiKey, baseUrl, model, maxPolls, pollIntervalMs, timeoutMs } = runtime;
  const commonHeaders = { Authorization: `Bearer ${apiKey}`, 'Content-Type': 'application/json' };
  const submit = await fetchJson(`${baseUrl}v1/images/generations`, timeoutMs, {
    method: 'POST', headers: { ...commonHeaders, 'X-ModelScope-Async-Mode': 'true' }, body: JSON.stringify({ model, prompt })
  });
  const taskId = submit.task_id;
  if (!taskId) throw new Error(`Missing task_id in response: ${JSON.stringify(submit)}`);
  let last, imageUrl;
  for (let i = 0; i < maxPolls; i++) {
    last = await fetchJson(`${baseUrl}v1/tasks/${taskId}`, timeoutMs, { headers: { ...commonHeaders, 'X-ModelScope-Task-Type': 'image_generation' } });
    if (last.task_status === 'SUCCEED') {
      imageUrl = last.output_images?.[0];
      if (!imageUrl) throw new Error(`Task succeeded but no output_images: ${JSON.stringify(last)}`);
      return { taskId, imageUrl, last };
    }
    if (last.task_status === 'FAILED') throw new Error(`Image generation failed: ${JSON.stringify(last)}`);
    await new Promise(r => setTimeout(r, pollIntervalMs));
  }
  throw new Error(`Timed out waiting for task ${taskId}. Last response: ${JSON.stringify(last)}`);
}

const args = parseArgs(process.argv.slice(2));
if (args.promptStdin) args.prompt = args.prompt || await readStdinText();
if (!args.prompt) fail('Usage: generate-selfie.mjs --prompt <text> --out <file> [--json] [--retry N]');
const runtime = loadModelScopeRuntime();
if (!runtime.apiKey) fail('MODELSCOPE_API_KEY / MODELSCOPE_TOKEN is required, or save the skill API key in OpenClaw Skills so it is written to ~/.openclaw/openclaw.json.');
const outPath = resolve(args.out || './claw-xiaoai-selfie.jpg');
let err;
for (let attempt = 1; attempt <= Math.max(1, args.retry); attempt++) {
  const prompt = attempt === 1 ? args.prompt : `${RETRY_PREFIX}, ${args.prompt}`;
  try {
    const { taskId, imageUrl, last } = await generate(prompt, runtime);
    const buf = await fetchBuffer(imageUrl, runtime.timeoutMs);
    mkdirSync(dirname(outPath), { recursive: true });
    writeFileSync(outPath, buf);
    const result = { ok: true, task_id: taskId, image_url: imageUrl, saved_path: outPath, model: runtime.model, task_status: last.task_status, attempt };
    if (args.json) console.log(JSON.stringify(result, null, 2));
    else console.log(outPath);
    process.exit(0);
  } catch (e) {
    err = e;
  }
}
fail(String(err?.message || err || 'unknown error'));
