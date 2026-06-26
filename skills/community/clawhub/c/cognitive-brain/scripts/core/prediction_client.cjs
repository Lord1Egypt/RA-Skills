#!/usr/bin/env node
/**
 * Cognitive Brain - 预测客户端
 * 在实际对话中使用预测功能，预加载相关记忆
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('prediction_client');
const fs = require('fs');
const path = require('path');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');
const CONFIG_PATH = path.join(SKILL_DIR, 'config.json');

let config = null;
try {
  config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
} catch (e) { console.error("[prediction_client] 错误:", e.message);
  console.error('[prediction-client] Config not found');
}

/**
 * 分析用户消息历史，预测下一个可能的话题
 */
async function predictNextTopic(pool, userId, lastMessages = []) {
  const predictions = [];
  
  try {
    // 1. 分析最近对话主题（不使用 metadata 字段）
    const recentTopics = await pool.query(`
      SELECT content, type, created_at
      FROM episodes
      WHERE created_at > NOW() - INTERVAL '30 minutes'
      ORDER BY created_at DESC
      LIMIT 5
    `);
    
    if (recentTopics.rows.length === 0) {
      return predictions;
    }
    
    // 2. 提取关键词
    const allContent = recentTopics.rows.map(r => r.content).join(' ');
    const keywords = extractKeywords(allContent);
    
    // 3. 基于关键词预测
    for (const keyword of keywords.slice(0, 3)) {
      // 查找与关键词相关的其他话题
      const related = await pool.query(`
        SELECT DISTINCT content, importance
        FROM episodes
        WHERE content ILIKE $1
          AND created_at > NOW() - INTERVAL '7 days'
        ORDER BY importance DESC
        LIMIT 3
      `, [`%${keyword}%`]);
      
      if (related.rows.length > 1) {
        predictions.push({
          keyword,
          confidence: 0.6,
          type: 'topic_continuation',
          reason: `用户最近关注"${keyword}"，可能继续相关话题`
        });
      }
    }
    
    // 4. 检测对话模式
    const patterns = detectPatterns(recentTopics.rows);
    predictions.push(...patterns);
    
    // 5. 基于时间预测
    const hour = new Date().getHours();
    const timePrediction = await predictByTime(pool, hour);
    if (timePrediction) {
      predictions.push(timePrediction);
    }
    
  } catch (e) { console.error("[prediction_client] 错误:", e.message);
    console.error('[prediction-client] Topic prediction failed:', e.message);
  }
  
  return predictions.sort((a, b) => b.confidence - a.confidence).slice(0, 3);
}

/**
 * 检测对话模式
 */
function detectPatterns(recentMessages) {
  const patterns = [];
  
  if (recentMessages.length < 2) return patterns;
  
  // 检查是否是连续提问模式
  const questionCount = recentMessages.filter(m => 
    m.content.includes('?') || m.content.includes('？') ||
    m.content.includes('吗') || m.content.includes('什么') ||
    m.content.includes('怎么') || m.content.includes('为什么')
  ).length;
  
  if (questionCount >= 2) {
    patterns.push({
      confidence: 0.7,
      type: 'question_chain',
      reason: '用户连续提问，可能还有后续问题'
    });
  }
  
  // 检查是否是探索模式
  const exploreKeywords = ['试试', '如果', '或者', '还有', '另外'];
  const exploreCount = recentMessages.filter(m =>
    exploreKeywords.some(kw => m.content.includes(kw))
  ).length;
  
  if (exploreCount >= 2) {
    patterns.push({
      confidence: 0.6,
      type: 'exploration',
      reason: '用户在探索多种可能性'
    });
  }
  
  // 检查是否是任务模式
  const taskKeywords = ['做', '完成', '修复', '添加', '创建', '实现'];
  const taskCount = recentMessages.filter(m =>
    taskKeywords.some(kw => m.content.includes(kw))
  ).length;
  
  if (taskCount >= 2) {
    patterns.push({
      confidence: 0.75,
      type: 'task_focus',
      reason: '用户专注于任务执行，可能需要技术支持'
    });
  }
  
  return patterns;
}

/**
 * 基于时间的预测
 */
async function predictByTime(pool, hour) {
  try {
    // 查找该时段用户通常做什么
    const timePatterns = await pool.query(`
      SELECT type, COUNT(*) as count
      FROM episodes
      WHERE EXTRACT(HOUR FROM created_at) = $1
        AND created_at > NOW() - INTERVAL '30 days'
      GROUP BY type
      ORDER BY count DESC
      LIMIT 1
    `, [hour]);
    
    if (timePatterns.rows.length > 0 && timePatterns.rows[0].count >= 3) {
      return {
        confidence: 0.5,
        type: 'time_pattern',
        reason: `用户通常在此时段进行"${timePatterns.rows[0].type}"类型活动`
      };
    }
  } catch (e) { console.error("[prediction_client] 错误:", e.message);
    // ignore
  }
  return null;
}

/**
 * 提取关键词
 */
function extractKeywords(text) {
  const keywords = [];
  const seen = new Set();
  
  // 技术术语
  const techTerms = text.match(/\b(Rust|Python|JavaScript|AI|API|SQL|Redis|PostgreSQL|Brain|Cognitive|Embedding|Vector|Git|Linux)\b/gi) || [];
  techTerms.forEach(term => {
    const normalized = term.toLowerCase();
    if (!seen.has(normalized)) {
      seen.add(normalized);
      keywords.push(term);
    }
  });
  
  // 中文关键词
  const chineseMatches = text.match(/(用户|记忆|系统|模块|功能|项目|任务|数据|配置|文件|脚本|服务|概念|实体|情感|意图|决策|对话|预测|反思|联想|遗忘|学习|优化|改进|更新|版本|日志|错误|分析|洞察|建议|偏好|兴趣|模式|趋势|关系|网络|节点|向量|嵌入|缓存|存储|数据库|查询|检索|编码|处理|参数|设置|环境|依赖|框架|工具|平台|接口|文档|测试|验证|检查|监控|性能|质量|准确性|安全性|路径|目录|格式|函数|方法|类|属性|变量|异常|内存|磁盘|网络|并发|异步|队列|索引|排序|搜索|过滤|创建|读取|写入|删除|事务|启动|停止|重启|初始化|安装|加载|保存|导出|导入|升级|发布|部署|维护|重构|修复|清理)/g) || [];
  chineseMatches.forEach(word => {
    if (!seen.has(word) && keywords.length < 10) {
      seen.add(word);
      keywords.push(word);
    }
  });
  
  return keywords;
}

/**
 * 根据预测预加载相关记忆
 */
async function preloadRelatedMemories(pool, predictions, limit = 5) {
  const memories = [];
  
  try {
    for (const pred of predictions) {
      if (pred.keyword) {
        // 基于关键词检索
        const result = await pool.query(`
          SELECT id, summary, content, importance
          FROM episodes
          WHERE content ILIKE $1
             OR summary ILIKE $1
          ORDER BY importance DESC, created_at DESC
          LIMIT $2
        `, [`%${pred.keyword}%`, limit]);
        
        memories.push(...result.rows.map(r => ({
          ...r,
          preloadReason: `预测话题: ${pred.keyword}`
        })));
      }
    }
    
    // 去重
    const uniqueMemories = [];
    const seen = new Set();
    for (const m of memories) {
      if (!seen.has(m.id)) {
        seen.add(m.id);
        uniqueMemories.push(m);
      }
    }
    
    return uniqueMemories.slice(0, limit);
    
  } catch (e) { console.error("[prediction_client] 错误:", e.message);
    console.error('[prediction-client] Preload failed:', e.message);
    return [];
  }
}

/**
 * 主预测函数 - 在 hook 中调用
 * @param {string} userId - 用户ID
 * @param {Object} context - 上下文
 * @param {Object} externalPool - 外部传入的 pool（可选，用于 hook 调用）
 */
async function predictAndPreload(userId, context = {}, externalPool = null) {
  if (!config) return { predictions: [], memories: [] };

  let pool = externalPool;
  let shouldEndPool = false;

  // 如果没有传入 pool，则创建自己的（CLI 模式）
  if (!pool) {
    const pg = require('pg');
    const { Pool } = pg;
    pool = new Pool(config.storage.primary);
    shouldEndPool = true;
  }

  try {
    // 1. 预测
    const predictions = await predictNextTopic(pool, userId, context.recentMessages);

    // 2. 预加载记忆
    const memories = predictions.length > 0
      ? await preloadRelatedMemories(pool, predictions)
      : [];

    return { predictions, memories };

  } catch (e) { console.error("[prediction_client] 错误:", e.message);
    console.error('[prediction-client] Error:', e.message);
    return { predictions: [], memories: [] };
  } finally {
    // 只有我们自己创建的 pool 才关闭
    if (shouldEndPool && pool) {
      await pool.end().catch(() => {});
    }
  }
}

module.exports = {
  predictAndPreload,
  predictNextTopic,
  preloadRelatedMemories
};

// CLI 支持
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args[0] === 'test' || args.length === 0) {
    console.log('🔮 测试预测功能...\n');
    
    predictAndPreload('test_user', {
      recentMessages: ['测试消息', '验证预测功能']
    }).then(({ predictions, memories }) => {
      console.log('=== 预测结果 ===');
      if (predictions.length === 0) {
        console.log('暂无预测（需要更多对话历史）');
      } else {
        predictions.forEach((p, i) => {
          console.log(`${i + 1}. ${p.keyword || p.topic} (置信度: ${(p.confidence * 100).toFixed(1)}%)`);
        });
      }
      
      console.log('\n=== 预加载记忆 ===');
      if (memories.length === 0) {
        console.log('0 条');
      } else {
        memories.forEach((m, i) => {
          console.log(`${i + 1}. ${m.summary?.substring(0, 50)}... (${m.preloadReason})`);
        });
      }
      
      process.exit(0);
    }).catch(err => {
      console.error('❌ 错误:', err.message);
      process.exit(1);
    });
  } else {
    console.log('用法: node prediction_client.cjs [test]');
    process.exit(0);
  }
}
