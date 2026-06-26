/**
 * File Manager 单元测试
 *
 * 测试文件管理器的核心功能：验证、分块读取、临时文件管理
 */

import { FileManager } from '../../src/core/file-manager.js';
import fs from 'fs/promises';
import path from 'path';

describe('FileManager', () => {
  let fileManager;
  let testFilePath;
  let testFileContent;

  beforeEach(async () => {
    fileManager = new FileManager({
      maxFileSize: 50 * 1024 * 1024, // 50MB
      chunkSize: 5 * 1024 * 1024, // 5MB
      tempDir: '/tmp/openclaw-test'
    });

    // 创建测试文件
    testFileContent = Buffer.alloc(10 * 1024, 'test content'); // 10KB
    testFilePath = path.join('/tmp', `test-file-${Date.now()}.txt`);
    await fs.writeFile(testFilePath, testFileContent);
  });

  afterEach(async () => {
    try {
      await fs.unlink(testFilePath);
    } catch {
      // 文件可能已被删除
    }
  });

  describe('构造函数', () => {
    test('应该使用默认配置创建实例', () => {
      const manager = new FileManager();
      expect(manager.config).toBeDefined();
      expect(manager.config.maxFileSize).toBe(100 * 1024 * 1024); // 100MB
      expect(manager.config.chunkSize).toBe(10 * 1024 * 1024); // 10MB
      expect(manager.config.allowedMimeTypes).toBeInstanceOf(Array);
      expect(manager.config.tempDir).toBe('/tmp/file-transfer');
    });

    test('应该使用自定义配置创建实例', () => {
      const customConfig = {
        maxFileSize: 200 * 1024 * 1024,
        chunkSize: 20 * 1024 * 1024,
        allowedMimeTypes: ['image/jpeg', 'image/png'],
        tempDir: '/custom/temp/dir'
      };

      const manager = new FileManager(customConfig);
      expect(manager.config.maxFileSize).toBe(200 * 1024 * 1024);
      expect(manager.config.chunkSize).toBe(20 * 1024 * 1024);
      expect(manager.config.allowedMimeTypes).toEqual(['image/jpeg', 'image/png']);
      expect(manager.config.tempDir).toBe('/custom/temp/dir');
    });
  });

  describe('validateFile方法', () => {
    test('应该成功验证有效文件', async () => {
      const result = await fileManager.validateFile(testFilePath);

      expect(result.valid).toBe(true);
      expect(result.name).toBe(path.basename(testFilePath));
      expect(result.size).toBe(testFileContent.length);
      expect(result.mimeType).toBe('text/plain');
      expect(result.extension).toBe('.txt');
      expect(new Date(result.lastModified).getTime()).not.toBeNaN();
    });

    test('应该拒绝超过大小限制的文件', async () => {
      const smallManager = new FileManager({ maxFileSize: 1024 }); // 1KB limit
      const result = await smallManager.validateFile(testFilePath); // 10KB file

      expect(result.valid).toBe(false);
      expect(result.error).toContain('文件大小超过限制');
    });

    test('应该拒绝不存在的文件', async () => {
      const result = await fileManager.validateFile('/tmp/non-existent-file-123456.txt');

      expect(result.valid).toBe(false);
      expect(result.error).toContain('文件验证失败');
    });

    test('应该拒绝不允许的MIME类型', async () => {
      const restrictedManager = new FileManager({
        allowedMimeTypes: ['image/jpeg', 'image/png']
      });

      const result = await restrictedManager.validateFile(testFilePath);

      expect(result.valid).toBe(false);
      expect(result.error).toContain('不支持的文件类型');
    });
  });

  describe('readFileInChunks方法', () => {
    test('应该分块读取文件并调用回调', async () => {
      const chunks = [];
      const result = await fileManager.readFileInChunks(testFilePath, async (chunk, index, total) => {
        chunks.push({ chunk, index, total });
      });

      expect(result.success).toBe(true);
      expect(result.filePath).toBe(testFilePath);
      expect(result.fileSize).toBe(testFileContent.length);
      expect(result.bytesRead).toBe(testFileContent.length);
      expect(result.totalChunks).toBeGreaterThan(0);
      expect(chunks.length).toBe(result.totalChunks);
    });

    test('应该拒绝无效文件', async () => {
      await expect(
        fileManager.readFileInChunks('/tmp/non-existent.txt', () => {})
      ).rejects.toThrow();
    });
  });

  describe('createTempFile和cleanupTempFile方法', () => {
    test('应该创建和清理临时文件', async () => {
      const testData = Buffer.from('test temporary data');

      const tempFilePath = await fileManager.createTempFile(testData, '.txt');

      expect(tempFilePath).toBeDefined();
      expect(tempFilePath).toContain(fileManager.config.tempDir);
      expect(tempFilePath).toMatch(/\.txt$/);

      // 验证文件存在
      const stats = await fs.stat(tempFilePath);
      expect(stats.size).toBe(testData.length);

      // 清理临时文件
      const cleanupResult = await fileManager.cleanupTempFile(tempFilePath);
      expect(cleanupResult).toBe(true);

      // 验证文件已被删除
      await expect(fs.access(tempFilePath)).rejects.toThrow();
    });

    test('应该处理清理不存在的文件', async () => {
      const result = await fileManager.cleanupTempFile('/tmp/non-existent-file.txt');
      expect(result).toBe(false);
    });
  });

  describe('getActiveTransfers方法', () => {
    test('应该在无活动传输时返回空数组', () => {
      const activeTransfers = fileManager.getActiveTransfers();
      expect(activeTransfers).toEqual([]);
    });
  });

  describe('formatBytes方法', () => {
    test('应该正确格式化字节大小', () => {
      expect(fileManager.formatBytes(0)).toBe('0 Bytes');
      expect(fileManager.formatBytes(1024)).toBe('1 KB');
      expect(fileManager.formatBytes(1024 * 1024)).toBe('1 MB');
      expect(fileManager.formatBytes(1024 * 1024 * 1024)).toBe('1 GB');
      expect(fileManager.formatBytes(1500)).toBe('1.46 KB');
    });

    test('应该支持自定义小数位数', () => {
      expect(fileManager.formatBytes(1500, 0)).toBe('1 KB');
      expect(fileManager.formatBytes(1500, 3)).toBe('1.465 KB');
    });
  });

  describe('getStatus方法', () => {
    test('应该返回管理器状态', () => {
      const status = fileManager.getStatus();

      expect(status).toBeDefined();
      expect(status.version).toBe('0.2.0-beta');
      expect(status.config).toBeDefined();
      expect(status.config.maxFileSize).toBe(50 * 1024 * 1024);
      expect(status.config.chunkSize).toBe(5 * 1024 * 1024);
      expect(status.config.allowedMimeTypesCount).toBeGreaterThan(0);
      expect(status.config.tempDir).toBe('/tmp/openclaw-test');
      expect(status.activeTransfers).toBe(0);
      expect(status.isOperational).toBe(true);
    });
  });
});
