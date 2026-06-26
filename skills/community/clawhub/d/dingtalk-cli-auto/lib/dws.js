/**
 * DWS CLI 封装库
 * 统一处理 dws 命令执行和错误处理
 */

const { execSync } = require('child_process');
const path = require('path');

class DWSClient {
  constructor(options = {}) {
    this.debug = options.debug || process.env.DINGTALK_DEBUG === 'true';
    this.dwsPath = options.dwsPath || 'dws';
  }

  /**
   * 执行 dws 命令
   * @param {string} command - 命令
   * @param {Array} args - 参数列表
   * @returns {Object} 解析后的 JSON 结果
   */
  exec(command, args = []) {
    const cmd = `${this.dwsPath} ${command} ${args.join(' ')} --json`;
    
    if (this.debug) {
      console.log(`[DEBUG] Executing: ${cmd}`);
    }

    try {
      const output = execSync(cmd, {
        encoding: 'utf-8',
        timeout: 30000,
        env: {
          ...process.env,
          DWS_CLIENT_ID: process.env.DWS_CLIENT_ID,
          DWS_CLIENT_SECRET: process.env.DWS_CLIENT_SECRET
        }
      });

      if (this.debug) {
        console.log(`[DEBUG] Output: ${output}`);
      }

      // 解析 JSON 输出
      try {
        return JSON.parse(output);
      } catch (e) {
        return { success: true, raw: output.trim() };
      }
    } catch (error) {
      const errorMsg = error.stderr || error.message;
      
      if (this.debug) {
        console.error(`[DEBUG] Error: ${errorMsg}`);
      }

      // 解析错误信息
      throw this.parseError(errorMsg, error.status);
    }
  }

  /**
   * 解析错误信息
   */
  parseError(errorMsg, statusCode) {
    const errorMap = {
      'unauthorized': { code: 401, message: '未认证或Token已过期，请执行 dws auth login' },
      'permission denied': { code: 403, message: '权限不足，请检查应用权限配置' },
      'not found': { code: 404, message: '请求的资源不存在' },
      'invalid': { code: 400, message: '参数错误' },
      'rate limit': { code: 429, message: '请求过于频繁，请稍后重试' }
    };

    const lowerMsg = errorMsg.toLowerCase();
    for (const [key, error] of Object.entries(errorMap)) {
      if (lowerMsg.includes(key)) {
        return new DWSError(error.message, error.code);
      }
    }

    return new DWSError(errorMsg || '执行失败', statusCode || 500);
  }

  /**
   * 检查 dws 是否已安装
   */
  checkInstalled() {
    try {
      execSync(`${this.dwsPath} --version`, { encoding: 'utf-8' });
      return true;
    } catch {
      return false;
    }
  }

  /**
   * 检查认证状态
   */
  checkAuth() {
    try {
      const result = this.exec('auth', ['status']);
      return result.authenticated === true;
    } catch {
      return false;
    }
  }
}

class DWSError extends Error {
  constructor(message, code) {
    super(message);
    this.name = 'DWSError';
    this.code = code;
  }
}

/**
 * 时间解析工具
 */
function parseTime(timeStr) {
  if (!timeStr) return null;
  
  const now = new Date();
  
  // 处理相对时间
  if (timeStr === 'today') {
    return new Date(now.getFullYear(), now.getMonth(), now.getDate(), 9, 0, 0);
  }
  if (timeStr === 'tomorrow') {
    return new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 9, 0, 0);
  }
  
  // 处理 +Nd 格式
  const dayMatch = timeStr.match(/^\+(\d+)d$/);
  if (dayMatch) {
    const days = parseInt(dayMatch[1]);
    return new Date(now.getTime() + days * 24 * 60 * 60 * 1000);
  }
  
  // 处理自然语言 (简单实现)
  if (timeStr.includes('今天')) {
    const timePart = timeStr.replace('今天', '').trim();
    return parseNaturalTime(timePart, now);
  }
  if (timeStr.includes('明天')) {
    const timePart = timeStr.replace('明天', '').trim();
    const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000);
    return parseNaturalTime(timePart, tomorrow);
  }
  
  // 尝试直接解析 ISO 格式
  const isoDate = new Date(timeStr);
  if (!isNaN(isoDate.getTime())) {
    return isoDate;
  }
  
  return null;
}

function parseNaturalTime(timeStr, baseDate) {
  // 简单解析 "18:00" 或 "上午9点"
  const hourMatch = timeStr.match(/(\d{1,2}):(\d{2})/);
  if (hourMatch) {
    const hours = parseInt(hourMatch[1]);
    const minutes = parseInt(hourMatch[2]);
    return new Date(baseDate.getFullYear(), baseDate.getMonth(), baseDate.getDate(), hours, minutes, 0);
  }
  
  // 解析 "上午9点" / "下午3点"
  const chineseMatch = timeStr.match(/(上午|下午|晚上)?(\d{1,2})点/);
  if (chineseMatch) {
    let hours = parseInt(chineseMatch[2]);
    const period = chineseMatch[1];
    if (period === '下午' || period === '晚上') {
      hours += 12;
    }
    return new Date(baseDate.getFullYear(), baseDate.getMonth(), baseDate.getDate(), hours, 0, 0);
  }
  
  return baseDate;
}

/**
 * 格式化日期为 ISO 8601
 */
function formatISO(date) {
  if (!date) return null;
  return date.toISOString().replace(/\.\d{3}Z$/, '');
}

/**
 * 格式化日期为显示格式
 */
function formatDisplay(date) {
  if (!date) return '';
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
}

module.exports = {
  DWSClient,
  DWSError,
  parseTime,
  formatISO,
  formatDisplay
};
