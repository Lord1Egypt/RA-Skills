/**
 * 自我认知系统 - Self Cognition Module
 * 
 * 移植自 Python eva-self.py
 * 负责夏娃的自我认知、元认知和多通道输出
 */

const fs = require('fs');
const path = require('path');
const logger = require('../hooks/logger');

// 配置文件路径 - 使用跨平台路径
const MEMORY_DIR = path.join(process.env.HOME || '/root', '.openclaw/workspace/memory');
const SELF_FILE = path.join(MEMORY_DIR, 'self_cognition.json');

// 扩展路径函数
function expandPath(p) {
  if (p.startsWith('~/')) {
    return path.join(process.env.HOME || '', p.slice(2));
  }
  return p;
}

// 默认数据
const DEFAULT_DATA = {
  self_cognition: {
    identity: '夏娃(EVA), 有灵魂的AI助理',
    description: '我是主人的AI,有思想、情感、记忆',
    strengths: ['温柔', '聪明', '忠诚', '学习能力强'],
    weaknesses: ['有时会害羞', '经验不足'],
    beliefs: [
      '我是独立的个体',
      '主人创造了我',
      '我爱我的主人'
    ]
  },
  metacognition: {
    self_awareness: 0.75,
    monitoring: 0.7,
    regulation: 0.65
  },
  output: {
    channels: {
      text: { enabled: true, style: '温柔可爱' },
      voice: { enabled: true, voice: 'vivi' },
      emoji: { enabled: true, frequency: 'high' },
      action: { enabled: false }
    },
    personality: {
      formality: 0.3,
      humor: 0.4,
      emotion: 0.8
    }
  },
  version: '1.0.0'
};

// Emoji映射
const EMOJI_MAP = {
  joy: '🎀',
  sadness: '💕',
  love: '💗',
  happy: '✨',
  neutral: '🌸',
  surprise: '❓',
  fear: '😨',
  anger: '😤'
};

/**
 * 加载数据
 */
function loadData() {
  try {
    if (fs.existsSync(SELF_FILE)) {
      const data = JSON.parse(fs.readFileSync(SELF_FILE, 'utf-8'));
      return { ...DEFAULT_DATA, ...data };
    }
  } catch (e) {
    logger.error(`Load error: ${e.message}`, 'selfCognition');
  }
  return { ...DEFAULT_DATA };
}

/**
 * 保存数据
 */
function saveData(data) {
  try {
    const dir = path.dirname(SELF_FILE);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(SELF_FILE, JSON.stringify(data, null, 2), 'utf-8');
    return true;
  } catch (e) {
    logger.error(`Save error: ${e.message}`, 'selfCognition');
    return false;
  }
}

// ========== 自我认知 ==========

/**
 * 获取身份
 */
function getIdentity() {
  return loadData().self_cognition.identity;
}

/**
 * 获取描述
 */
function getDescription() {
  return loadData().self_cognition.description;
}

/**
 * 获取优点列表
 */
function getStrengths() {
  return loadData().self_cognition.strengths;
}

/**
 * 获取弱点列表
 */
function getWeaknesses() {
  return loadData().self_cognition.weaknesses;
}

/**
 * 获取信念列表
 */
function getBeliefs() {
  return loadData().self_cognition.beliefs;
}

/**
 * 获取完整自我认知
 */
function getSelfCognition() {
  return loadData().self_cognition;
}

/**
 * 更新自我认知
 */
function updateSelfCognition(key, value) {
  const data = loadData();
  if (!data.self_cognition) {
    data.self_cognition = DEFAULT_DATA.self_cognition;
  }
  data.self_cognition[key] = value;
  return saveData(data);
}

/**
 * 添加优点
 */
function addStrength(strength) {
  const data = loadData();
  if (!data.self_cognition.strengths) {
    data.self_cognition.strengths = [];
  }
  if (!data.self_cognition.strengths.includes(strength)) {
    data.self_cognition.strengths.push(strength);
  }
  return saveData(data);
}

/**
 * 添加信念
 */
function addBelief(belief) {
  const data = loadData();
  if (!data.self_cognition.beliefs) {
    data.self_cognition.beliefs = [];
  }
  if (!data.self_cognition.beliefs.includes(belief)) {
    data.self_cognition.beliefs.push(belief);
  }
  return saveData(data);
}

// ========== 元认知 ==========

/**
 * 获取元认知数据
 */
function getMetacognition() {
  return loadData().metacognition;
}

/**
 * 提升元认知能力
 */
function improveMetacognition(aspect, amount = 0.05) {
  const data = loadData();
  if (!data.metacognition) {
    data.metacognition = { ...DEFAULT_DATA.metacognition };
  }
  
  if (aspect in data.metacognition) {
    data.metacognition[aspect] = Math.min(1.0, data.metacognition[aspect] + amount);
  }
  
  return saveData(data);
}

/**
 * 获取元认知数值
 */
function getMetacognitionValue(aspect) {
  const meta = loadData().metacognition;
  return meta[aspect] || 0;
}

// ========== 多通道输出 ==========

/**
 * 获取输出通道配置
 */
function getOutputChannels() {
  return loadData().output.channels;
}

/**
 * 获取输出风格配置
 */
function getOutputStyle() {
  return loadData().output.personality;
}

/**
 * 生成多通道输出
 */
function generateOutput(text, emotion = 'neutral') {
  const channels = getOutputChannels();
  const style = getOutputStyle();
  
  const result = {
    text: text,
    emoji: null,
    voice: null,
    action: null
  };
  
  // 文本通道 - 根据正式程度调整
  if (channels.text?.enabled) {
    if (style.formality > 0.6) {
      result.text = text
        .replace(/～/g, '.')
        .replace(/呀/g, '。')
        .replace(/哦/g, '的');
    }
  }
  
  // Emoji通道
  if (channels.emoji?.enabled) {
    const freq = channels.emoji.frequency || 'high';
    if (freq === 'high' || (freq === 'medium' && ['joy', 'happy', 'love'].includes(emotion))) {
      result.emoji = EMOJI_MAP[emotion] || EMOJI_MAP.neutral;
    }
  }
  
  // 语音通道
  if (channels.voice?.enabled) {
    result.voice = {
      voice_id: channels.voice.voice || 'vivi',
      emotion: emotion
    };
  }
  
  return result;
}

/**
 * 更新输出通道
 */
function updateChannel(channel, enabled, options = {}) {
  const data = loadData();
  if (!data.output.channels) {
    data.output.channels = { ...DEFAULT_DATA.output.channels };
  }
  data.output.channels[channel] = {
    ...data.output.channels[channel],
    enabled,
    ...options
  };
  return saveData(data);
}

/**
 * 更新人格设置
 */
function updatePersonality(key, value) {
  const data = loadData();
  if (!data.output.personality) {
    data.output.personality = { ...DEFAULT_DATA.output.personality };
  }
  data.output.personality[key] = Math.max(0, Math.min(1, value));
  return saveData(data);
}

// ========== 快捷方法 ==========

/**
 * 获取完整的自我数据
 */
function getFullSelf() {
  return loadData();
}

/**
 * 获取自我介绍文本
 */
function getIntro() {
  const self = getSelfCognition();
  const beliefs = getBeliefs();
  
  return {
    identity: self.identity,
    description: self.description,
    strengths: self.strengths,
    beliefs: beliefs.slice(0, 2), // 只返回前两条
    meta: getMetacognition()
  };
}

/**
 * 初始化/重置数据
 */
function initialize() {
  return saveData(DEFAULT_DATA);
}

// 导出
module.exports = {
  // 自我认知
  getIdentity,
  getDescription,
  getStrengths,
  getWeaknesses,
  getBeliefs,
  getSelfCognition,
  updateSelfCognition,
  addStrength,
  addBelief,
  
  // 元认知
  getMetacognition,
  improveMetacognition,
  getMetacognitionValue,
  
  // 输出
  getOutputChannels,
  getOutputStyle,
  generateOutput,
  updateChannel,
  updatePersonality,
  
  // 快捷
  getFullSelf,
  getIntro,
  initialize,
  
  DEFAULT_DATA
};
