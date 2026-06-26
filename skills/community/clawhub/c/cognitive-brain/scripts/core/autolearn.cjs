#!/usr/bin/env node
/**
 * Cognitive Brain - 自主学习脚本
 * 在空闲时自动执行学习任务
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('autolearn');
const fs = require('fs');
const path = require('path');

const configPath = path.join(__dirname, '..', '..', 'config.json');
let config;
try {
  config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
} catch (e) { console.error("[autolearn] 错误:", e.message);
  console.error('❌ 无法加载配置文件:', e.message);
  process.exit(1);
}

// ===== 反思总结 =====
// P7: 优化 SQL 查询，只选择需要的字段
async function runReflection(pool) {
  logger.info('🤔 执行反思任务...');

  try {
    const episodes = await pool.query(`
      SELECT id, type, importance, created_at FROM episodes
      WHERE created_at > NOW() - INTERVAL '24 hours'
      ORDER BY created_at DESC
      LIMIT 100
    `);
    
    if (episodes.rows.length === 0) {
      return { task: 'reflection', result: 'no_data' };
    }
    
    const failures = episodes.rows.filter(e => 
      e.type === 'error' || e.type === 'correction'
    ).length;
    const successes = episodes.rows.filter(e => e.type === 'success').length;
    
    const insights = [];
    
    if (failures > 3) {
      insights.push({
        type: 'warning',
        content: `今日错误较多(${failures}次)，需要检查常见问题`,
        priority: 'high'
      });
    }
    
    if (successes > failures) {
      insights.push({
        type: 'success',
        content: `表现良好，成功率 ${((successes / episodes.rows.length) * 100).toFixed(1)}%`,
        priority: 'info'
      });
    }
    
    // 存储反思结果
    for (const insight of insights) {
      await pool.query(`
        INSERT INTO reflections (trigger_type, trigger_event, insights, importance)
        VALUES ('auto_reflection', 'daily_analysis', $1, 0.7)
      `, [JSON.stringify([insight])]);
    }
    
    logger.info(`✅ 反思完成，生成 ${insights.length} 条洞察`);
    return { task: 'reflection', insights: insights.length };
    
  } catch (e) { console.error("[autolearn] 错误:", e.message);
    logger.info(`❌ 反思失败: ${e.message}`);
    return { task: 'reflection', error: e.message };
  }
}

// ===== 联想强化 =====
async function runAssociationStrengthening(pool) {
  logger.info('🔗 执行联想强化...');
  
  try {
    // 检查 entities 字段是否存在且为数组
    const cooccurrences = await pool.query(`
      SELECT 
        e1->>'value' as entity1,
        e2->>'value' as entity2,
        COUNT(*) as co_count
      FROM episodes ep,
        jsonb_array_elements(ep.entities::jsonb) e1,
        jsonb_array_elements(ep.entities::jsonb) e2
      WHERE e1->>'value' < e2->>'value'
        AND ep.created_at > NOW() - INTERVAL '7 days'
        AND ep.entities IS NOT NULL
        AND jsonb_typeof(ep.entities::jsonb) = 'array'
      GROUP BY e1->>'value', e2->>'value'
      HAVING COUNT(*) >= 2
      ORDER BY co_count DESC
      LIMIT 50
    `);
    
    let strengthened = 0;
    
    for (const co of cooccurrences.rows) {
      await pool.query(`
        INSERT INTO associations (from_id, to_id, weight, type)
        SELECT c1.id, c2.id, LEAST($3, 1.0), 'co_occurs'
        FROM concepts c1, concepts c2
        WHERE c1.name = $1 AND c2.name = $2
        ON CONFLICT (from_id, to_id, type) DO UPDATE SET
          weight = LEAST(associations.weight + 0.02, 1.0),
          evidence_count = associations.evidence_count + 1,
          last_reinforced = NOW()
      `, [co.entity1, co.entity2, 0.3 + co.co_count * 0.05]);
      
      strengthened++;
    }
    
    logger.info(`✅ 联想强化完成，更新 ${strengthened} 条关联`);
    return { task: 'association', strengthened };
    
  } catch (e) { console.error("[autolearn] 错误:", e.message);
    logger.info(`❌ 联想强化失败: ${e.message}`);
    return { task: 'association', error: e.message };
  }
}

// ===== 记忆优化 =====
async function runMemoryOptimization(pool) {
  logger.info('♻️ 执行记忆优化...');
  
  try {
    const result = await pool.query(`
      DELETE FROM episodes
      WHERE importance < 0.1
        AND created_at < NOW() - INTERVAL '7 days'
        AND access_count = 0
      RETURNING id
    `);
    
    logger.info(`✅ 记忆优化完成，清理 ${result.rowCount} 条记忆`);
    return { task: 'optimization', deleted: result.rowCount };
    
  } catch (e) { console.error("[autolearn] 错误:", e.message);
    logger.info(`❌ 记忆优化失败: ${e.message}`);
    return { task: 'optimization', error: e.message };
  }
}

// ===== 主函数 =====
async function main() {
  const task = process.argv[2] || 'all';
  
  logger.info('🧠 Cognitive Brain - 自主学习');
  logger.info('================================\n');
  
  const results = [];
  
  try {
    const pg = require('pg');
    const { Pool } = pg;
    const pool = new Pool(config.storage.primary);
    
    const tasks = {
      reflection: () => runReflection(pool),
      association: () => runAssociationStrengthening(pool),
      optimization: () => runMemoryOptimization(pool)
    };
    
    if (task === 'all') {
      for (const [name, fn] of Object.entries(tasks)) {
        try {
          const result = await fn();
          results.push(result);
        } catch (e) { console.error("[autolearn] 错误:", e.message);
          results.push({ task: name, error: e.message });
        }
      }
    } else if (tasks[task]) {
      const result = await tasks[task]();
      results.push(result);
    } else {
      logger.info('未知任务:', task);
      logger.info('可用任务:', Object.keys(tasks).join(', '));
      process.exit(1);
    }
    
    await pool.end();
    
  } catch (e) { console.error("[autolearn] 错误:", e.message);
    logger.info('⚠️ 数据库不可用，跳过学习任务');
    logger.info('   请确保 PostgreSQL 已启动并配置正确');
  }
  
  logger.info('\n📋 学习报告:');
  logger.info(JSON.stringify(results, null, 2));
}

main();

