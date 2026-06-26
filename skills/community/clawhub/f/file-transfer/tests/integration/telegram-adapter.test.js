/**
 * Telegram适配器集成测试
 */

import { TelegramAdapter } from '../../src/adapters/telegram-adapter.js';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

describe('TelegramAdapter Integration Tests', () => {
  let adapter;
  let testFilePath;

  beforeAll(async () => {
    // 创建测试适配器
    adapter = new TelegramAdapter({
      maxFileSize: 10 * 1024 * 1024, // 10MB测试限制
      chunkSize: 1 * 1024 * 1024 // 1MB分块
    });

    // 创建测试文件
    const testDir = path.join(__dirname, '../../test-data');
    await fs.mkdir(testDir, { recursive: true });
    
    testFilePath = path.join(testDir, 'test-document.txt');
    const testContent = '这是一个测试文件内容，用于Telegram适配器集成测试。\n'.repeat(1000);
    await fs.writeFile(testFilePath, testContent, 'utf-8');
  });

  afterAll(async () => {
    // 清理测试文件
    try {
      await fs.unlink(testFilePath);
      const testDir = path.join(__dirname, '../../test-data');
      await fs.rmdir(testDir);
    } catch (error) {
      // 忽略清理错误
    }
  });

  describe('适配器初始化', () => {
    test('应该成功创建适配器实例', () => {
      expect(adapter).toBeDefined();
      expect(adapter.getInfo).toBeInstanceOf(Function);
    });

    test('应该返回正确的适配器信息', () => {
      const info = adapter.getInfo();
      
      expect(info.name).toBe('Telegram File Transfer Adapter');
      expect(info.version).toBe('0.2.0-beta');
      expect(info.platform).toBe('telegram');
      expect(info.maxFileSize).toBe(10 * 1024 * 1024);
      expect(info.coreModules.contextEngine).toBe('loaded');
      expect(info.coreModules.fileManager).toBe('loaded');
    });
  });

  describe('文件传输功能', () => {
    test('应该成功发送文件（模拟）', async () => {
      const result = await adapter.sendFile({
        filePath: testFilePath,
        chatId: '-1003655501651', // 测试群组ID
        caption: '集成测试文件',
        options: {
          disableNotification: true
        }
      });

      expect(result.success).toBe(true);
      expect(result.transferId).toBeDefined();
      expect(result.messageId).toBeDefined();
      expect(result.fileSize).toBeGreaterThan(0);
      expect(result.duration).toBeGreaterThan(0);
      expect(result.analysis).toBeDefined();
    });

    test('应该跟踪传输状态', async () => {
      const result = await adapter.sendFile({
        filePath: testFilePath,
        chatId: '123456789', // 测试私聊ID
        caption: '状态跟踪测试'
      });

      const status = adapter.getTransferStatus(result.transferId);
      
      expect(status.found).toBe(true);
      expect(status.transferId).toBe(result.transferId);
      expect(status.status).toBe('completed');
      expect(status.progress).toBe(100);
      expect(status.fileName).toBe('test-document.txt');
    });

    test('应该返回活动传输列表', () => {
      const activeTransfers = adapter.getActiveTransfers();
      
      expect(Array.isArray(activeTransfers)).toBe(true);
      // 传输会在5分钟后清理，所以这里可能有或没有活动传输
    });
  });

  describe('错误处理', () => {
    test('应该处理不存在的文件', async () => {
      await expect(
        adapter.sendFile({
          filePath: '/nonexistent/file.txt',
          chatId: '123456789',
          caption: '不存在的文件'
        })
      ).rejects.toThrow();
    });

    test('应该处理过大的文件', async () => {
      // 创建一个大文件（超过限制）
      const largeFilePath = path.join(__dirname, '../../test-data/large-file.txt');
      const largeContent = 'X'.repeat(20 * 1024 * 1024); // 20MB
      
      try {
        await fs.writeFile(largeFilePath, largeContent, 'utf-8');
        
        await expect(
          adapter.sendFile({
            filePath: largeFilePath,
            chatId: '123456789',
            caption: '过大文件测试'
          })
        ).rejects.toThrow();
      } finally {
        try {
          await fs.unlink(largeFilePath);
        } catch (error) {
          // 忽略清理错误
        }
      }
    });
  });

  describe('上下文分析集成', () => {
    test('应该集成上下文分析引擎', async () => {
      const result = await adapter.sendFile({
        filePath: testFilePath,
        chatId: '-1003655501651',
        caption: '上下文分析测试'
      });

      expect(result.analysis).toBeDefined();
      expect(result.analysis.scenario).toBeDefined();
      expect(result.analysis.urgency).toBeDefined();
      expect(result.analysis.recommendedTargets).toBeDefined();
      expect(result.analysis.confidence).toBeGreaterThan(0);
    });

    test('应该根据聊天类型调整分析', async () => {
      // 测试群聊
      const groupResult = await adapter.sendFile({
        filePath: testFilePath,
        chatId: '-1003655501651', // 群聊ID
        caption: '群聊测试'
      });

      // 测试私聊
      const privateResult = await adapter.sendFile({
        filePath: testFilePath,
        chatId: '8772264920', // 私聊ID
        caption: '私聊测试'
      });

      expect(groupResult.analysis.isGroupChat).toBe(true);
      expect(privateResult.analysis.isGroupChat).toBe(false);
    });
  });
});