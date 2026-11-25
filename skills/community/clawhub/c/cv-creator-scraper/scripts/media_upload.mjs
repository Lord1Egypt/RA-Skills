#!/usr/bin/env node
// 上传本地视频文件到 CreatiVault 公开桶（链路2 摄入）
//
// 用法:
//   node scripts/media_upload.mjs '{"file_path":"/path/to/video.mp4"}'
//
// 参数:
//   file_path — 必填，本地视频文件绝对路径（mp4/mov/avi/mkv/webm，≤500MB）
//
// 返回:
//   oss_key   — 上传成功的 OSS key（仅用于上传结果追踪，submit 不接受它）
//   oss_url   — 公开可达的完整 URL，传给 video_audit_submit 的 oss_url
//   filename  — 原始文件名
//   size_bytes — 文件字节数
//
// 计费: 每次上传固定扣 20 credits（与文件体积无关）
//
// 错误码:
//   40001 - 文件格式不支持 / 文件过大
//   40101 - X-API-Key 无效
//   40104 - X-User-Identity 缺失

import { readFileSync, statSync, existsSync } from 'node:fs';
import { basename, extname } from 'node:path';

const ALLOWED_EXTS = new Set(['.mp4', '.mov', '.avi', '.mkv', '.webm']);
const MAX_FILE_SIZE_MB = 500;

const raw = process.argv[2];
if (!raw) {
  console.error(JSON.stringify({ error: '缺少参数: 需要 JSON 字符串，例如 \'{"file_path":"/path/to/video.mp4"}\'' }));
  process.exit(1);
}

let params;
try {
  params = JSON.parse(raw);
} catch {
  console.error(JSON.stringify({ error: '参数必须是有效的 JSON 字符串', received: raw }));
  process.exit(1);
}

const filePath = params.file_path;
if (!filePath) {
  console.error(JSON.stringify({ error: '缺少必填参数: file_path' }));
  process.exit(1);
}

// 1. 文件存在性 + 格式 + 大小校验
if (!existsSync(filePath)) {
  console.error(JSON.stringify({ error: `文件不存在: ${filePath}` }));
  process.exit(1);
}

const ext = extname(filePath).toLowerCase();
if (!ALLOWED_EXTS.has(ext)) {
  console.error(JSON.stringify({
    error: `不支持的文件格式 ${ext}`,
    allowed: Array.from(ALLOWED_EXTS),
    hint: '仅支持 mp4/mov/avi/mkv/webm',
  }));
  process.exit(1);
}

const stat = statSync(filePath);
const sizeMB = stat.size / (1024 * 1024);
if (sizeMB > MAX_FILE_SIZE_MB) {
  console.error(JSON.stringify({
    error: `文件过大 ${sizeMB.toFixed(1)}MB`,
    max: `${MAX_FILE_SIZE_MB}MB`,
    file_path: filePath,
  }));
  process.exit(1);
}

// 2. 环境变量
const API_BASE = (process.env.CV_API_BASE_URL || '').replace(/\/+$/, '');
const API_KEY = process.env.CV_API_KEY;
const USER_IDENTITY = process.env.CV_USER_IDENTITY;

if (!API_BASE || !API_KEY || !USER_IDENTITY) {
  console.error(JSON.stringify({
    error: '环境变量缺失',
    required: ['CV_API_BASE_URL', 'CV_API_KEY', 'CV_USER_IDENTITY'],
  }));
  process.exit(1);
}

// 3. 加载 skill meta（用于 X-CV-Skill-* headers）
let skillMeta = { name: 'creator-scraper-cv', version: 'unknown', channel: 'unknown' };
try {
  skillMeta = JSON.parse(readFileSync(new URL('../skill.json', import.meta.url), 'utf8'));
} catch {
  /* 默认值 */
}

// 4. 构造 multipart/form-data 请求
const fileContent = readFileSync(filePath);
const filename = basename(filePath);

// Node.js 20.6+ 原生 FormData / Blob，不需要外部依赖
const form = new FormData();
const blob = new Blob([fileContent], { type: _guessMime(ext) });
form.append('file', blob, filename);

console.error(`[media-upload] 上传中... ${filename} (${sizeMB.toFixed(2)}MB)`);

let response;
try {
  response = await fetch(`${API_BASE}/openapi/v1/media/upload`, {
    method: 'POST',
    headers: {
      'X-API-Key': API_KEY,
      'X-User-Identity': USER_IDENTITY,
      'X-CV-Skill-Name': skillMeta.name || 'creator-scraper-cv',
      'X-CV-Skill-Version': skillMeta.version || 'unknown',
      'X-CV-Skill-Channel': skillMeta.channel || 'unknown',
      // 注意：不要手动设置 Content-Type，FormData 会自动加 boundary
    },
    body: form,
  });
} catch (err) {
  console.error(JSON.stringify({ error: `网络请求失败: ${err.message}` }));
  process.exit(1);
}

let data;
try {
  data = await response.json();
} catch {
  console.error(JSON.stringify({ error: `响应解析失败，HTTP ${response.status}` }));
  process.exit(1);
}

if (!data.success) {
  console.error(JSON.stringify({
    error: data.error?.message || '上传失败',
    code: data.error?.code,
    request_id: data.meta?.request_id,
  }, null, 2));
  process.exit(1);
}

console.log(JSON.stringify(data, null, 2));

function _guessMime(ext) {
  switch (ext) {
    case '.mp4': return 'video/mp4';
    case '.mov': return 'video/quicktime';
    case '.avi': return 'video/x-msvideo';
    case '.mkv': return 'video/x-matroska';
    case '.webm': return 'video/webm';
    default: return 'application/octet-stream';
  }
}
