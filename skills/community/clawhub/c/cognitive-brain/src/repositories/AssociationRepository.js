/**
 * 关联仓储
 */
const { BaseRepository } = require('./BaseRepository');
const { Association } = require('../domain/Association');

class AssociationRepository extends BaseRepository {
  constructor(pool) {
    super(pool, 'associations');
  }

  /**
   * 创建关联
   */
  async create(association) {
    const result = await this.pool.query(
      `INSERT INTO associations (id, from_id, to_id, type, weight, bidirectional, created_at, updated_at)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
       ON CONFLICT ON CONSTRAINT unique_association DO UPDATE SET
         weight = LEAST(1.0, associations.weight + EXCLUDED.weight),
         updated_at = NOW()
       RETURNING *`,
      [
        association.id,
        association.fromId,
        association.toId,
        association.type,
        association.weight,
        association.bidirectional,
        association.createdAt,
        association.updatedAt
      ]
    );
    
    return Association.fromRow(result.rows[0]);
  }

  /**
   * 查找概念的所有关联
   */
  async findByConcept(conceptId) {
    const result = await this.pool.query(
      `SELECT * FROM associations 
       WHERE from_id = $1 OR to_id = $1
       ORDER BY weight DESC`,
      [conceptId]
    );
    
    return result.rows.map(row => Association.fromRow(row));
  }

  /**
   * 查找两个概念间的关联
   */
  async findBetween(fromId, toId) {
    const result = await this.pool.query(
      `SELECT * FROM associations 
       WHERE (from_id = $1 AND to_id = $2) OR (from_id = $2 AND to_id = $1)`,
      [fromId, toId]
    );
    
    return result.rows.map(row => Association.fromRow(row));
  }

  /**
   * 更新权重
   */
  async updateWeight(id, delta) {
    await this.pool.query(
      `UPDATE associations 
       SET weight = LEAST(1.0, GREATEST(0.0, weight + $1)), updated_at = NOW() 
       WHERE id = $2`,
      [delta, id]
    );
  }

  /**
   * 查找最强关联
   */
  async findStrongest(conceptId, limit = 5) {
    const result = await this.pool.query(
      `SELECT * FROM associations 
       WHERE from_id = $1 OR to_id = $1
       ORDER BY weight DESC
       LIMIT $2`,
      [conceptId, limit]
    );
    
    return result.rows.map(row => Association.fromRow(row));
  }

  /**
   * 查找关联路径（广度优先）
   */
  async findPath(fromId, toId, maxDepth = 3) {
    const result = await this.pool.query(
      `WITH RECURSIVE path AS (
        SELECT from_id, to_id, weight, 1 as depth, ARRAY[from_id] as visited
        FROM associations
        WHERE from_id = $1
        
        UNION
        
        SELECT a.from_id, a.to_id, p.weight * a.weight, p.depth + 1, p.visited || a.from_id
        FROM associations a
        JOIN path p ON a.from_id = p.to_id
        WHERE p.depth < $3 AND NOT a.to_id = ANY(p.visited)
      )
      SELECT * FROM path WHERE to_id = $2 LIMIT 1`,
      [fromId, toId, maxDepth]
    );
    
    return result.rows[0] || null;
  }

  /**
   * 批量创建关联（优化版，单次查询）
   */
  async createMany(associations) {
    if (associations.length === 0) return [];

    // 构建批量插入数据
    const fromIds = associations.map(a => a.fromId);
    const toIds = associations.map(a => a.toId);
    const types = associations.map(a => a.type);
    const weights = associations.map(a => a.weight);
    const bidirectionals = associations.map(a => a.bidirectional);

    const result = await this.pool.query(
      `INSERT INTO associations (id, from_id, to_id, type, weight, bidirectional, created_at, updated_at)
       SELECT 
         gen_random_uuid(),
         unnest($1::uuid[]),
         unnest($2::uuid[]),
         unnest($3::text[]),
         unnest($4::float[]),
         unnest($5::boolean[]),
         NOW(),
         NOW()
       ON CONFLICT ON CONSTRAINT unique_association DO UPDATE SET
         weight = LEAST(1.0, associations.weight + EXCLUDED.weight),
         updated_at = NOW()
       RETURNING *`,
      [fromIds, toIds, types, weights, bidirectionals]
    );

    return result.rows.map(row => Association.fromRow(row));
  }

  /**
   * 衰减所有关联权重
   */
  async decayAll(factor = 0.95) {
    await this.pool.query(
      `UPDATE associations SET weight = weight * $1, updated_at = NOW() WHERE weight > 0.01`,
      [factor]
    );
  }

  /**
   * 删除弱关联
   */
  async deleteWeak(threshold = 0.1) {
    const result = await this.pool.query(
      `DELETE FROM associations WHERE weight < $1 RETURNING id`,
      [threshold]
    );
    
    return result.rows.length;
  }
}

module.exports = { AssociationRepository };

