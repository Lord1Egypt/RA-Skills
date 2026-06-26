/**
 * Cognitive Brain v5.0 主入口
 */
const { getPool } = require('../scripts/core/db.cjs');
const { MemoryService } = require('./services/MemoryService.js');
const { ConceptService } = require('./services/ConceptService.js');
const { AssociationService } = require('./services/AssociationService.js');
const { UnitOfWork } = require('./repositories/UnitOfWork.js');

class CognitiveBrain {
  constructor(pool = null) {
    this.pool = pool || getPool();
    this.memory = new MemoryService(this.pool);
    this.concept = new ConceptService(this.pool);
    this.association = new AssociationService(this.pool);
  }

  /**
   * 编码记忆（主API）
   */
  async encode(content, metadata = {}) {
    return await this.memory.encode(content, metadata);
  }

  /**
   * 检索记忆（主API）
   */
  async recall(query, options = {}) {
    return await this.memory.recall(query, options);
  }

  /**
   * 执行事务
   */
  async transaction(fn) {
    return await UnitOfWork.withTransaction(this.pool, fn);
  }

  /**
   * 获取统计
   */
  async stats() {
    const [memoryStats, conceptStats] = await Promise.all([
      this.memory.getStats(),
      this.concept.getStats()
    ]);
    
    return {
      memory: memoryStats,
      concept: conceptStats
    };
  }
}

// 单例模式
let brainInstance = null;

function getBrain() {
  if (!brainInstance) {
    brainInstance = new CognitiveBrain();
  }
  return brainInstance;
}

module.exports = { CognitiveBrain, getBrain };

// CLI 支持
if (require.main === module) {
  async function main() {
    const brain = new CognitiveBrain();
    const stats = await brain.stats();
    console.log('Cognitive Brain Stats:', JSON.stringify(stats, null, 2));
  }
  
  main().catch(console.error);
}

