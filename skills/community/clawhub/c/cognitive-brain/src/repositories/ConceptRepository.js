/**
 * 概念仓储
 */
const { BaseRepository } = require('./BaseRepository');
const { Concept } = require('../domain/Concept');

class ConceptRepository extends BaseRepository {
  constructor(pool) {
    super(pool, 'concepts');
  }

  /**
   * 创建概念
   */
  async create(concept) {
    const result = await this.pool.query(
      `INSERT INTO concepts (id, name, type, attributes, importance, activation, access_count, last_accessed, embedding, created_at, last_updated)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
       ON CONFLICT (name) DO UPDATE SET
         access_count = concepts.access_count + 1,
         last_accessed = NOW(),
         last_updated = NOW()
       RETURNING *`,
      [
        concept.id,
        concept.name,
        concept.type,
        JSON.stringify(concept.attributes),
        concept.importance,
        concept.activation,
        concept.accessCount,
        concept.lastAccessed,
        concept.embedding,
        concept.createdAt,
        concept.updatedAt || new Date()
      ]
    );
    
    return Concept.fromRow(result.rows[0]);
  }

  /**
   * 根据名称查找
   */
  async findByName(name) {
    const result = await this.pool.query(
      `SELECT * FROM concepts WHERE name = $1`,
      [name]
    );
    
    return result.rows[0] ? Concept.fromRow(result.rows[0]) : null;
  }

  /**
   * 批量创建概念（优化版，单次查询）
   */
  async createMany(names, type = 'general') {
    if (names.length === 0) return [];

    // 使用 UNNEST 进行真正的批量插入
    const result = await this.pool.query(
      `INSERT INTO concepts (id, name, type, attributes, importance, activation, access_count, last_accessed, created_at, last_updated)
       SELECT 
         gen_random_uuid(),
         unnest($1::text[]),
         $2,
         '{}',
         0.5,
         0.0,
         1,
         NOW(),
         NOW(),
         NOW()
       ON CONFLICT (name) DO UPDATE SET
         access_count = concepts.access_count + 1,
         last_accessed = NOW(),
         last_updated = NOW()
       RETURNING *`,
      [names, type]
    );

    return result.rows.map(row => Concept.fromRow(row));
  }

  /**
   * 更新激活度
   */
  async updateActivation(id, activation) {
    await this.pool.query(
      `UPDATE concepts SET activation = $1, updated_at = NOW() WHERE id = $2`,
      [activation, id]
    );
  }

  /**
   * 查找热门概念
   */
  async findTop(limit = 10) {
    const result = await this.pool.query(
      `SELECT * FROM concepts ORDER BY access_count DESC LIMIT $1`,
      [limit]
    );
    
    return result.rows.map(row => Concept.fromRow(row));
  }

  /**
   * 查找孤立概念（无关联）
   */
  async findOrphan(limit = 10) {
    const result = await this.pool.query(
      `SELECT c.* FROM concepts c
       LEFT JOIN associations a ON c.id = a.from_id OR c.id = a.to_id
       WHERE a.id IS NULL
       LIMIT $1`,
      [limit]
    );
    
    return result.rows.map(row => Concept.fromRow(row));
  }

  /**
   * 查找最近访问的概念
   */
  async findRecent(limit = 10) {
    const result = await this.pool.query(
      `SELECT * FROM concepts 
       WHERE last_accessed IS NOT NULL
       ORDER BY last_accessed DESC 
       LIMIT $1`,
      [limit]
    );
    
    return result.rows.map(row => Concept.fromRow(row));
  }
}

module.exports = { ConceptRepository };

