#!/usr/bin/env node
/**
 * Cognitive Brain - 遗忘模块
 * 实现记忆衰减和清理机制
 */

const fs = require('fs');
const path = require('path');
const { createLogger } = require('../../src/utils/logger.cjs');

// 创建模块级 logger
const logger = createLogger('forget');

const HOME = process.env.HOME || '/root';
const SKILL_DIR = path.join(HOME, '.openclaw/workspace/skills/cognitive-brain');
const CONFIG_PATH = path.join(SKILL_DIR, 'config.json');
const FORGET_LOG_PATH = path.join(SKILL_DIR, '.forget-log.json');

// 遗忘配置
const DEFAULT_CONFIG = {
  enabled: true,
  schedule: '0 3 * * *',  // 每天凌晨 3 点
  retentionDays: {
    high: 365,     // 高重要性
    medium: 30,    // 中等重要性
    low: 7         // 低重要性
  },
  minImportance: 0.1,
  batchSize: 100,
  typeRetention: {
    test: { days: 0.5, maxImportance: 0.3, autoDecay: true },
    thought: { days: 7, maxImportance: 0.7 },
    reflection: { days: 14, maxImportance: 0.8 },
    conversation: { days: 30, maxImportance: 1.0 },
    milestone: { days: 365, maxImportance: 1.0 }
  },
  cleanupOrphans: true,
  minAssociationCount: 1
};

// 遗忘日志
let forgetLog = [];

/**
 * 加载配置
 */
function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_PATH)) {
      const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
      return { ...DEFAULT_CONFIG, ...config.forgetting };
    }
  } catch (e) { logger.error("操作失败", { error: e.message });
    // ignore
  }
  return DEFAULT_CONFIG;
}

/**
 * 加载日志
 */
function loadLog() {
  try {
    if (fs.existsSync(FORGET_LOG_PATH)) {
      forgetLog = JSON.parse(fs.readFileSync(FORGET_LOG_PATH, 'utf8'));
    }
  } catch (e) { logger.error("操作失败", { error: e.message });
    forgetLog = [];
  }
}

/**
 * 保存日志
 */
function saveLog() {
  try {
    forgetLog = forgetLog.slice(-100);
    fs.writeFileSync(FORGET_LOG_PATH, JSON.stringify(forgetLog, null, 2));
  } catch (e) { logger.error("操作失败", { error: e.message });
    // ignore
  }
}

/**
 * 计算遗忘曲线
 * 艾宾浩斯遗忘曲线: R = e^(-t/S)
 * R = 保留率, t = 时间, S = 记忆强度
 */
function calculateRetention(importance, ageMs) {
  // 根据重要性确定记忆强度（天数转毫秒）
  const config = loadConfig();
  let strengthDays;

  if (importance >= 0.8) {
    strengthDays = config.retentionDays.high;
  } else if (importance >= 0.5) {
    strengthDays = config.retentionDays.medium;
  } else {
    strengthDays = config.retentionDays.low;
  }

  const strengthMs = strengthDays * 24 * 60 * 60 * 1000;
  const retention = Math.exp(-ageMs / strengthMs);

  return retention;
}

/**
 * 判断是否应该遗忘
 */
function shouldForget(memory, config) {
  // 验证时间戳有效性
  const ts = memory.timestamp || memory.created_at;
  if (!ts) {
    return { shouldForget: true, retention: 0, reason: 'no_timestamp' };
  }
  const tsObj = new Date(ts);
  if (isNaN(tsObj.getTime())) {
    return { shouldForget: true, retention: 0, reason: 'invalid_timestamp' };
  }

  const ageMs = Date.now() - tsObj.getTime();
  let retention = 1.0;
  let shouldDelete = false;
  const importance = memory.importance || 0.5;

  // 按类型处理记忆（A1: 测试记忆过滤）
  const typeConfig = config.typeRetention?.[memory.type];
  if (typeConfig) {
    const retentionDays = typeConfig.days || 1;
    const maxImportance = typeConfig.maxImportance || 1.0;

    // 如果重要性超过类型最大值，降低它
    const effectiveImportance = Math.min(importance, maxImportance);

    const strengthMs = retentionDays * 24 * 60 * 60 * 1000;
    retention = Math.exp(-ageMs / strengthMs);
    shouldDelete = retention < 0.3 || ageMs > retentionDays * 2 * 24 * 60 * 60 * 1000;

    return { shouldForget: shouldDelete, retention, reason: 'type_based_' + memory.type };
  }

  // 普通记忆的遗忘逻辑
  // 如果重要性低于阈值，直接遗忘
  if (importance < config.minImportance) {
    return { shouldForget: true, retention: 0 };
  }

  // 计算保留率
  retention = calculateRetention(importance, ageMs);
  shouldDelete = retention < 0.3;

  // 返回对象，包含 shouldForget 和 retention
  return { shouldForget: shouldDelete, retention };
}

/**
 * 执行遗忘
 */
async function forget(config = null) {
  config = config || loadConfig();

  if (!config.enabled) {
    logger.info('[forget] 遗忘功能已禁用');
    return { enabled: false };
  }

  loadLog();

  const result = {
    timestamp: Date.now(),
    forgotten: 0,
    retained: 0,
    errors: 0,
    details: []
  };

  try {
    // P1: 使用连接池复用
    const pool = getPool();

    // 获取所有记忆
    const memories = await pool.query(`
      SELECT id, type, summary, importance, timestamp, created_at, access_count
      FROM episodes
      ORDER BY importance ASC, timestamp ASC
      LIMIT $1
    `, [config.batchSize * 10]);

    const toDelete = [];
    const toRetain = [];

    // 评估每条记忆
    for (const memory of memories.rows) {
      const evaluation = shouldForget(memory, config);

      if (evaluation.shouldForget) {
        toDelete.push(memory.id);
        result.details.push({
          id: memory.id,
          summary: memory.summary?.slice(0, 50),
          retention: evaluation.retention,
          importance: memory.importance
        });
      } else {
        toRetain.push(memory.id);
      }
    }

    // 执行删除 (已经是批量删除)
    if (toDelete.length > 0) {
      await pool.query(`
        DELETE FROM episodes
        WHERE id = ANY($1)
      `, [toDelete]);

      result.forgotten = toDelete.length;
    }

    result.retained = toRetain.length;

    // A1: 清理孤立概念
    if (config.cleanupOrphans) {
      const orphanResult = await cleanupOrphanConcepts(pool, config);
      result.orphansCleaned = orphanResult.cleaned;
      result.orphanDetails = orphanResult.details;
    }

  } catch (e) { logger.error("操作失败", { error: e.message });
    console.error('[forget] 数据库错误:', e.message);
    result.errors++;
    result.error = e.message;
  } finally {
    // P1: 在 main 函数结束时关闭连接池
  }

  // 记录日志
  forgetLog.push(result);
  saveLog();

  logger.info(`[forget] 完成: 遗忘 ${result.forgotten} 条，保留 ${result.retained} 条`);
  if (result.orphansCleaned) {
    logger.info(`         清理孤立概念: ${result.orphansCleaned} 个`);
  }

  return result;
}

/**
 * A1: 清理孤立概念
 * 删除没有关联的概念，特别是测试产生的临时概念
 */
async function cleanupOrphanConcepts(pool, config) {
  const result = {
    cleaned: 0,
    details: []
  };

  try {
    // 查找孤立概念（没有关联的概念）
    const orphans = await pool.query(`
      SELECT c.id, c.name, c.type, c.importance
      FROM concepts c
      LEFT JOIN associations a ON c.id = a.from_id OR c.id = a.to_id
      WHERE a.id IS NULL
      ORDER BY c.importance ASC
      LIMIT 50
    `);

    const toDelete = [];

    for (const concept of orphans.rows) {
      // 测试产生的概念优先删除
      const isTestConcept = concept.name?.match(/test|测试|v\d+\.\d+|面测|区全|功能/i) ||
                            concept.type === 'test';
      
      if (isTestConcept || concept.importance < 0.3) {
        toDelete.push(concept.id);
        result.details.push({
          id: concept.id,
          name: concept.name,
          reason: isTestConcept ? 'test_concept' : 'low_importance'
        });
      }
    }

    if (toDelete.length > 0) {
      await pool.query(`DELETE FROM concepts WHERE id = ANY($1)`, [toDelete]);
      result.cleaned = toDelete.length;
    }

    logger.info(`[cleanupOrphans] 清理 ${result.cleaned} 个孤立概念`);

  } catch (e) { logger.error("操作失败", { error: e.message });
    console.error('[cleanupOrphans] 错误:', e.message);
  }

  return result;
}

/**
 * 软遗忘（降低重要性而不是删除）
 */
async function softForget(config = null) {
  config = config || loadConfig();

  const result = {
    timestamp: Date.now(),
    decayed: 0,
    errors: 0
  };

  try {
    // P1: 使用连接池复用
    const pool = getPool();

    // 衰减所有记忆的重要性
    const decayFactor = 0.95;

    await pool.query(`
      UPDATE episodes
      SET importance = importance * $1
      WHERE importance > $2
    `, [decayFactor, config.minImportance]);

    const updated = await pool.query(`
      SELECT COUNT(*) as count
      FROM episodes
      WHERE importance > $1
    `, [config.minImportance]);

    result.decayed = parseInt(updated.rows[0].count);

  } catch (e) { console.error("[forget] 软遗忘错误:", e.message);
    result.errors++;
  }

  return result;
}

// P1: 连接池缓存
let globalPool = null;

function getPool() {
  if (!globalPool) {
    try {
      const pg = require(path.join(SKILL_DIR, 'node_modules/pg'));
      const dbConfig = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
      const { Pool } = pg;
      globalPool = new Pool(dbConfig.storage.primary);
    } catch (e) {
      console.error('[forget] Failed to create pool:', e.message);
      return null;
    }
  }
  return globalPool;
}

async function closePool() {
  if (globalPool) {
    await globalPool.end();
    globalPool = null;
  }
}

/**
 * 强化记忆 (P1: 使用连接池复用)
 */
async function strengthenMemory(memoryId, factor = 1.2) {
  try {
    const pool = getPool();

    await pool.query(`
      UPDATE episodes
      SET
        importance = LEAST(1.0, importance * $1),
        access_count = access_count + 1,
        last_accessed = NOW()
      WHERE id = $2
    `, [factor, memoryId]);

    return { success: true, memoryId, factor };

  } catch (e) { logger.error("操作失败", { error: e.message });
    return { success: false, error: e.message };
  }
}

/**
 * 获取遗忘统计
 */
function getStats() {
  loadLog();

  const stats = {
    totalRuns: forgetLog.length,
    totalForgotten: forgetLog.reduce((sum, l) => sum + (l.forgotten || 0), 0),
    totalRetained: forgetLog.reduce((sum, l) => sum + (l.retained || 0), 0),
    lastRun: forgetLog.length > 0 ? forgetLog[forgetLog.length - 1] : null
  };

  return stats;
}

/**
 * 预览将被遗忘的记忆
 */
async function preview(config = null) {
  config = config || loadConfig();

  const preview = {
    willForget: [],
    willRetain: [],
    stats: { total: 0, toForget: 0, toRetain: 0 }
  };

  try {
    // P1: 使用连接池复用
    const pool = getPool();

    const memories = await pool.query(`
      SELECT id, type, summary, importance, timestamp, created_at, access_count
      FROM episodes
      ORDER BY importance ASC
      LIMIT 100
    `);

    preview.stats.total = memories.rows.length;

    for (const memory of memories.rows) {
      const evaluation = shouldForget(memory, config);

      if (evaluation.shouldForget) {
        preview.willForget.push({
          id: memory.id,
          summary: memory.summary?.slice(0, 50),
          importance: memory.importance,
          retention: evaluation.retention
        });
      } else {
        preview.willRetain.push({
          id: memory.id,
          summary: memory.summary?.slice(0, 50),
          importance: memory.importance,
          retention: evaluation.retention
        });
      }
    }

    preview.stats.toForget = preview.willForget.length;
    preview.stats.toRetain = preview.willRetain.length;

  } catch (e) { console.error("[forget] 预览错误:", e.message);
    preview.error = e.message;
  }

  return preview;
}

// ===== 主函数 =====
async function main() {
  const action = process.argv[2];
  const args = process.argv.slice(3);

  try {
    switch (action) {
      case 'run':
        const result = await forget();
        logger.info('🗑️ 遗忘完成:');
        logger.info(`   遗忘: ${result.forgotten} 条`);
        logger.info(`   保留: ${result.retained} 条`);
        if (result.orphansCleaned) {
          logger.info(`   孤立概念: ${result.orphansCleaned} 个`);
        }
        break;

      case 'soft':
        const softResult = await softForget();
        logger.info('📉 软遗忘完成:');
        logger.info(JSON.stringify(softResult, null, 2));
        break;

      case 'preview':
        const previewResult = await preview();
        logger.info('👀 预览结果:');
        logger.info(`   总计: ${previewResult.stats.total}`);
        logger.info(`   将遗忘: ${previewResult.stats.toForget}`);
        logger.info(`   将保留: ${previewResult.stats.toRetain}`);
        if (previewResult.willForget.length > 0) {
          logger.info('\n   将被遗忘的记忆:');
          previewResult.willForget.slice(0, 5).forEach(m => {
            logger.info(`     - ${m.summary} (重要性: ${m.importance?.toFixed(2)})`);
          });
        }
        break;

      case 'stats':
        logger.info('📊 遗忘统计:');
        logger.info(JSON.stringify(getStats(), null, 2));
        break;

      case 'strengthen':
        if (args[0]) {
          const result = await strengthenMemory(args[0], parseFloat(args[1]) || 1.2);
          logger.info('💪 强化结果:', result);
        }
        break;

      default:
        logger.info(`
遗忘模块

用法:
  node forget.cjs run              # 执行遗忘
  node forget.cjs soft             # 软遗忘（降低重要性）
  node forget.cjs preview          # 预览将被遗忘的记忆
  node forget.cjs stats            # 查看统计
  node forget.cjs strengthen <id> [factor]  # 强化记忆

遗忘条件:
  - 重要性 < 0.1 且超过 7 天未访问
  - 保留率 < 10% 且从未被访问

保留率计算:
  高重要性 (≥0.8): 365 天
  中重要性 (0.5-0.8): 30 天
  低重要性 (<0.5): 7 天
      `);
    }
  } finally {
    // P1: 确保关闭连接池
    await closePool();
  }
}

main();

