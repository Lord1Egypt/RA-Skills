/**
 * 基础仓储类
 * 所有 Repository 继承此类
 */
class BaseRepository {
  constructor(pool, tableName) {
    this.pool = pool;
    this.tableName = tableName;
  }

  /**
   * 获取数据库连接（用于事务）
   */
  async getClient() {
    return await this.pool.connect();
  }

  /**
   * 根据ID查找
   */
  async findById(id) {
    const result = await this.pool.query(
      `SELECT * FROM ${this.tableName} WHERE id = $1`,
      [id]
    );
    return result.rows[0] || null;
  }

  /**
   * 查找所有
   */
  async findAll(options = {}) {
    const { limit = 100, offset = 0, orderBy = 'created_at DESC' } = options;
    
    const result = await this.pool.query(
      `SELECT * FROM ${this.tableName} ORDER BY ${orderBy} LIMIT $1 OFFSET $2`,
      [limit, offset]
    );
    
    return result.rows;
  }

  /**
   * 统计数量
   */
  async count() {
    const result = await this.pool.query(
      `SELECT COUNT(*) as count FROM ${this.tableName}`
    );
    return parseInt(result.rows[0].count);
  }

  /**
   * 删除
   */
  async delete(id) {
    const result = await this.pool.query(
      `DELETE FROM ${this.tableName} WHERE id = $1 RETURNING id`,
      [id]
    );
    return result.rows.length > 0;
  }

  /**
   * 批量删除
   */
  async deleteMany(ids) {
    if (ids.length === 0) return 0;
    
    const result = await this.pool.query(
      `DELETE FROM ${this.tableName} WHERE id = ANY($1) RETURNING id`,
      [ids]
    );
    
    return result.rows.length;
  }

  /**
   * 检查是否存在
   */
  async exists(id) {
    const result = await this.pool.query(
      `SELECT 1 FROM ${this.tableName} WHERE id = $1 LIMIT 1`,
      [id]
    );
    return result.rows.length > 0;
  }
}

module.exports = { BaseRepository };

