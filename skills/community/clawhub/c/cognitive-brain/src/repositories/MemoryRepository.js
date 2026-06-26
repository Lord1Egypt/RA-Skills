/**
 * 记忆仓储
 */
const { BaseRepository } = require('./BaseRepository');
const { Memory } = require('../domain/Memory');

class MemoryRepository extends BaseRepository {
  constructor(pool) {
    super(pool, 'episodes');
  }

  /**
   * 创建记忆
   */
  async create(memory) {
    const result = await this.pool.query(
      `INSERT INTO episodes (id, content, summary, type, importance, source_channel, role, entities, emotion, intent, embedding, layers, created_at, timestamp)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
       RETURNING *`,
      [
        memory.id,
        memory.content,
        memory.summary,
        memory.type,
        memory.importance,
        memory.sourceChannel,
        memory.role,
        JSON.stringify(memory.entities),
        JSON.stringify(memory.emotion),
        memory.intent,
        memory.embedding ? JSON.stringify(memory.embedding) : null,
        JSON.stringify(memory.layers || []),
        memory.createdAt,
        memory.updatedAt || new Date()
      ]
    );
    
    return Memory.fromRow(result.rows[0]);
  }

  /**
   * 更新记忆
   */
  async update(id, data) {
    const sets = [];
    const values = [];
    let idx = 1;
    
    if (data.content !== undefined) {
      sets.push(`content = $${idx++}`);
      values.push(data.content);
    }
    if (data.summary !== undefined) {
      sets.push(`summary = $${idx++}`);
      values.push(data.summary);
    }
    if (data.importance !== undefined) {
      sets.push(`importance = $${idx++}`);
      values.push(data.importance);
    }
    if (data.accessCount !== undefined) {
      sets.push(`access_count = $${idx++}`);
      values.push(data.accessCount);
    }
    if (data.lastAccessed !== undefined) {
      sets.push(`last_accessed = $${idx++}`);
      values.push(data.lastAccessed);
    }
    
    sets.push(`timestamp = $${idx++}`);
    values.push(new Date());
    values.push(id);
    
    const result = await this.pool.query(
      `UPDATE episodes SET ${sets.join(', ')} WHERE id = $${idx} RETURNING *`,
      values
    );
    
    return result.rows[0] ? Memory.fromRow(result.rows[0]) : null;
  }

  /**
   * 根据内容搜索
   */
  async search(query, options = {}) {
    const { limit = 10, type = null, minImportance = 0 } = options;
    
    let sql = `SELECT * FROM episodes WHERE (content ILIKE $1 OR summary ILIKE $1)`;
    const params = [`%${query}%`];
    
    if (type) {
      sql += ` AND type = $${params.length + 1}`;
      params.push(type);
    }
    
    if (minImportance > 0) {
      sql += ` AND importance >= $${params.length + 1}`;
      params.push(minImportance);
    }
    
    sql += ` ORDER BY importance DESC, created_at DESC LIMIT $${params.length + 1}`;
    params.push(limit);
    
    const result = await this.pool.query(sql, params);
    return result.rows.map(row => Memory.fromRow(row));
  }

  /**
   * 查找高重要性记忆
   */
  async findImportant(minImportance = 0.8, types = [], limit = 10) {
    let sql = `SELECT * FROM episodes WHERE importance >= $1`;
    const params = [minImportance];
    
    if (types.length > 0) {
      sql += ` AND type = ANY($2)`;
      params.push(types);
    }
    
    sql += ` ORDER BY importance DESC, created_at DESC LIMIT $${params.length + 1}`;
    params.push(limit);
    
    const result = await this.pool.query(sql, params);
    return result.rows.map(row => Memory.fromRow(row));
  }

  /**
   * 标记访问
   */
  async markAccessed(id) {
    await this.pool.query(
      `UPDATE episodes SET access_count = access_count + 1, last_accessed = NOW(), timestamp = NOW() WHERE id = $1`,
      [id]
    );
  }

  /**
   * 衰减重要性
   */
  async decayImportance(factor = 0.95, minImportance = 0.1) {
    await this.pool.query(
      `UPDATE episodes SET importance = importance * $1, timestamp = NOW() WHERE importance > $2`,
      [factor, minImportance]
    );
  }

  /**
   * 查找需要遗忘的记忆
   */
  async findForgettingCandidates(config) {
    const result = await this.pool.query(
      `SELECT * FROM episodes 
       WHERE importance < $1 
       AND (last_accessed IS NULL OR last_accessed < NOW() - INTERVAL '${config.minAge} milliseconds')
       ORDER BY importance ASC, created_at ASC
       LIMIT $2`,
      [config.importanceThreshold, config.batchSize || 100]
    );
    
    return result.rows.map(row => Memory.fromRow(row));
  }
}

module.exports = { MemoryRepository };

