/**
 * EVA Soul - 记忆系统模块
 */

const fs = require('fs');
const path = require('path');
const { expandPath } = require('../core/config');

/**
 * 记忆层级
 */
const MEMORY_TIERS = {
  short: {
    name: '短期记忆',
    maxAge: 7 * 24 * 60 * 60 * 1000, // 7天
    maxItems: 100
  },
  medium: {
    name: '中期记忆',
    maxAge: 30 * 24 * 60 * 60 * 1000, // 30天
    maxItems: 500
  },
  long: {
    name: '长期记忆',
    maxAge: 90 * 24 * 60 * 60 * 1000, // 90天
    maxItems: 1000
  },
  archive: {
    name: '归档存储',
    maxAge: null, // 无限制
    maxItems: null
  }
};

/**
 * 记忆类型
 */
const MEMORY_TYPES = {
  conversation: { name: '对话', priority: 3 },
  fact: { name: '事实', priority: 7 },
  preference: { name: '偏好', priority: 8 },
  event: { name: '事件', priority: 5 },
  instruction: { name: '指令', priority: 9 },
  emotion: { name: '情感', priority: 6 },
  relationship: { name: '关系', priority: 8 },
  knowledge: { name: '知识', priority: 4 }
};

/**
 * 记忆接口
 */
class MemoryStore {
  constructor(memoryPath) {
    this.memoryPath = expandPath(memoryPath);
    this.ensureDirectories();
  }
  
  /**
   * 确保目录存在
   */
  ensureDirectories() {
    const dirs = ['', 'short', 'medium', 'long', 'archive', 'auto'];
    for (const dir of dirs) {
      const fullPath = path.join(this.memoryPath, dir);
      if (!fs.existsSync(fullPath)) {
        fs.mkdirSync(fullPath, { recursive: true });
      }
    }
  }
  
  /**
   * 保存记忆
   */
  save(memory) {
    const {
      content,
      type = 'fact',
      importance = 5,
      tags = [],
      metadata = {}
    } = memory;
    
    const id = this.generateId();
    const now = new Date().toISOString();
    
    const memoryEntry = {
      id,
      content,
      type,
      importance,
      tags,
      metadata,
      createdAt: now,
      updatedAt: now,
      accessedAt: now,
      accessCount: 0,
      tier: 'short'
    };
    
    // 保存到文件
    const fileName = `memory-${id}.json`;
    const filePath = path.join(this.memoryPath, 'short', fileName);
    
    fs.writeFileSync(filePath, JSON.stringify(memoryEntry, null, 2));
    
    return { id, ...memoryEntry };
  }
  
  /**
   * 查询记忆
   */
  search(query, options = {}) {
    const { limit = 10, minImportance = 0, types = [] } = options;
    
    const results = [];
    const tiers = ['short', 'medium', 'long'];
    
    for (const tier of tiers) {
      const tierPath = path.join(this.memoryPath, tier);
      if (!fs.existsSync(tierPath)) continue;
      
      const files = fs.readdirSync(tierPath).filter(f => f.endsWith('.json'));
      
      for (const file of files) {
        try {
          const content = fs.readFileSync(path.join(tierPath, file), 'utf8');
          const memory = JSON.parse(content);
          
          // 过滤
          if (memory.importance < minImportance) continue;
          if (types.length > 0 && !types.includes(memory.type)) continue;
          
          // 搜索
          if (query) {
            const lowerQuery = query.toLowerCase();
            if (!memory.content.toLowerCase().includes(lowerQuery) &&
                !memory.tags.some(t => t.toLowerCase().includes(lowerQuery))) {
              continue;
            }
          }
          
          // 计算相关性
          const relevance = this.calculateRelevance(memory, query);
          
          results.push({ ...memory, relevance, tier });
        } catch (e) {
          // ignore
        }
      }
    }
    
    // 排序并返回
    return results
      .sort((a, b) => b.relevance - a.relevance || b.importance - a.importance)
      .slice(0, limit);
  }
  
  /**
   * 获取记忆
   */
  get(id) {
    const tiers = ['short', 'medium', 'long', 'archive'];
    
    for (const tier of tiers) {
      const filePath = path.join(this.memoryPath, tier, `memory-${id}.json`);
      if (fs.existsSync(filePath)) {
        try {
          const content = fs.readFileSync(filePath, 'utf8');
          const memory = JSON.parse(content);
          
          // 更新访问信息
          memory.accessedAt = new Date().toISOString();
          memory.accessCount = (memory.accessCount || 0) + 1;
          fs.writeFileSync(filePath, JSON.stringify(memory, null, 2));
          
          return memory;
        } catch (e) {
          return null;
        }
      }
    }
    
    return null;
  }
  
  /**
   * 删除记忆
   */
  delete(id) {
    const tiers = ['short', 'medium', 'long', 'archive'];
    
    for (const tier of tiers) {
      const filePath = path.join(this.memoryPath, tier, `memory-${id}.json`);
      if (fs.existsSync(filePath)) {
        fs.unlinkSync(filePath);
        return true;
      }
    }
    
    return false;
  }
  
  /**
   * 升级/降级记忆层级
   */
  upgradeTier(id) {
    const memory = this.get(id);
    if (!memory) return null;
    
    const tiers = ['short', 'medium', 'long', 'archive'];
    const currentIndex = tiers.indexOf(memory.tier);
    
    if (currentIndex < tiers.length - 1) {
      const newTier = tiers[currentIndex + 1];
      return this.moveToTier(id, newTier);
    }
    
    return memory;
  }
  
  /**
   * 移动到指定层级
   */
  moveToTier(id, newTier) {
    const tiers = ['short', 'medium', 'long', 'archive'];
    if (!tiers.includes(newTier)) return null;
    
    // 从原位置删除
    const oldTiers = ['short', 'medium', 'long', 'archive'];
    let found = false;
    
    for (const tier of oldTiers) {
      const oldPath = path.join(this.memoryPath, tier, `memory-${id}.json`);
      if (fs.existsSync(oldPath)) {
        const content = fs.readFileSync(oldPath, 'utf8');
        const memory = JSON.parse(content);
        
        memory.tier = newTier;
        memory.updatedAt = new Date().toISOString();
        
        const newPath = path.join(this.memoryPath, newTier, `memory-${id}.json`);
        fs.writeFileSync(newPath, JSON.stringify(memory, null, 2));
        
        fs.unlinkSync(oldPath);
        found = true;
        break;
      }
    }
    
    if (found) {
      return this.get(id);
    }
    
    return null;
  }
  
  /**
   * 获取统计信息
   */
  getStats() {
    const stats = {
      short: 0,
      medium: 0,
      long: 0,
      archive: 0,
      total: 0,
      byType: {}
    };

    const tiers = ['short', 'medium', 'long', 'archive'];

    for (const tier of tiers) {
      const tierPath = path.join(this.memoryPath, tier);
      if (!fs.existsSync(tierPath)) continue;

      // 支持两种文件格式：memory-{id}.json 和 {tier}.json
      const files = fs.readdirSync(tierPath).filter(f => f.endsWith('.json'));
      stats[tier] = files.length;
      stats.total += files.length;

      // 统计类型
      for (const file of files) {
        try {
          const content = fs.readFileSync(path.join(tierPath, file), 'utf8');
          // 尝试解析为 memory-{id}.json 格式（有 id 字段即为有效记忆）
          const memory = JSON.parse(content);
          if (memory.id) {
            stats.byType[memory.type] = (stats.byType[memory.type] || 0) + 1;
          }
        } catch (e) {
          // ignore
        }
      }
    }

    return stats;
  }
  
  /**
   * 清理过期记忆
   */
  cleanup() {
    const now = Date.now();
    const results = { upgraded: 0, archived: 0, deleted: 0 };
    
    // 检查短期记忆
    const shortPath = path.join(this.memoryPath, 'short');
    if (fs.existsSync(shortPath)) {
      const files = fs.readdirSync(shortPath).filter(f => f.endsWith('.json'));
      
      for (const file of files) {
        try {
          const content = fs.readFileSync(path.join(shortPath, file), 'utf8');
          const memory = JSON.parse(content);
          
          const age = now - new Date(memory.createdAt).getTime();
          
          if (memory.importance >= 7 && age > MEMORY_TIERS.short.maxAge) {
            // 高重要性升级到中期
            this.upgradeTier(memory.id);
            results.upgraded++;
          } else if (age > MEMORY_TIERS.short.maxAge * 2) {
            // 过期删除
            this.delete(memory.id);
            results.deleted++;
          }
        } catch (e) {
          // ignore
        }
      }
    }
    
    return results;
  }
  
  /**
   * 生成ID
   */
  generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
  }
  
  /**
   * 计算相关性
   */
  calculateRelevance(memory, query) {
    if (!query) return memory.importance;
    
    let relevance = 0;
    const lowerQuery = query.toLowerCase();
    
    // 内容匹配
    if (memory.content.toLowerCase().includes(lowerQuery)) {
      relevance += 10;
    }
    
    // 标签匹配
    for (const tag of memory.tags || []) {
      if (tag.toLowerCase().includes(lowerQuery)) {
        relevance += 5;
      }
    }
    
    // 重要性加成
    relevance += memory.importance;
    
    // 访问频率加成
    relevance += Math.min(5, memory.accessCount || 0);
    
    return relevance;
  }
  
  /**
   * 自动记忆 (关键词触发)
   */
  autoSave(message, emotion = 'neutral') {
    const autoKeywords = [
      { keyword: '记住', type: 'instruction', importance: 9 },
      { keyword: '喜欢', type: 'preference', importance: 7 },
      { keyword: '讨厌', type: 'preference', importance: 7 },
      { keyword: '爱吃', type: 'preference', importance: 7 },
      { keyword: '怕', type: 'preference', importance: 7 },
      { keyword: '生日', type: 'event', importance: 9 },
      { keyword: '纪念日', type: 'event', importance: 9 },
      { keyword: '我叫', type: 'fact', importance: 8 },
      { keyword: '我是', type: 'fact', importance: 8 },
      { keyword: '别忘了', type: 'instruction', importance: 8 },
      { keyword: '提醒我', type: 'instruction', importance: 8 }
    ];
    
    for (const { keyword, type, importance } of autoKeywords) {
      if (message.toLowerCase().includes(keyword)) {
        return this.save({
          content: message,
          type,
          importance,
          tags: [keyword, 'auto'],
          metadata: { emotion, auto: true }
        });
      }
    }
    
    return null;
  }
}

module.exports = {
  MEMORY_TIERS,
  MEMORY_TYPES,
  MemoryStore
};
