/**
 * PII (个人身份信息) 过滤模块
 * 检测并阻止包含敏感信息的文本发布
 */

const PII_PATTERNS = {
  email: {
    pattern: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/,
    description: '邮箱地址'
  },
  phone: {
    pattern: /(?:(?:\+86)?1[3-9]\d{9})|\b\d{11}\b/,
    description: '手机号'
  },
  idCard: {
    pattern: /\b\d{6}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b/,
    description: '身份证号'
  },
  ipv4: {
    pattern: /\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b/,
    description: 'IPv4 地址'
  }
};

/**
 * 检测文本中是否包含 PII
 * @param {string} text - 要检测的文本
 * @returns {{detected: boolean, type?: string, description?: string, match?: string}}
 */
function detectPII(text) {
  if (typeof text !== 'string') {
    return { detected: false };
  }

  for (const [type, { pattern, description }] of Object.entries(PII_PATTERNS)) {
    const match = text.match(pattern);
    if (match) {
      return {
        detected: true,
        type,
        description,
        match: match[0].substring(0, 20) + (match[0].length > 20 ? '...' : '') // 只返回部分匹配内容
      };
    }
  }

  return { detected: false };
}

/**
 * 验证文本是否安全（不包含 PII）
 * @param {string} text - 要验证的文本
 * @returns {{safe: boolean, reason?: string}}
 */
function validateSafe(text) {
  const result = detectPII(text);

  if (result.detected) {
    return {
      safe: false,
      reason: `检测到可能的 ${result.description} (${result.type})`
    };
  }

  return { safe: true };
}

module.exports = {
  detectPII,
  validateSafe,
  PII_PATTERNS
};
