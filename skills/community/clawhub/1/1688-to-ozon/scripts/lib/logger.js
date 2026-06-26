#!/usr/bin/env node
/**
 * 日志 + 进度报告模块
 * 
 * 功能：
 * - 控制台日志输出（带时间戳、颜色）
 * - 进度文件写入（progress.json）
 * - 支持详细日志模式
 */

const fs = require('fs');
const path = require('path');

// ANSI 颜色代码
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m',
  gray: '\x1b[90m'
};

/**
 * 获取当前时间戳字符串
 */
function timestamp() {
  const now = new Date();
  return now.toISOString().replace('T', ' ').substring(0, 19);
}

/**
 * 输出日志
 */
function log(message, level = 'info') {
  const ts = timestamp();
  let color = colors.white;
  let prefix = 'ℹ️';
  
  switch (level) {
    case 'error':
      color = colors.red;
      prefix = '❌';
      break;
    case 'warn':
      color = colors.yellow;
      prefix = '⚠️';
      break;
    case 'success':
      color = colors.green;
      prefix = '✅';
      break;
    case 'info':
      color = colors.blue;
      prefix = 'ℹ️';
      break;
    case 'debug':
      color = colors.gray;
      prefix = '🔍';
      break;
  }
  
  console.log(`${color}${prefix} [${ts}]${colors.reset} ${message}`);
}

/**
 * 写入进度报告
 */
function writeProgress(outputDir, step, status, details = {}) {
  const progressFile = path.join(outputDir, 'progress.json');
  
  let progress = {
    startTime: new Date().toISOString(),
    status: 'running',
    steps: []
  };
  
  // 读取现有进度
  if (fs.existsSync(progressFile)) {
    try {
      progress = JSON.parse(fs.readFileSync(progressFile, 'utf-8'));
    } catch (e) {
      // 忽略读取错误
    }
  }
  
  // 更新步骤
  const existingStep = progress.steps.find(s => s.step === step);
  if (existingStep) {
    existingStep.status = status;
    existingStep.timestamp = new Date().toISOString();
    existingStep.details = { ...existingStep.details, ...details };
  } else {
    progress.steps.push({
      step,
      status,
      timestamp: new Date().toISOString(),
      details
    });
  }
  
  // 更新整体状态
  if (status === 'failed') {
    progress.status = 'failed';
    progress.error = details.error || 'Unknown error';
  } else if (status === 'completed' && progress.steps.every(s => s.status === 'completed')) {
    progress.status = 'completed';
  }
  
  // 写入文件
  fs.writeFileSync(progressFile, JSON.stringify(progress, null, 2));
}

/**
 * 读取进度报告
 */
function readProgress(outputDir) {
  const progressFile = path.join(outputDir, 'progress.json');
  if (!fs.existsSync(progressFile)) {
    return null;
  }
  return JSON.parse(fs.readFileSync(progressFile, 'utf-8'));
}

/**
 * 飞书通知（使用 App 认证）
 */
let feishuConfig = null;
let accessToken = null;
let tokenExpiry = 0;

async function getFeishuAccessToken(config) {
  // 优先使用环境变量，其次使用配置
  const appId = process.env.FEISHU_APP_ID || config?.feishu?.appId || 'cli_a90b1d9903385ceb';
  const appSecret = process.env.FEISHU_APP_SECRET || config?.feishu?.appSecret || 'G9TdEypJQ9SDOBdExTJVrdn2LtxbdFcV';
  
  if (!appId || !appSecret) {
    return null;
  }
  
  // 检查缓存的 token
  if (accessToken && Date.now() < tokenExpiry) {
    return accessToken;
  }
  
  try {
    const { execSync } = require('child_process');
    const response = execSync(
      `curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
        -H "Content-Type: application/json" \
        -d '{"app_id": "${appId}", "app_secret": "${appSecret}"}'`,
      { encoding: 'utf-8' }
    );
    const data = JSON.parse(response);
    if (data.tenant_access_token) {
      accessToken = data.tenant_access_token;
      tokenExpiry = Date.now() + (data.expire - 300) * 1000; // 提前 5 分钟过期
      return accessToken;
    }
  } catch (e) {
    log(`获取飞书 token 失败：${e.message}`, 'warn');
  }
  return null;
}

/**
 * 发送飞书消息（使用 OpenClaw 工具）
 */
async function notifyFeishu(message, config) {
  // 优先使用环境变量，其次使用配置
  const chatId = process.env.FEISHU_CHAT_ID || config?.feishu?.chatId || 'oc_57bd4ab12e061043ec6d4f3805332b83';
  if (!chatId) {
    return false;
  }
  
  try {
    // 使用 OpenClaw 的飞书消息工具
    const { execSync } = require('child_process');
    const cmd = `openclaw feishu send --to "${chatId}" --message "${message.replace(/"/g, '\\"')}"`;
    const result = execSync(cmd, { encoding: 'utf-8', timeout: 10000 });
    log(`飞书通知已发送`, 'debug');
    return true;
  } catch (e) {
    log(`飞书通知失败：${e.message}`, 'warn');
  }
  return false;
}

module.exports = {
  log,
  writeProgress,
  readProgress,
  colors,
  timestamp,
  notifyFeishu
};
