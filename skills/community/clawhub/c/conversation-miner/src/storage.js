/**
 * 数据存储模块
 * 负责本地 JSON 文件的读写操作
 */

const fs = require('fs');
const path = require('path');

// 数据目录
const DATA_DIR = process.env.MINER_DATA_DIR || path.join(process.env.HOME || '', '.conversation-miner', 'data');

/**
 * 初始化数据目录
 */
function initDataDir() {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
}

/**
 * 获取数据文件路径
 * @param {string} userId - 用户 ID
 * @returns {string} 数据文件路径
 */
function getDataFilePath(userId) {
  return path.join(DATA_DIR, `${userId || 'default'}.json`);
}

/**
 * 加载用户数据
 * @param {string} userId - 用户 ID
 * @returns {Object} 用户数据
 */
function loadUserData(userId) {
  initDataDir();
  const filePath = getDataFilePath(userId);
  
  if (!fs.existsSync(filePath)) {
    return {
      sessions: [],
      tags: []
    };
  }
  
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(content);
  } catch (error) {
    console.error('加载数据失败:', error.message);
    return {
      sessions: [],
      tags: []
    };
  }
}

/**
 * 保存用户数据
 * @param {string} userId - 用户 ID
 * @param {Object} data - 用户数据
 */
function saveUserData(userId, data) {
  initDataDir();
  const filePath = getDataFilePath(userId);
  
  try {
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
  } catch (error) {
    console.error('保存数据失败:', error.message);
  }
}

/**
 * 添加会话
 * @param {string} userId - 用户 ID
 * @param {Object} session - 会话数据
 * @returns {Object} 添加后的会话
 */
function addSession(userId, session) {
  const data = loadUserData(userId);
  
  const newSession = {
    id: session.id || `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
    title: session.title || '未命名对话',
    date: session.date || new Date().toISOString().split('T')[0],
    timestamp: session.timestamp || Date.now(),
    summary: session.summary || '',
    todos: session.todos || [],
    ideas: session.ideas || [],
    decisions: session.decisions || [],
    code: session.code || [],
    tags: session.tags || [],
    favorite: session.favorite || false,
    content: session.content || ''
  };
  
  data.sessions.unshift(newSession);
  saveUserData(userId, data);
  
  return newSession;
}

/**
 * 更新会话
 * @param {string} userId - 用户 ID
 * @param {string} sessionId - 会话 ID
 * @param {Object} updates - 更新内容
 * @returns {Object|null} 更新后的会话，未找到返回 null
 */
function updateSession(userId, sessionId, updates) {
  const data = loadUserData(userId);
  const sessionIndex = data.sessions.findIndex(s => s.id === sessionId);
  
  if (sessionIndex === -1) {
    return null;
  }
  
  data.sessions[sessionIndex] = {
    ...data.sessions[sessionIndex],
    ...updates
  };
  
  saveUserData(userId, data);
  return data.sessions[sessionIndex];
}

/**
 * 获取会话列表
 * @param {string} userId - 用户 ID
 * @param {Object} options - 选项
 * @returns {Array} 会话列表
 */
function getSessions(userId, options = {}) {
  const data = loadUserData(userId);
  let sessions = [...data.sessions];
  
  // 按日期过滤
  if (options.after) {
    sessions = sessions.filter(s => s.date >= options.after);
  }
  if (options.before) {
    sessions = sessions.filter(s => s.date <= options.before);
  }
  
  // 按标签过滤
  if (options.tag) {
    sessions = sessions.filter(s => s.tags.includes(options.tag));
  }
  
  // 只获取收藏
  if (options.favorite) {
    sessions = sessions.filter(s => s.favorite);
  }
  
  // 限制数量
  if (options.limit) {
    sessions = sessions.slice(0, options.limit);
  }
  
  return sessions;
}

/**
 * 获取会话详情
 * @param {string} userId - 用户 ID
 * @param {string} sessionId - 会话 ID
 * @returns {Object|null} 会话详情
 */
function getSession(userId, sessionId) {
  const data = loadUserData(userId);
  return data.sessions.find(s => s.id === sessionId) || null;
}

/**
 * 获取最近会话
 * @param {string} userId - 用户 ID
 * @param {number} limit - 数量限制
 * @returns {Array} 最近会话列表
 */
function getRecentSessions(userId, limit = 5) {
  return getSessions(userId, { limit });
}

/**
 * 删除会话
 * @param {string} userId - 用户 ID
 * @param {string} sessionId - 会话 ID
 * @returns {boolean} 是否删除成功
 */
function deleteSession(userId, sessionId) {
  const data = loadUserData(userId);
  const initialLength = data.sessions.length;
  
  data.sessions = data.sessions.filter(s => s.id !== sessionId);
  
  if (data.sessions.length < initialLength) {
    saveUserData(userId, data);
    return true;
  }
  
  return false;
}

/**
 * 添加标签
 * @param {string} userId - 用户 ID
 * @param {Array<string>} newTags - 新标签列表
 * @returns {Array<string>} 更新后的标签列表
 */
function addTags(userId, newTags) {
  const data = loadUserData(userId);
  
  newTags.forEach(tag => {
    if (!data.tags.includes(tag)) {
      data.tags.push(tag);
    }
  });
  
  saveUserData(userId, data);
  return data.tags;
}

/**
 * 获取所有标签
 * @param {string} userId - 用户 ID
 * @returns {Array<string>} 标签列表
 */
function getTags(userId) {
  const data = loadUserData(userId);
  return data.tags;
}

/**
 * 搜索会话
 * @param {string} userId - 用户 ID
 * @param {string} query - 搜索关键词
 * @returns {Array} 匹配的会话列表
 */
function searchSessions(userId, query) {
  const data = loadUserData(userId);
  const lowerQuery = query.toLowerCase();
  
  return data.sessions.filter(session => {
    const searchText = [
      session.title,
      session.summary,
      session.content,
      ...(session.tags || [])
    ].join(' ').toLowerCase();
    
    return searchText.includes(lowerQuery);
  });
}

module.exports = {
  initDataDir,
  loadUserData,
  saveUserData,
  addSession,
  updateSession,
  getSessions,
  getSession,
  getRecentSessions,
  deleteSession,
  addTags,
  getTags,
  searchSessions,
  DATA_DIR
};
