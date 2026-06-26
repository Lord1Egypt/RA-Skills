/**
 * 搜索策略模块
 * 多种记忆检索策略
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('search_strategies');
const { getEmbeddingService } = require('./embedding_service.cjs');

/**
 * 向量搜索（语义相似度）
 * @param {Object} pool - 数据库连接池
 * @param {string} query - 查询文本
 * @param {number} limit - 返回数量
 * @returns {Promise<Array>}
 */
async function vectorSearch(pool, query, limit = 10) {
  const embeddingService = getEmbeddingService();
  let embedding = null;

  try {
    if (embeddingService && embeddingService.isReady()) {
      embedding = await embeddingService.embed(query);
    }
  } catch (e) {
    console.log('[search] Embedding 服务不可用');
  }

  if (!embedding) return [];

  try {
    const result = await pool.query(`
      SELECT id, summary, content, timestamp, importance, type,
        1 - (embedding <=> $1::vector) as similarity
      FROM episodes
      WHERE embedding IS NOT NULL
      ORDER BY embedding <=> $1::vector
      LIMIT $2
    `, [JSON.stringify(embedding), limit]);

    return result.rows;
  } catch (e) {
    console.error('[search] 向量搜索错误:', e.message);
    return [];
  }
}

/**
 * 关键词搜索
 * @param {Object} pool - 数据库连接池
 * @param {string} query - 查询文本
 * @param {number} limit - 返回数量
 * @returns {Promise<Array>}
 */
async function keywordSearch(pool, query, limit = 10) {
  try {
    const keywords = query.split(/\s+/).filter(k => k.length > 0);

    if (keywords.length === 0) return [];

    const conditions = keywords.map((_, i) =>
      `(summary ILIKE $${i + 1} OR content ILIKE $${i + 1})`
    ).join(' OR ');

    const params = keywords.map(k => `%${k}%`);
    params.push(limit);

    const result = await pool.query(`
      SELECT id, summary, content, timestamp, importance, type
      FROM episodes
      WHERE ${conditions}
      ORDER BY importance DESC, timestamp DESC
      LIMIT $${params.length}
    `, params);

    return result.rows;
  } catch (e) {
    console.error('[search] 关键词搜索错误:', e.message);
    return [];
  }
}

/**
 * 联想激活搜索
 * @param {Object} pool - 数据库连接池
 * @param {string} query - 查询文本
 * @param {number} limit - 返回数量
 * @returns {Promise<Array>}
 */
async function associationSearch(pool, query, limit = 10) {
  try {
    // 1. 找到查询相关的概念
    const concepts = await pool.query(`
      SELECT id, name FROM concepts 
      WHERE name ILIKE $1
      LIMIT 5
    `, [`%${query}%`]);

    if (concepts.rows.length === 0) return [];

    // 2. 激活传播
    const activated = new Map();
    const frontier = new Map();

    concepts.rows.forEach(c => frontier.set(c.id, { name: c.name, level: 1.0 }));

    const threshold = 0.3;
    const decay = 0.9;

    for (let depth = 0; depth < 3; depth++) {
      const newFrontier = new Map();

      for (const [conceptId, data] of frontier) {
        if (data.level < threshold) continue;

        activated.set(conceptId, data);

        const edges = await pool.query(`
          SELECT c.id, c.name, a.weight 
          FROM associations a
          JOIN concepts c ON c.id = a.to_id
          WHERE a.from_id = $1
        `, [conceptId]);

        for (const edge of edges.rows) {
          const newLevel = data.level * decay * edge.weight;
          if (!newFrontier.has(edge.id) || newFrontier.get(edge.id).level < newLevel) {
            newFrontier.set(edge.id, { name: edge.name, level: newLevel });
          }
        }
      }

      frontier.clear();
      newFrontier.forEach((v, k) => frontier.set(k, v));
    }

    // 3. 用激活的概念检索记忆（使用 ILIKE 匹配内容）
    const conceptNames = [...activated.values()].map(a => a.name);

    if (conceptNames.length === 0) return [];

    // 构建 OR 条件：内容或摘要包含任一概念
    const conditions = conceptNames.map((_, i) => 
      `(e.content ILIKE $${i + 2} OR e.summary ILIKE $${i + 2})`
    ).join(' OR ');
    
    const params = conceptNames.map(c => `%${c}%`);
    
    const result = await pool.query(`
      SELECT DISTINCT e.id, e.summary, e.content, e.timestamp, e.importance, e.type
      FROM episodes e
      WHERE ${conditions}
      ORDER BY e.importance DESC, e.timestamp DESC
      LIMIT $1
    `, [limit, ...params]);

    return result.rows;
  } catch (e) {
    console.error('[search] 联想搜索错误:', e.message);
    return [];
  }
}

/**
 * 混合搜索（综合多种策略）
 * @param {Object} pool - 数据库连接池
 * @param {string} query - 查询文本
 * @param {Object} options - 选项
 * @returns {Promise<Array>}
 */
async function hybridSearch(pool, query, options = {}) {
  const { useVector = true, useKeyword = true, useAssociation = true, limit = 10 } = options;

  const results = [];
  const seen = new Set();

  // 向量搜索
  if (useVector) {
    const vectorResults = await vectorSearch(pool, query, limit);
    vectorResults.forEach(r => {
      if (!seen.has(r.id)) {
        seen.add(r.id);
        results.push({ ...r, source: 'vector', score: r.similarity || 0 });
      }
    });
  }

  // 关键词搜索
  if (useKeyword) {
    const keywordResults = await keywordSearch(pool, query, limit);
    keywordResults.forEach(r => {
      if (!seen.has(r.id)) {
        seen.add(r.id);
        results.push({ ...r, source: 'keyword', score: r.importance || 0.5 });
      }
    });
  }

  // 联想搜索
  if (useAssociation) {
    const assocResults = await associationSearch(pool, query, limit);
    assocResults.forEach(r => {
      if (!seen.has(r.id)) {
        seen.add(r.id);
        results.push({ ...r, source: 'association', score: r.importance || 0.3 });
      }
    });
  }

  // 按综合得分排序
  return results
    .sort((a, b) => (b.score || 0) - (a.score || 0))
    .slice(0, limit);
}

module.exports = {
  vectorSearch,
  keywordSearch,
  associationSearch,
  hybridSearch
};

