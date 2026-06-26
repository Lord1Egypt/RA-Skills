/**
 * 视频下载模块
 * 支持 yt-dlp 和第三方解析服务
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const { promisify } = require('util');

const execAsync = promisify(exec);

const USER_AGENTS = [
  'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
  'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
];

function getRandomUserAgent() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

/**
 * 检查 yt-dlp 是否安装
 * @returns {Promise<boolean>}
 */
async function checkYtDlp() {
  try {
    await execAsync('yt-dlp --version');
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * 使用 yt-dlp 下载视频
 * @param {string} videoUrl - 视频链接
 * @param {string} outputDir - 输出目录
 * @param {string} videoId - 视频ID
 * @returns {Promise<{success: boolean, filePath: string, error?: string}>}
 */
async function downloadWithYtDlp(videoUrl, outputDir, videoId) {
  ensureDir(outputDir);
  const outputPath = path.join(outputDir, `${videoId}.mp4`);
  
  // 如果文件已存在，直接返回
  if (fs.existsSync(outputPath)) {
    console.log(`  📁 视频已存在: ${outputPath}`);
    return { success: true, filePath: outputPath };
  }
  
  try {
    console.log(`  🔄 使用 yt-dlp 下载视频...`);
    
    // yt-dlp 命令
    const command = `yt-dlp -o "${outputPath}" --no-warnings "${videoUrl}" 2>&1`;
    
    const { stdout, stderr } = await execAsync(command, { timeout: 120000 });
    
    if (fs.existsSync(outputPath)) {
      console.log(`  ✅ 下载完成: ${outputPath}`);
      return { success: true, filePath: outputPath };
    } else {
      // 检查是否需要 cookies
      if (stderr && stderr.includes('cookies')) {
        return { 
          success: false, 
          error: '该视频需要登录才能下载。请使用以下方法之一：\n1. 使用 yt-dlp --cookies-from-browser 提供 cookies\n2. 使用第三方解析工具（如 snapany.com）手动下载视频\n3. 直接分析本地视频文件：node scripts/analyze.js ./video.mp4'
        };
      }
      return { success: false, error: `下载失败: ${stderr || stdout}` };
    }
  } catch (error) {
    if (error.message.includes('cookies')) {
      return { 
        success: false, 
        error: '该视频需要登录才能下载。建议：\n1. 使用第三方工具（snapany.com）下载视频\n2. 然后分析本地文件：node scripts/analyze.js ./video.mp4'
      };
    }
    return { success: false, error: `yt-dlp 错误: ${error.message}` };
  }
}

/**
 * 从 URL 下载视频
 * @param {string} videoUrl - 视频下载链接
 * @param {string} outputDir - 输出目录
 * @param {string} videoId - 视频ID（用于文件名）
 * @returns {Promise<{success: boolean, filePath: string, error?: string}>}
 */
async function downloadVideo(videoUrl, outputDir, videoId) {
  // 优先使用 yt-dlp
  const hasYtDlp = await checkYtDlp();
  if (hasYtDlp) {
    return downloadWithYtDlp(videoUrl, outputDir, videoId);
  }
  
  // 降级到直接下载（仅适用于直接视频链接）
  return downloadDirect(videoUrl, outputDir, videoId);
}

/**
 * 直接下载（备用方案）
 */
async function downloadDirect(videoUrl, outputDir, videoId) {
  ensureDir(outputDir);
  
  const fileName = `${videoId}.mp4`;
  const filePath = path.join(outputDir, fileName);
  
  // 如果文件已存在，直接返回
  if (fs.existsSync(filePath)) {
    console.log(`  📁 视频已存在: ${filePath}`);
    return { success: true, filePath };
  }
  
  return new Promise((resolve, reject) => {
    const options = {
      headers: {
        'User-Agent': getRandomUserAgent(),
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://www.douyin.com/',
        'Connection': 'keep-alive'
      },
      timeout: 60000
    };
    
    const req = https.get(videoUrl, options, (res) => {
      // 处理重定向
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        console.log(`  🔄 跟随重定向...`);
        downloadDirect(res.headers.location, outputDir, videoId)
          .then(resolve)
          .catch(reject);
        return;
      }
      
      if (res.statusCode !== 200) {
        reject(new Error(`下载失败: HTTP ${res.statusCode}`));
        return;
      }
      
      const fileStream = fs.createWriteStream(filePath);
      let downloadedBytes = 0;
      let totalBytes = parseInt(res.headers['content-length'], 10) || 0;
      
      res.on('data', (chunk) => {
        downloadedBytes += chunk.length;
        if (totalBytes > 0) {
          const percent = Math.round((downloadedBytes / totalBytes) * 100);
          process.stdout.write(`  ⬇️  下载进度: ${percent}%\r`);
        }
      });
      
      res.pipe(fileStream);
      
      fileStream.on('finish', () => {
        fileStream.close();
        console.log(`  ✅ 下载完成: ${filePath}`);
        resolve({ success: true, filePath });
      });
      
      fileStream.on('error', (err) => {
        fs.unlink(filePath, () => {});
        reject(new Error(`文件写入失败: ${err.message}`));
      });
    });
    
    req.on('error', (err) => {
      reject(new Error(`请求失败: ${err.message}`));
    });
    
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('下载超时'));
    });
  });
}

/**
 * 获取视频下载链接
 * 从视频详情中提取无水印下载链接
 * @param {Object} videoData - 从 scraper 获取的视频数据
 * @returns {string|null}
 */
function getVideoDownloadUrl(videoData) {
  // 优先使用无水印链接
  if (videoData.videoUrl) {
    return videoData.videoUrl;
  }
  return null;
}

module.exports = {
  downloadVideo,
  downloadWithYtDlp,
  checkYtDlp,
  getVideoDownloadUrl,
  ensureDir
};
