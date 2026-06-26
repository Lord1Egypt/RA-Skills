#!/usr/bin/env node
import { existsSync, readFileSync } from 'node:fs';

function usage() {
  console.error(`Usage:
  node scripts/validate-publish-task.js --task templates/publish-task.stability.json [--allow-unsupported]
`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) continue;
    const key = item.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
    } else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

export function loadPublishTask(taskPath) {
  return JSON.parse(readFileSync(taskPath, 'utf8'));
}

function hasValue(value) {
  if (Array.isArray(value)) return value.length > 0;
  if (value && typeof value === 'object') return Object.keys(value).length > 0;
  return value !== null && value !== undefined && value !== '';
}

function isHttpUrl(value) {
  if (typeof value !== 'string') return false;
  try {
    const url = new URL(value.trim());
    return ['http:', 'https:'].includes(url.protocol);
  } catch {
    return false;
  }
}

function charLength(value) {
  return Array.from(String(value || '')).length;
}

export function validatePublishTask(task, opts = {}) {
  const errors = [];
  const warnings = [];
  const unsupported = [];

  if (!task || typeof task !== 'object') errors.push('task must be an object');
  if (task?.type !== 'video') errors.push('type must be "video"');

  const videoPaths = Array.isArray(task?.media?.videoPaths)
    ? task.media.videoPaths.filter((item) => typeof item === 'string' && item.trim())
    : [];
  const videoUrl = task?.media?.videoUrl;
  const videoPath = task?.media?.videoPath || videoPaths[0];
  if (!videoPath || typeof videoPath !== 'string') {
    if (!isHttpUrl(videoUrl)) errors.push('media.videoPath, media.videoPaths[0], or media.videoUrl is required');
  } else if (!existsSync(videoPath)) {
    errors.push(`media.videoPath does not exist: ${videoPath}`);
  }
  if (hasValue(videoUrl) && !isHttpUrl(videoUrl)) errors.push(`media.videoUrl must be http(s): ${videoUrl}`);
  for (const path of videoPaths) {
    if (!existsSync(path)) errors.push(`media.videoPaths item does not exist: ${path}`);
  }

  const coverMode = task?.media?.cover?.mode || 'auto_recommended';
  if (coverMode !== 'auto_recommended') {
    unsupported.push(`media.cover.mode=${coverMode}`);
  }
  const coverImagePath = task?.media?.cover?.imagePath;
  const coverImageUrl = task?.media?.cover?.imageUrl;
  if (hasValue(coverImagePath) && !existsSync(coverImagePath)) {
    errors.push(`media.cover.imagePath does not exist: ${coverImagePath}`);
  }
  if (hasValue(coverImageUrl) && !isHttpUrl(coverImageUrl)) errors.push(`media.cover.imageUrl must be http(s): ${coverImageUrl}`);
  if (hasValue(coverImageUrl) && !hasValue(coverImagePath)) warnings.push('media.cover.imageUrl must be downloaded to imagePath before publishing');

  const title = task?.metadata?.title;
  if (!title || typeof title !== 'string') errors.push('metadata.title is required');
  if (title && charLength(title) > 60) errors.push('metadata.title must be <=60 characters for Douyin');
  else if (title && charLength(title) > 30) warnings.push('metadata.title is longer than 30 characters; verify the page accepted it fully before publishing');

  const description = task?.metadata?.description;
  const topics = Array.isArray(task?.metadata?.topics) ? task.metadata.topics : [];
  const tags = Array.isArray(task?.metadata?.tags) ? task.metadata.tags : [];
  if (description !== undefined && typeof description !== 'string') errors.push('metadata.description must be a string');
  if (!description && !topics.length && !tags.length) errors.push('metadata.description or metadata.topics/tags is required');

  const metadata = task?.metadata || {};
  for (const key of ['mentions', 'collection', 'declaration', 'chapters', 'location', 'hotspot']) {
    if (hasValue(metadata[key])) unsupported.push(`metadata.${key}`);
  }

  const settings = task?.settings || {};
  if (!['public', 'friends', 'private'].includes(settings.visibility || 'public')) {
    errors.push('settings.visibility must be public, friends, or private');
  }
  if ((settings.visibility || 'public') !== 'public') unsupported.push(`settings.visibility=${settings.visibility}`);
  if (settings.allowSave !== undefined && settings.allowSave !== true) unsupported.push('settings.allowSave=false');
  const publishMode = settings.publishTime?.mode || 'now';
  if (!['now', 'scheduled'].includes(publishMode)) errors.push('settings.publishTime.mode must be now or scheduled');
  if (publishMode !== 'now') unsupported.push(`settings.publishTime.mode=${publishMode}`);
  if (hasValue(settings.publishTime?.scheduledAt)) unsupported.push('settings.publishTime.scheduledAt');

  if (unsupported.length && !opts.allowUnsupported) {
    errors.push(`unsupported fields requested: ${unsupported.join(', ')}`);
  }

  return {
    ok: errors.length === 0,
    stableAutomationOnly: unsupported.length === 0,
    errors,
    warnings,
    unsupported,
    normalized: {
      type: 'video',
      videoPath,
      videoPaths,
      videoUrl,
      coverImagePath,
      coverImageUrl,
      title,
      description,
      topics,
      tags,
      visibility: settings.visibility || 'public',
      allowSave: settings.allowSave !== false,
      publishTimeMode: publishMode,
    },
  };
}

function printJson(payload) {
  console.log(JSON.stringify(payload, null, 2));
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.task || args.help) {
    usage();
    process.exit(args.help ? 0 : 2);
  }
  const task = loadPublishTask(args.task);
  const result = validatePublishTask(task, { allowUnsupported: Boolean(args.allowUnsupported) });
  printJson(result);
  if (!result.ok) process.exitCode = 1;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((err) => {
    printJson({ ok: false, error: err.message, stack: err.stack });
    process.exit(1);
  });
}
