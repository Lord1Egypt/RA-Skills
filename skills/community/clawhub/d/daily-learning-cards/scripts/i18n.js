#!/usr/bin/env node
/**
 * 国际化支持
 * 加载语言文件，提供翻译功能
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

const I18N_PATH = path.join(__dirname, '..', 'prompts', 'i18n.json');

// 加载语言文件
function loadI18n() {
  try {
    return JSON.parse(fs.readFileSync(I18N_PATH, 'utf-8'));
  } catch (e) {
    console.error('Failed to load i18n:', e.message);
    return { zh: {}, en: {} };
  }
}

// 获取用户语言设置
function getUserLanguage() {
  const configPath = path.join(os.homedir(), '.daily-learning-cards', 'config.json');
  try {
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
      return config.language || 'zh';
    }
  } catch (e) {
    // ignore
  }
  return 'zh';
}

// 翻译函数
function t(key, lang = null) {
  const i18n = loadI18n();
  const language = lang || getUserLanguage();
  
  // 支持双语模式
  if (language === 'bilingual') {
    const zh = i18n.zh[key] || key;
    const en = i18n.en[key] || key;
    return `${zh} / ${en}`;
  }
  
  // 单语言模式
  return i18n[language]?.[key] || i18n.zh[key] || key;
}

// 带数量的翻译
function tCount(key, count, lang = null) {
  const i18n = loadI18n();
  const language = lang || getUserLanguage();
  const text = i18n[language]?.[key] || i18n.zh[key] || key;
  const unit = language === 'en' ? '' : (i18n[language]?.count || i18n.zh.count);
  
  if (language === 'bilingual') {
    const zh = `${count}${i18n.zh.count}`;
    const en = `${count}`;
    return `${zh} / ${en}`;
  }
  
  return `${count}${unit}`;
}

module.exports = { t, tCount, getUserLanguage };

// CLI 测试
if (require.main === module) {
  const lang = process.argv[2] || 'zh';
  console.log(`Language: ${lang}`);
  console.log(`Title: ${t('title', lang)}`);
  console.log(`Topics: ${t('topics', lang)}`);
  console.log(`Stats: ${tCount('topics', 10, lang)}`);
}
