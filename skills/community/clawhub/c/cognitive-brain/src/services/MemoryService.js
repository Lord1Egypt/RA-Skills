/**
 * 记忆服务
 * 处理记忆相关的业务逻辑
 */
const { Memory } = require('../domain/Memory');
const { MemoryRepository } = require('../repositories/MemoryRepository');
const { ConceptRepository } = require('../repositories/ConceptRepository');
const { AssociationRepository } = require('../repositories/AssociationRepository');
const { UnitOfWork } = require('../repositories/UnitOfWork');

// v4.x 遗留功能模块
const { extractEntities } = require('../../scripts/core/entity_extractor.cjs');
const { analyzeEmotion, detectExplicitIntent } = require('../../scripts/core/emotion_analyzer.cjs');
const { calculateImportance, selectLayer } = require('../../scripts/core/importance_calculator.cjs');
const { getEmbeddingService } = require('../../scripts/core/embedding_service.cjs');
const { hybridSearch } = require('../../scripts/core/search_strategies.cjs');
const { predictAndPreload } = require('../../scripts/core/prediction_client.cjs');
const { getCache, setCache } = require('../../scripts/core/cache.cjs');
const { Association } = require('../domain/Association');
const { metrics } = require('../utils/metrics.cjs');
const { getCircuitBreaker } = require('../utils/circuit_breaker.cjs');
const { CONSTANTS } = require('../utils/constants.cjs');
const { createLogger } = require('../utils/logger.cjs');
const logger = createLogger('MemoryService');

class MemoryService {
  constructor(pool) {
    this.pool = pool;
    this.memoryRepo = new MemoryRepository(pool);
    this.conceptRepo = new ConceptRepository(pool);
    this.embeddingService = null;
    
    // 限流状态（使用 Map 存储每个 IP 的限流状态，避免并发问题）
    this.rateLimitMap = new Map();
    
    // 熔断器
    this.dbBreaker = getCircuitBreaker('database', {
      failureThreshold: CONSTANTS.CIRCUIT_BREAKER.FAILURE_THRESHOLD,
      successThreshold: CONSTANTS.CIRCUIT_BREAKER.SUCCESS_THRESHOLD,
      timeout: CONSTANTS.CIRCUIT_BREAKER.TIMEOUT_MS
    });
  }

  /**
   * 限流检查（基于 IP，避免并发问题）
   */
  checkRateLimit(clientId = 'default') {
    const now = Date.now();
    let clientData = this.rateLimitMap.get(clientId);
    
    if (!clientData || now - clientData.resetTime > CONSTANTS.ENCODING.RATE_LIMIT_WINDOW_MS) {
      // 重置或新建
      clientData = { count: 0, resetTime: now };
    }
    
    clientData.count++;
    this.rateLimitMap.set(clientId, clientData);
    
    // 检查是否超过限制
    if (clientData.count > CONSTANTS.ENCODING.RATE_LIMIT_MAX) {
      throw new Error(`Rate limit exceeded: max ${CONSTANTS.ENCODING.RATE_LIMIT_MAX} encodes per minute for client ${clientId}`);
    }
    
    // 清理过期条目（每100次检查清理一次）
    if (clientData.count % 100 === 0) {
      this.cleanupRateLimitMap();
    }
  }
  
  /**
   * 清理过期限流条目
   */
  cleanupRateLimitMap() {
    const now = Date.now();
    for (const [key, data] of this.rateLimitMap) {
      if (now - data.resetTime > CONSTANTS.ENCODING.RATE_LIMIT_WINDOW_MS * 2) {
        this.rateLimitMap.delete(key);
      }
    }
  }

  /**
   * 获取 embedding 服务（懒加载）
   */
  async getEmbeddingService() {
    if (!this.embeddingService) {
      this.embeddingService = await getEmbeddingService();
    }
    return this.embeddingService;
  }

  /**
   * 编码记忆（创建新记忆）- 完整版
   */
  async encode(content, metadata = {}, clientId = 'default') {
    const timer = metrics.startTimer('encode_duration');

    try {
      // 0. 限流检查
      this.checkRateLimit(clientId);

      // 1. 提取实体
    const entities = metadata.entities || extractEntities(content);
    
    // 2. 情感分析
    const emotion = analyzeEmotion(content);
    
    // 3. 意图检测
    const intent = detectExplicitIntent(content);
    
    // 4. 计算重要性（如果未提供）
    const importance = metadata.importance !== undefined 
      ? metadata.importance 
      : calculateImportance({ content, emotion, intent, entities });
    
    // 5. 选择存储层
    const layers = selectLayer(importance);
    
    // 6. 生成 embedding
    let embedding = null;
    try {
      const embeddingService = await this.getEmbeddingService();
      if (embeddingService && embeddingService.embed) {
        embedding = await embeddingService.embed(content);
      }
    } catch (e) {
      logger.warn('Embedding 生成失败', { error: e.message });
    }

    // 7. 创建记忆实体
    const memory = new Memory({
      content,
      type: metadata.type || 'episodic',
      importance,
      sourceChannel: metadata.sourceChannel || 'unknown',
      role: metadata.role || 'user',
      entities,
      emotion,
      intent,
      embedding,
      layers
    });

    // 8. 使用事务保存记忆和提取概念（带熔断器保护）
    await this.dbBreaker.execute(async () => {
      await UnitOfWork.withTransaction(this.pool, async (uow) => {
        // 保存记忆
        const memRepo = new MemoryRepository(uow.getQueryClient());
        await memRepo.create(memory);

        // 提取并保存概念（批量优化）
        const conceptRepo = new ConceptRepository(uow.getQueryClient());
        const assocRepo = new AssociationRepository(uow.getQueryClient());

        // 限制最多 N 个实体，避免关联爆炸
        const limitedEntities = entities.slice(0, CONSTANTS.ENCODING.MAX_ASSOC_ENTITIES);

        // 批量创建概念（单次查询）
        const savedConcepts = await conceptRepo.createMany(limitedEntities, 'extracted');
        const conceptIds = savedConcepts.map(c => c.id);

        // 批量建立概念关联（单次查询）
        if (conceptIds.length > 1) {
          const associations = [];
          for (let i = 0; i < conceptIds.length; i++) {
            for (let j = i + 1; j < conceptIds.length; j++) {
              associations.push(new Association({
                fromId: conceptIds[i],
                toId: conceptIds[j],
                type: 'related',
                weight: 0.5,
                bidirectional: true
              }));
            }
          }
          await assocRepo.createMany(associations);
        }
      });
    });

      // 成功计数
      metrics.inc('memories_encoded_total');
      timer.end();
      return memory;
    } catch (error) {
      // 失败计数
      metrics.inc('encode_errors_total');
      timer.end();
      throw error;
    }
  }

  /**
   * 检索记忆 - 使用混合搜索（语义+关键词+联想）+ 缓存
   */
  async recall(query, options = {}) {
    // 1. 检查缓存
    const cacheKey = `recall:${query}:${options.limit || 10}`;
    const cached = await getCache(cacheKey);
    if (cached && !options.skipCache) {
      return cached;
    }

    // 2. 使用 hybridSearch 进行混合搜索
    const results = await hybridSearch(this.pool, query, {
      useVector: options.vector !== false,
      useKeyword: options.keyword !== false,
      useAssociation: options.association !== false,
      limit: options.limit || 10
    });

    // 3. 转换为 Memory 对象
    const memories = results.map(r => Memory.fromRow({
      id: r.id,
      content: r.content,
      summary: r.summary,
      timestamp: r.timestamp,
      importance: r.importance,
      type: r.type,
      source_channel: r.source,
      score: r.score
    }));

    // 4. 标记访问（异步，不阻塞返回）
    for (const memory of memories) {
      this.memoryRepo.markAccessed(memory.id).catch(() => {});
    }

    // 5. 写入缓存（60秒）
    await setCache(cacheKey, memories, 60);

    return memories;
  }

  /**
   * 获取高重要性记忆（教训、反思等）
   */
  async getImportantMemories(types = ['reflection', 'lesson', 'milestone'], limit = 5) {
    return await this.memoryRepo.findImportant(0.8, types, limit);
  }

  /**
   * 更新记忆重要性
   */
  async updateImportance(id, delta) {
    const memory = await this.memoryRepo.findById(id);
    if (!memory) {
      throw new Error(`Memory not found: ${id}`);
    }
    
    const newImportance = Math.max(0, Math.min(1, memory.importance + delta));
    await this.memoryRepo.update(id, { importance: newImportance });
    
    return { ...memory, importance: newImportance };
  }

  /**
   * 删除记忆
   */
  async delete(id) {
    const exists = await this.memoryRepo.exists(id);
    if (!exists) {
      throw new Error(`Memory not found: ${id}`);
    }
    
    await this.memoryRepo.delete(id);
    return true;
  }

  /**
   * 批量删除（遗忘）
   */
  async deleteMany(ids) {
    return await this.memoryRepo.deleteMany(ids);
  }

  /**
   * 获取统计信息
   */
  async getStats() {
    const total = await this.memoryRepo.count();
    const recent = await this.memoryRepo.findAll({ limit: 100 });
    
    const recentCount = recent.length;
    const avgImportance = recentCount > 0 
      ? recent.reduce((sum, m) => sum + m.importance, 0) / recentCount 
      : 0;
    
    return {
      total,
      recentCount,
      avgImportance
    };
  }

  /**
   * 预测用户下一个话题并预加载相关记忆
   */
  async predictAndPreload(userId, lastMessages = []) {
    try {
      const result = await predictAndPreload(this.pool, userId, lastMessages);
      return {
        predictions: result.predictions || [],
        preloadedMemories: result.memories || []
      };
    } catch (e) {
      logger.warn('预测失败', { error: e.message });
      return { predictions: [], preloadedMemories: [] };
    }
  }
}

module.exports = { MemoryService };

