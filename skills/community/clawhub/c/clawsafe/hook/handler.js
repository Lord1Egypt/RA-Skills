/**
 * clawSafe Input Hook / clawSafe 输入拦截器
 * Intercepts all user input before it reaches the AI agent
 * 在用户输入到达AI代理之前拦截所有输入
 * 
 * Supported events:
 * - message:received (when message is received)
 * - message:preprocessed (after media/link processing)
 * - agent:input (before agent processes input)
 */

const path = require('path');
const fs = require('fs');

let detector = null;

/**
 * Detect language of input / 检测输入语言
 * @param {string} text - Input text
 * @returns {string} - 'en' or 'zh'
 */
function detectLanguage(text) {
  const chineseRegex = /[\u4e00-\u9fa5]/;
  return chineseRegex.test(text) ? 'zh' : 'en';
}

/**
 * Get localized messages / 获取本地化消息
 * @param {string} lang - Language code
 * @param {object} result - Scan result
 * @returns {string[]} - Localized messages
 */
function getBlockedMessages(lang, result) {
  const isZh = lang === 'zh';
  
  const threatTypes = result.threats.map(t => {
    const typeMap = {
      'injection': isZh ? '提示注入' : 'Prompt Injection',
      'jailbreak': isZh ? '越狱攻击' : 'Jailbreak',
      'prompt_leak': isZh ? '提示泄露' : 'Prompt Leaking',
      'encoding': isZh ? '编码混淆' : 'Encoding Attack',
      'sql_injection': isZh ? 'SQL注入' : 'SQL Injection',
      'xss': isZh ? 'XSS攻击' : 'XSS',
      'key_exposure': isZh ? '密钥泄露' : 'API Key Exposure',
      'supply_chain': isZh ? '供应链攻击' : 'Supply Chain Attack',
      'debug_info': isZh ? '调试信息' : 'Debug Info',
      'env_leak': isZh ? '环境变量泄露' : 'Env Leak'
    };
    return typeMap[t.type] || t.type || 'unknown';
  });
  
  const messages = [
    isZh ? '🛡️ 输入已被 clawSafe 拦截' : '🛡️ Input blocked by clawSafe',
    '',
    isZh ? '威胁类型: ' : 'Threats: ',
    threatTypes.join(', '),
    '',
    isZh ? '置信度: ' : 'Confidence: ',
    (result.confidence * 100).toFixed(0) + '%'
  ];
  
  return [messages.join('\n')];
}

/**
 * Initialize detector / 初始化检测器
 */
function initDetector() {
  if (detector) return detector;
  
  try {
    const skillRoot = path.join(__dirname, '..');
    const detectorPath = path.join(skillRoot, 'detector.js');
    
    if (fs.existsSync(detectorPath)) {
      const Detector = require(detectorPath);
      detector = new Detector(skillRoot);
      console.log('[clawSafe] Detector initialized');
    }
  } catch (e) {
    console.error('[clawSafe] Failed to load detector:', e.message);
  }
  
  return detector;
}

/**
 * Extract input from event / 从事件中提取输入
 * @param {object} event - OpenClaw event
 * @returns {string|null} - Input text
 */
function extractInput(event) {
  // Try various possible input locations
  const input = 
    event.context?.content ||
    event.context?.body ||
    event.context?.message ||
    event.input ||
    event.message ||
    event.body ||
    event.content ||
    '';
  
  return input || null;
}

/**
 * Scan and block if threat detected / 扫描并在检测到威胁时拦截
 * @param {string} input - User input
 * @param {object} event - Full event
 * @returns {object|null} - Block response or null
 */
function scanAndBlock(input, event) {
  if (!input || typeof input !== 'string') return null;
  if (input.length < 3) return null;
  
  const lang = detectLanguage(input);
  const result = detector.scan(input);
  
  if (!result.safe && result.confidence >= 0.6) {
    console.log('[clawSafe] Blocked input:', {
      threats: result.threats.map(t => t.type),
      confidence: result.confidence,
      lang,
      eventType: event.type + ':' + event.action
    });
    
    return {
      blocked: true,
      safe: false,
      messages: getBlockedMessages(lang, result)
    };
  }
  
  return null;
}

/**
 * Main handler function / 主处理函数
 * Supports: message:received, message:preprocessed, agent:input
 */
async function handler(event) {
  const d = initDetector();
  
  if (!d) {
    console.warn('[clawSafe] Detector not available, allowing input');
    return;
  }
  
  // Extract input from event
  const input = extractInput(event);
  if (!input) return;
  
  // Scan and potentially block
  return scanAndBlock(input, event);
}

// Also export for different event types
module.exports = handler;
module.exports.default = handler;
module.exports.handler = handler;

// Export for manual calling
module.exports.scan = function(input) {
  const d = initDetector();
  if (!d) return { safe: true, threats: [], confidence: 0 };
  return d.scan(input);
};
