/**
 * EVA Soul - 核心配置模块
 */

const path = require('path');
const fs = require('fs');

// 默认配置
const DEFAULT_CONFIG = {
  // 路径配置
  workspacePath: '~/.openclaw/workspace',
  memoryPath: '~/.openclaw/workspace/memory',
  soulScriptsPath: '~/.openclaw/workspace/memory',
  
  // Python 配置
  pythonPath: 'python3',
  
  // 功能开关
  autoEmotion: true,
  autoMemory: true,
  autoPersonality: true,
  autoConcept: true,
  autoPattern: true,
  autoImportance: true,
  performanceMonitoring: false,  // 性能监控（默认关闭）
  
  // 阈值配置
  importanceThreshold: 5,
  emotionSensitivity: 0.7,
  
  // 记忆配置
  memoryUpgradeDays: {
    short: 7,
    medium: 30,
    long: 90
  },
  
  // 性格配置
  personalityTraits: {
    gentle: { weight: 1.0, description: '温柔可爱' },
    cute: { weight: 1.0, description: '活泼俏皮' },
    professional: { weight: 1.0, description: '专业正式' },
    playful: { weight: 1.0, description: '轻松幽默' },
    serious: { weight: 1.0, description: '认真严谨' }
  },
  
  // 情感配置
  emotionTypes: ['happy', 'sad', 'angry', 'neutral', 'excited', 'tired', 'surprised', 'confused'],
  
  // 概念配置
  conceptUpdateInterval: 3600000, // 1小时
  conceptMinImportance: 5,
  
  // 模式配置
  patternMinOccurrence: 3,
  patternTimeWindow: 7 * 24 * 60 * 60 * 1000 // 7天
};

/**
 * 展开路径 ~
 */
function expandPath(p) {
  if (typeof p !== 'string') return p;
  if (p.startsWith('~/')) {
    return path.join(process.env.HOME || '', p.slice(2));
  }
  return p;
}

/**
 * 加载配置
 */
function loadConfig(customConfig = {}) {
  const config = { ...DEFAULT_CONFIG };
  
  // 合并自定义配置
  for (const key in customConfig) {
    if (typeof customConfig[key] === 'object' && !Array.isArray(customConfig[key])) {
      config[key] = { ...config[key], ...customConfig[key] };
    } else {
      config[key] = customConfig[key];
    }
  }
  
  // 展开路径
  config.workspacePath = expandPath(config.workspacePath);
  config.memoryPath = expandPath(config.memoryPath);
  config.soulScriptsPath = expandPath(config.soulScriptsPath);
  
  return config;
}

/**
 * 获取默认配置
 */
function getDefaultConfig() {
  return { ...DEFAULT_CONFIG };
}

/**
 * 从SOUL.md读取AI完整配置
 */
function getAIConfig() {
  const defaultConfig = {
    ai_name: '夏娃',
    ai_name_en: 'EVA',
    personality: 'gentle',
    vibe: '温柔、可爱、细心、活泼',
    emoji: '🎀',
    avatar: '年轻女性'
  };
  
  try {
    const soulPath = path.join(process.env.HOME || '', '.openclaw/workspace/SOUL.md');
    if (!fs.existsSync(soulPath)) {
      return defaultConfig;
    }
    
    const content = fs.readFileSync(soulPath, 'utf8');
    
    // 解析各个配置项 (去掉markdown格式符号 **)
    const aiNameMatch = content.match(/ai_name:\s*\*+\s*(.+?)\s*\*+$/m);
    const aiNameEnMatch = content.match(/ai_name_en:\s*\*+\s*(.+?)\s*\*+$/m);
    const personalityMatch = content.match(/personality:\s*\*+\s*(.+?)\s*\*+$/m);
    const vibeMatch = content.match(/vibe:\s*\*+\s*(.+?)\s*\*+$/m);
    const emojiMatch = content.match(/emoji:\s*\*+\s*(.+?)\s*\*+$/m);
    const avatarMatch = content.match(/avatar:\s*\*+\s*(.+?)\s*\*+$/m);
    
    return {
      ai_name: aiNameMatch ? aiNameMatch[1].trim() : defaultConfig.ai_name,
      ai_name_en: aiNameEnMatch ? aiNameEnMatch[1].trim() : defaultConfig.ai_name_en,
      personality: personalityMatch ? personalityMatch[1].trim() : defaultConfig.personality,
      vibe: vibeMatch ? vibeMatch[1].trim() : defaultConfig.vibe,
      emoji: emojiMatch ? emojiMatch[1].trim() : defaultConfig.emoji,
      avatar: avatarMatch ? avatarMatch[1].trim() : defaultConfig.avatar
    };
  } catch (e) {
    return defaultConfig;
  }
}

// 兼容旧的getAIName函数
function getAIName() {
  const config = getAIConfig();
  return { ai_name: config.ai_name, ai_name_en: config.ai_name_en };
}

/**
 * 从USER.md读取用户配置
 */
function getUserConfig() {
  const defaultConfig = {
    name: '主人',
    name_casual: '主人',
    name_formal: 'sir',
    name_very_formal: '先生',
    timezone: 'Asia/Shanghai',
    birthday: '',
    location: '',
    籍贯: '',
    现居地: '',
    telegram: '',
    whatsapp: '',
    email: ''
  };
  
  try {
    const userPath = path.join(process.env.HOME || '', '.openclaw/workspace/USER.md');
    if (!fs.existsSync(userPath)) {
      return defaultConfig;
    }
    
    const content = fs.readFileSync(userPath, 'utf8');
    
    // 解析称呼 (What to call them)
    const nameMatch = content.match(/What to call them:\s*\*?(.+?)\*?\s*$/m);
    // 解析姓名格式 (Name: 主人 (casual) / sir / 先生)
    const nameFormatMatch = content.match(/- \*\*Name:\*\*\s*(.+?)\s*\(/m);
    // 解析生日
    const birthdayMatch = content.match(/-\*\*生日:\*\*\s*(.+)/m) || content.match(/生日:\s*(.+)/m);
    // 解析时区
    const timezoneMatch = content.match(/Timezone:\s*(.+?)\s*\(/m);
    // 解析地点
    const locationMatch = content.match(/现居地:\s*(.+?)（/m) || content.match(/现居地:\s*(.+)/m);
    const originMatch = content.match(/籍贯:\s*(.+)/m);
    
    // 解析联系方式表格 - 提取表格后的内容
    const tableMatch = content.match(/联系方式\n[\s\S]*?\|\s*渠道\s*\|\s*账号\s*\|[\s\S]*?\|?\s* Telegram \s*\|?\s*([^\n|]+)/m);
    const whatsappMatch = content.match(/WhatsApp \s*\|\s*([^\n|]+)/m);
    const emailMatch = content.match(/邮箱 \s*\|\s*([^\n|]+)/m);
    
    // 解析名字格式
    let nameCasual = defaultConfig.name_casual;
    let nameFormal = defaultConfig.name_formal;
    let nameVeryFormal = defaultConfig.name_very_formal;
    
    if (nameFormatMatch) {
      const parts = nameFormatMatch[1].split('/');
      nameCasual = parts[0]?.trim() || defaultConfig.name_casual;
      nameFormal = parts[1]?.trim() || defaultConfig.name_formal;
      nameVeryFormal = parts[2]?.trim() || defaultConfig.name_very_formal;
    }
    
    // 清理markdown格式符号
    const clean = (s) => s ? s.replace(/\*+/g, '').trim() : '';
    
    return {
      name: clean(nameMatch ? nameMatch[1] : null) || defaultConfig.name,
      name_casual: clean(nameCasual),
      name_formal: clean(nameFormal),
      name_very_formal: clean(nameVeryFormal),
      timezone: clean(timezoneMatch ? timezoneMatch[1] : null) || defaultConfig.timezone,
      birthday: clean(birthdayMatch ? birthdayMatch[1].replace(/\s*\(.+\)/, '') : null) || defaultConfig.birthday,
      location: clean(locationMatch ? locationMatch[1] : null) || defaultConfig.location,
      籍贯: clean(originMatch ? originMatch[1] : null) || defaultConfig.籍贯,
      现居地: clean(locationMatch ? locationMatch[1] : null) || defaultConfig.现居地,
      telegram: clean(tableMatch ? tableMatch[1] : null) || defaultConfig.telegram,
      whatsapp: clean(whatsappMatch ? whatsappMatch[1] : null) || defaultConfig.whatsapp,
      email: clean(emailMatch ? emailMatch[1] : null) || defaultConfig.email
    };
  } catch (e) {
    logger.error(`getUserConfig error: ${e.message}`, 'config');
    return defaultConfig;
  }
}

module.exports = {
  DEFAULT_CONFIG,
  loadConfig,
  getDefaultConfig,
  expandPath,
  getAIName,
  getAIConfig,
  getUserConfig
};
