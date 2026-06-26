/**
 * 概念服务
 */
const { Concept } = require('../domain/Concept');
const { ConceptRepository } = require('../repositories/ConceptRepository');

class ConceptService {
  constructor(pool) {
    this.pool = pool;
    this.conceptRepo = new ConceptRepository(pool);
  }

  /**
   * 创建或获取概念
   */
  async getOrCreate(name, type = 'general') {
    let concept = await this.conceptRepo.findByName(name);
    
    if (!concept) {
      concept = new Concept({ name, type });
      concept = await this.conceptRepo.create(concept);
    } else {
      // 标记访问
      await this.conceptRepo.create(concept); // 会触发 access_count ++
    }
    
    return concept;
  }

  /**
   * 批量创建概念
   */
  async createMany(names, type = 'general') {
    return await this.conceptRepo.createMany(names, type);
  }

  /**
   * 查找热门概念
   */
  async getTopConcepts(limit = 10) {
    return await this.conceptRepo.findTop(limit);
  }

  /**
   * 查找孤立概念
   */
  async getOrphanConcepts(limit = 10) {
    return await this.conceptRepo.findOrphan(limit);
  }

  /**
   * 更新概念激活度
   */
  async activate(id, value) {
    await this.conceptRepo.updateActivation(id, value);
    return await this.conceptRepo.findById(id);
  }

  /**
   * 获取概念统计
   */
  async getStats() {
    const total = await this.conceptRepo.count();
    const top = await this.conceptRepo.findTop(5);
    const orphan = await this.conceptRepo.findOrphan(5);
    
    return {
      total,
      topConcepts: top.map(c => c.name),
      orphanCount: orphan.length
    };
  }
}

module.exports = { ConceptService };

