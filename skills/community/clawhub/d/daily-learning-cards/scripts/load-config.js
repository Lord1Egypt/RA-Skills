#!/usr/bin/env node
/**
 * 配置加载器
 * 支持默认配置和用户自定义配置
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 默认配置
const DEFAULT_CONFIG = {
  // 提取设置
  extract: {
    maxTopics: 5,
    maxPitfalls: 3,
    maxConcepts: 3,
    maxInsights: 3,
    minInsightLength: 10
  },
  
  // 摘要设置
  summary: {
    includeTopics: true,
    includeDecisions: true,
    includePitfalls: true,
    includeConcepts: true,
    includeInsights: true,
    emojiStyle: 'unicode'  // 'unicode' 或 'text'
  },
  
  // 时间设置
  schedule: {
    hour: 10,
    minute: 30,
    timezone: 'Asia/Shanghai'
  },
  
  // 渠道设置
  channels: {
    sources: ['feishu', 'webui'],
    delivery: 'feishu'
  },
  
  // 语言设置
  language: 'zh'  // 'zh', 'en', 'bilingual'
};

// 路径
const SKILL_DIR = path.dirname(path.dirname(__filename));
const USER_CONFIG_DIR = path.join(os.homedir(), '.daily-learning-cards');
const USER_CONFIG_FILE = path.join(USER_CONFIG_DIR, 'config.json');

// 加载配置
function loadConfig() {
  let userConfig = {};
  
  // 尝试加载用户配置
  if (fs.existsSync(USER_CONFIG_FILE)) {
    try {
      userConfig = JSON.parse(fs.readFileSync(USER_CONFIG_FILE, 'utf-8'));
      console.error(`✅ 已加载用户配置: ${USER_CONFIG_FILE}`);
    } catch (e) {
      console.error(`⚠️ 用户配置加载失败: ${e.message}`);
    }
  } else {
    console.error(`ℹ️ 使用默认配置（无用户配置）`);
  }
  
  // 合并配置
  const config = {
    ...DEFAULT_CONFIG,
    ...userConfig,
    // 深度合并嵌套对象
    extract: { ...DEFAULT_CONFIG.extract, ...(userConfig.extract || {}) },
    summary: { ...DEFAULT_CONFIG.summary, ...(userConfig.summary || {}) },
    schedule: { ...DEFAULT_CONFIG.schedule, ...(userConfig.schedule || {}) },
    channels: { ...DEFAULT_CONFIG.channels, ...(userConfig.channels || {}) }
  };
  
  return config;
}

// 保存默认配置到用户目录
function initUserConfig() {
  if (!fs.existsSync(USER_CONFIG_DIR)) {
    fs.mkdirSync(USER_CONFIG_DIR, { recursive: true });
  }
  
  if (!fs.existsSync(USER_CONFIG_FILE)) {
    fs.writeFileSync(USER_CONFIG_FILE, JSON.stringify(DEFAULT_CONFIG, null, 2), 'utf-8');
    console.error(`✅ 默认配置已生成: ${USER_CONFIG_FILE}`);
    console.error(``);
    console.error(`请编辑该文件修改以下设置：`);
    console.error(`  • channels.sources — 对话渠道（默认: feishu, webui）`);
    console.error(`  • channels.delivery — 推送渠道（默认: feishu）`);
    console.error(`  • schedule.hour / minute — 定时时间（默认: 10:30）`);
    console.error(`  • feishu.target — 飞书推送目标（群/私聊 ID）`);
  } else {
    console.error(`ℹ️ 配置已存在: ${USER_CONFIG_FILE}`);
    console.error(`如需修改，直接编辑该文件。`);
  }
}

// 主函数
function main() {
  const command = process.argv[2];
  
  if (command === 'init') {
    initUserConfig();
  } else {
    const config = loadConfig();
    console.log(JSON.stringify(config, null, 2));
  }
}

main();
