/**
 * 关联服务
 */
const { Association } = require('../domain/Association');
const { AssociationRepository } = require('../repositories/AssociationRepository');
const { UnitOfWork } = require('../repositories/UnitOfWork');

class AssociationService {
  constructor(pool) {
    this.pool = pool;
    this.associationRepo = new AssociationRepository(pool);
  }

  /**
   * 创建关联
   */
  async create(fromId, toId, type = 'related', weight = 0.5) {
    const association = new Association({
      fromId,
      toId,
      type,
      weight
    });

    return await this.associationRepo.create(association);
  }

  /**
   * 批量创建关联（从实体列表，优化版）
   */
  async createFromEntities(entities) {
    if (entities.length < 2) return [];

    // 构建所有关联对象
    const associations = [];
    for (let i = 0; i < entities.length; i++) {
      for (let j = i + 1; j < entities.length; j++) {
        associations.push(new Association({
          fromId: entities[i],
          toId: entities[j],
          type: 'cooccurrence',
          weight: 0.3
        }));
      }
    }

    // 批量插入（单次查询）
    return await UnitOfWork.withTransaction(this.pool, async (uow) => {
      const repo = new AssociationRepository(uow.getQueryClient());
      return await repo.createMany(associations);
    });
  }

  /**
   * 查找概念的关联网络
   */
  async getNetwork(conceptId, depth = 1) {
    const visited = new Set([conceptId]);
    const layers = [{ [conceptId]: { weight: 1.0, depth: 0 } }];
    
    for (let d = 0; d < depth; d++) {
      const currentLayer = layers[layers.length - 1];
      const nextLayer = {};
      
      for (const id of Object.keys(currentLayer)) {
        const associations = await this.associationRepo.findByConcept(id);
        
        for (const assoc of associations) {
          const neighborId = assoc.fromId === id ? assoc.toId : assoc.fromId;
          
          if (!visited.has(neighborId)) {
            visited.add(neighborId);
            const currentWeight = currentLayer[id].weight;
            nextLayer[neighborId] = {
              weight: currentWeight * assoc.weight,
              depth: d + 1,
              via: assoc
            };
          }
        }
      }
      
      if (Object.keys(nextLayer).length === 0) break;
      layers.push(nextLayer);
    }
    
    return layers;
  }

  /**
   * 查找路径
   */
  async findPath(fromId, toId, maxDepth = 3) {
    return await this.associationRepo.findPath(fromId, toId, maxDepth);
  }

  /**
   * 强化关联
   */
  async strengthen(id, factor = 0.1) {
    await this.associationRepo.updateWeight(id, factor);
    return await this.associationRepo.findById(id);
  }

  /**
   * 清理弱关联
   */
  async cleanup(threshold = 0.1) {
    return await this.associationRepo.deleteWeak(threshold);
  }

  /**
   * 衰减所有关联
   */
  async decay(factor = 0.95) {
    await this.associationRepo.decayAll(factor);
  }
}

module.exports = { AssociationService };

