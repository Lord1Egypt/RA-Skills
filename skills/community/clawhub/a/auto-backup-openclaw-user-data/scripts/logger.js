/**
 * 日志管理模块
 * 负责日志的记录和管理
 */

const fs = require('fs-extra');
const path = require('path');
const { LOG_FILE, ensureConfigDir } = require('./config');

// 日志级别
const LOG_LEVELS = {
  DEBUG: 0,
  INFO: 1,
  WARN: 2,
  ERROR: 3
};

// 当前日志级别（默认 INFO）
let currentLevel = LOG_LEVELS.INFO;

// 日志颜色（终端输出）
const COLORS = {
  DEBUG: '\x1b[36m',  // 青色
  INFO: '\x1b[32m',   // 绿色
  WARN: '\x1b[33m',   // 黄色
  ERROR: '\x1b[31m',  // 红色
  RESET: '\x1b[0m'
};

/**
 * 设置日志级别
 */
function setLevel(level) {
  if (LOG_LEVELS[level] !== undefined) {
    currentLevel = LOG_LEVELS[level];
  }
}

/**
 * 格式化时间戳
 */
function formatTimestamp() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  const ms = String(now.getMilliseconds()).padStart(3, '0');
  
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${ms}`;
}

/**
 * 写入日志到文件
 */
async function writeToFile(message) {
  try {
    await ensureConfigDir();
    await fs.appendFile(LOG_FILE, message + '\n');
  } catch (error) {
    // 写入失败，只输出到控制台
    console.error(`[Logger] 写入日志文件失败: ${error.message}`);
  }
}

/**
 * 格式化日志消息
 */
function formatMessage(level, module, message) {
  const timestamp = formatTimestamp();
  return `[${timestamp}] [${level.padEnd(5)}] [${module}] ${message}`;
}

/**
 * 记录日志
 */
async function log(level, module, message) {
  // 检查日志级别
  if (LOG_LEVELS[level] < currentLevel) {
    return;
  }
  
  const formattedMessage = formatMessage(level, module, message);
  
  // 输出到控制台（带颜色）
  const color = COLORS[level] || COLORS.RESET;
  console.log(`${color}${formattedMessage}${COLORS.RESET}`);
  
  // 写入到文件
  await writeToFile(formattedMessage);
}

/**
 * DEBUG 级别日志
 */
async function debug(module, message) {
  await log('DEBUG', module, message);
}

/**
 * INFO 级别日志
 */
async function info(module, message) {
  await log('INFO', module, message);
}

/**
 * WARN 级别日志
 */
async function warn(module, message) {
  await log('WARN', module, message);
}

/**
 * ERROR 级别日志
 */
async function error(module, message) {
  await log('ERROR', module, message);
}

/**
 * 清理旧日志文件
 */
async function cleanOldLogs(maxSize = '10MB', maxFiles = 5) {
  try {
    if (!(await fs.pathExists(LOG_FILE))) {
      return;
    }
    
    const stats = await fs.stat(LOG_FILE);
    const sizeInBytes = stats.size;
    
    // 解析最大大小
    const sizeMatch = maxSize.match(/^(\d+)(MB|KB|GB)?$/i);
    if (!sizeMatch) return;
    
    const sizeValue = parseInt(sizeMatch[1]);
    const sizeUnit = (sizeMatch[2] || 'B').toUpperCase();
    
    let maxSizeInBytes;
    switch (sizeUnit) {
      case 'KB': maxSizeInBytes = sizeValue * 1024; break;
      case 'MB': maxSizeInBytes = sizeValue * 1024 * 1024; break;
      case 'GB': maxSizeInBytes = sizeValue * 1024 * 1024 * 1024; break;
      default: maxSizeInBytes = sizeValue;
    }
    
    // 如果超过最大大小，进行轮转
    if (sizeInBytes > maxSizeInBytes) {
      await rotateLogs(maxFiles);
    }
  } catch (err) {
    console.error(`[Logger] 清理日志失败: ${err.message}`);
  }
}

/**
 * 日志轮转
 */
async function rotateLogs(maxFiles) {
  try {
    // 删除最旧的日志文件
    const oldestLogFile = `${LOG_FILE}.${maxFiles}`;
    if (await fs.pathExists(oldestLogFile)) {
      await fs.remove(oldestLogFile);
    }
    
    // 重命名现有日志文件
    for (let i = maxFiles - 1; i >= 1; i--) {
      const oldFile = `${LOG_FILE}.${i}`;
      const newFile = `${LOG_FILE}.${i + 1}`;
      if (await fs.pathExists(oldFile)) {
        await fs.move(oldFile, newFile);
      }
    }
    
    // 重命名当前日志文件
    if (await fs.pathExists(LOG_FILE)) {
      await fs.move(LOG_FILE, `${LOG_FILE}.1`);
    }
    
    await info('Logger', `日志轮转完成，保留 ${maxFiles} 个日志文件`);
  } catch (err) {
    console.error(`[Logger] 日志轮转失败: ${err.message}`);
  }
}

/**
 * 读取日志内容
 */
async function readLogs(lines = 100) {
  try {
    if (!(await fs.pathExists(LOG_FILE))) {
      return [];
    }
    
    const content = await fs.readFile(LOG_FILE, 'utf-8');
    const logLines = content.trim().split('\n');
    
    // 返回最后 N 行
    return logLines.slice(-lines);
  } catch (err) {
    console.error(`[Logger] 读取日志失败: ${err.message}`);
    return [];
  }
}

module.exports = {
  debug,
  info,
  warn,
  error,
  setLevel,
  cleanOldLogs,
  readLogs,
  LOG_LEVELS
};