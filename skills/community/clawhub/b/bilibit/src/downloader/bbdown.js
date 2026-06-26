/**
 * BBDown wrapper for Bilibili video downloading
 * @module downloader/bbdown
 */

const { execSync, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

/**
 * Error message translation table
 * Maps BBDown errors to user-friendly Chinese messages
 */
const ERROR_MESSAGES = {
  '你没有权限': '大会员内容，请使用 --cookie 参数',
  '稿件不可观看': '视频不存在或已被删除',
  'timed out': '网络超时，请检查网络',
  'timeout': '网络超时，请检查网络',
  'BBDown not found': 'BBDown 未安装，运行: bilibit --check',
  'not installed': 'BBDown 未安装，运行: bilibit --check',
  'ENOENT': 'BBDown 未安装，运行: bilibit --check',
  'permission denied': '权限不足，请检查文件权限',
  'Connection refused': '网络连接被拒绝，请检查网络',
  'getaddrinfo': 'DNS 解析失败，请检查网络',
};

/**
 * Translate raw error to user-friendly message
 * @param {string} rawError - Raw error string
 * @returns {string} - Translated error message
 */
function translateError(rawError) {
  if (!rawError) return '未知错误';

  for (const [key, message] of Object.entries(ERROR_MESSAGES)) {
    if (rawError.includes(key)) {
      return message;
    }
  }

  return rawError;
}

/**
 * Check if BBDown is installed
 * @returns {boolean}
 */
function isBBDownInstalled() {
  try {
    // 优先使用本地 BBDown
    const localBBDown = path.join(__dirname, '..', '..', 'node_modules', '.bin', 'BBDown');
    if (fs.existsSync(localBBDown)) {
      return true;
    }

    // 否则使用全局 BBDown
    execSync('BBDown --version', { stdio: 'ignore' });
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * Get default download directory
 * @returns {string}
 */
function getDefaultDownloadDir() {
  const homeDir = process.env.HOME || process.env.USERPROFILE;
  const downloadDir = path.join(homeDir, 'Downloads', 'bilibit');
  
  if (!fs.existsSync(downloadDir)) {
    fs.mkdirSync(downloadDir, { recursive: true });
  }
  
  return downloadDir;
}

/**
 * Get the path to BBDown executable
 * @returns {string|null}
 */
function getBBDownPath() {
  // 优先使用本地 BBDown
  const localBBDown = path.join(__dirname, '..', '..', 'node_modules', '.bin', 'BBDown');
  if (fs.existsSync(localBBDown)) {
    return localBBDown;
  }
  
  // 使用全局 BBDown
  try {
    const result = execSync('which BBDown', { stdio: 'pipe' }).toString().trim();
    if (result) return result;
  } catch (e) {}
  
  return null;
}

/**
 * Parse video info from BBDown --info output
 * @param {string} infoOutput - Raw output from BBDown --info
 * @returns {Object} - Parsed video info
 */
function parseInfoOutput(infoOutput) {
  const info = {
    title: '',
    duration: '',
    quality: '',
    size: '',
    hasAudio: true,
  };

  if (!infoOutput) return info;

  // Extract title (line starting with "Title: " or similar)
  const titleMatch = infoOutput.match(/Title:\s*(.+)/i) || infoOutput.match(/标题:\s*(.+)/i);
  if (titleMatch) {
    info.title = titleMatch[1].trim();
  }

  // Extract duration
  const durationMatch = infoOutput.match(/Duration:\s*([\d:]+)/i) || infoOutput.match(/时长:\s*([\d:]+)/i);
  if (durationMatch) {
    info.duration = durationMatch[1].trim();
  }

  // Extract quality
  const qualityMatch = infoOutput.match(/Quality:\s*(.+)/i) || infoOutput.match(/画质:\s*(.+)/i);
  if (qualityMatch) {
    info.quality = qualityMatch[1].trim();
  }

  // Extract file size
  const sizeMatch = infoOutput.match(/Size:\s*([\d.]+\s*\w+)/i) || infoOutput.match(/大小:\s*([\d.]+\s*\w+)/i);
  if (sizeMatch) {
    info.size = sizeMatch[1].trim();
  }

  // Check for audio
  if (/no audio|无音频/i.test(infoOutput)) {
    info.hasAudio = false;
  }

  return info;
}

/**
 * Parse real file path from BBDown output
 * @param {string} output - BBDown stdout/stderr output
 * @param {string} outputDir - Expected output directory
 * @returns {string|null} - Real file path or null
 */
function parseOutputFilePath(output, outputDir) {
  if (!output) return null;

  // Try to match "Output: /path/to/file.mp4" pattern
  const outputMatch = output.match(/Output:\s*(.+)/i);
  if (outputMatch) {
    const filePath = outputMatch[1].trim();
    if (fs.existsSync(filePath)) {
      return filePath;
    }
    return filePath;
  }

  // Try to match "Merging to: /path/to/file.mp4" pattern
  const mergingMatch = output.match(/Merging to:\s*(.+)/i);
  if (mergingMatch) {
    const filePath = mergingMatch[1].trim();
    if (fs.existsSync(filePath)) {
      return filePath;
    }
    return filePath;
  }

  // Fallback: look for .mp4/.flv files in output directory modified recently
  if (outputDir && fs.existsSync(outputDir)) {
    try {
      const files = fs.readdirSync(outputDir);
      const mp4Files = files.filter(f => f.endsWith('.mp4') || f.endsWith('.flv'));
      if (mp4Files.length > 0) {
        // Return the most recently modified file
        const sorted = mp4Files
          .map(f => ({
            name: f,
            path: path.join(outputDir, f),
            mtime: fs.statSync(path.join(outputDir, f)).mtime.getTime()
          }))
          .sort((a, b) => b.mtime - a.mtime);
        return sorted[0].path;
      }
    } catch (e) {}
  }

  return null;
}

/**
 * Fetch video info without downloading
 * @param {string} url - Video URL or BV/AV ID
 * @param {Object} options - Options
 * @returns {Promise<{success: boolean, info?: Object, error?: string}>}
 */
async function info(url, options = {}) {
  return new Promise((resolve) => {
    const bbdownPath = getBBDownPath();
    if (!bbdownPath) {
      resolve({
        success: false,
        error: translateError('BBDown not found')
      });
      return;
    }

    const args = ['--only-show-info', url];

    if (options.cookieFile) {
      args.push('--cookie', options.cookieFile);
    }

    const child = spawn(bbdownPath, args, {
      stdio: ['inherit', 'pipe', 'pipe']
    });

    let output = '';
    let errorOutput = '';

    child.stdout.on('data', (data) => {
      output += data.toString();
    });

    child.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });

    child.on('close', (code) => {
      const combined = output + errorOutput;

      if (code === 0 || output.includes('Title:') || output.includes('标题:')) {
        resolve({
          success: true,
          info: parseInfoOutput(combined)
        });
      } else {
        resolve({
          success: false,
          error: translateError(errorOutput.trim() || `BBDown --info failed with code ${code}`)
        });
      }
    });

    child.on('error', (err) => {
      resolve({
        success: false,
        error: translateError(err.message)
      });
    });
  });
}

/**
 * Build BBDown command arguments
 * @param {string} url - Video URL
 * @param {Object} options - Download options
 * @returns {string[]}
 */
function buildArgs(url, options = {}) {
  const args = [];
  
  // Video URL
  args.push(url);
  
  // Quality selection
  if (options.quality) {
    args.push('-p', options.quality);
  }
  
  // Download danmaku
  if (options.danmaku) {
    args.push('--danmaku');
  }
  
  // Cookie file
  if (options.cookieFile) {
    args.push('--cookie', options.cookieFile);
  }
  
  // Output directory
  const outputDir = options.outputDir || getDefaultDownloadDir();
  args.push('-d', outputDir);
  
  // Video format
  args.push('--video-accept-ids', '127,126,125,120,116,112,80,74,64,32,16');
  
  // Audio format
  args.push('--audio-accept-ids', '30280,30232,30216,30280');
  
  return args;
}

/**
 * Download a Bilibili video using BBDown
 * @param {string} url - Video URL or BV/AV ID
 * @param {Object} options - Download options
 * @param {string} options.quality - Video quality (4K, 1080P, etc.)
 * @param {boolean} options.danmaku - Download danmaku
 * @param {string} options.cookieFile - Path to cookie file
 * @param {string} options.outputDir - Output directory
 * @returns {Promise<{success: boolean, output?: string, error?: string}>}
 */
async function download(url, options = {}) {
  return new Promise((resolve) => {
    const bbdownPath = getBBDownPath();
    if (!bbdownPath) {
      resolve({
        success: false,
        error: translateError('BBDown not found')
      });
      return;
    }
    
    const args = buildArgs(url, options);
    
    const outputDir = options.outputDir || getDefaultDownloadDir();
    
    const child = spawn(bbdownPath, args, {
      stdio: ['inherit', 'pipe', 'pipe']
    });
    
    let output = '';
    let errorOutput = '';
    
    child.stdout.on('data', (data) => {
      const text = data.toString();
      output += text;
      process.stdout.write(text);
    });
    
    child.stderr.on('data', (data) => {
      const text = data.toString();
      errorOutput += text;
      process.stderr.write(text);
    });
    
    child.on('close', (code) => {
      if (code === 0) {
        // Try to parse the real file path from output
        const realPath = parseOutputFilePath(output + errorOutput, outputDir);
        resolve({
          success: true,
          output: realPath || output.trim()
        });
      } else {
        resolve({
          success: false,
          error: translateError(errorOutput.trim() || `BBDown exited with code ${code}`)
        });
      }
    });
    
    child.on('error', (err) => {
      resolve({
        success: false,
        error: translateError(err.message)
      });
    });
  });
}

/**
 * Parse video URL to extract BV/AV ID
 * @param {string} url - Video URL
 * @returns {string|null}
 */
function extractVideoId(url) {
  const patterns = [
    /\/video\/(BV\w+)/,
    /\/video\/(av\d+)/,
    /(BV\w+)/,
    /(av\d+)/
  ];
  
  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) {
      return match[1];
    }
  }
  
  return null;
}

module.exports = {
  isBBDownInstalled,
  getBBDownPath,
  info,
  download,
  extractVideoId,
  getDefaultDownloadDir,
  parseInfoOutput,
  parseOutputFilePath,
  translateError
};
