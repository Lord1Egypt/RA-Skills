// src/storage/capsule-store.js
const Database = require('better-sqlite3');
const { AEIFValidator } = require('./validator');

class CapsuleStore {
  constructor(dbPath = 'data/engram.db') {
    this.db = new Database(dbPath);
    this.validator = new AEIFValidator();
    this._initDB();
  }

  /**
   * 初始化数据库，创建超融合表
   * @private
   */
  _initDB() {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS engram_capsules (
          capsuleId TEXT PRIMARY KEY,
          schemaVersion TEXT NOT NULL,
          category TEXT DEFAULT 'general',
          trustScore REAL DEFAULT 0.5,
          useCount INTEGER DEFAULT 0,
          tags TEXT,                     -- 存储格式: JSON Array
          vector TEXT NOT NULL,          -- 存储格式: 向量序列化 string，手动解析为数组进行暴力检索
          rawPayload TEXT NOT NULL,      -- 完整的 AEIF Capsule JSON 原始数据
          createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
          lastUsedAt DATETIME DEFAULT CURRENT_TIMESTAMP
      );
      CREATE INDEX IF NOT EXISTS idx_category ON engram_capsules(category);
      CREATE INDEX IF NOT EXISTS idx_trust ON engram_capsules(trustScore);
    `);
  }

  /**
   * 保存经验胶囊
   * @param {Object} capsule - AEIF 1.0 胶囊对象
   */
  save(capsule) {
    // 1. 数据防御验证
    this.validator.assertValid(capsule);

    // 2. 数据转换处理
    const embeddingString = JSON.stringify(capsule.triggerSignature.embedding);
    const tagsString = JSON.stringify(capsule.tags || []);

    // 3. 幂等性存入
    const stmt = this.db.prepare(`
      INSERT OR REPLACE INTO engram_capsules 
      (capsuleId, schemaVersion, category, trustScore, useCount, tags, vector, rawPayload)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `);
stmt.run(
  capsule.capsuleId,
  capsule.schemaVersion,
  capsule.category,
  capsule.trustScore,
  capsule.useCount,
  tagsString,
  embeddingString,
  JSON.stringify(capsule)
);
}

/**
* 更新胶囊的信任分
* @param {string} capsuleId - 目标 ID
* @param {number} newScore - 计算后的最新 TrustScore (0.0 - 1.0)
*/
updateTrustScore(capsuleId, newScore) {
const stmt = this.db.prepare('UPDATE engram_capsules SET trustScore = ? WHERE capsuleId = ?');
stmt.run(newScore, capsuleId);
}

/**
* V1.0 破冰级: 纯 JS 内存相似度计算（可负载 ~10k 数据级，免驱动）
...
   * @param {number[]} targetVector - 目标搜索向量
   * @param {Object} options - 检索配置 (k: 检索数量, threshold: 最低分)
   */
  findSimilar(targetVector, { k = 3, threshold = 0.82 } = {}) {
    // 拉取所有信任分通过的活跃数据到内存（如果数据量极大，后续再加分类初筛）
    const rows = this.db.prepare('SELECT capsuleId, vector, trustScore, rawPayload FROM engram_capsules WHERE trustScore > 0.35').all();

    let results = [];
    for (const row of rows) {
      const currentVector = JSON.parse(row.vector);
      const similarity = this.cosineSimilarity(targetVector, currentVector);

      // 核心算法：相关性 (70%) + 历史信用分 (30%) 加权
      const finalScore = (similarity * 0.7) + (row.trustScore * 0.3);

      if (finalScore >= threshold) {
        results.push({
          capsule: JSON.parse(row.rawPayload),
          score: finalScore
        });
      }
    }

    // 按最终分数倒序排列并返回 Top-K
    return results.sort((a, b) => b.score - a.score).slice(0, k);
  }

  /**
   * 余弦相似度计算 (极致性能优化：尽量避免重复 norm 计算)
   */
  cosineSimilarity(vecA, vecB) {
    if (vecA.length !== vecB.length) return 0;
    let dotProduct = 0, normA = 0, normB = 0;
    for (let i = 0; i < vecA.length; i++) {
      dotProduct += vecA[i] * vecB[i];
      normA += vecA[i] ** 2;
      normB += vecB[i] ** 2;
    }
    if (normA === 0 || normB === 0) return 0;
    return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
  }
}

module.exports = CapsuleStore;
