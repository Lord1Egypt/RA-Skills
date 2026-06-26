/**
 * EVA Soul - 国际化模块
 * 支持 zh / en / ja / zh-TW 四种语言
 */

const fs = require('fs');
const path = require('path');
const { getUserConfig } = require('../lib/core/config');

// 语言列表
const SUPPORTED = ['zh', 'en', 'ja', 'zh-TW'];
const DEFAULT = 'zh';

// 语言名称映射
const LANG_NAMES = {
  zh: '简体中文',
  en: 'English',
  ja: '日本語',
  'zh-TW': '繁體中文'
};

// 缓存已加载的翻译
const cache = {};

/**
 * 检测用户语言偏好
 * 优先级：plugin.config.lang > USER.md locale > system locale
 */
function detectLocale(config, userConfig) {
  // 1. 插件配置优先
  if (config?.lang && SUPPORTED.includes(config.lang)) return config.lang;

  // 2. USER.md 中的 locale
  if (userConfig?.timezone) {
    const tz = userConfig.timezone || '';
    if (tz.includes('TW') || tz.includes('HK')) return 'zh-TW';
    if (tz.includes('Japan')) return 'ja';
  }

  // 3. 系统 locale
  const sysLocale = (process.env.LANG || process.env.LC_ALL || '').toLowerCase();
  if (sysLocale.includes('zh_tw') || sysLocale.includes('zh-hk')) return 'zh-TW';
  if (sysLocale.includes('ja')) return 'ja';
  if (sysLocale.includes('en')) return 'en';

  return DEFAULT;
}

/**
 * 加载语言文件
 */
function load(locale) {
  if (cache[locale]) return cache[locale];

  const langFile = path.join(__dirname, `${locale}.json`);
  if (fs.existsSync(langFile)) {
    try {
      cache[locale] = JSON.parse(fs.readFileSync(langFile, 'utf8'));
      return cache[locale];
    } catch (e) {
      // fall through
    }
  }
  // 找不到则 fallback 中文
  if (locale !== DEFAULT) return load(DEFAULT);
  return {};
}

/**
 * 翻译函数
 * @param {string} locale 当前语言
 * @param {string} key 如 'hooks.sessionStart.loaded'
 * @param {object} params 插值参数，如 { name: 'EVA' } → "你好, EVA"
 * @returns {string} 翻译后文本
 */
function t(locale, key, params = {}) {
  const dict = load(locale);
  const keys = key.split('.');
  let value = dict;

  for (const k of keys) {
    if (value && typeof value === 'object') {
      value = value[k];
    } else {
      value = undefined;
      break;
    }
  }

  if (value === undefined) {
    // 找不到则尝试中文 fallback
    if (locale !== DEFAULT) return t(DEFAULT, key, params);
    return key; // 彻底找不到就返回 key
  }

  if (typeof value !== 'string') return String(value);

  // 插值：{{name}} → params.name
  return value.replace(/\{\{(\w+)\}\}/g, (_, k) => params[k] !== undefined ? params[k] : `{${k}}`);
}

/**
 * 批量翻译（用于获取对象中所有字符串）
 */
function translateObj(locale, obj) {
  const result = {};
  for (const [k, v] of Object.entries(obj)) {
    result[k] = typeof v === 'string' ? t(locale, v) : v;
  }
  return result;
}

module.exports = {
  SUPPORTED,
  LANG_NAMES,
  detectLocale,
  t,
  translateObj,
  load
};
