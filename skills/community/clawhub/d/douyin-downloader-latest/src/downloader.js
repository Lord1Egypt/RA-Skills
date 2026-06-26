/**
 * 抖音视频下载器
 * 支持单文件下载和批量下载
 */

import axios from 'axios';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * 确保目录存在
 */
function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
  return dirPath;
}

/**
 * 清理文件名，移除非法字符
 */
function sanitizeFilename(filename) {
  return filename
    .replace(/[<>:"/\\|？*]/g, '')
    .replace(/\s+/g, '_')
    .substring(0, 100); // 限制长度
}

/**
 * 下载文件
 * @param {string} url - 文件 URL
 * @param {string} destPath - 保存路径
 * @param {Function} onProgress - 进度回调
 */
export async function downloadFile(url, destPath, onProgress) {
  const response = await axios({
    url,
    method: 'GET',
    responseType: 'stream',
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Referer': 'https://www.douyin.com/',
    }
  });

  const totalSize = parseInt(response.headers['content-length'] || '0', 10);
  let downloadedSize = 0;

  return new Promise((resolve, reject) => {
    const writer = fs.createWriteStream(destPath);

    response.data.on('data', (chunk) => {
      downloadedSize += chunk.length;
      if (onProgress && totalSize > 0) {
        const progress = ((downloadedSize / totalSize) * 100).toFixed(1);
        onProgress(progress);
      }
    });

    writer.on('finish', () => {
      resolve({
        path: destPath,
        size: downloadedSize,
        success: true
      });
    });

    writer.on('error', (error) => {
      reject(error);
    });

    response.data.pipe(writer);
  });
}

/**
 * 下载抖音视频
 * @param {Object} videoInfo - 视频信息对象（来自 parser）
 * @param {string} saveDir - 保存目录
 * @param {Object} options - 选项
 */
export async function downloadDouyinVideo(videoInfo, saveDir, options = {}) {
  const {
    saveMetadata = true,
    filenameTemplate = '{author}_{title}_{id}'
  } = options;

  try {
    // 确保保存目录存在
    ensureDir(saveDir);

    // 生成文件名
    const filename = filenameTemplate
      .replace('{author}', sanitizeFilename(videoInfo.author || 'unknown'))
      .replace('{title}', sanitizeFilename(videoInfo.title || 'video'))
      .replace('{id}', videoInfo.id || 'unknown')
      .replace('{date}', new Date().toISOString().split('T')[0]);

    const videoPath = path.join(saveDir, `${filename}.mp4`);

    // 检查文件是否已存在
    if (fs.existsSync(videoPath)) {
      console.log(`文件已存在：${videoPath}`);
      return {
        success: true,
        path: videoPath,
        skipped: true,
        message: '文件已存在'
      };
    }

    // 下载视频
    console.log(`开始下载：${videoInfo.title}`);
    const result = await downloadFile(videoInfo.videoUrl, videoPath, (progress) => {
      console.log(`下载进度：${progress}%`);
    });

    // 保存元数据（可选）
    if (saveMetadata) {
      const metadataPath = path.join(saveDir, `${filename}.json`);
      fs.writeFileSync(metadataPath, JSON.stringify(videoInfo, null, 2));
      console.log(`元数据已保存：${metadataPath}`);
    }

    return {
      success: true,
      path: videoPath,
      size: result.size,
      metadata: videoInfo
    };
  } catch (error) {
    console.error('下载失败:', error.message);
    return {
      success: false,
      error: error.message,
      videoInfo
    };
  }
}

/**
 * 批量下载
 * @param {Array} videoInfos - 视频信息数组
 * @param {string} saveDir - 保存目录
 * @param {Object} options - 选项
 */
export async function batchDownload(videoInfos, saveDir, options = {}) {
  const {
    concurrency = 3, // 并发数
    ...downloadOptions
  } = options;

  const results = [];
  const queue = [...videoInfos];
  const active = [];

  while (queue.length > 0 || active.length > 0) {
    // 填充并发队列
    while (active.length < concurrency && queue.length > 0) {
      const videoInfo = queue.shift();
      const promise = downloadDouyinVideo(videoInfo, saveDir, downloadOptions)
        .then(result => {
          results.push(result);
          active.splice(active.indexOf(promise), 1);
          return result;
        });
      active.push(promise);
    }

    // 等待至少一个完成
    if (active.length > 0) {
      await Promise.race(active);
    }
  }

  return results;
}

/**
 * 获取默认保存目录
 */
export function getDefaultSaveDir() {
  const homeDir = process.env.HOME || process.env.USERPROFILE;
  const defaultDir = path.join(homeDir, 'Videos', 'douyin');
  ensureDir(defaultDir);
  return defaultDir;
}
