/**
 * 音频处理模块 - 提取音频并使用 GLM-ASR-2512 识别
 */

const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const https = require('https');

/**
 * 从视频中提取音频 (MP3 格式)
 */
async function extractAudio(videoPath, audioPathRaw) {
  const finalAudioPath = `${audioPathRaw}.wav`;
  return new Promise((resolve, reject) => {
    // 改用 wav 格式，指定输出文件名带后缀
    const cmd = `ffmpeg -i "${videoPath}" -vn -acodec pcm_s16le -ac 1 -ar 16000 -y "${finalAudioPath}"`;
    exec(cmd, (error) => {
      if (error) reject(error);
      else resolve(finalAudioPath);
    });
  });
}

/**
 * 将音频转换为 Base64
 */
function audioToBase64(audioPath) {
  return fs.readFileSync(audioPath).toString('base64');
}

/**
 * 核心：支持长音频的分段识别逻辑
 * 智谱限制：单段必须 < 30秒
 */
async function recognizeSpeech(audioPath, apiKey) {
  if (!apiKey) throw new Error('缺少 API Key');
  
  // 1. 获取视频总时长并计算分段
  const getDurationCmd = `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "${audioPath}"`;
  const duration = await new Promise((resolve) => {
    exec(getDurationCmd, (err, stdout) => resolve(parseFloat(stdout) || 0));
  });

  const SEGMENT_DURATION = 20; // 优化：每段 20 秒，对齐视觉请求步长
  const numSegments = Math.ceil(duration / SEGMENT_DURATION);
  
  console.log(`  🎙️ 视频总长 ${Math.round(duration)}s，将切分为 ${numSegments} 段进行识别...`);

  const results = [];
  const tempBase = audioPath.replace('.wav', '_seg');

  for (let i = 0; i < numSegments; i++) {
    const startTime = i * SEGMENT_DURATION;
    const segmentPath = `${tempBase}_${i}.wav`;
    
    // 切割音频
    await new Promise((resolve, reject) => {
      const cutCmd = `ffmpeg -ss ${startTime} -t ${SEGMENT_DURATION} -i "${audioPath}" -acodec copy -y "${segmentPath}"`;
      exec(cutCmd, (err) => err ? reject(err) : resolve());
    });

    console.log(`    ⏳ 正在识别第 ${i + 1}/${numSegments} 段...`);
    
    // 调用单段转录
    const text = await callTranscribeAPI(segmentPath, apiKey);
    results.push(text);

    // 清理临时段
    if (fs.existsSync(segmentPath)) fs.unlinkSync(segmentPath);
  }

  return results.join(' ');
}

/**
 * 内部方法：调用单段智谱转录
 */
async function callTranscribeAPI(filePath, apiKey) {
  const FormData = require('form-data');
  const formData = new FormData();
  formData.append('file', fs.createReadStream(filePath));
  formData.append('model', 'glm-asr-2512');

  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'open.bigmodel.cn',
      path: '/api/paas/v4/audio/transcriptions',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        ...formData.getHeaders()
      }
    };

    const req = https.request(options, (res) => {
      let out = '';
      res.on('data', c => out += c);
      res.on('end', () => {
        try {
          const json = JSON.parse(out);
          if (json.error) resolve(`[Error: ${json.error.message}]`);
          else resolve(json.text || '');
        } catch (e) { resolve(''); }
      });
    });
    req.on('error', (e) => resolve(`[Request Error]`));
    formData.pipe(req);
  });
}

module.exports = {
  extractAudio,
  recognizeSpeech
};
