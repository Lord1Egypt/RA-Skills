#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { loadPublishTask, validatePublishTask } from './validate-publish-task.js';

function usage() {
  console.error(`Usage:
  node scripts/run-publish-task-stability.js --task templates/publish-task.stability.json [--rounds 3] [--execute] [--allow-unsupported]

Default mode is dry-run. Add --execute to publish for real.
Pass condition: every round must publish and verify successfully; default is 3 consecutive successes.
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

function runNode(args, opts = {}) {
  const result = spawnSync(process.execPath, args, {
    cwd: process.cwd(),
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
    timeout: Number(opts.timeout || 480000),
  });
  return {
    ok: result.status === 0,
    status: result.status,
    signal: result.signal,
    timedOut: result.error?.code === 'ETIMEDOUT' || result.signal === 'SIGTERM',
    stdout: result.stdout || '',
    stderr: result.stderr || '',
    output: `${result.stderr || ''}${result.stdout || ''}`.trim(),
  };
}

function shouldAvoidCleanupNavigation(payload) {
  const error = payload?.error || payload?.publish?.error;
  const url = payload?.detail?.url || payload?.publish?.detail?.url || payload?.publish?.state?.url;
  return error === 'editor_has_unpublished_changes'
    || error === 'publish_verification_required'
    || error === 'publish_submit_unconfirmed'
    || error === 'upload_timeout'
    || (typeof url === 'string' && url.includes('/content/post/video'));
}

function parseLastJson(text) {
  const trimmed = String(text || '').trim();
  const candidates = [];
  let depth = 0;
  let start = -1;
  let inString = false;
  let escaped = false;
  for (let i = 0; i < trimmed.length; i += 1) {
    const ch = trimmed[i];
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
      if (depth === 0 && start !== -1) {
        candidates.push(trimmed.slice(start, i + 1));
        start = -1;
      }
    }
  }
  for (let i = candidates.length - 1; i >= 0; i -= 1) {
    try {
      return JSON.parse(candidates[i]);
    } catch {
      continue;
    }
  }
  return null;
}

function roundTitle(base, index) {
  const stamp = Date.now().toString().slice(-6);
  const suffix = ` r${index}-${stamp}`;
  return `${String(base || '模板稳定测试').slice(0, 30 - suffix.length)}${suffix}`;
}

function roundDescription(task, index, title) {
  const metadata = task.metadata || {};
  const baseDescription = metadata.description || title;
  return [
    baseDescription,
    `稳定性测试第 ${index} 轮`,
  ].filter(Boolean).join('\n');
}

function topicsFromTask(task) {
  const metadata = task.metadata || {};
  const raw = [
    ...(Array.isArray(metadata.topics) ? metadata.topics : []),
    ...(Array.isArray(metadata.tags) ? metadata.tags : []),
  ];
  const seen = new Set();
  return raw
    .map((item) => String(item || '').trim().replace(/^#+/, ''))
    .filter(Boolean)
    .filter((item) => {
      if (seen.has(item)) return false;
      seen.add(item);
      return true;
    });
}

function verifyPublishedWithRetry(title, opts = {}) {
  const attempts = Number(opts.attempts || 6);
  const waitMs = Number(opts.waitMs || 8000);
  const results = [];
  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    const verify = runNode([
      'scripts/douyin-cli.js',
      'verify-published',
      '--title',
      title,
      '--wait-ms',
      String(waitMs),
    ], { timeout: Math.max(90000, waitMs + 45000) });
    const payload = parseLastJson(verify.output);
    results.push({ attempt, ok: verify.ok, verify: payload || verify });
    if (verify.ok && payload?.found) {
      return { ok: true, attempts: results, verify: payload };
    }
  }
  return { ok: false, attempts: results, verify: results.at(-1)?.verify || null };
}

function planRounds(task, rounds) {
  const result = [];
  const videoPaths = Array.isArray(task.media?.videoPaths) && task.media.videoPaths.length
    ? task.media.videoPaths
    : [task.media.videoPath];
  for (let i = 1; i <= rounds; i += 1) {
    const title = roundTitle(task.metadata?.title, i);
    const videoPath = videoPaths[(i - 1) % videoPaths.length];
    result.push({
      round: i,
      title,
      description: roundDescription(task, i, title),
      topics: topicsFromTask(task),
      videoPath,
      coverImagePath: task.media?.cover?.imagePath || null,
      stableFields: {
        cover: task.media?.cover?.imagePath ? 'custom_image' : (task.media?.cover?.mode || 'auto_recommended'),
        visibility: task.settings?.visibility || 'public',
        allowSave: task.settings?.allowSave !== false,
        publishTime: task.settings?.publishTime?.mode || 'now',
      },
    });
  }
  return result;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.task || args.help) {
    usage();
    process.exit(args.help ? 0 : 2);
  }

  const rounds = Number(args.rounds || 3);
  const execute = Boolean(args.execute);
  const task = loadPublishTask(args.task);
  const validation = validatePublishTask(task, { allowUnsupported: Boolean(args.allowUnsupported) });
  const plan = validation.ok ? planRounds(task, rounds) : [];

  if (!validation.ok || !execute) {
    console.log(JSON.stringify({
      ok: validation.ok,
      mode: execute ? 'execute' : 'dry-run',
      passRule: `${rounds} consecutive successful publish+verify rounds`,
      validation,
      plan,
      executeCommand: `node scripts/run-publish-task-stability.js --task ${args.task} --rounds ${rounds} --execute`,
    }, null, 2));
    if (!validation.ok) process.exitCode = 1;
    return;
  }

  const preflight = runNode(['scripts/preflight.js'], { timeout: 120000 });
  const preflightPayload = parseLastJson(preflight.output);
  if (!preflight.ok || !preflightPayload?.ok) {
    console.log(JSON.stringify({
      ok: false,
      stage: 'preflight',
      preflight: preflightPayload || preflight,
    }, null, 2));
    process.exitCode = 1;
    return;
  }

  const results = [];
  for (const item of plan) {
    const publish = runNode([
      'scripts/publish-with-guard.js',
      '--file',
      item.videoPath,
      '--title',
      item.title,
      ...(item.description ? ['--description', item.description] : []),
      ...(item.topics?.length ? ['--topics', item.topics.join(',')] : []),
      ...(item.coverImagePath ? ['--cover-image', item.coverImagePath] : []),
      '--fresh',
    ], { timeout: 600000 });
    const publishPayload = parseLastJson(publish.output);
    if (!publish.ok) {
      let cleanup = null;
      if (!shouldAvoidCleanupNavigation(publishPayload)) {
        cleanup = runNode(['--input-type=module', '-e', `
          import { createDouyinSession, disconnect } from './src/index.js';
          const { ops } = await createDouyinSession();
          try {
            await ops.goUploadPage({ force: true });
            await ops.abandonUnpublishedDraft();
          } finally {
            disconnect();
          }
        `], { timeout: 60000 });
      }
      results.push({
        ...item,
        ok: false,
        stage: 'publish',
        publish: publishPayload || publish,
        cleanupSkipped: cleanup === null,
        cleanup: cleanup ? parseLastJson(cleanup.output) || cleanup : null,
      });
      break;
    }

    const verifyResult = verifyPublishedWithRetry(item.title);
    const verified = Boolean(verifyResult.ok);
    results.push({
      ...item,
      ok: verified,
      stage: verified ? 'verified' : 'verify',
      publish: publishPayload,
      verify: verifyResult.verify,
      verifyAttempts: verifyResult.attempts,
    });
    if (!verified) break;
  }

  const successCount = results.filter((item) => item.ok).length;
  const ok = successCount === rounds;
  console.log(JSON.stringify({
    ok,
    passRule: `${rounds} consecutive successful publish+verify rounds`,
    successCount,
    rounds,
    results,
  }, null, 2));
  if (!ok) process.exitCode = 1;
}

main().catch((err) => {
  console.log(JSON.stringify({ ok: false, error: err.message, stack: err.stack }, null, 2));
  process.exit(1);
});
