/**
 * 把用户本机的参考图 / 首帧 / 人脸照片传上去，换成网站接口认的 https 地址。
 *
 * 和网页一样：先拿网站发的 OSS 直传签名（/api/get-oss-signature，temporary=true 传到临时目录，
 * 网站几天后自动清理），再把文件直接 POST 给 OSS，不经过网站服务器。
 * 已经是 http(s) 地址的原样返回，不重复上传。
 */
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { ApiError, request, requestJson } from './http.mjs';
import { SITE, api } from './store.mjs';

const MIME = {
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.gif': 'image/gif',
  '.bmp': 'image/bmp', '.mp4': 'video/mp4', '.mov': 'video/quicktime', '.mp3': 'audio/mpeg', '.wav': 'audio/wav', '.m4a': 'audio/mp4',
};
const MAX_BYTES = 30 * 1024 * 1024;
const MAX_VIDEO_BYTES = 200 * 1024 * 1024;

let signature = null;

async function getSignature(token) {
  if (signature && Date.now() < signature.expiresAt) return signature;
  const res = await requestJson(api('get-oss-signature'), { data: { temporary: true }, token });
  const d = res.data || {};
  signature = { ...d, expiresAt: Date.now() + 5 * 60 * 1000 };
  return signature;
}

export function isUrl(v) {
  return /^https?:\/\//i.test(String(v || ''));
}

/** 本地路径或 URL → 可公开访问的 https 地址 */
export async function ensureUrl(input, token) {
  const value = String(input || '').trim();
  if (!value) return '';
  if (isUrl(value)) return value;
  const file = path.resolve(value.replace(/^~(?=\/|$)/, process.env.HOME || ''));
  if (!fs.existsSync(file) || !fs.statSync(file).isFile()) throw new ApiError(`找不到文件：${value}`, { code: 'FILE' });
  const stat = fs.statSync(file);
  // 参考视频（Seedance / H3）上游允许到 200MB，其他素材 30MB
  const limit = /\.(mp4|mov)$/i.test(file) ? MAX_VIDEO_BYTES : MAX_BYTES;
  if (stat.size > limit) throw new ApiError(`${path.basename(file)} 超过 ${limit / 1024 / 1024}MB，先压缩一下再传`, { code: 'FILE' });

  const sig = await getSignature(token);
  const ext = path.extname(file).toLowerCase() || '.png';
  const key = `${sig.dir}agent-${Date.now()}-${crypto.randomBytes(4).toString('hex')}${ext}`;
  const form = new FormData();
  form.append('key', key);
  form.append('policy', sig.policy);
  form.append('OSSAccessKeyId', sig.accessId);
  form.append('success_action_status', '200');
  form.append('signature', sig.signature);
  form.append('file', new Blob([fs.readFileSync(file)], { type: MIME[ext] || 'application/octet-stream' }), path.basename(file));
  const host = String(sig.host || '').startsWith('//') ? `https:${sig.host}` : sig.host;
  const res = await request(host, { method: 'POST', body: form, timeout: 120_000 });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new ApiError(`上传 ${path.basename(file)} 失败（HTTP ${res.status}）${text.slice(0, 160)}`, { code: 'UPLOAD' });
  }
  return `${SITE.ossBase}/${key}`;
}

export async function ensureUrls(list, token) {
  const out = [];
  for (const item of list || []) out.push(await ensureUrl(item, token));
  return out.filter(Boolean);
}
