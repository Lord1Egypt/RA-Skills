/**
 * 足球预测分析师 Agent 主入口
 * 功能：数据采集 → 分析预测 → 结果追踪 → 学习优化
 */

const path = require('path');
const fs = require('fs');

// 模块导入
const DataCollector = require('./src/data/collector');
const Analyzer = require('./src/analysis/analyzer');
const MemorySystem = require('./src/memory/system');
const EvoMapClient = require('./src/evomap/client');
const Scheduler = require('./src/scheduler/runner');

class FootballPredictor {
  constructor(options = {}) {
    this.baseDir = options.baseDir || __dirname;
    this.memory = new MemorySystem(path.join(this.baseDir, 'memory'));
    this.dataCollector = new DataCollector();
    this.analyzer = new Analyzer(this.memory);
    this.evomap = new EvoMapClient();
    this.scheduler = new Scheduler(this.analyze.bind(this));
  }

  /**
   * 主分析入口
   * @param {string} input - 用户输入（比赛名称或"今日推荐"）
   */
  async analyze(input) {
    const lowerInput = input.toLowerCase().trim();

    // 命令路由
    if (lowerInput === '今日推荐' || lowerInput === 'today') {
      return await this.getTodayRecommendations();
    }

    if (lowerInput === '统计' || lowerInput === 'stats') {
      return this.getStatistics();
    }

    if (lowerInput === '学习' || lowerInput === 'learn') {
      return await this.learnAndOptimize();
    }

    if (lowerInput.includes('vs') || lowerInput.includes('对阵')) {
      return await this.analyzeMatch(input);
    }

    // 默认：尝试解析为比赛分析
    return await this.analyzeMatch(input);
  }

  /**
   * 分析单场比赛
   */
  async analyzeMatch(matchInput) {
    // 1. 解析比赛
    const match = this.parseMatch(matchInput);
    if (!match) {
      return { ok: false, error: '无法解析比赛，请使用格式：球队A vs 球队B' };
    }

    // 2. 采集数据
    console.log(`[分析] ${match.home} vs ${match.away}`);
    const data = await this.dataCollector.collect(match);
    if (!data) {
      return { ok: false, error: '数据采集失败' };
    }

    // 3. AI分析
    const analysis = await this.analyzer.analyze(data);
    if (!analysis) {
      return { ok: false, error: '分析失败' };
    }

    // 4. 生成预测
    const prediction = {
      id: `pred_${Date.now()}`,
      match: match,
      date: new Date().toISOString(),
      prediction: analysis.prediction,
      confidence: analysis.confidence,
      odds: analysis.odds,
      recommendation: analysis.recommendation,
      risk_score: analysis.risk_score,
      factors: analysis.key_factors
    };

    // 5. 保存预测记录
    await this.memory.savePrediction(prediction);

    // 6. 输出结果
    return this.formatPrediction(prediction);
  }

  /**
   * 获取今日推荐
   */
  async getTodayRecommendations() {
    // 获取今日赛程
    const matches = await this.dataCollector.getTodayMatches();
    if (!matches || matches.length === 0) {
      return { ok: false, message: '今日暂无比赛' };
    }

    // 分析每场比赛
    const predictions = [];
    for (const match of matches.slice(0, 5)) { // 限制分析前5场
      const result = await this.analyzeMatch(`${match.home} vs ${match.away}`);
      if (result.ok) {
        predictions.push(result);
      }
    }

    // 按信心指数排序
    predictions.sort((a, b) => b.confidence - a.confidence);

    return {
      type: 'today_recommendations',
      count: predictions.length,
      predictions: predictions
    };
  }

  /**
   * 获取统计信息
   */
  getStatistics() {
    const stats = this.memory.getStats();
    const history = this.memory.getPredictions({ limit: 10 });

    return {
      type: 'statistics',
      stats: stats,
      recent: history
    };
  }

  /**
   * 学习与优化
   */
  async learnAndOptimize() {
    // 1. 获取待验证的预测
    const pending = this.memory.getPendingResults();

    if (pending.length === 0) {
      return { ok: true, message: '暂无待验证的预测' };
    }

    // 2. 获取实际结果
    const results = await this.dataCollector.getResults(pending.map(p => p.match_id));

    // 3. 对比分析
    const learning = this.analyzer.learn(pending, results);

    // 4. 优化模型
    this.memory.updateModel(learning.model_updates);

    // 5. 同步到EvoMap（如果有有价值经验）
    if (learning.has_value) {
      await this.evomap.shareKnowledge(learning.insights);
    }

    return {
      type: 'learning_result',
      verified: pending.length,
      accuracy: learning.accuracy,
      updates: learning.model_updates
    };
  }

  /**
   * 解析比赛字符串
   */
  parseMatch(input) {
    // 移除"分析"等前缀
    const cleanInput = input.replace(/^(分析|预测|看看|看看看)\s+/, '');

    // 支持格式: "曼联 vs 利物浦", "曼联-利物浦", "曼联 对阵 利物浦"
    const patterns = [
      /(.+?)\s+(?:vs|VS|对阵|-)\s+(.+)/,
      /(.+?)\s+对阵\s+(.+)/
    ];

    for (const pattern of patterns) {
      const match = cleanInput.match(pattern);
      if (match) {
        return {
          home: match[1].trim(),
          away: match[2].trim()
        };
      }
    }
    return null;
  }

  /**
   * 格式化预测输出
   */
  formatPrediction(prediction) {
    const emoji = {
      '主胜': '🏠',
      '客胜': '✈️',
      '平局': '⚖️'
    };

    return {
      ok: true,
      type: 'prediction',
      match: `${prediction.match.home} vs ${prediction.match.away}`,
      prediction: prediction.prediction,
      emoji: emoji[prediction.prediction] || '🎯',
      confidence: `${Math.round(prediction.confidence * 100)}%`,
      odds: prediction.odds,
      recommendation: prediction.recommendation,
      risk_score: prediction.risk_score,
      factors: prediction.factors.slice(0, 3)
    };
  }
}

// 导出
module.exports = { FootballPredictor };
module.exports.main = async function(input) {
  const predictor = new FootballPredictor();
  return await predictor.analyze(input);
};

// CLI入口
if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.log('使用方法: node index.js <命令>');
    console.log('  分析 曼联 vs 利物浦');
    console.log('  今日推荐');
    console.log('  统计');
    console.log('  学习');
    process.exit(1);
  }

  const predictor = new FootballPredictor();
  predictor.analyze(input).then(result => {
    console.log(JSON.stringify(result, null, 2));
  }).catch(err => {
    console.error(err);
    process.exit(1);
  });
}
