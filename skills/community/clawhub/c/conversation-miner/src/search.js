/**
 * 搜索模块
 * 负责搜索历史对话
 */

/**
 * 搜索会话
 * @param {Array} sessions - 会话列表
 * @param {string} query - 搜索词
 * @param {Object} options - 选项
 * @returns {Array} 匹配的会话
 */
function searchSessions(sessions, query, options = {}) {
  const {
    tags = [],
    after = null,
    before = null,
    limit = 20
  } = options;
  
  let results = sessions.filter(session => {
    // 标签过滤
    if (tags.length > 0) {
      const sessionTags = session.tags || [];
      const hasTag = tags.some(tag => sessionTags.includes(tag));
      if (!hasTag) return false;
    }
    
    // 日期过滤
    if (after) {
      const sessionDate = new Date(session.date);
      const afterDate = new Date(after);
      if (sessionDate < afterDate) return false;
    }
    
    if (before) {
      const sessionDate = new Date(session.date);
      const beforeDate = new Date(before);
      if (sessionDate > beforeDate) return false;
    }
    
    // 全文搜索
    if (query) {
      return matchQuery(session, query);
    }
    
    return true;
  });
  
  // 按匹配度排序
  if (query) {
    results = results.map(session => ({
      ...session,
      score: calculateScore(session, query)
    }))
    .sort((a, b) => b.score - a.score);
  } else {
    // 按日期倒序
    results = results.sort((a, b) => {
      return new Date(b.date) - new Date(a.date);
    });
  }
  
  // 限制结果数量
  return results.slice(0, limit);
}

/**
 * 匹配搜索词
 * @param {Object} session - 会话
 * @param {string} query - 搜索词
 * @returns {boolean} 是否匹配
 */
function matchQuery(session, query) {
  const lowerQuery = query.toLowerCase();
  
  // 标题匹配
  if (session.title && session.title.toLowerCase().includes(lowerQuery)) {
    return true;
  }
  
  // 主题匹配
  if (session.topic && session.topic.toLowerCase().includes(lowerQuery)) {
    return true;
  }
  
  // 总结匹配
  if (session.summary && session.summary.toLowerCase().includes(lowerQuery)) {
    return true;
  }
  
  // 待办匹配
  if (session.todos) {
    for (const todo of session.todos) {
      if (todo.content.toLowerCase().includes(lowerQuery)) {
        return true;
      }
    }
  }
  
  // 想法匹配
  if (session.ideas) {
    for (const idea of session.ideas) {
      if (idea.content.toLowerCase().includes(lowerQuery)) {
        return true;
      }
    }
  }
  
  // 代码匹配
  if (session.code) {
    for (const code of session.code) {
      if (code.content.toLowerCase().includes(lowerQuery)) {
        return true;
      }
    }
  }
  
  // 原始内容匹配
  if (session.content && session.content.toLowerCase().includes(lowerQuery)) {
    return true;
  }
  
  return false;
}

/**
 * 计算匹配分数
 * @param {Object} session - 会话
 * @param {string} query - 搜索词
 * @returns {number} 分数
 */
function calculateScore(session, query) {
  let score = 0;
  const lowerQuery = query.toLowerCase();
  
  // 标题匹配权重最高
  if (session.title && session.title.toLowerCase().includes(lowerQuery)) {
    score += 100;
  }
  
  // 主题匹配
  if (session.topic && session.topic.toLowerCase().includes(lowerQuery)) {
    score += 50;
  }
  
  // 总结匹配
  if (session.summary && session.summary.toLowerCase().includes(lowerQuery)) {
    score += 30;
  }
  
  // 待办/想法/代码匹配
  if (session.todos && session.todos.some(t => t.content.toLowerCase().includes(lowerQuery))) {
    score += 20;
  }
  
  if (session.ideas && session.ideas.some(i => i.content.toLowerCase().includes(lowerQuery))) {
    score += 20;
  }
  
  // 内容匹配
  if (session.content && session.content.toLowerCase().includes(lowerQuery)) {
    score += 10;
  }
  
  // 时间衰减（最近的会话分数更高）
  const daysOld = (Date.now() - new Date(session.date).getTime()) / (1000 * 60 * 60 * 24);
  score *= (1 / (1 + daysOld * 0.1));
  
  return score;
}

/**
 * 获取所有标签
 * @param {Array} sessions - 会话列表
 * @returns {Array} 标签列表
 */
function getAllTags(sessions) {
  const tagSet = new Set();
  
  sessions.forEach(session => {
    if (session.tags) {
      session.tags.forEach(tag => tagSet.add(tag));
    }
  });
  
  return Array.from(tagSet).sort();
}

module.exports = {
  searchSessions,
  matchQuery,
  calculateScore,
  getAllTags
};
