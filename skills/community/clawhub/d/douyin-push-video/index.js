/**
 * 抖音视频发布 Skill - Node.js 实现
 * 流程：上传视频获取 video_id → 调用创建视频接口发布
 * 配置：从 .env 或环境变量读取 DOUYIN_OPEN_ID、DOUYIN_ACCESS_TOKEN（.env 会一直保留）
 */

import fs from 'fs';
import path from 'path';
import { createReadStream } from 'fs';
import FormData from 'form-data';
import { fileURLToPath } from 'url';
import { config } from 'dotenv';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 加载项目根目录 .env，使「配置上去」的记录一直生效
config({ path: path.resolve(__dirname, '.env') });

const BASE = 'https://open.douyin.com';

/**
 * 上传视频到抖音文件服务器，获取加密 video_id
 * @param {string} videoPath - 本地视频文件路径
 * @param {string} openId - 用户 open_id（OAuth 获取）
 * @param {string} accessToken - 用户 access_token
 * @returns {Promise<{ video_id: string, width?: number, height?: number }>}
 */
export async function uploadVideo(videoPath, openId, accessToken) {
  const absPath = path.isAbsolute(videoPath) ? videoPath : path.resolve(process.cwd(), videoPath);
  if (!fs.existsSync(absPath)) {
    throw new Error(`视频文件不存在: ${absPath}`);
  }

  const form = new FormData();
  form.append('video', createReadStream(absPath), {
    filename: path.basename(absPath),
    contentType: 'video/mp4',
  });

  const url = `${BASE}/api/douyin/v1/video/upload_video/?open_id=${encodeURIComponent(openId)}`;
  const body = await new Promise((resolve, reject) => {
    form.getBuffer((err, buf) => {
      if (err) reject(err);
      else resolve(buf);
    });
  });

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'access-token': accessToken,
      ...form.getHeaders(),
    },
    body,
  });

  let data;
  try {
    data = await res.json();
  } catch {
    throw new Error(`上传失败: 响应非 JSON (HTTP ${res.status})`);
  }
  if (!res.ok) {
    const desc = data?.extra?.description || data?.data?.description || JSON.stringify(data);
    throw new Error(`上传失败 HTTP ${res.status}: ${desc}`);
  }
  const video = data?.data?.video;
  if (!video?.video_id) {
    const desc = data?.extra?.description || data?.data?.description || JSON.stringify(data);
    throw new Error(`上传失败: ${desc}`);
  }
  return { video_id: video.video_id, width: video.width, height: video.height };
}

/**
 * 创建/发布抖音视频（使用上传得到的 video_id）
 * openId、accessToken 由调用方传入；postToDouyin 会从 .env 的 DOUYIN_OPEN_ID、DOUYIN_ACCESS_TOKEN 读取后传入。
 * @param {object} opts
 * @param {string} opts.video_id - 必填，上传接口返回的加密 video_id
 * @param {string} [opts.text] - 标题，可含话题、@用户，不超过 1000 字
 * @param {string} opts.openId - 用户 open_id（OAuth 获取，或由 postToDouyin 从 .env 读取）
 * @param {string} opts.accessToken - 用户 access_token（同上）
 * @param {number} [opts.private_status] - 0 全部可见，1 自见，2 好友可见
 * @param {number} [opts.cover_tsp] - 封面时间点（秒）
 * @param {string[]} [opts.at_users] - @用户的 open_id 数组
 * @returns {Promise<{ item_id: string, video_id: string }>}
 */
export async function createVideo(opts) {
  const { video_id, openId, accessToken, text = '', private_status = 0, cover_tsp, at_users } = opts;
  if (!video_id || !openId || !accessToken) {
    throw new Error('缺少 video_id、openId 或 accessToken');
  }

  const url = `${BASE}/api/douyin/v1/video/create_video/?open_id=${encodeURIComponent(openId)}`;
  const body = { video_id, text, private_status };
  if (cover_tsp != null) body.cover_tsp = cover_tsp;
  if (at_users && at_users.length) body.at_users = at_users;

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'access-token': accessToken,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  let data;
  try {
    data = await res.json();
  } catch {
    throw new Error(`发布失败: 响应非 JSON (HTTP ${res.status})`);
  }
  if (!res.ok) {
    const desc = data?.extra?.description || data?.data?.description || JSON.stringify(data);
    throw new Error(`发布失败 HTTP ${res.status}: ${desc}`);
  }
  const d = data?.data;
  const errCode = d?.error_code ?? data?.extra?.error_code;
  if (errCode != null && errCode !== 0) {
    const desc = data?.extra?.description || d?.description || JSON.stringify(data);
    throw new Error(`发布失败: ${desc}`);
  }
  return { item_id: d?.item_id, video_id: d?.video_id };
}

/**
 * 一键上传并发布到抖音
 * @param {string} videoPath - 本地视频路径
 * @param {object} options - 需 openId、accessToken；text 为标题；其余同 createVideo
 * @returns {Promise<{ item_id: string, video_id: string }>}
 */
export async function postToDouyin(videoPath, options = {}) {
  const openId = options.openId ?? process.env.DOUYIN_OPEN_ID;
  const accessToken = options.accessToken ?? process.env.DOUYIN_ACCESS_TOKEN;
  const { text = '', ...rest } = options;
  if (!openId || !accessToken) {
    throw new Error('请提供 openId 和 accessToken，或在 .env 中配置 DOUYIN_OPEN_ID、DOUYIN_ACCESS_TOKEN');
  }
  const { video_id } = await uploadVideo(videoPath, openId, accessToken);
  return createVideo({
    video_id,
    openId,
    accessToken,
    text,
    ...rest,
  });
}

/** 从环境或 .env 读取是否已配置抖音凭证 */
export function hasDouyinCredential() {
  const openId = process.env.DOUYIN_OPEN_ID;
  const accessToken = process.env.DOUYIN_ACCESS_TOKEN;
  return !!(openId && accessToken);
}

// CLI：node index.js <视频路径> [标题]
async function main() {
  const videoPath = process.argv[2];
  const title = process.argv[3] || '';

  if (!videoPath) {
    console.log(`
用法: node index.js <视频路径> [标题]

示例:
  node index.js ./my.mp4 我的第一条抖音
  node index.js ./video.mp4 "#话题"

配置（二选一）:
  - 在项目根目录 .env 中设置 DOUYIN_OPEN_ID、DOUYIN_ACCESS_TOKEN
  - 或设置环境变量 DOUYIN_OPEN_ID、DOUYIN_ACCESS_TOKEN
`);
    process.exit(1);
  }

  if (!hasDouyinCredential()) {
    console.error('未检测到抖音凭证，请在 .env 或环境变量中配置 DOUYIN_OPEN_ID、DOUYIN_ACCESS_TOKEN');
    process.exit(1);
  }

  try {
    const result = await postToDouyin(videoPath, { text: title });
    console.log('发布成功:', result);
  } catch (e) {
    console.error('失败:', e.message);
    process.exit(1);
  }
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === path.resolve(__filename);
if (isMain) {
  main();
}
