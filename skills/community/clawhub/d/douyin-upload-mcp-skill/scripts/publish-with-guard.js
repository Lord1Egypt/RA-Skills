#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';

function usage() {
  console.error(`Usage:
  node scripts/publish-with-guard.js --file /abs/video.mp4 [--title 标题] [--description 简介] [--topics 话题1,话题2] [--cover-image /abs/cover.png] [--timeout 1800000] [--assistant-timeout 600000] [--notify] [--fresh]
`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) continue;
    const key = item.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (next === undefined || next.startsWith('--')) {
      args[key] = true;
    } else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function runNode(args) {
  return spawnSync(process.execPath, args, {
    cwd: process.cwd(),
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
}

function extractJson(stdout) {
  const start = stdout.indexOf('{');
  const end = stdout.lastIndexOf('}');
  if (start === -1 || end === -1 || end <= start) {
    throw new Error(`No JSON payload found in output:\n${stdout}`);
  }
  return JSON.parse(stdout.slice(start, end + 1));
}

function printResult(result) {
  console.log(JSON.stringify(result, null, 2));
}

function safeExtractJson(text) {
  try {
    return extractJson(text || '');
  } catch {
    return null;
  }
}

function isRetryablePublishError(payload) {
  return [
    'publish_btn_not_found',
    'publish_btn_obstructed',
    'publish_btn_disabled',
    'publish_submit_unconfirmed',
    'publish_click_returned_to_upload',
    'publish_editor_not_ready',
    'editor_has_unpublished_changes',
  ].includes(payload?.error);
}

function cleanupFailedUploadDraft() {
  return runNode(['--input-type=module', '-e', `
    import { createDouyinSession, disconnect } from './src/index.js';
    const { ops } = await createDouyinSession();
    try {
      await ops.goUploadPage({ force: true });
      console.log(JSON.stringify(await ops.abandonUnpublishedDraft(), null, 2));
    } finally {
      disconnect();
    }
  `]);
}

const args = parseArgs(process.argv.slice(2));
if (!args.file || args.help) {
  usage();
  process.exit(args.help ? 0 : 2);
}
if (!existsSync(args.file)) {
  printResult({ ok: false, error: 'file_not_found', file: args.file });
  process.exit(2);
}

// Preflight must not pass --title here: title verification navigates to the
// works-management page and can interrupt an active publish editor.
const stateArgs = ['scripts/douyin-cli.js', 'publish-state'];
const stateBefore = runNode(stateArgs);
const statePayload = (() => {
  try {
    return extractJson(stateBefore.stdout || '');
  } catch {
    return null;
  }
})();
if (statePayload?.verification?.found) {
  printResult({
    ok: false,
    error: 'publish_verification_required',
    detail: statePayload.verification,
  });
  process.exit(1);
}
if (
  !args.fresh
  &&
  statePayload?.currentPage?.url?.includes('/content/post/video')
  && statePayload?.assistant
  && statePayload.assistant.ready !== true
) {
  printResult({
    ok: false,
    error: 'editor_in_progress',
    detail: {
      message: '当前仍在发布编辑页且发文助手/上传状态未完成，已停止新上传，避免触发离开页面弹窗。',
      assistant: statePayload.assistant,
      currentPage: statePayload.currentPage,
    },
  });
  process.exit(1);
}

const checkArgs = ['scripts/douyin-login-monitor.js', 'check'];
if (args.notify) checkArgs.push('--notify', '--send-qr', 'ask');
const check = runNode(checkArgs);
process.stderr.write(check.stderr || '');
const checkPayload = extractJson(check.stdout);

if (checkPayload.kind !== 'logged_in') {
  printResult({
    ok: false,
    blocked: true,
    reason: checkPayload.kind,
    phase: checkPayload.phase,
    qrcodePath: checkPayload.qrcodePath,
    screenshotPath: checkPayload.screenshotPath,
    advice: checkPayload.advice,
    notify: checkPayload.notify,
  });
  process.exit(3);
}

const publishArgs = ['scripts/douyin-cli.js', 'publish-video', '--file', args.file];
if (args.title) publishArgs.push('--title', args.title);
if (args.description) publishArgs.push('--description', args.description);
if (args.topics) publishArgs.push('--topics', args.topics);
if (args.coverImage) publishArgs.push('--cover-image', args.coverImage);
if (args.timeout) publishArgs.push('--timeout', args.timeout);
if (args.assistantTimeout) publishArgs.push('--assistant-timeout', args.assistantTimeout);
if (args.fresh) publishArgs.push('--fresh');
let publish = runNode(publishArgs);
let payload = safeExtractJson(publish.stdout || publish.output || '');

if (publish.status !== 0 && payload?.error === 'upload_failed') {
  const cleanup = cleanupFailedUploadDraft();
  const second = runNode(publishArgs);
  const secondPayload = safeExtractJson(second.stdout || second.output || '');
  if (second.status === 0) {
    process.stderr.write(`${publish.stderr || ''}${cleanup.stderr || ''}${second.stderr || ''}`);
    process.stdout.write(second.stdout || '');
    process.exit(0);
  }
  publish = second;
  payload = secondPayload || payload;
}

if (publish.status !== 0 && isRetryablePublishError(payload)) {
  const retryArgs = ['scripts/douyin-cli.js', 'publish-current-draft'];
  if (args.title) retryArgs.push('--title', args.title);
  const retry = runNode(retryArgs);
  if (retry.status === 0) {
    process.stderr.write(`${publish.stderr || ''}${retry.stderr || ''}`);
    process.stdout.write(retry.stdout || '');
    process.exit(0);
  }
  printResult({
    ok: false,
    error: 'publish_retry_failed',
    first: payload || safeExtractJson(publish.stdout || '') || { status: publish.status, output: publish.output },
    retry: safeExtractJson(retry.stdout || '') || { status: retry.status, output: retry.output },
  });
  process.exit(1);
}

process.stderr.write(publish.stderr || '');
process.stdout.write(publish.stdout || '');
process.exit(publish.status ?? 1);
