/**
 * 输入验证
 * 请求参数验证中间件
 */

const logger = require('./logger.cjs').logger;

/**
 * 验证字符串
 */
function isString(value, min = 1, max = 10000) {
  if (typeof value !== 'string') return false;
  if (value.length < min || value.length > max) return false;
  return true;
}

/**
 * 验证数字
 */
function isNumber(value, min = -Infinity, max = Infinity) {
  if (typeof value !== 'number' || isNaN(value)) return false;
  if (value < min || value > max) return false;
  return true;
}

/**
 * 验证枚举
 */
function isEnum(value, allowedValues) {
  return allowedValues.includes(value);
}

/**
 * 验证数组
 */
function isArray(value, minLength = 0, maxLength = 1000) {
  if (!Array.isArray(value)) return false;
  if (value.length < minLength || value.length > maxLength) return false;
  return true;
}

/**
 * 清理 XSS
 */
function sanitizeXss(str) {
  return str
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;');
}

/**
 * 验证 encode 请求
 */
function validateEncode(req, res, next) {
  const { content, metadata = {} } = req.body;
  const errors = [];

  // 验证 content
  if (!content) {
    errors.push('content is required');
  } else if (!isString(content, 1, 10000)) {
    errors.push('content must be a string between 1 and 10000 characters');
  }

  // 验证 metadata
  if (metadata.importance !== undefined) {
    if (!isNumber(metadata.importance, 0, 1)) {
      errors.push('metadata.importance must be a number between 0 and 1');
    }
  }

  if (metadata.type && !isEnum(metadata.type, ['episodic', 'semantic', 'working', 'sensory', 'reflection', 'lesson', 'milestone', 'test'])) {
    errors.push('metadata.type must be a valid type');
  }

  if (metadata.entities && !isArray(metadata.entities, 0, 50)) {
    errors.push('metadata.entities must be an array with max 50 items');
  }

  if (errors.length > 0) {
    logger.warn('Validation failed', { errors, body: req.body });
    return res.status(400).json({ error: 'Validation failed', details: errors });
  }

  // 清理 XSS
  if (typeof req.body.content === 'string') {
    req.body.content = sanitizeXss(req.body.content);
  }

  next();
}

/**
 * 验证 recall 请求
 */
function validateRecall(req, res, next) {
  const { q, limit = 10 } = req.query;
  const errors = [];

  if (!q) {
    errors.push('q (query) is required');
  } else if (!isString(q, 1, 1000)) {
    errors.push('q must be a string between 1 and 1000 characters');
  }

  const limitNum = parseInt(limit);
  if (!isNumber(limitNum, 1, 100)) {
    errors.push('limit must be a number between 1 and 100');
  }

  if (errors.length > 0) {
    logger.warn('Validation failed', { errors, query: req.query });
    return res.status(400).json({ error: 'Validation failed', details: errors });
  }

  // 清理 XSS
  if (req.query.q) {
    req.query.q = sanitizeXss(req.query.q);
  }

  next();
}

/**
 * 验证 ID 参数
 */
function validateId(req, res, next) {
  const { id } = req.params;
  
  if (!id || !/^[a-zA-Z0-9_-]+$/.test(id)) {
    return res.status(400).json({ error: 'Invalid id format' });
  }

  next();
}

module.exports = {
  validateEncode,
  validateRecall,
  validateId,
  isString,
  isNumber,
  isEnum,
  isArray,
  sanitizeXss
};
