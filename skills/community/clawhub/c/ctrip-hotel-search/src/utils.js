// 工具函数模块

/**
 * 延迟函数
 * @param {number} ms - 毫秒数
 */
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 格式化日期（携程格式）
 * @param {Date} date - 日期对象
 * @returns {string} 格式化后的日期字符串
 */
function formatDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * 解析价格字符串
 * @param {string} priceStr - 价格字符串（如"¥358"）
 * @returns {number} 价格数字
 */
function parsePrice(priceStr) {
  const match = priceStr.match(/¥?(\d+)/);
  return match ? parseInt(match[1]) : 0;
}

/**
 * 解析评分字符串
 * @param {string} ratingStr - 评分字符串（如"4.8分"）
 * @returns {number} 评分数字
 */
function parseRating(ratingStr) {
  const match = ratingStr.match(/(\d+\.?\d*)/);
  return match ? parseFloat(match[1]) : 0;
}

/**
 * 生成搜索ID（用于追踪搜索会话）
 * @returns {string} 唯一ID
 */
function generateSearchId() {
  return 'search_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

/**
 * 验证配置文件
 * @param {object} config - 配置对象
 * @returns {boolean} 是否有效
 */
function validateConfig(config) {
  if (!config.ctrip || !config.ctrip.username || !config.ctrip.password) {
    console.error('❌ 配置错误：请在 config.json 中设置携程账号和密码');
    return false;
  }
  return true;
}

module.exports = {
  delay,
  formatDate,
  parsePrice,
  parseRating,
  generateSearchId,
  validateConfig
};