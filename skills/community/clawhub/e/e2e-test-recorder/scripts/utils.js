/**
 * 工具函数模块
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const { exec } = require('child_process');
const util = require('util');
const execAsync = util.promisify(exec);

/**
 * 检查依赖是否安装
 */
async function checkDependencies() {
  const dependencies = ['puppeteer', 'puppeteer-screen-recorder', 'ffmpeg-static'];
  const missing = [];
  
  console.log(chalk.blue('🔍 检查依赖...'));
  
  for (const dep of dependencies) {
    try {
      require.resolve(dep);
      console.log(chalk.green(`  ✅ ${dep}`));
    } catch (error) {
      missing.push(dep);
      console.log(chalk.red(`  ❌ ${dep}`));
    }
  }
  
  if (missing.length > 0) {
    console.log(chalk.yellow('\n⚠️  缺少以下依赖:'));
    missing.forEach(dep => console.log(chalk.yellow(`  - ${dep}`)));
    console.log(chalk.cyan('\n运行以下命令安装:'));
    console.log(chalk.cyan(`  npm install ${missing.join(' ')}`));
    return false;
  }
  
  console.log(chalk.green('\n✅ 所有依赖已安装'));
  return true;
}

/**
 * 检查FFmpeg是否可用
 */
async function checkFFmpeg() {
  try {
    const { stdout } = await execAsync('ffmpeg -version');
    if (stdout.includes('ffmpeg version')) {
      console.log(chalk.green('✅ FFmpeg 已安装'));
      return true;
    }
  } catch (error) {
    // 尝试使用ffmpeg-static
    try {
      const ffmpegStatic = require('ffmpeg-static');
      if (fs.existsSync(ffmpegStatic)) {
        console.log(chalk.green('✅ FFmpeg (静态版本) 可用'));
        return true;
      }
    } catch (staticError) {
      console.log(chalk.yellow('⚠️  FFmpeg 未安装，使用 ffmpeg-static'));
    }
  }
  
  return false;
}

/**
 * 创建目录结构
 */
function createDirectoryStructure(baseDir) {
  const directories = [
    'recordings',
    'configs',
    'templates',
    'examples',
    'logs',
    'test-data'
  ];
  
  directories.forEach(dir => {
    const dirPath = path.join(baseDir, dir);
    fs.ensureDirSync(dirPath);
    console.log(chalk.gray(`  创建目录: ${dir}`));
  });
}

/**
 * 生成唯一文件名
 */
function generateUniqueFilename(prefix = 'recording', extension = 'mp4') {
  const timestamp = new Date().toISOString()
    .replace(/[:.]/g, '-')
    .replace('T', '_')
    .split('.')[0];
  
  return `${prefix}_${timestamp}.${extension}`;
}

/**
 * 格式化文件大小
 */
function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * 格式化时间
 */
function formatTime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  
  const parts = [];
  if (hours > 0) parts.push(`${hours}h`);
  if (minutes > 0) parts.push(`${minutes}m`);
  parts.push(`${secs}s`);
  
  return parts.join(' ');
}

/**
 * 验证配置文件
 */
function validateConfig(config, schema) {
  const errors = [];
  
  for (const [key, rule] of Object.entries(schema)) {
    if (rule.required && !(key in config)) {
      errors.push(`缺少必需字段: ${key}`);
      continue;
    }
    
    if (key in config) {
      const value = config[key];
      
      // 类型检查
      if (rule.type && typeof value !== rule.type) {
        errors.push(`字段 ${key} 应为 ${rule.type} 类型，实际为 ${typeof value}`);
      }
      
      // 枚举检查
      if (rule.enum && !rule.enum.includes(value)) {
        errors.push(`字段 ${key} 应为以下值之一: ${rule.enum.join(', ')}`);
      }
      
      // 范围检查
      if (rule.min !== undefined && value < rule.min) {
        errors.push(`字段 ${key} 应大于等于 ${rule.min}`);
      }
      
      if (rule.max !== undefined && value > rule.max) {
        errors.push(`字段 ${key} 应小于等于 ${rule.max}`);
      }
    }
  }
  
  return errors;
}

/**
 * 加载配置文件
 */
async function loadConfig(configPath) {
  try {
    const config = await fs.readJson(configPath);
    console.log(chalk.green(`✅ 加载配置文件: ${configPath}`));
    return config;
  } catch (error) {
    console.error(chalk.red(`❌ 加载配置文件失败: ${configPath}`), error);
    return null;
  }
}

/**
 * 保存配置文件
 */
async function saveConfig(config, configPath) {
  try {
    await fs.writeJson(configPath, config, { spaces: 2 });
    console.log(chalk.green(`✅ 保存配置文件: ${configPath}`));
    return true;
  } catch (error) {
    console.error(chalk.red(`❌ 保存配置文件失败: ${configPath}`), error);
    return false;
  }
}

/**
 * 记录日志
 */
class Logger {
  constructor(logDir = './logs') {
    this.logDir = logDir;
    fs.ensureDirSync(logDir);
    
    const timestamp = new Date().toISOString()
      .replace(/[:.]/g, '-')
      .replace('T', '_')
      .split('.')[0];
    
    this.logFile = path.join(logDir, `recorder_${timestamp}.log`);
  }
  
  log(level, message, data = null) {
    const timestamp = new Date().toISOString();
    const logEntry = {
      timestamp,
      level,
      message,
      data
    };
    
    // 控制台输出
    const colors = {
      info: chalk.blue,
      success: chalk.green,
      warn: chalk.yellow,
      error: chalk.red,
      debug: chalk.gray
    };
    
    const color = colors[level] || chalk.white;
    console.log(color(`[${timestamp}] ${level.toUpperCase()}: ${message}`));
    
    // 文件记录
    const logLine = JSON.stringify(logEntry) + '\n';
    fs.appendFileSync(this.logFile, logLine);
  }
  
  info(message, data = null) {
    this.log('info', message, data);
  }
  
  success(message, data = null) {
    this.log('success', message, data);
  }
  
  warn(message, data = null) {
    this.log('warn', message, data);
  }
  
  error(message, data = null) {
    this.log('error', message, data);
  }
  
  debug(message, data = null) {
    this.log('debug', message, data);
  }
}

/**
 * 进度条显示
 */
class ProgressBar {
  constructor(total, width = 40) {
    this.total = total;
    this.width = width;
    this.current = 0;
  }
  
  update(current) {
    this.current = current;
    this.render();
  }
  
  increment() {
    this.current++;
    this.render();
  }
  
  render() {
    const percentage = this.current / this.total;
    const filledWidth = Math.round(this.width * percentage);
    const emptyWidth = this.width - filledWidth;
    
    const filledBar = '█'.repeat(filledWidth);
    const emptyBar = '░'.repeat(emptyWidth);
    
    const percentText = Math.round(percentage * 100);
    
    process.stdout.write(`\r[${filledBar}${emptyBar}] ${percentText}% (${this.current}/${this.total})`);
    
    if (this.current >= this.total) {
      process.stdout.write('\n');
    }
  }
}

/**
 * 视频文件信息
 */
async function getVideoInfo(filePath) {
  try {
    const { stdout } = await execAsync(`ffprobe -v quiet -print_format json -show_format -show_streams "${filePath}"`);
    const info = JSON.parse(stdout);
    
    return {
      duration: parseFloat(info.format.duration),
      size: parseInt(info.format.size),
      bitrate: parseInt(info.format.bit_rate),
      format: info.format.format_name,
      streams: info.streams.map(stream => ({
        type: stream.codec_type,
        codec: stream.codec_name,
        width: stream.width,
        height: stream.height,
        fps: stream.r_frame_rate ? eval(stream.r_frame_rate) : null
      }))
    };
  } catch (error) {
    console.error(chalk.red(`❌ 获取视频信息失败: ${filePath}`), error);
    return null;
  }
}

/**
 * 转换视频格式
 */
async function convertVideo(inputPath, outputPath, options = {}) {
  const {
    format = 'mp4',
    quality = 23,
    fps = 30,
    width = null,
    height = null
  } = options;
  
  const commands = ['ffmpeg', '-i', `"${inputPath}"`];
  
  // 视频参数
  commands.push('-c:v', 'libx264');
  commands.push('-crf', quality.toString());
  commands.push('-preset', 'medium');
  commands.push('-r', fps.toString());
  
  // 音频参数
  commands.push('-c:a', 'aac');
  commands.push('-b:a', '128k');
  
  // 尺寸调整
  if (width && height) {
    commands.push('-vf', `scale=${width}:${height}`);
  }
  
  commands.push('-y', `"${outputPath}"`);
  
  const command = commands.join(' ');
  
  try {
    console.log(chalk.blue(`🔄 转换视频: ${inputPath} -> ${outputPath}`));
    const { stdout, stderr } = await execAsync(command);
    
    const inputInfo = await getVideoInfo(inputPath);
    const outputInfo = await getVideoInfo(outputPath);
    
    if (inputInfo && outputInfo) {
      const compressionRatio = (1 - outputInfo.size / inputInfo.size) * 100;
      console.log(chalk.green(`✅ 视频转换完成`));
      console.log(chalk.cyan(`   原始大小: ${formatFileSize(inputInfo.size)}`));
      console.log(chalk.cyan(`   转换后大小: ${formatFileSize(outputInfo.size)}`));
      console.log(chalk.cyan(`   压缩率: ${compressionRatio.toFixed(1)}%`));
    }
    
    return outputPath;
  } catch (error) {
    console.error(chalk.red(`❌ 视频转换失败`), error);
    throw error;
  }
}

/**
 * 提取视频帧
 */
async function extractFrames(inputPath, outputDir, options = {}) {
  const { fps = 1, format = 'png', width = null, height = null } = options;
  
  fs.ensureDirSync(outputDir);
  
  const commands = ['ffmpeg', '-i', `"${inputPath}"`];
  
  // 帧率
  commands.push('-vf', `fps=${fps}`);
  
  // 尺寸调整
  if (width && height) {
    commands.push('-vf', `fps=${fps},scale=${width}:${height}`);
  }
  
  // 输出格式
  const outputPattern = path.join(outputDir, `frame_%04d.${format}`);
  commands.push('-y', `"${outputPattern}"`);
  
  const command = commands.join(' ');
  
  try {
    console.log(chalk.blue(`🖼️  提取视频帧: ${inputPath}`));
    const { stdout, stderr } = await execAsync(command);
    
    const frames = fs.readdirSync(outputDir)
      .filter(file => file.startsWith('frame_'))
      .sort();
    
    console.log(chalk.green(`✅ 提取完成，共 ${frames.length} 帧`));
    return frames.map(frame => path.join(outputDir, frame));
  } catch (error) {
    console.error(chalk.red(`❌ 提取视频帧失败`), error);
    throw error;
  }
}

module.exports = {
  checkDependencies,
  checkFFmpeg,
  createDirectoryStructure,
  generateUniqueFilename,
  formatFileSize,
  formatTime,
  validateConfig,
  loadConfig,
  saveConfig,
  Logger,
  ProgressBar,
  getVideoInfo,
  convertVideo,
  extractFrames
};