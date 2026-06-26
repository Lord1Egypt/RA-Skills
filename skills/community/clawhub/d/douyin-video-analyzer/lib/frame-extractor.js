/**
 * 帧提取模块
 * 使用 ffmpeg 从视频中提取关键帧
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const fs = require('fs');
const path = require('path');
const util = require('./utils');

const execAsync = promisify(exec);

/**
 * 检查 ffmpeg 是否安装
 * @returns {Promise<boolean>}
 */
async function checkFfmpeg() {
  try {
    await execAsync('ffmpeg -version');
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * 获取视频时长（秒）
 * @param {string} videoPath - 视频文件路径
 * @returns {Promise<number>}
 */
async function getVideoDuration(videoPath) {
  try {
    const { stdout } = await execAsync(
      `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "${videoPath}"`
    );
    return parseFloat(stdout.trim());
  } catch (error) {
    console.error('  ❌ 获取视频时长失败:', error.message);
    return 0;
  }
}

/**
 * 从视频中提取关键帧
 * @param {string} videoPath - 视频文件路径
 * @param {string} outputDir - 输出目录
 * @param {Object} options - 配置选项
 * @param {number} options.interval - 提取间隔（秒），默认 1
 * @param {number} options.maxFrames - 最大帧数，默认 30
 * @returns {Promise<{frames: string[], duration: number}>}
 */
async function extractKeyframes(videoPath, outputDir, options = {}) {
  const { interval = 1, maxFrames = 30 } = options;
  
  // 检查 ffmpeg
  const hasFfmpeg = await checkFfmpeg();
  if (!hasFfmpeg) {
    throw new Error('ffmpeg 未安装，请安装 ffmpeg: https://ffmpeg.org/download.html');
  }
  
  // 创建输出目录
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  // 获取视频时长
  const duration = await getVideoDuration(videoPath);
  if (duration === 0) {
    throw new Error('无法获取视频时长');
  }
  
  console.log(`  🎬 视频时长: ${Math.round(duration)}秒`);
  
  // 计算需要提取的帧数
  const totalFrames = Math.floor(duration / interval);
  const frameCount = Math.min(totalFrames, maxFrames);
  const actualInterval = totalFrames > maxFrames 
    ? duration / maxFrames 
    : interval;
  
  console.log(`  📸 提取帧数: ${frameCount}帧 (间隔: ${actualInterval.toFixed(1)}秒)`);
  
  const frames = [];
  
  // 使用 ffmpeg 提取帧
  // -vf "fps=1/${actualInterval}" 表示每 N 秒提取一帧
  // -q:v 2 表示最高质量
  const framePattern = path.join(outputDir, 'frame_%03d.png');
  
  try {
    const fps = 1 / actualInterval;
    const command = `ffmpeg -i "${videoPath}" -vf "fps=${fps},scale='min(1280,iw)':-1" -q:v 2 "${framePattern}" -y`;
    
    console.log(`  🔄 正在提取关键帧...`);
    await execAsync(command);
    
    // 读取生成的帧文件
    const files = fs.readdirSync(outputDir)
      .filter(f => f.startsWith('frame_') && f.endsWith('.png'))
      .sort()
      .map(f => path.join(outputDir, f));
    
    frames.push(...files);
    
    console.log(`  ✅ 成功提取 ${frames.length} 帧`);
    
  } catch (error) {
    console.error('  ❌ 帧提取失败:', error.message);
    throw error;
  }
  
  return { frames, duration };
}

/**
 * 清理临时帧文件
 * @param {string} framesDir - 帧文件目录
 */
function cleanupFrames(framesDir) {
  try {
    if (fs.existsSync(framesDir)) {
      const files = fs.readdirSync(framesDir);
      for (const file of files) {
        if (file.startsWith('frame_') && file.endsWith('.png')) {
          fs.unlinkSync(path.join(framesDir, file));
        }
      }
      console.log(`  🧹 已清理 ${files.length} 个临时帧文件`);
    }
  } catch (error) {
    console.error('  ⚠️ 清理帧文件失败:', error.message);
  }
}

/**
 * 将图片转换为 base64
 * @param {string} imagePath - 图片路径
 * @returns {string} base64 编码的图片
 */
function imageToBase64(imagePath) {
  const imageBuffer = fs.readFileSync(imagePath);
  return imageBuffer.toString('base64');
}

module.exports = {
  checkFfmpeg,
  extractKeyframes,
  cleanupFrames,
  imageToBase64,
  getVideoDuration
};
