#!/usr/bin/env node
/**
 * feishu-tts-pro: 文字转语音发送脚本
 * - Edge-TTS 生成 MP3
 * - FFmpeg 转码为 ogg/opus
 * - 上传飞书 (file_type=opus, audio/ogg)
 * - 发送 audio 消息气泡
 * 
 * 环境变量:
 *   FEISHU_APP_ID       飞书应用 App ID (必填)
 *   FEISHU_APP_SECRET   飞书应用 App Secret (必填)
 *   FEISHU_DEFAULT_USER 默认接收者 open_id (可选)
 *   EDGE_TTS_VOICE      音色 (默认: zh-CN-YunxiNeural)
 *   PYTHON_BIN          Python 路径 (默认: python3)
 */

import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';
import os from 'os';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ============ 配置（从环境变量读取）============
const FEISHU_APP_ID = process.env.FEISHU_APP_ID;
const FEISHU_APP_SECRET = process.env.FEISHU_APP_SECRET;
const DEFAULT_USER = process.env.FEISHU_DEFAULT_USER || '';
const VOICE = process.env.EDGE_TTS_VOICE || 'zh-CN-YunxiNeural';
const PYTHON_BIN = process.env.PYTHON_BIN || 'python3';

// ============ 参数解析 ================
const text = process.argv[2];
let toUser = process.argv[3] || DEFAULT_USER;

if (!text || text === '--help' || text === '-h') {
  console.log('🎤 feishu-tts-pro - 文字转飞书语音气泡');
  console.log('');
  console.log('用法:');
  console.log('  tts-send <文本> [接收者open_id]');
  console.log('');
  console.log('参数:');
  console.log('  <文本>          要转换的中文文本');
  console.log('  [接收者open_id] 飞书用户 open_id（可选，默认用 FEISHU_DEFAULT_USER）');
  console.log('');
  console.log('环境变量:');
  console.log('  FEISHU_APP_ID       飞书 App ID (必填)');
  console.log('  FEISHU_APP_SECRET   飞书 App Secret (必填)');
  console.log('  FEISHU_DEFAULT_USER 默认接收者 open_id');
  console.log('  EDGE_TTS_VOICE      音色 (默认: zh-CN-YunxiNeural)');
  console.log('  PYTHON_BIN          Python 路径 (默认: python3)');
  console.log('');
  console.log('示例:');
  console.log('  FEISHU_APP_ID=cli_xxx FEISHU_APP_SECRET=xxx tts-send "你好"');
  console.log('  tts-send "测试语音" ou_abc123');
  process.exit(0);
}

// ============ 验证配置 ================
if (!FEISHU_APP_ID || !FEISHU_APP_SECRET) {
  console.error('❌ 缺少必填环境变量: FEISHU_APP_ID 和 FEISHU_APP_SECRET 必须设置');
  console.error('   或在 AGENTS.md 中配置 skills.entries.feishu-tts-pro.env');
  process.exit(1);
}

if (!toUser) {
  console.error('❌ 未指定接收者，且未设置 FEISHU_DEFAULT_USER');
  console.error('   请通过命令行参数传入 open_id，或设置环境变量 FEISHU_DEFAULT_USER');
  process.exit(1);
}

// ============ 临时文件 ================
const tmpDir = os.tmpdir();
const mp3File = path.join(tmpDir, `tts_${Date.now()}.mp3`);
const oggFile = path.join(tmpDir, `tts_${Date.now()}.ogg`);

// ============ 飞书 API ================
async function getAccessToken() {
  const resp = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: FEISHU_APP_ID, app_secret: FEISHU_APP_SECRET }),
  });
  const data = await resp.json();
  if (data.code !== 0) throw new Error(`获取 token 失败: ${data.msg} (code=${data.code})`);
  return data.tenant_access_token;
}

async function uploadAudioOgg(token, filePath, durationMs) {
  const fileBuffer = fs.readFileSync(filePath);
  const form = new FormData();
  const blob = new Blob([fileBuffer], { type: 'audio/ogg' });
  form.append('file', blob, 'voice.ogg');
  form.append('file_name', 'voice.ogg');
  form.append('file_type', 'opus');
  if (durationMs) form.append('duration', String(Math.round(durationMs)));

  const resp = await fetch('https://open.feishu.cn/open-apis/im/v1/files', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: form,
  });
  const data = await resp.json();
  if (data.code !== 0) throw new Error(`上传失败: ${data.msg} (code=${data.code})`);
  return data.data.file_key;
}

async function sendAudioMessage(token, fileKey) {
  const resp = await fetch('https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      receive_id: toUser,
      msg_type: 'audio',
      content: JSON.stringify({ file_key: fileKey }),
    }),
  });
  const data = await resp.json();
  if (data.code !== 0) throw new Error(`发送失败: ${data.msg} (code=${data.code})`);
  return data.data.message_id;
}

// ============ 音频处理 ================
function getDuration(filePath) {
  return new Promise((resolve) => {
    const ffprobe = spawn('ffprobe', [
      '-v', 'error',
      '-show_entries', 'format=duration',
      '-of', 'default=noprint_wrappers=1:nokey=1',
      filePath,
    ]);
    let output = '';
    ffprobe.stdout.on('data', (d) => { output += d; });
    ffprobe.on('close', (code) => {
      if (code === 0) resolve(parseFloat(output.trim()) * 1000);
      else resolve(0);
    });
    ffprobe.on('error', () => resolve(0));
  });
}

async function ttsToOgg(text) {
  return new Promise((resolve, reject) => {
    const pyCode = `
import asyncio
import edge_tts
async def tts():
    communicate = edge_tts.Communicate(${JSON.stringify(text)}, ${JSON.stringify(VOICE)})
    await communicate.save(${JSON.stringify(mp3File)})
asyncio.run(tts())
`;
    const py = spawn(PYTHON_BIN, ['-c', pyCode]);
    py.on('close', (code) => {
      if (code !== 0) return reject(new Error(`TTS 生成失败 (exit ${code})，请确认 edge-tts 已安装: pip install edge-tts`));

      const ffmpeg = spawn('ffmpeg', [
        '-i', mp3File, '-acodec', 'libopus',
        '-ar', '16000', '-ac', '1', '-y', oggFile,
      ]);
      ffmpeg.on('close', (code2) => {
        fs.unlink(mp3File, () => {});
        if (code2 !== 0) return reject(new Error(`音频转换失败 (ffmpeg exit ${code2})`));
        resolve(oggFile);
      });
      ffmpeg.on('error', reject);
    });
    py.on('error', (err) => reject(new Error(`Python 执行失败: ${err.message}`)));
  });
}

// ============ 主流程 ================
async function main() {
  try {
    console.log(`🎤 生成语音 (音色: ${VOICE}): ${text.substring(0, 20)}${text.length > 20 ? '...' : ''}`);
    const oggPath = await ttsToOgg(text);
    const duration = await getDuration(oggPath);
    console.log(`📤 上传音频 (${Math.round(duration)}ms)...`);
    const token = await getAccessToken();
    const fileKey = await uploadAudioOgg(token, oggPath, duration);
    const msgId = await sendAudioMessage(token, fileKey);
    console.log(`✅ 语音气泡发送成功！消息ID: ${msgId}`);
    fs.unlink(oggPath, () => {});
  } catch (err) {
    console.error(`❌ 失败: ${err.message}`);
    process.exit(1);
  }
}

main();