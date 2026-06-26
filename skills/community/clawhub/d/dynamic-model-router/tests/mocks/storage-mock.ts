/**
 * 存储模块Mock - 用于测试中替代真实的文件系统存储
 */

// 内存存储实现
const memoryStorage = new Map<string, any>();
const memoryStats = {
  totalSize: 0,
  fileCount: 0,
  directoryCount: 0,
  availableSpace: 1024 * 1024 * 100, // 100MB
};

export class MockStorage {
  private initialized = false;
  
  async initialize(): Promise<void> {
    console.log('[MockStorage] 初始化内存存储');
    this.initialized = true;
    return Promise.resolve();
  }
  
  async saveHistoricalPerformance(data: any): Promise<void> {
    if (!this.initialized) await this.initialize();
    const key = `historical_${Date.now()}_${Math.random()}`;
    memoryStorage.set(key, data);
    memoryStats.fileCount++;
    memoryStats.totalSize += JSON.stringify(data).length;
    return Promise.resolve();
  }
  
  async loadHistoricalPerformance(limit = 100): Promise<any[]> {
    if (!this.initialized) await this.initialize();
    const results: any[] = [];
    for (const [key, value] of memoryStorage.entries()) {
      if (key.startsWith('historical_')) {
        results.push(value);
        if (results.length >= limit) break;
      }
    }
    return Promise.resolve(results);
  }
  
  async saveLearningModel(modelId: string, data: any): Promise<void> {
    if (!this.initialized) await this.initialize();
    memoryStorage.set(`model_${modelId}`, data);
    memoryStats.fileCount++;
    memoryStats.totalSize += JSON.stringify(data).length;
    return Promise.resolve();
  }
  
  async loadLearningModel(modelId: string): Promise<any | null> {
    if (!this.initialized) await this.initialize();
    return Promise.resolve(memoryStorage.get(`model_${modelId}`) || null);
  }
  
  async getStorageStats(): Promise<any> {
    return Promise.resolve({
      ...memoryStats,
      isHealthy: true,
      lastCheck: new Date(),
    });
  }
  
  async cleanupOldData(_maxAgeHours = 24): Promise<void> {
    // 内存存储不需要清理
    return Promise.resolve();
  }
  
  async shutdown(): Promise<void> {
    memoryStorage.clear();
    this.initialized = false;
    return Promise.resolve();
  }
  
  // 测试辅助方法
  clear(): void {
    memoryStorage.clear();
    memoryStats.totalSize = 0;
    memoryStats.fileCount = 0;
  }
  
  getSize(): number {
    return memoryStorage.size;
  }
}

// 创建Mock的getStorage函数
export function getMockStorage() {
  return new MockStorage();
}

// 默认导出
export default getMockStorage;