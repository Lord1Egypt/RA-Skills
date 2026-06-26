/**
 * Jest自动Mock for basic-storage模块
 */

const mockBasicStorage = {
  BasicStorage: class {
    private initialized = false;
    
    constructor(config?: any) {
      console.log('[Mock BasicStorage] 创建实例，配置:', config);
    }
    
    async initialize(): Promise<void> {
      console.log('[Mock BasicStorage] 初始化');
      this.initialized = true;
      return Promise.resolve();
    }
    
    async saveHistoricalPerformance(data: any): Promise<void> {
      console.log('[Mock BasicStorage] 保存历史性能数据');
      return Promise.resolve();
    }
    
    async loadHistoricalPerformance(limit = 100): Promise<any[]> {
      console.log('[Mock BasicStorage] 加载历史性能数据');
      return Promise.resolve([]);
    }
    
    async saveLearningModel(modelId: string, data: any): Promise<void> {
      console.log('[Mock BasicStorage] 保存学习模型:', modelId);
      return Promise.resolve();
    }
    
    async loadLearningModel(modelId: string): Promise<any | null> {
      console.log('[Mock BasicStorage] 加载学习模型:', modelId);
      return Promise.resolve(null);
    }
    
    async getStorageStats(): Promise<any> {
      return Promise.resolve({
        totalSize: 0,
        fileCount: 0,
        directoryCount: 0,
        availableSpace: 100 * 1024 * 1024,
        isHealthy: true,
        lastCheck: new Date(),
      });
    }
    
    async cleanupOldData(maxAgeHours = 24): Promise<void> {
      return Promise.resolve();
    }
    
    async shutdown(): Promise<void> {
      this.initialized = false;
      return Promise.resolve();
    }
  },
  
  getStorage: function(config?: any) {
    console.log('[Mock getStorage] 调用，配置:', config);
    return new mockBasicStorage.BasicStorage(config);
  },
  
  reinitializeStorage: function(config?: any) {
    console.log('[Mock reinitializeStorage] 调用，配置:', config);
    return new mockBasicStorage.BasicStorage(config);
  }
};

export const BasicStorage = mockBasicStorage.BasicStorage;
export const getStorage = mockBasicStorage.getStorage;
export const reinitializeStorage = mockBasicStorage.reinitializeStorage;
export default mockBasicStorage.getStorage;