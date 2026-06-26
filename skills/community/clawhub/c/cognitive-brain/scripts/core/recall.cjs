#!/usr/bin/env node
/**
 * Cognitive Brain - 记忆检索脚本（重构版）
 * 从记忆系统中检索相关信息
 */

const fs = require('fs');
const path = require('path');
const { resolveModule } = require('../module_resolver.cjs');
const { createLogger } = require('../../src/utils/logger.cjs');

// 创建模块级 logger
const logger = createLogger('recall');

// 导入拆分的模块
const { initRedis, getCache, setCache, closeRedis } = require('./cache.cjs');
const { hybridSearch } = require('./search_strategies.cjs');
const { getPool } = require('./db.cjs');

// 加载配置
const SKILL_DIR = path.join(__dirname, '..', '..');
const configPath = path.join(SKILL_DIR, 'config.json');
let config;
try {
  config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
} catch (e) {
  logger.error('无法加载配置文件', { error: e.message });
  process.exit(1);
}

// 解析参数
function parseArgs() {
  const args = process.argv.slice(2);
  const params = {};
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace('--', '');
    params[key] = args[i + 1];
  }
  return params;
}

// 主召回函数
async function recall(query, options = {}) {
  if (!query || query.trim().length === 0) {
    return { memories: [], suggestions: [] };
  }

  const pool = getPool();
  if (!pool) {
    throw new Error('数据库连接不可用');
  }

  // 检查缓存
  const cacheKey = `recall:${query}`;
  const cached = await getCache(cacheKey);
  if (cached && !options.skipCache) {
    logger.debug('命中缓存');
    return cached;
  }

  // 执行混合搜索
  const results = await hybridSearch(pool, query, {
    useVector: options.vector !== 'false',
    useKeyword: options.keyword !== 'false',
    useAssociation: options.association !== 'false',
    limit: parseInt(options.limit) || 10
  });

  // 格式化结果
  const memories = results.map(r => ({
    id: r.id,
    content: r.content,
    summary: r.summary,
    timestamp: r.timestamp,
    importance: r.importance,
    type: r.type,
    source: r.source,
    relevance: r.score
  }));

  const result = {
    memories,
    suggestions: [],
    query,
    total: memories.length
  };

  // 缓存结果
  await setCache(cacheKey, result, 60);

  return result;
}

// 生成主动建议
async function generateProactiveSuggestions(pool, query, results) {
  const suggestions = [];

  // 基于查询生成建议
  if (query.includes('问题') || query.includes('错误')) {
    suggestions.push({
      type: 'pattern',
      text: '需要我帮你查找相关的解决方案吗？',
      relevance: 0.8
    });
  }

  if (query.includes('学习') || query.includes('了解')) {
    suggestions.push({
      type: 'resource',
      text: '我可以推荐一些相关的学习资源',
      relevance: 0.7
    });
  }

  // 基于结果生成建议
  if (results.length > 0 && results[0].importance > 0.8) {
    suggestions.push({
      type: 'highlight',
      text: `找到一条重要记忆：${results[0].summary?.substring(0, 50)}...`,
      relevance: results[0].importance
    });
  }

  return suggestions.sort((a, b) => b.relevance - a.relevance);
}

// 命令行接口
async function main() {
  const args = parseArgs();
  const query = args.query || args.q || args._?.[0];

  if (!query) {
    logger.error('请提供查询内容');
    process.stdout.write('用法: node recall.cjs --query "搜索内容"\n');
    process.exit(1);
  }

  try {
    // 初始化 Redis
    await initRedis();

    const result = await recall(query, {
      limit: args.limit || 10,
      vector: args.vector,
      keyword: args.keyword,
      association: args.association
    });

    // 命令行输出保留给用户
    process.stdout.write(`\n🔍 查询: "${query}"\n`);
    process.stdout.write(`找到 ${result.memories.length} 条记忆:\n\n`);

    result.memories.forEach((m, i) => {
      process.stdout.write(`${i + 1}. [${m.type}] ${m.summary?.substring(0, 60)}...\n`);
      process.stdout.write(`   重要性: ${(m.importance || 0).toFixed(2)} | 来源: ${m.source}\n`);
    });

    if (result.suggestions.length > 0) {
      process.stdout.write('\n💡 建议:\n');
      result.suggestions.forEach(s => process.stdout.write(`   - ${s.text}\n`));
    }

    // 关闭连接
    await closeRedis();
    process.exit(0);
  } catch (err) {
    logger.error('检索失败', { error: err.message });
    await closeRedis();
    process.exit(1);
  }
}

// 导出函数
module.exports = {
  recall,
  generateProactiveSuggestions
};

// 主入口
if (require.main === module) {
  main();
}
