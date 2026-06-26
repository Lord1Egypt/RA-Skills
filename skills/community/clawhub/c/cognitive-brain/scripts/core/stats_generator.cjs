/**
 * 统计生成器模块
 * 生成知识网络的各种统计报告
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('stats_generator');
const { getPool } = require('./db.cjs');

/**
 * 生成系统统计报告
 */
async function generateStats() {
  const pool = getPool();

  try {
    const stats = await pool.query(`
      SELECT 
        (SELECT COUNT(*) FROM episodes) as memory_count,
        (SELECT COUNT(*) FROM concepts) as concept_count,
        (SELECT COUNT(*) FROM associations) as association_count,
        (SELECT COUNT(*) FROM reflections) as reflection_count
    `);

    const s = stats.rows[0];

    // 计算联想密度
    const maxPossible = s.concept_count * (s.concept_count - 1) / 2;
    const density = maxPossible > 0 ? (s.association_count / maxPossible * 100).toFixed(2) : 0;

    // 记忆类型分布
    const types = await pool.query(`
      SELECT type, COUNT(*) as count 
      FROM episodes 
      GROUP BY type 
      ORDER BY count DESC
    `);

    // 热门概念
    const hotConcepts = await pool.query(`
      SELECT name, access_count, importance
      FROM concepts
      ORDER BY access_count DESC, importance DESC
      LIMIT 10
    `);

    // 孤立概念
    const orphans = await pool.query(`
      SELECT c.name, c.importance
      FROM concepts c
      LEFT JOIN associations a ON c.id = a.from_id OR c.id = a.to_id
      WHERE a.id IS NULL
      ORDER BY c.importance DESC
      LIMIT 5
    `);

    // 时间线统计
    const timeline = await pool.query(`
      SELECT 
        DATE_TRUNC('day', created_at) as day,
        COUNT(*) as count
      FROM episodes
      WHERE created_at > NOW() - INTERVAL '7 days'
      GROUP BY day
      ORDER BY day
    `);

    return {
      memoryCount: parseInt(s.memory_count),
      conceptCount: parseInt(s.concept_count),
      associationCount: parseInt(s.association_count),
      reflectionCount: parseInt(s.reflection_count),
      density: parseFloat(density),
      types: types.rows,
      hotConcepts: hotConcepts.rows,
      orphans: orphans.rows,
      timeline: timeline.rows
    };
  } catch (e) {
    console.error('[stats] 统计生成失败:', e.message);
    throw e;
  }
}

/**
 * 打印统计报告到控制台
 */
function printStats(stats) {
  console.log('\n📊 Cognitive Brain 知识网络统计\n');
  console.log('='.repeat(50));

  console.log('\n📈 基础指标:');
  console.log(`  记忆数: ${stats.memoryCount}`);
  console.log(`  概念数: ${stats.conceptCount}`);
  console.log(`  关联数: ${stats.associationCount}`);
  console.log(`  反思数: ${stats.reflectionCount}`);
  console.log(`  联想密度: ${stats.density}%`);

  console.log('\n📝 记忆类型分布:');
  stats.types.forEach(t => {
    const bar = '█'.repeat(Math.min(20, parseInt(t.count)));
    console.log(`  ${t.type.padEnd(15)} ${bar} ${t.count}`);
  });

  console.log('\n🔥 热门概念 (Top 10):');
  stats.hotConcepts.forEach((c, i) => {
    console.log(`  ${i+1}. ${c.name} (访问:${c.access_count}, 重要度:${(c.importance*100).toFixed(0)}%)`);
  });

  if (stats.orphans.length > 0) {
    console.log('\n⚠️ 孤立概念 (建议关联):');
    stats.orphans.forEach(c => {
      console.log(`  - ${c.name} (重要度:${(c.importance*100).toFixed(0)}%)`);
    });
  }

  if (stats.timeline.length > 0) {
    console.log('\n📅 最近7天记忆增长:');
    stats.timeline.forEach(t => {
      const date = new Date(t.day).toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' });
      const bar = '▓'.repeat(Math.min(20, parseInt(t.count)));
      console.log(`  ${date} ${bar} ${t.count}`);
    });
  }
}

module.exports = {
  generateStats,
  printStats
};
