#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { createWriteStream, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { basename, extname, join } from 'node:path';
import { pipeline } from 'node:stream/promises';
import { validatePublishTask } from './validate-publish-task.js';

const DEFAULT_STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(process.env.HOME || '.', '.openclaw', 'workspace', 'douyin-ops');
const DEFAULT_CACHE_DIR = process.env.DOUYIN_FEISHU_UPSTREAM_CACHE_DIR || join(DEFAULT_STATE_DIR, 'upstream');

function usage() {
  console.error(`Usage:
  node scripts/prepare-upstream-publish-task.js --input upstream.json [--output templates/publish-task.from-upstream.json] [--cache-dir /path]

Input can use either normalized publishTask fields or field aliases:
  tags: "#宠物险#保险"
  标题: "养宠不焦虑的秘诀？"
  视频地址: "https://.../video.mp4"
  封面图片: "https://.../cover.png"
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

function trimString(value) {
  return typeof value === 'string' ? value.trim() : value;
}

function parseMaybeJson(text) {
  const raw = text.trim();
  if (raw.startsWith('{')) return JSON.parse(raw);

  const result = {};
  for (const line of raw.split(/\r?\n/)) {
    const cleaned = line.trim().replace(/,$/, '');
    if (!cleaned) continue;
    const match = cleaned.match(/^"?([^":：]+)"?\s*[:：]\s*(.+)$/);
    if (!match) continue;
    const key = match[1].trim();
    let value = match[2].trim().replace(/^["“”]|["“”]$/g, '').trim();
    result[key] = value;
  }
  return result;
}

function splitTags(value) {
  if (Array.isArray(value)) return value.map((item) => String(item).replace(/^#+/, '').trim()).filter(Boolean);
  if (typeof value !== 'string') return [];
  return value
    .split(/(?=#)|[,，\s]+/)
    .map((item) => item.replace(/^#+/, '').trim())
    .filter(Boolean);
}

function normalizePublishTitle(value, maxLength = 60) {
  const clean = trimString(value);
  if (typeof clean !== 'string') return clean;
  const withoutTags = clean
    .replace(/#[^\s#，。,;；!！?？)）(（]+/g, '')
    .replace(/\s+/g, ' ')
    .replace(/[，,、；;：:|｜\\/-]+$/g, '')
    .trim();
  return Array.from(withoutTags).slice(0, maxLength).join('');
}

function extensionFromUrl(url, fallback) {
  try {
    const parsed = new URL(url);
    const ext = extname(parsed.pathname);
    if (ext) return ext;
  } catch {
    // Fall through.
  }
  return fallback;
}

async function downloadToCache(url, opts = {}) {
  const cleanUrl = trimString(url);
  if (!cleanUrl) return null;
  const cacheDir = opts.cacheDir || DEFAULT_CACHE_DIR;
  mkdirSync(cacheDir, { recursive: true });
  const hash = createHash('sha256').update(cleanUrl).digest('hex').slice(0, 16);
  const ext = extensionFromUrl(cleanUrl, opts.fallbackExt || '.bin');
  const outputPath = join(cacheDir, `${hash}${ext}`);
  if (existsSync(outputPath)) return outputPath;

  let response;
  try {
    response = await fetch(cleanUrl);
  } catch (err) {
    const label = opts.label || '资源';
    const error = new Error(`${label}下载失败，请重新发送可访问的${label}链接。`);
    error.code = `${opts.kind || 'resource'}_download_failed`;
    error.customerMessage = error.message;
    error.detail = err.message;
    error.url = cleanUrl;
    throw error;
  }
  if (!response.ok || !response.body) {
    const label = opts.label || '资源';
    const error = new Error(`${label}下载失败，请重新发送可访问的${label}链接。`);
    error.code = `${opts.kind || 'resource'}_download_failed`;
    error.customerMessage = error.message;
    error.status = response.status;
    error.url = cleanUrl;
    throw error;
  }
  await pipeline(response.body, createWriteStream(outputPath));
  return outputPath;
}

function normalizeUpstream(input, downloaded = {}) {
  const title = normalizePublishTitle(input['标题'] ?? input.title ?? input.metadata?.title);
  const videoUrl = trimString(input['视频地址'] ?? input.videoUrl ?? input.media?.videoUrl);
  const coverUrl = trimString(input['封面图片'] ?? input.coverImageUrl ?? input.media?.cover?.imageUrl);
  const topics = splitTags(input.tags ?? input['tags'] ?? input.metadata?.topics ?? input.metadata?.tags);
  const description = trimString(input.description ?? input.metadata?.description) || '';

  return {
    type: 'video',
    media: {
      videoPath: downloaded.videoPath || input.media?.videoPath || null,
      videoUrl,
      videoPaths: [],
      cover: {
        mode: 'auto_recommended',
        imagePath: downloaded.coverImagePath || input.media?.cover?.imagePath || null,
        imageUrl: coverUrl || null,
      },
    },
    metadata: {
      title,
      description,
      topics,
      mentions: [],
      collection: null,
      declaration: null,
      chapters: [],
      tags: topics,
      location: null,
      hotspot: null,
    },
    settings: {
      visibility: 'public',
      allowSave: true,
      publishTime: {
        mode: 'now',
        scheduledAt: null,
      },
    },
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.input || args.help) {
    usage();
    process.exit(args.help ? 0 : 2);
  }
  const inputPath = args.input;
  const outputPath = args.output || 'templates/publish-task.from-upstream.json';
  const cacheDir = args.cacheDir || DEFAULT_CACHE_DIR;
  const input = parseMaybeJson(readFileSync(inputPath, 'utf8'));
  const initial = normalizeUpstream(input);
  const downloaded = {
    videoPath: initial.media.videoUrl ? await downloadToCache(initial.media.videoUrl, { cacheDir, fallbackExt: '.mp4', kind: 'video', label: '视频' }) : null,
    coverImagePath: initial.media.cover.imageUrl ? await downloadToCache(initial.media.cover.imageUrl, { cacheDir, fallbackExt: '.png', kind: 'cover', label: '封面' }) : null,
  };
  const task = normalizeUpstream(input, downloaded);
  writeFileSync(outputPath, `${JSON.stringify(task, null, 2)}\n`);
  const validation = validatePublishTask(task);
  console.log(JSON.stringify({
    ok: validation.ok,
    outputPath,
    source: basename(inputPath),
    downloaded,
    validation,
  }, null, 2));
  if (!validation.ok) process.exitCode = 1;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((err) => {
    console.log(JSON.stringify({
      ok: false,
      error: err.code || 'prepare_failed',
      message: err.message,
      customerMessage: err.customerMessage || '素材处理失败，请重新发送可用的视频和封面。',
      detail: err.detail,
      status: err.status,
      url: err.url,
      stack: err.stack,
    }, null, 2));
    process.exit(1);
  });
}
