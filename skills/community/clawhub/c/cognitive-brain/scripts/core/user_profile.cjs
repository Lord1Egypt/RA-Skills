/**
 * 用户画像模块
 * 管理用户基本信息和偏好
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('user_profile');
const fs = require('fs');
const path = require('path');

const SKILL_DIR = path.join(process.env.HOME || '/root', '.openclaw/workspace/skills/cognitive-brain');
const USER_MODEL_PATH = path.join(SKILL_DIR, '.user-model.json');

// 默认用户画像
const defaultProfile = {
  basic: {
    name: null,
    preferredName: null,
    timezone: null,
    language: 'zh-CN',
    communicationStyle: 'casual'
  },
  preferences: {
    topics: {},
    communicationTone: 'friendly',
    responseLength: 'medium',
    levelOfDetail: 'balanced',
    proactivity: 'moderate'
  }
};

let profile = { ...defaultProfile };

/**
 * 加载用户画像
 */
function loadProfile() {
  try {
    if (fs.existsSync(USER_MODEL_PATH)) {
      const data = JSON.parse(fs.readFileSync(USER_MODEL_PATH, 'utf8'));
      profile = { ...defaultProfile, ...data };
    }
  } catch (e) {
    console.error('[user_profile] 加载失败:', e.message);
  }
  return profile;
}

/**
 * 保存用户画像
 */
function saveProfile() {
  try {
    fs.writeFileSync(USER_MODEL_PATH, JSON.stringify(profile, null, 2));
  } catch (e) {
    console.error('[user_profile] 保存失败:', e.message);
  }
}

/**
 * 更新基本信息
 */
function updateBasic(info) {
  profile.basic = { ...profile.basic, ...info };
  saveProfile();
}

/**
 * 记录兴趣偏好
 */
function recordInterest(topic, delta = 0.1) {
  if (!topic) return;
  
  const current = profile.preferences.topics[topic] || 0;
  profile.preferences.topics[topic] = Math.min(1, Math.max(0, current + delta));
  saveProfile();
}

/**
 * 获取用户偏好
 */
function getPreferences() {
  return {
    ...profile.preferences,
    tone: profile.preferences.communicationTone,
    length: profile.preferences.responseLength,
    detail: profile.preferences.levelOfDetail,
    proactivity: profile.preferences.proactivity
  };
}

/**
 * 获取画像摘要
 */
function getProfileSummary() {
  const topTopics = Object.entries(profile.preferences.topics)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([t, s]) => `${t}(${(s * 100).toFixed(0)}%)`);

  return {
    name: profile.basic.preferredName || profile.basic.name || '未知用户',
    style: profile.basic.communicationStyle,
    topTopics,
    tone: profile.preferences.communicationTone,
    proactivity: profile.preferences.proactivity
  };
}

module.exports = {
  loadProfile,
  saveProfile,
  updateBasic,
  recordInterest,
  getPreferences,
  getProfileSummary,
  defaultProfile
};

