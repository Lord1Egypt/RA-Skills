#!/usr/bin/env node
/**
 * Decision Recorder - 决策记录器
 * 核心功能模块
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

// 决策存储目录
const DECISION_DIR = path.join(os.homedir(), '.decision-recorder');

// 决策关键词
const DECISION_KEYWORDS = [
  '决定', '选择', '采用', '选用', '选定', '确定', '选定', '采纳',
  'decide', 'choose', 'select', 'adopt', 'determine', 'opt'
];

/**
 * 初始化存储目录
 */
function initStorage() {
  if (!fs.existsSync(DECISION_DIR)) {
    fs.mkdirSync(DECISION_DIR, { recursive: true });
  }
}

/**
 * 生成唯一ID
 */
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2, 5);
}

/**
 * 获取当前时间戳
 */
function getTimestamp() {
  return new Date().toISOString();
}

/**
 * 检测决策关键词
 * @param {string} text - 要检测的文本
 * @returns {boolean} - 是否包含决策关键词
 */
function detectDecisionKeywords(text) {
  if (!text) return false;
  const lowerText = text.toLowerCase();
  return DECISION_KEYWORDS.some(keyword => 
    lowerText.includes(keyword.toLowerCase())
  );
}

/**
 * 创建决策记录
 * @param {Object} decision - 决策对象
 * @returns {Object} - 保存的决策记录
 */
function createDecision(decision) {
  initStorage();
  
  const record = {
    id: generateId(),
    timestamp: getTimestamp(),
    question: decision.question || '',
    options: decision.options || [],
    reasoning: decision.reasoning || '',
    result: decision.result || '',
    context: decision.context || '',
    tags: decision.tags || []
  };

  const filePath = path.join(DECISION_DIR, `${record.id}.json`);
  fs.writeFileSync(filePath, JSON.stringify(record, null, 2), 'utf8');
  
  return record;
}

/**
 * 列出所有决策记录
 * @param {Object} filters - 过滤条件
 * @returns {Array} - 决策记录列表
 */
function listDecisions(filters = {}) {
  initStorage();
  
  const files = fs.readdirSync(DECISION_DIR)
    .filter(f => f.endsWith('.json'))
    .map(f => {
      const filePath = path.join(DECISION_DIR, f);
      const content = fs.readFileSync(filePath, 'utf8');
      return JSON.parse(content);
    })
    .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

  // 应用过滤器
  let results = files;
  
  if (filters.tag) {
    results = results.filter(d => d.tags && d.tags.includes(filters.tag));
  }
  
  if (filters.keyword) {
    const kw = filters.keyword.toLowerCase();
    results = results.filter(d => 
      (d.question && d.question.toLowerCase().includes(kw)) ||
      (d.reasoning && d.reasoning.toLowerCase().includes(kw)) ||
      (d.result && d.result.toLowerCase().includes(kw))
    );
  }
  
  if (filters.dateFrom) {
    const fromDate = new Date(filters.dateFrom);
    results = results.filter(d => new Date(d.timestamp) >= fromDate);
  }
  
  if (filters.dateTo) {
    const toDate = new Date(filters.dateTo);
    results = results.filter(d => new Date(d.timestamp) <= toDate);
  }
  
  return results;
}

/**
 * 搜索决策记录
 * @param {string} query - 搜索关键词
 * @returns {Array} - 匹配的决策记录
 */
function searchDecisions(query) {
  if (!query) return [];
  return listDecisions({ keyword: query });
}

/**
 * 获取单个决策详情
 * @param {string} id - 决策ID
 * @returns {Object|null} - 决策记录
 */
function getDecision(id) {
  const filePath = path.join(DECISION_DIR, `${id}.json`);
  if (!fs.existsSync(filePath)) return null;
  
  const content = fs.readFileSync(filePath, 'utf8');
  return JSON.parse(content);
}

/**
 * 分析决策模式
 * @returns {Object} - 分析报告
 */
function analyzeDecisions() {
  const decisions = listDecisions();
  
  if (decisions.length === 0) {
    return {
      total: 0,
      message: '暂无决策记录'
    };
  }

  // 时间分布
  const timeDistribution = {};
  decisions.forEach(d => {
    const date = d.timestamp.split('T')[0];
    timeDistribution[date] = (timeDistribution[date] || 0) + 1;
  });

  // 标签统计
  const tagStats = {};
  decisions.forEach(d => {
    if (d.tags) {
      d.tags.forEach(tag => {
        tagStats[tag] = (tagStats[tag] || 0) + 1;
      });
    }
  });

  // 高频关键词
  const keywordFreq = {};
  decisions.forEach(d => {
    const text = `${d.question} ${d.reasoning} ${d.result}`.toLowerCase();
    const words = text.match(/[\u4e00-\u9fa5]+|[a-zA-Z]+/g) || [];
    words.forEach(word => {
      if (word.length > 1) {
        keywordFreq[word] = (keywordFreq[word] || 0) + 1;
      }
    });
  });

  const topKeywords = Object.entries(keywordFreq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  // 决策频率趋势
  const dates = Object.keys(timeDistribution).sort();
  const trend = dates.map(date => ({
    date,
    count: timeDistribution[date]
  }));

  return {
    total: decisions.length,
    timeDistribution,
    tagStats,
    topKeywords,
    trend,
    firstDecision: decisions[decisions.length - 1].timestamp,
    latestDecision: decisions[0].timestamp
  };
}

/**
 * 删除决策记录
 * @param {string} id - 决策ID
 * @returns {boolean} - 是否成功
 */
function deleteDecision(id) {
  const filePath = path.join(DECISION_DIR, `${id}.json`);
  if (!fs.existsSync(filePath)) return false;
  
  fs.unlinkSync(filePath);
  return true;
}

/**
 * 更新决策记录
 * @param {string} id - 决策ID
 * @param {Object} updates - 更新内容
 * @returns {Object|null} - 更新后的记录
 */
function updateDecision(id, updates) {
  const decision = getDecision(id);
  if (!decision) return null;
  
  const updated = { ...decision, ...updates, id, timestamp: decision.timestamp };
  const filePath = path.join(DECISION_DIR, `${id}.json`);
  fs.writeFileSync(filePath, JSON.stringify(updated, null, 2), 'utf8');
  
  return updated;
}

// 导出模块
module.exports = {
  DECISION_KEYWORDS,
  detectDecisionKeywords,
  createDecision,
  listDecisions,
  searchDecisions,
  getDecision,
  analyzeDecisions,
  deleteDecision,
  updateDecision,
  initStorage,
  DECISION_DIR
};

// CLI 入口
if (require.main === module) {
  const { runCLI } = require('./cli');
  runCLI();
}
