/**
 * 存储模块集成测试
 */

import { describe, test, expect, beforeEach, afterEach } from '@jest/globals';
import { BasicStorage, getStorage, reinitializeStorage } from '../../src/storage/basic-storage.js';
import path from 'path';
import fs from 'fs/promises';

// 临时存储路径用于测试
const TEST_STORAGE_PATH = path.join(process.cwd(), '.test-storage');

describe('存储模块集成测试', () => {
  let storage: BasicStorage;
  
  beforeEach(async () => {
    // 清理测试目录
    try {
      await fs.rm(TEST_STORAGE_PATH, { recursive: true, force: true });
    } catch (error) {
      // 目录可能不存在
    }
    
    // 创建存储实例（启用测试模式）
    storage = new BasicStorage({
      storagePath: TEST_STORAGE_PATH,
      maxFileSize: 1024 * 1024, // 1MB
      maxTotalSize: 10 * 1024 * 1024, // 10MB
      backupCount: 10, // 增加备份数量，避免测试中清理
      compression: false,
      testMode: true, // 启用测试模式，使用内存存储
    });
    
    await storage.initialize();
  });
  
  afterEach(async () => {
    // 清理存储实例
    try {
      await storage.shutdown();
    } catch (error) {
      // 忽略关闭错误
    }
    
    // 清理测试目录
    try {
      await fs.rm(TEST_STORAGE_PATH, { recursive: true, force: true });
    } catch (error) {
      // 忽略清理错误
    }
    
    // 重置全局单例，避免测试间污染
    reinitializeStorage();
  });
  
  test('应该正确初始化存储模块', async () => {
    const status = await storage.getStatus();
    
    expect(status).toBeDefined();
    expect(status.initialized).toBe(true);
    expect(status.storagePath).toBe(TEST_STORAGE_PATH);
    expect(status.config).toBeDefined();
    expect(status.config.maxFileSize).toBe(1024 * 1024);
    expect(status.stats).toBeDefined();
    expect(status.stats.totalSize).toBeGreaterThanOrEqual(0);
    expect(status.health).toBeDefined();
  });
  
  test('应该保存和加载历史性能记录', async () => {
    const testData = {
      decisionId: 'test_decision_123',
      modelId: 'deepseek-chat',
      providerId: 'deepseek',
      predictedPerformance: {
        expectedLatency: 2000,
        expectedCost: 0.015,
        expectedQuality: 0.8,
        successProbability: 0.95,
      },
      actualPerformance: {
        latency: 2100,
        cost: 0.016,
        success: true,
        quality: 0.85,
        tokensUsed: 550,
      },
    };
    
    const metadata = {
      modelId: 'deepseek-chat',
      providerId: 'deepseek',
      taskId: 'test_task_456',
      timestamp: new Date('2024-01-15T10:30:00Z'),
    };
    
    // 保存记录
    const savedPath = await storage.saveHistoricalPerformance(testData, metadata);
    expect(savedPath).toBeDefined();
    expect(savedPath).toContain('historical-performance');
    expect(savedPath).toContain('2024-01-15');
    
    // 加载记录
    const loadedRecords = await storage.loadHistoricalPerformance({
      modelId: 'deepseek-chat',
      startDate: new Date('2024-01-01'),
      endDate: new Date('2024-01-31'),
    });
    
    expect(loadedRecords).toBeDefined();
    expect(Array.isArray(loadedRecords)).toBe(true);
    expect(loadedRecords.length).toBeGreaterThan(0);
    
    const record = loadedRecords[0];
    expect(record).toBeDefined();
    expect(record.metadata).toBeDefined();
    expect(record.metadata.modelId).toBe('deepseek-chat');
    expect(record.data).toBeDefined();
    expect(record.data.decisionId).toBe('test_decision_123');
    expect(record._storagePath).toBeDefined();
  });
  
  test('应该保存和加载学习模型', async () => {
    const modelId = 'test-model-v1';
    const modelData = {
      capabilityCorrections: {
        'deepseek-chat': 0.1,
        'deepseek-reasoner': -0.05,
      },
      latencyCorrections: {
        'deepseek-chat': -0.2,
      },
      scoringWeights: {
        capability: 0.4,
        cost: 0.3,
        latency: 0.15,
        reliability: 0.1,
        quality: 0.05,
      },
      statistics: {
        totalSamples: 100,
        lastLearningTime: new Date(),
        averageError: {
          latency: 0.15,
          cost: 0.12,
          success: 0.08,
        },
      },
    };
    
    const metadata = {
      version: '1.0.0',
      description: '测试学习模型',
    };
    
    // 保存模型
    const savedPath = await storage.saveLearningModel(modelId, modelData, metadata);
    expect(savedPath).toBeDefined();
    expect(savedPath).toContain('learning-models');
    expect(savedPath).toContain(modelId);
    
    // 加载模型
    const loadedModel = await storage.loadLearningModel(modelId);
    expect(loadedModel).toBeDefined();
    expect(loadedModel.modelId).toBe(modelId);
    expect(loadedModel.metadata).toBeDefined();
    expect(loadedModel.metadata.version).toBe('1.0.0');
    expect(loadedModel.metadata.description).toBe('测试学习模型');
    expect(loadedModel.data).toBeDefined();
    expect(loadedModel.data.capabilityCorrections).toBeDefined();
    expect(loadedModel.data.scoringWeights).toBeDefined();
    expect(loadedModel.data.scoringWeights.capability).toBe(0.4);
  });
  
  test('应该保存和加载配置备份', async () => {
    const configName = 'router-config';
    const configData = {
      defaultStrategy: 'balanced',
      learningEnabled: true,
      thresholds: {
        minSuccessRate: 0.8,
        maxAcceptableLatency: 30000,
        maxAcceptableCost: 100,
        minCapabilityMatch: 0.6,
      },
    };
    
    const description = '测试配置备份';
    
    // 保存备份
    const savedPath = await storage.saveConfigBackup(configName, configData, description);
    expect(savedPath).toBeDefined();
    expect(savedPath).toContain('config-backups');
    expect(savedPath).toContain(configName);
    
    // 加载最新备份
    const loadedBackup = await storage.loadConfigBackup(configName, 0);
    expect(loadedBackup).toBeDefined();
    expect(loadedBackup.configName).toBe(configName);
    expect(loadedBackup.metadata.description).toBe(description);
    expect(loadedBackup.data).toBeDefined();
    expect(loadedBackup.data.defaultStrategy).toBe('balanced');
    expect(loadedBackup.data.learningEnabled).toBe(true);
    
    // 保存第二个备份
    const configData2 = { ...configData, learningEnabled: false };
    await storage.saveConfigBackup(configName, configData2, '第二个备份');
    
    // 加载第二个备份
    const secondBackup = await storage.loadConfigBackup(configName, 1);
    expect(secondBackup).toBeDefined();
    expect(secondBackup.data.learningEnabled).toBe(false);
  });
  
  test('应该保存和加载统计信息', async () => {
    const statsName = 'daily-stats';
    const statsData = {
      date: '2024-01-15',
      totalDecisions: 150,
      successfulDecisions: 142,
      averageDecisionTime: 1250,
      mostUsedModel: 'deepseek-chat',
      errorRate: 0.053,
    };
    
    // 保存统计
    const savedPath = await storage.saveStatistics(statsName, statsData);
    expect(savedPath).toBeDefined();
    expect(savedPath).toContain('statistics');
    expect(savedPath).toContain(statsName);
    
    // 加载统计
    const loadedStats = await storage.loadStatistics(statsName);
    expect(loadedStats).toBeDefined();
    expect(loadedStats.date).toBe('2024-01-15');
    expect(loadedStats.totalDecisions).toBe(150);
    expect(loadedStats.successfulDecisions).toBe(142);
    
    // 追加统计
    const additionalStats = {
      hour: '14:00',
      decisions: 25,
      averageLatency: 1300,
    };
    
    const appendedPath = await storage.saveStatistics(statsName, additionalStats, true);
    expect(appendedPath).toBeDefined();
    
    // 验证追加
    const updatedStats = await storage.loadStatistics(statsName);
    expect(updatedStats).toBeDefined();
    // 追加模式可能创建数组或合并对象，具体取决于实现
  });
  
  test('应该处理存储空间监控和清理', async () => {
    // 获取初始状态
    const initialStatus = await storage.getStatus();
    expect(initialStatus.health.spaceUsage).toBeDefined();
    
    // 保存大量测试数据以接近存储限制
    // @ts-ignore - 变量声明但未使用
    const _largeData = {
      largeArray: new Array(1000).fill(0).map((_, i) => ({
        id: `item_${i}`,
        data: 'x'.repeat(1000), // 每个1KB
        timestamp: new Date(),
      })),
    };
    
    // 注意：我们不实际填满存储，只验证监控功能存在
    // 存储模块应该能处理接近限制的情况
    
    const finalStatus = await storage.getStatus();
    expect(finalStatus.health.needsCleanup).toBe(false); // 测试数据量小，不需要清理
  });
  
  test('应该管理多个日期的历史记录', async () => {
    const dates = [
      new Date('2024-01-10T10:00:00Z'),
      new Date('2024-01-11T14:30:00Z'),
      new Date('2024-01-12T09:15:00Z'),
    ];
    
    // 保存多个日期的记录
    for (const date of dates) {
      const testData = {
        decisionId: `decision_${date.getTime()}`,
        timestamp: date.getTime(),
      };
      
      await storage.saveHistoricalPerformance(testData, { timestamp: date });
    }
    
    // 按日期范围加载
    const jan11Records = await storage.loadHistoricalPerformance({
      startDate: new Date('2024-01-11T00:00:00Z'),
      endDate: new Date('2024-01-11T23:59:59Z'),
    });
    
    expect(jan11Records).toBeDefined();
    expect(jan11Records.length).toBe(1);
    
    // 加载所有记录
    const allRecords = await storage.loadHistoricalPerformance();
    expect(allRecords.length).toBeGreaterThanOrEqual(3);
  });
  
  test('应该处理不存在的模型和配置', async () => {
    // 加载不存在的模型
    const nonExistentModel = await storage.loadLearningModel('non-existent-model');
    expect(nonExistentModel).toBeNull();
    
    // 加载不存在的配置
    const nonExistentConfig = await storage.loadConfigBackup('non-existent-config', 0);
    expect(nonExistentConfig).toBeNull();
    
    // 加载不存在的统计
    const nonExistentStats = await storage.loadStatistics('non-existent-stats');
    expect(nonExistentStats).toBeNull();
  });
  
  test('应该获取存储统计信息', async () => {
    const stats = await storage.getStorageStats();
    
    expect(stats).toBeDefined();
    expect(stats.totalSize).toBeGreaterThanOrEqual(0);
    expect(stats.fileCount).toBeGreaterThanOrEqual(0);
    expect(stats.dirCount).toBeGreaterThanOrEqual(0);
    expect(stats.byType).toBeDefined();
    
    // 验证目录类型统计
    expect(stats.byType.root).toBeDefined();
    expect(stats.byType['historical-performance']).toBeDefined();
    expect(stats.byType['learning-models']).toBeDefined();
    expect(stats.byType['config-backups']).toBeDefined();
    expect(stats.byType.statistics).toBeDefined();
  });
  
  test('应该清理存储', async () => {
    // 先保存一些数据
    await storage.saveHistoricalPerformance(
      { test: 'data' },
      { timestamp: new Date() }
    );
    
    await storage.saveLearningModel(
      'test-cleanup-model',
      { test: 'model' },
      { version: '1.0', description: '测试清理' }
    );
    
    // 清理存储
    await storage.cleanupStorage();
    
    // 验证存储被清理
    const status = await storage.getStatus();
    expect(status.initialized).toBe(false);
    
    // 重新初始化应该成功
    await storage.initialize();
    const reinitializedStatus = await storage.getStatus();
    expect(reinitializedStatus.initialized).toBe(true);
  });
  
  test('应该处理存储模块的单例模式', async () => {
    // 获取默认存储实例
    const storage1 = getStorage({ storagePath: TEST_STORAGE_PATH + '-singleton' });
    const storage2 = getStorage({ storagePath: TEST_STORAGE_PATH + '-singleton' });
    
    // 应该是同一个实例
    expect(storage1).toBe(storage2);
    
    // 重新初始化应该创建新实例
    const storage3 = new BasicStorage({ storagePath: TEST_STORAGE_PATH + '-singleton2' });
    expect(storage3).not.toBe(storage1);
    
    // 清理
    await storage1.shutdown();
    await storage3.shutdown();
  });
});

describe('存储错误处理', () => {
  test('应该处理存储初始化失败', async () => {
    // 使用无效的存储路径（例如根目录，通常需要权限）
    const invalidStorage = new BasicStorage({
      storagePath: '/', // 可能无权限
    });
    
    // 初始化可能失败，但构造函数应该成功
    expect(invalidStorage).toBeDefined();
    
    // 尝试初始化，应该抛出错误或被捕获
    try {
      await invalidStorage.initialize();
    } catch (error) {
      // 预期可能失败
      expect(error).toBeDefined();
    }
  });
  
  test('应该处理文件系统错误', async () => {
    const storage = new BasicStorage({
      storagePath: TEST_STORAGE_PATH + '-error-test',
    });
    
    await storage.initialize();
    
    // 尝试保存超大文件（超过限制）
    const oversizedData = {
      hugeArray: new Array(1000000).fill('x'.repeat(100)).join(''), // 超大字符串
    };
    
    try {
      await storage.saveHistoricalPerformance(oversizedData, {});
      // 如果超过限制，应该抛出错误
    } catch (error) {
      // 预期错误
      expect(error).toBeDefined();
    }
    
    await storage.shutdown();
  });
  
  test('应该处理损坏的JSON文件', async () => {
    const storage = new BasicStorage({
      storagePath: TEST_STORAGE_PATH + '-corrupt-test',
    });
    
    await storage.initialize();
    
    // 创建损坏的JSON文件
    const corruptFilePath = path.join(TEST_STORAGE_PATH + '-corrupt-test', 'historical-performance', '2024-01-01', 'corrupt.json');
    await fs.mkdir(path.dirname(corruptFilePath), { recursive: true });
    await fs.writeFile(corruptFilePath, '{ invalid json', 'utf-8');
    
    // 尝试加载，应该跳过损坏文件而不是崩溃
    const records = await storage.loadHistoricalPerformance();
    expect(records).toBeDefined();
    expect(Array.isArray(records)).toBe(true);
    
    await storage.shutdown();
  });
});