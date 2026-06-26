/**
 * Unit of Work 模式
 * 管理事务中的多个操作
 */
const { createLogger } = require('../utils/logger.cjs');
const logger = createLogger('UnitOfWork');

class UnitOfWork {
  constructor(pool) {
    this.pool = pool;
    this.client = null;
    this.isInTransaction = false;
    this.operations = [];
  }

  /**
   * 开始事务
   */
  async begin(isolationLevel = 'READ COMMITTED') {
    if (this.isInTransaction) {
      throw new Error('Transaction already started');
    }

    // 验证隔离级别，防止 SQL 注入
    const validLevels = ['READ UNCOMMITTED', 'READ COMMITTED', 'REPEATABLE READ', 'SERIALIZABLE'];
    if (!validLevels.includes(isolationLevel)) {
      throw new Error(`Invalid isolation level: ${isolationLevel}. Must be one of: ${validLevels.join(', ')}`);
    }

    this.client = await this.pool.connect();
    await this.client.query(`BEGIN TRANSACTION ISOLATION LEVEL ${isolationLevel}`);
    this.isInTransaction = true;
    this.operations = [];
  }

  /**
   * 提交事务
   */
  async commit() {
    if (!this.isInTransaction) {
      throw new Error('No transaction to commit');
    }
    
    try {
      await this.client.query('COMMIT');
      this.operations = [];
    } finally {
      this.client.release();
      this.client = null;
      this.isInTransaction = false;
    }
  }

  /**
   * 回滚事务
   */
  async rollback() {
    if (!this.isInTransaction) {
      throw new Error('No transaction to rollback');
    }
    
    try {
      await this.client.query('ROLLBACK');
      this.operations = [];
    } finally {
      this.client.release();
      this.client = null;
      this.isInTransaction = false;
    }
  }

  /**
   * 获取查询客户端（事务中或普通连接）
   */
  getQueryClient() {
    return this.client || this.pool;
  }

  /**
   * 执行查询（自动使用事务连接）
   */
  async query(sql, params) {
    const client = this.getQueryClient();
    return await client.query(sql, params);
  }

  /**
   * 记录操作（用于审计）
   */
  recordOperation(type, entity, data) {
    this.operations.push({
      type,
      entity,
      data,
      timestamp: new Date()
    });
  }

  /**
   * 自动包装事务（带重试机制）
   */
  static async withTransaction(pool, fn, options = {}) {
    const { maxRetries = 3, retryDelay = 100 } = options;
    let lastError;
    
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      const uow = new UnitOfWork(pool);
      
      try {
        await uow.begin();
        const result = await fn(uow);
        await uow.commit();
        return result;
      } catch (error) {
        await uow.rollback();
        lastError = error;
        
        // 检测死锁和锁超时
        const isRetryable = error.code === '40P01' || // deadlock_detected
                           error.code === '55P03' || // lock_not_available
                           error.code === '40001' || // serialization_failure
                           error.message?.includes('deadlock') ||
                           error.message?.includes('lock timeout');
        
        if (!isRetryable || attempt === maxRetries) {
          throw error;
        }
        
        logger.info(`检测到死锁/锁超时，${retryDelay}ms后重试 (尝试 ${attempt + 1}/${maxRetries})`);
        await new Promise(resolve => setTimeout(resolve, retryDelay * (attempt + 1)));
      }
    }
    
    throw lastError;
  }
}

module.exports = { UnitOfWork };

