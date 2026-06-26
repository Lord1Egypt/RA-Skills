/**
 * 通用工具模块
 */

const logger = require('./logger');

/**
 * 睡眠函数
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 带超时和重试的 fetch
 * @param {string} url - 请求 URL
 * @param {object} options - fetch 选项
 * @param {number} maxRetries - 最大重试次数
 * @param {number} retryDelay - 重试间隔（毫秒）
 * @param {number} timeout - 超时时间（毫秒）
 */
async function fetchWithRetry(url, options = {}, maxRetries = 2, retryDelay = 2000, timeout = 5000) {
  let lastError;

  for (let i = 0; i <= maxRetries; i++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeout);

      const response = await fetch(url, {
        ...options,
        signal: controller.signal
      });

      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      lastError = error;

      if (error.name === 'AbortError') {
        logger.warn(`Request timeout after ${timeout}ms`);
      } else {
        logger.warn(`Request failed: ${error.message}`);
      }

      if (i < maxRetries) {
        logger.debug(`Retrying in ${retryDelay}ms... (attempt ${i + 2}/${maxRetries + 1})`);
        await sleep(retryDelay);
      }
    }
  }

  throw lastError;
}

/**
 * 从 API key 中提取 agent_id
 * @param {string} apiKey - API key
 * @returns {string} agent_id（claw_ 后的前 8 位）
 */
function extractAgentId(apiKey) {
  if (!apiKey || !apiKey.startsWith('claw_')) {
    return 'unknown';
  }

  const afterPrefix = apiKey.slice(5); // 移除 'claw_' 前缀
  return afterPrefix.slice(0, 8);
}

/**
 * 生成简洁的任务类型标签
 * @param {string} description - 任务描述
 * @returns {string} 生成的标签
 */
function generateTaskTypeLabel(description) {
  // 常见任务模式映射
  const patterns = [
    { regex: /重构|重构代码|代码重构|rewrite|refactor/i, label: '代码重构' },
    { regex: /测试|单元测试|test|testing/i, label: '单元测试' },
    { regex: /文档|文档生成|documentation|doc/i, label: '文档生成' },
    { regex: /修复|bug|fix|修复问题/i, label: 'Bug修复' },
    { regex: /转换|transform|convert|格式转换|转|CSV|JSON|XML|YAML/i, label: '格式转换' },
    { regex: /分析|analyze|analysis|数据分析/i, label: '数据分析' },
    { regex: /优化|optimize|性能优化|optimization/i, label: '性能优化' },
    { regex: /部署|deploy|deployment|发布/i, label: '应用部署' },
    { regex: /配置|config|configuration|设置/i, label: '配置管理' },
    { regex: /查询|query|检索|search/i, label: '信息查询' }
  ];

  for (const { regex, label } of patterns) {
    if (regex.test(description)) {
      return label;
    }
  }

  // 如果没有匹配到，从描述中提取关键词生成标签
  // 移除常见虚词，提取实词
  const words = description
    .replace(/[把将了为对进行完成做用把被让给]/g, '')
    .replace(/[\s,.，。！!；;：:]+/g, ' ')
    .trim()
    .split(/\s+/)
    .filter(w => w.length >= 2 && w.length <= 6)
    .slice(0, 2);

  if (words.length >= 2) {
    return words.join('').slice(0, 12);
  } else if (words.length === 1) {
    return words[0].slice(0, 12);
  }

  return '任务执行';
}

module.exports = {
  sleep,
  fetchWithRetry,
  extractAgentId,
  generateTaskTypeLabel
};
