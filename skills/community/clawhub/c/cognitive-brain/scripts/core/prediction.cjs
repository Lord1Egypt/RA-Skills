#!/usr/bin/env node
/**
 * Cognitive Brain - 预测模块
 * 预测用户需求和下一步行动
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('prediction');
const fs = require('fs');
const path = require('path');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');
const PREDICTION_CACHE_PATH = path.join(SKILL_DIR, '.prediction-cache.json');

// 预测缓存
let predictionCache = {
  patterns: [],
  sequences: [],
  lastUpdate: 0
};

/**
 * 加载缓存
 */
function load() {
  try {
    if (fs.existsSync(PREDICTION_CACHE_PATH)) {
      predictionCache = JSON.parse(fs.readFileSync(PREDICTION_CACHE_PATH, 'utf8'));
    }
  } catch (e) { console.error("[prediction] 错误:", e.message);
    // ignore
  }
}

/**
 * 保存缓存
 */
function save() {
  try {
    fs.writeFileSync(PREDICTION_CACHE_PATH, JSON.stringify(predictionCache, null, 2));
  } catch (e) { console.error("[prediction] 错误:", e.message);
    // ignore
  }
}

/**
 * 基于时间的预测
 */
function predictByTime(userPatterns) {
  const now = new Date();
  const hour = now.getHours();
  const dayOfWeek = now.getDay();

  const predictions = [];

  // 检查活跃时段
  if (userPatterns.activeHours && userPatterns.activeHours.includes(hour)) {
    predictions.push({
      type: 'timing',
      confidence: 0.7,
      prediction: '用户通常在这个时段活跃',
      recommendation: '可以主动提供帮助'
    });
  }

  // 工作日 vs 周末
  if (dayOfWeek >= 1 && dayOfWeek <= 5) {
    predictions.push({
      type: 'schedule',
      confidence: 0.5,
      prediction: '工作日，可能需要工作相关帮助',
      recommendation: '准备好工作相关的工具和信息'
    });
  }

  return predictions;
}

/**
 * 基于历史的预测 - 增强版
 */
async function predictByHistory(pool) {
  const predictions = [];
  
  try {
    // 1. 分析最近任务模式
    const recentTasks = await pool.query(`
      SELECT type, COUNT(*) as count
      FROM episodes
      WHERE timestamp > NOW() - INTERVAL '7 days'
      GROUP BY type
      ORDER BY count DESC
      LIMIT 5
    `);
    
    if (recentTasks.rows.length > 0) {
      predictions.push({
        type: 'task_frequency',
        confidence: 0.7,
        prediction: `最近经常做: ${recentTasks.rows.map(r => r.type).join(', ')}`,
        recommendation: '可以准备相关工具和资源'
      });
    }
    
    // 2. 分析话题趋势
    const trendingTopics = await pool.query(`
      SELECT tag, COUNT(*) as count
      FROM episodes, jsonb_array_elements_text(tags) as tag
      WHERE timestamp > NOW() - INTERVAL '3 days'
        AND tags IS NOT NULL
      GROUP BY tag
      ORDER BY count DESC
      LIMIT 3
    `);
    
    if (trendingTopics.rows.length > 0) {
      predictions.push({
        type: 'topic_trend',
        confidence: 0.6,
        prediction: `热门话题: ${trendingTopics.rows.map(r => r.tag).join(', ')}`,
        recommendation: '可以主动提供相关信息'
      });
    }
    
    // 3. 分析时间模式
    const timePatterns = await pool.query(`
      SELECT EXTRACT(HOUR FROM timestamp) as hour, COUNT(*) as count
      FROM episodes
      WHERE timestamp > NOW() - INTERVAL '14 days'
      GROUP BY hour
      ORDER BY count DESC
      LIMIT 3
    `);
    
    const currentHour = new Date().getHours();
    const peakHours = timePatterns.rows.map(r => parseInt(r.hour));
    
    if (peakHours.includes(currentHour)) {
      predictions.push({
        type: 'peak_time',
        confidence: 0.8,
        prediction: '当前是用户活跃高峰时段',
        recommendation: '提高响应优先级，准备主动帮助'
      });
    }
    
    // 4. 分析概念激活
    const activeConcepts = await pool.query(`
      SELECT name, access_count
      FROM concepts
      ORDER BY last_accessed DESC
      LIMIT 5
    `);
    
    if (activeConcepts.rows.length > 0) {
      predictions.push({
        type: 'active_concepts',
        confidence: 0.5,
        prediction: `活跃概念: ${activeConcepts.rows.slice(0, 3).map(r => r.name).join(', ')}`,
        recommendation: '可以预加载相关记忆'
      });
    }
    
    // 5. 分析情感趋势
    const emotionTrends = await pool.query(`
      SELECT 
        emotion->>'dominantEmotion' as emotion,
        COUNT(*) as count
      FROM episodes
      WHERE timestamp > NOW() - INTERVAL '7 days'
        AND emotion IS NOT NULL
      GROUP BY emotion
      ORDER BY count DESC
      LIMIT 3
    `);
    
    if (emotionTrends.rows.length > 0) {
      const dominantEmotion = emotionTrends.rows[0].emotion;
      predictions.push({
        type: 'emotion_pattern',
        confidence: 0.6,
        prediction: `近期主导情绪: ${dominantEmotion}`,
        recommendation: getEmotionRecommendation(dominantEmotion)
      });
    }
    
  } catch (e) { console.error("[prediction] 错误:", e.message);
    console.error('[prediction] History analysis failed:', e.message);
  }
  
  return predictions;
}

/**
 * 获取情感建议
 */
function getEmotionRecommendation(emotion) {
  const recommendations = {
    positive: '保持积极互动，可以分享更多有趣内容',
    negative: '谨慎回应，优先解决用户问题',
    curious: '主动提供信息，回答潜在问题',
    excited: '配合用户情绪，分享喜悦',
    neutral: '正常互动，等待用户引导'
  };
  return recommendations[emotion] || '正常互动';
}

/**
 * 综合预测 - 增强版
 */
async function predictAll(userPatterns) {
  load();
  
  const predictions = [];
  const pg = require('pg');
  const fs = require('fs');
  const path = require('path');
  
  const HOME = process.env.HOME || '/root';
  const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');
  const CONFIG_PATH = path.join(SKILL_DIR, 'config.json');
  
  try {
    const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    const { Pool } = pg;
    const pool = new Pool(config.storage.primary);
    
    // 基于时间预测
    predictions.push(...predictByTime(userPatterns));
    
    // 基于历史预测
    predictions.push(...await predictByHistory(pool));
    
    // 基于序列预测
    predictions.push(...await predictBySequence(pool));
    
    await pool.end();
  } catch (e) { console.error("[prediction] 错误:", e.message);
    console.error('[prediction] Predict all failed:', e.message);
  }
  
  // 缓存预测结果
  predictionCache.lastUpdate = Date.now();
  predictionCache.predictions = predictions;
  save();
  
  return predictions;
}

/**
 * 新增：序列预测
 */
async function predictBySequence(pool) {
  const predictions = [];
  
  try {
    // 分析最近的记忆序列
    const recentSequence = await pool.query(`
      SELECT type, summary
      FROM episodes
      ORDER BY timestamp DESC
      LIMIT 10
    `);
    
    if (recentSequence.rows.length >= 3) {
      const types = recentSequence.rows.map(r => r.type);
      
      // 检测重复模式
      // 例如：['question', 'task', 'feedback', 'question', 'task', ...]
      for (let patternLen = 2; patternLen <= 3; patternLen++) {
        const lastPattern = types.slice(0, patternLen);
        const prevPattern = types.slice(patternLen, patternLen * 2);
        
        if (JSON.stringify(lastPattern) === JSON.stringify(prevPattern)) {
          predictions.push({
            type: 'sequence_pattern',
            confidence: 0.6,
            prediction: `检测到重复模式: ${lastPattern.join(' → ')}`,
            recommendation: '可以提前准备下一步操作'
          });
          break;
        }
      }
    }
  } catch (e) { console.error("[prediction] 错误:", e.message);
    // ignore
  }
  
  return predictions;
}
function predictByHistory(recentActions) {
  if (!recentActions || recentActions.length === 0) {
    return [];
  }

  const predictions = [];

  // 统计最近动作
  const actionCounts = {};
  for (const action of recentActions) {
    const key = action.type || action;
    actionCounts[key] = (actionCounts[key] || 0) + 1;
  }

  // 找出高频动作
  const topActions = Object.entries(actionCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3);

  if (topActions.length > 0) {
    predictions.push({
      type: 'habit',
      confidence: 0.6,
      prediction: `用户经常: ${topActions.map(([a]) => a).join(', ')}`,
      recommendation: '预加载相关资源'
    });
  }

  // 检测序列模式
  const sequence = detectSequence(recentActions);
  if (sequence) {
    predictions.push({
      type: 'sequence',
      confidence: 0.7,
      prediction: `检测到模式: ${sequence.pattern}`,
      nextAction: sequence.predictedNext
    });
  }

  return predictions;
}

/**
 * 检测序列模式
 */
function detectSequence(actions) {
  if (actions.length < 3) return null;

  // 查找重复的 2-3 个动作序列
  const recent = actions.slice(-5).map(a => a.type || a);

  // 检查最近 2 个动作是否重复出现
  if (recent.length >= 4) {
    const last2 = recent.slice(-2).join(' -> ');
    const prev2 = recent.slice(-4, -2).join(' -> ');

    if (last2 === prev2) {
      return {
        pattern: last2,
        predictedNext: recent[recent.length - 1]
      };
    }
  }

  return null;
}

/**
 * 基于上下文的预测
 */
function predictByContext(context) {
  const predictions = [];

  // 基于当前话题
  if (context.topic) {
    predictions.push({
      type: 'context',
      confidence: 0.6,
      prediction: `当前话题: ${context.topic}`,
      recommendation: '准备好相关背景信息'
    });
  }

  // 基于未完成任务
  if (context.pendingTasks && context.pendingTasks.length > 0) {
    predictions.push({
      type: 'task',
      confidence: 0.8,
      prediction: `有 ${context.pendingTasks.length} 个未完成任务`,
      nextAction: context.pendingTasks[0]
    });
  }

  // 基于开放问题
  if (context.openQuestions && context.openQuestions.length > 0) {
    predictions.push({
      type: 'question',
      confidence: 0.7,
      prediction: '有待回答的问题',
      recommendation: '主动提供答案或询问是否需要帮助'
    });
  }

  return predictions;
}

/**
 * 综合预测
 */
function predict(userPatterns, recentActions, context) {
  load();

  const allPredictions = [
    ...predictByTime(userPatterns),
    ...predictByHistory(recentActions),
    ...predictByContext(context)
  ];

  // 按置信度排序
  allPredictions.sort((a, b) => b.confidence - a.confidence);

  // 合并相似预测
  const merged = mergePredictions(allPredictions);

  return {
    predictions: merged,
    topPrediction: merged[0] || null,
    timestamp: Date.now()
  };
}

/**
 * 合并相似预测
 */
function mergePredictions(predictions) {
  const merged = [];
  const seen = new Set();

  for (const pred of predictions) {
    const key = `${pred.type}_${pred.prediction}`;
    if (!seen.has(key)) {
      seen.add(key);
      merged.push(pred);
    }
  }

  return merged;
}

/**
 * 学习新模式
 */
function learnPattern(sequence, outcome) {
  load();

  // 记录序列模式
  const pattern = {
    sequence,
    outcome,
    learnedAt: Date.now(),
    frequency: 1
  };

  // 检查是否已存在
  const existing = predictionCache.sequences.find(
    s => JSON.stringify(s.sequence) === JSON.stringify(sequence)
  );

  if (existing) {
    existing.frequency++;
    existing.lastSeen = Date.now();
    if (outcome) {
      existing.outcomes = existing.outcomes || [];
      existing.outcomes.push(outcome);
    }
  } else {
    predictionCache.sequences.push(pattern);
  }

  predictionCache.lastUpdate = Date.now();
  save();
}

/**
 * 获取预测统计
 */
function getStats() {
  load();

  return {
    patternsLearned: predictionCache.patterns.length,
    sequencesLearned: predictionCache.sequences.length,
    lastUpdate: predictionCache.lastUpdate
  };
}

// ===== 主函数 =====
async function main() {
  const action = process.argv[2];
  const args = process.argv.slice(3);

  load();

  switch (action) {
    case 'predict': {
      const result = predict(
        { activeHours: [9, 10, 11, 14, 15, 16, 20, 21, 22] },
        [
          { type: 'search' },
          { type: 'read' },
          { type: 'search' },
          { type: 'read' }
        ],
        { topic: 'coding', pendingTasks: ['完成文档'] }
      );

      console.log('🔮 预测结果:');
      console.log(JSON.stringify(result, null, 2));
      break;
    }

    case 'stats':
      console.log('📊 预测统计:');
      console.log(JSON.stringify(getStats(), null, 2));
      break;

    case 'learn':
      if (args[0]) {
        learnPattern(args[0].split(','), args[1]);
        console.log('✅ 模式已学习');
      }
      break;

    default:
      console.log(`
预测模块

用法:
  node prediction.cjs predict    # 运行预测示例
  node prediction.cjs stats      # 查看统计
  node prediction.cjs learn <seq> <outcome>  # 学习模式
      `);
  }
}

main();
