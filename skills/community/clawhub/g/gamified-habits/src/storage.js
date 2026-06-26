/**
 * 数据存储模块
 * 负责用户数据的读写和持久化
 * 
 * 多用户支持：每个用户独立数据文件
 * 数据路径：~/.openclaw/skills/gamified-habits/data/{user_id}.json
 */

const fs = require('fs');
const path = require('path');

// 技能目录
const SKILL_DIR = path.join(process.env.HOME, '.openclaw', 'skills', 'gamified-habits');
// 数据目录
const DATA_DIR = path.join(SKILL_DIR, 'data');

/**
 * 获取当前用户 ID
 * 优先级：命令行参数 > OpenClaw Context > 环境变量 > 默认值
 */
function getUserId() {
  // 1. 命令行参数优先
  const args = process.argv.slice(2);
  const userArg = args.find(arg => arg.startsWith('--user='));
  if (userArg) {
    return userArg.split('=')[1];
  }
  
  // 2. OpenClaw Context（渠道 + 用户 ID）
  const channel = process.env.OPENCLAW_CHANNEL || process.env.CHANNEL;
  const accountId = process.env.OPENCLAW_ACCOUNT_ID || process.env.ACCOUNT_ID;
  if (channel && accountId) {
    return `${channel}-${accountId}`;
  }
  
  // 3. 环境变量
  if (process.env.GAMIFIED_HABITS_USER) {
    return process.env.GAMIFIED_HABITS_USER;
  }
  
  // 4. 默认值
  return 'default';
}

/**
 * 获取当前用户 ID（用于显示）
 */
function getUserIdDisplay() {
  const userId = getUserId();
  const parts = userId.split('-');
  if (parts.length >= 2) {
    return {
      channel: parts[0],
      accountId: parts.slice(1).join('-'),
      full: userId
    };
  }
  return {
    channel: 'unknown',
    accountId: userId,
    full: userId
  };
}

// 当前用户的数据路径
const DATA_PATH = path.join(DATA_DIR, `${getUserId()}.json`);

/**
 * 初始化默认数据结构
 */
function getDefaultData() {
  return {
    user: {
      level: 1,
      xp: 0,
      xpToNext: 100,
      attributes: {
        physical: 0,    // 体力
        intellectual: 0, // 智力
        wealth: 0,      // 财富
        spiritual: 0,   // 心灵
        social: 0       // 社交
      }
    },
    habits: [],
    achievements: [],
    checkinHistory: []
  };
}

/**
 * 加载用户数据
 */
function loadData() {
  // 尝试迁移旧数据
  migrateOldData();
  
  try {
    if (fs.existsSync(DATA_PATH)) {
      const data = fs.readFileSync(DATA_PATH, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.error('读取数据失败:', error.message);
  }
  
  // 返回默认数据并保存
  const defaultData = getDefaultData();
  saveData(defaultData);
  return defaultData;
}

/**
 * 保存用户数据
 */
function saveData(data) {
  try {
    // 确保数据目录存在
    if (!fs.existsSync(DATA_DIR)) {
      fs.mkdirSync(DATA_DIR, { recursive: true });
    }
    fs.writeFileSync(DATA_PATH, JSON.stringify(data, null, 2), 'utf8');
    return true;
  } catch (error) {
    console.error('保存数据失败:', error.message);
    return false;
  }
}

/**
 * 生成唯一 ID
 */
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

/**
 * 获取当前日期字符串
 */
function getTodayStr() {
  return new Date().toISOString().split('T')[0];
}

/**
 * 检查是否首次使用
 */
function isFirstTime() {
  return !fs.existsSync(DATA_PATH);
}

/**
 * 迁移旧数据（从 ~/.gamified-habits/user-data.json 到新位置）
 */
function migrateOldData() {
  const oldPath = path.join(process.env.HOME, '.gamified-habits', 'user-data.json');
  if (fs.existsSync(oldPath) && !fs.existsSync(DATA_PATH)) {
    try {
      const oldData = JSON.parse(fs.readFileSync(oldPath, 'utf8'));
      // 确保数据目录存在
      if (!fs.existsSync(DATA_DIR)) {
        fs.mkdirSync(DATA_DIR, { recursive: true });
      }
      // 复制数据到新位置
      fs.writeFileSync(DATA_PATH, JSON.stringify(oldData, null, 2), 'utf8');
      console.log(`✅ 数据已迁移到：${DATA_PATH}`);
      // 备份旧数据（重命名）
      fs.renameSync(oldPath, oldPath + '.bak');
      console.log(`📦 旧数据已备份到：${oldPath}.bak`);
    } catch (error) {
      console.error('迁移数据失败:', error.message);
    }
  }
}

module.exports = {
  loadData,
  saveData,
  getDefaultData,
  generateId,
  getTodayStr,
  getUserId,
  getUserIdDisplay,
  migrateOldData,
  isFirstTime,
  DATA_PATH,
  DATA_DIR
};
