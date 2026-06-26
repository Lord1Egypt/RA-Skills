/**
 * EVA Soul - 跨平台同步模块
 * 实现多设备记忆同步
 */

const fs = require('fs');
const path = require('path');
const logger = require('../../hooks/logger');

const SYNC_CONFIG = {
  enabled: true,
  centralPath: path.join(process.env.HOME || '/root', '.openclaw/workspace/memory/sync'),
  syncInterval: 60000, // 60秒同步一次
  maxConflictHistory: 100
};

/**
 * 中央存储管理器
 */
class CentralStore {
  constructor(syncPath) {
    this.syncPath = syncPath;
    this.ensureDirectories();
  }
  
  ensureDirectories() {
    const dirs = ['memories', 'devices', 'conflicts', 'logs'];
    for (const dir of dirs) {
      const fullPath = path.join(this.syncPath, dir);
      if (!fs.existsSync(fullPath)) {
        fs.mkdirSync(fullPath, { recursive: true });
      }
    }
  }
  
  // 保存中央记忆
  saveMemory(memory) {
    const file = path.join(this.syncPath, 'memories', `${memory.id}.json`);
    memory.updatedAt = new Date().toISOString();
    fs.writeFileSync(file, JSON.stringify(memory, null, 2));
    return memory;
  }
  
  // 获取所有中央记忆
  getAllMemories() {
    const dir = path.join(this.syncPath, 'memories');
    if (!fs.existsSync(dir)) return [];
    
    const files = fs.readdirSync(dir).filter(f => f.endsWith('.json'));
    const memories = [];
    
    for (const file of files) {
      try {
        const data = JSON.parse(fs.readFileSync(path.join(dir, file), 'utf8'));
        memories.push(data);
      } catch (e) {}
    }
    
    return memories;
  }
  
  // 注册设备
  registerDevice(deviceId, info) {
    const file = path.join(this.syncPath, 'devices', `${deviceId}.json`);
    const device = {
      ...info,
      registeredAt: new Date().toISOString(),
      lastSync: new Date().toISOString(),
      status: 'online'
    };
    fs.writeFileSync(file, JSON.stringify(device, null, 2));
    return device;
  }
  
  // 获取设备信息
  getDevice(deviceId) {
    const file = path.join(this.syncPath, 'devices', `${deviceId}.json`);
    if (!fs.existsSync(file)) return null;
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  }
  
  // 记录冲突
  logConflict(memoryId, localVersion, centralVersion) {
    const file = path.join(this.syncPath, 'conflicts', `${Date.now()}.json`);
    const conflict = {
      memoryId,
      localVersion,
      centralVersion,
      resolved: false,
      resolvedAt: null,
      winner: null
    };
    fs.writeFileSync(file, JSON.stringify(conflict, null, 2));
    return conflict;
  }
}

/**
 * 同步服务
 */
class SyncService {
  constructor(syncPath) {
    this.central = new CentralStore(syncPath);
    this.localPath = null;
  }
  
  // 初始化本地路径
  setLocalPath(localPath) {
    this.localPath = localPath;
  }
  
  // 获取本地记忆
  getLocalMemories(tier = 'short') {
    if (!this.localPath) return [];
    
    const file = path.join(this.localPath, tier, `${tier}.json`);
    if (!fs.existsSync(file)) return [];
    
    try {
      return JSON.parse(fs.readFileSync(file, 'utf8'));
    } catch (e) {
      return [];
    }
  }
  
  // 同步记忆
  async sync(deviceId, localMemories) {
    const centralMemories = this.central.getAllMemories();
    
    // 合并记忆（时间戳优先）
    const merged = this.mergeMemories(localMemories, centralMemories);
    
    // 保存到中央存储
    for (const m of merged) {
      this.central.saveMemory(m);
    }
    
    // 更新设备同步时间
    this.central.registerDevice(deviceId, {
      lastSync: new Date().toISOString(),
      memoryCount: merged.length
    });
    
    return {
      success: true,
      memoryCount: merged.length,
      merged: merged.length - localMemories.length
    };
  }
  
  // 合并策略：时间戳优先
  mergeMemories(local, central) {
    const all = [...local, ...central];
    const merged = {};
    
    for (const m of all) {
      const existing = merged[m.id];
      const localTime = new Date(m.updatedAt || m.created_at || 0).getTime();
      const existingTime = existing 
        ? new Date(existing.updatedAt || existing.created_at || 0).getTime()
        : 0;
      
      // 时间戳优先，保留最新的
      if (!existing || localTime > existingTime) {
        merged[m.id] = m;
      } else if (localTime !== existingTime) {
        // 记录冲突但不覆盖
        this.central.logConflict(m.id, m, existing);
      }
    }
    
    return Object.values(merged);
  }
  
  // 获取中央记忆（供其他设备下载）
  getCentralMemories(since = null) {
    let memories = this.central.getAllMemories();
    
    if (since) {
      const sinceTime = new Date(since).getTime();
      memories = memories.filter(m => 
        new Date(m.updatedAt || m.created_at || 0).getTime() > sinceTime
      );
    }
    
    return memories;
  }
}

/**
 * 设备端同步
 */
class DeviceSync {
  constructor(centralUrl, deviceId) {
    this.centralUrl = centralUrl;
    this.deviceId = deviceId;
    this.localPath = null;
    this.lastSync = null;
  }
  
  setLocalPath(localPath) {
    this.localPath = localPath;
  }
  
  // 从中央获取更新
  async pull() {
    try {
      const response = await fetch(`${this.centralUrl}/sync/pull?device=${this.deviceId}&since=${this.lastSync}`);
      const data = await response.json();
      
      if (data.memories && data.memories.length > 0) {
        // 合并到本地
        this.mergeToLocal(data.memories);
      }
      
      this.lastSync = new Date().toISOString();
      return data;
    } catch (e) {
      logger.warn(`同步失败: ${e.message}`, 'sync');
      return { error: e.message };
    }
  }
  
  // 推送到中央
  async push(localMemories) {
    try {
      const response = await fetch(`${this.centralUrl}/sync/push`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          device: this.deviceId,
          memories: localMemories
        })
      });
      return await response.json();
    } catch (e) {
      logger.warn(`推送失败: ${e.message}`, 'sync');
      return { error: e.message };
    }
  }
  
  // 合并到本地
  mergeToLocal(centralMemories) {
    if (!this.localPath) return;
    
    const tiers = ['short', 'medium', 'long'];
    
    for (const tier of tiers) {
      const localFile = path.join(this.localPath, tier, `${tier}.json`);
      let local = [];
      
      if (fs.existsSync(localFile)) {
        local = JSON.parse(fs.readFileSync(localFile, 'utf8'));
      }
      
      // 合并
      const merged = this.mergeMemories(local, centralMemories);
      fs.writeFileSync(localFile, JSON.stringify(merged, null, 2));
    }
  }
  
  mergeMemories(local, central) {
    const all = [...local, ...central];
    const merged = {};
    
    for (const m of all) {
      const existing = merged[m.id];
      const centralTime = new Date(m.updatedAt || m.created_at || 0).getTime();
      const existingTime = existing 
        ? new Date(existing.updatedAt || existing.created_at || 0).getTime()
        : 0;
      
      if (!existing || centralTime > existingTime) {
        merged[m.id] = m;
      }
    }
    
    return Object.values(merged);
  }
}

module.exports = {
  SYNC_CONFIG,
  CentralStore,
  SyncService,
  DeviceSync
};
