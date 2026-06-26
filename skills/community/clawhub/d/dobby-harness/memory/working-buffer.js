/**
 * Working Buffer - 工作缓冲区机制
 * 
 * 功能：
 * - 防止上下文丢失
 * - 保存中间状态
 * - 支持会话恢复
 * - 自动持久化
 * 
 * @example
 * const buffer = new WorkingBuffer('./memory/buffer');
 * 
 * await buffer.set('task-123', { status: 'running', data: {...} });
 * await buffer.save();
 * 
 * // 恢复
 * const state = await buffer.get('task-123');
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync, readdirSync, unlinkSync } from 'fs';
import { join } from 'path';

// ============================================================================
// 配置
// ============================================================================

const DEFAULT_CONFIG = {
  bufferDir: './memory/buffer',
  autoSave: true,
  autoSaveInterval: 60000,  // 60 秒
  maxAge: 7 * 24 * 60 * 60 * 1000,  // 7 天
  enableCompression: false,
};

// ============================================================================
// 缓冲区条目
// ============================================================================

class BufferEntry {
  constructor(key, value, metadata = {}) {
    this.key = key;
    this.value = value;
    this.createdAt = Date.now();
    this.updatedAt = Date.now();
    this.accessCount = 0;
    this.lastAccessedAt = null;
    this.metadata = metadata;
    this.version = 1;
  }

  update(value) {
    this.value = value;
    this.updatedAt = Date.now();
    this.version++;
  }

  touch() {
    this.accessCount++;
    this.lastAccessedAt = Date.now();
  }

  isExpired(maxAge) {
    return Date.now() - this.updatedAt > maxAge;
  }

  toJSON() {
    return {
      key: this.key,
      value: this.value,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
      accessCount: this.accessCount,
      lastAccessedAt: this.lastAccessedAt,
      metadata: this.metadata,
      version: this.version,
    };
  }

  static fromJSON(obj) {
    const entry = new BufferEntry(obj.key, obj.value, obj.metadata);
    entry.createdAt = obj.createdAt;
    entry.updatedAt = obj.updatedAt;
    entry.accessCount = obj.accessCount;
    entry.lastAccessedAt = obj.lastAccessedAt;
    entry.version = obj.version;
    return entry;
  }
}

// ============================================================================
// Working Buffer 类
// ============================================================================

export class WorkingBuffer {
  constructor(config = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.bufferDir = this.config.bufferDir;
    
    // 确保目录存在
    if (!existsSync(this.bufferDir)) {
      mkdirSync(this.bufferDir, { recursive: true });
    }
    
    // 内存中的缓冲区
    this.entries = new Map();
    
    // 自动保存定时器
    this.saveTimer = null;
    
    // 加载现有数据
    this.load();
    
    // 启动自动保存
    if (this.config.autoSave) {
      this.startAutoSave();
    }
  }

  /**
   * 设置键值
   */
  async set(key, value, metadata = {}) {
    const entry = this.entries.get(key);
    
    if (entry) {
      entry.update(value);
      if (metadata) {
        entry.metadata = { ...entry.metadata, ...metadata };
      }
    } else {
      this.entries.set(key, new BufferEntry(key, value, metadata));
    }
    
    // 立即保存（如果启用）
    if (this.config.autoSave) {
      await this.save();
    }
    
    return { key, version: entry?.version || 1 };
  }

  /**
   * 获取键值
   */
  async get(key, options = {}) {
    const entry = this.entries.get(key);
    
    if (!entry) {
      return { found: false, value: null };
    }
    
    // 检查是否过期
    if (entry.isExpired(this.config.maxAge)) {
      await this.delete(key);
      return { found: false, value: null, expired: true };
    }
    
    entry.touch();
    
    if (options.withMetadata) {
      return {
        found: true,
        value: entry.value,
        metadata: entry.metadata,
        createdAt: entry.createdAt,
        updatedAt: entry.updatedAt,
        version: entry.version,
      };
    }
    
    return { found: true, value: entry.value };
  }

  /**
   * 删除键值
   */
  async delete(key) {
    const deleted = this.entries.delete(key);
    
    if (deleted && this.config.autoSave) {
      await this.save();
    }
    
    return deleted;
  }

  /**
   * 检查键是否存在
   */
  async has(key) {
    const entry = this.entries.get(key);
    
    if (!entry) {
      return false;
    }
    
    if (entry.isExpired(this.config.maxAge)) {
      await this.delete(key);
      return false;
    }
    
    return true;
  }

  /**
   * 获取所有键
   */
  keys() {
    return Array.from(this.entries.keys());
  }

  /**
   * 获取所有值
   */
  values() {
    return Array.from(this.entries.values()).map(e => e.value);
  }

  /**
   * 获取所有条目
   */
  entries() {
    return Array.from(this.entries.entries());
  }

  /**
   * 获取大小
   */
  size() {
    return this.entries.size;
  }

  /**
   * 清空缓冲区
   */
  async clear() {
    this.entries.clear();
    await this.save();
  }

  /**
   * 保存到磁盘
   */
  async save() {
    const data = {
      version: 1,
      timestamp: Date.now(),
      count: this.entries.size,
      entries: {},
    };
    
    for (const [key, entry] of this.entries) {
      data.entries[key] = entry.toJSON();
    }
    
    const filePath = join(this.bufferDir, 'buffer.json');
    const content = JSON.stringify(data, null, 2);
    writeFileSync(filePath, content);
    
    return { saved: true, count: this.entries.size };
  }

  /**
   * 从磁盘加载
   */
  async load() {
    const filePath = join(this.bufferDir, 'buffer.json');
    
    if (!existsSync(filePath)) {
      return { loaded: false, reason: 'File not found' };
    }
    
    try {
      const content = readFileSync(filePath, 'utf-8');
      const data = JSON.parse(content);
      
      for (const [key, obj] of Object.entries(data.entries || {})) {
        const entry = BufferEntry.fromJSON(obj);
        
        // 检查是否过期
        if (!entry.isExpired(this.config.maxAge)) {
          this.entries.set(key, entry);
        }
      }
      
      return {
        loaded: true,
        count: this.entries.size,
        timestamp: data.timestamp,
      };
    } catch (error) {
      console.error('[WorkingBuffer] Load error:', error);
      return { loaded: false, error: error.message };
    }
  }

  /**
   * 启动自动保存
   */
  startAutoSave() {
    if (this.saveTimer) {
      clearInterval(this.saveTimer);
    }
    
    this.saveTimer = setInterval(async () => {
      await this.save();
    }, this.config.autoSaveInterval);
  }

  /**
   * 停止自动保存
   */
  stopAutoSave() {
    if (this.saveTimer) {
      clearInterval(this.saveTimer);
      this.saveTimer = null;
    }
  }

  /**
   * 清理过期条目
   */
  async cleanup() {
    let cleaned = 0;
    
    for (const [key, entry] of this.entries) {
      if (entry.isExpired(this.config.maxAge)) {
        this.entries.delete(key);
        cleaned++;
      }
    }
    
    if (cleaned > 0) {
      await this.save();
    }
    
    return { cleaned };
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const now = Date.now();
    let totalAccessCount = 0;
    let oldestUpdate = now;
    let newestUpdate = 0;
    
    for (const entry of this.entries.values()) {
      totalAccessCount += entry.accessCount;
      if (entry.updatedAt < oldestUpdate) oldestUpdate = entry.updatedAt;
      if (entry.updatedAt > newestUpdate) newestUpdate = entry.updatedAt;
    }
    
    return {
      count: this.entries.size,
      totalAccessCount,
      oldestUpdate: oldestUpdate < now ? new Date(oldestUpdate).toISOString() : null,
      newestUpdate: newestUpdate > 0 ? new Date(newestUpdate).toISOString() : null,
      autoSaveEnabled: this.config.autoSave,
      maxAge: this.config.maxAge / (1000 * 60 * 60) + 'h',
    };
  }

  /**
   * 导出为 JSON
   */
  export() {
    return {
      timestamp: Date.now(),
      count: this.entries.size,
      entries: Array.from(this.entries.entries()).map(([key, entry]) => entry.toJSON()),
    };
  }

  /**
   * 从 JSON 导入
   */
  import(data) {
    for (const obj of data.entries || []) {
      const entry = BufferEntry.fromJSON(obj);
      this.entries.set(entry.key, entry);
    }
    
    return { imported: data.entries?.length || 0 };
  }
}

export default WorkingBuffer;
