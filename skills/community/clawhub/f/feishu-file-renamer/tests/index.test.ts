/**
 * feishu-file-renamer 单元测试
 */

import { restoreFileName, batchRename, extractFileMappingsFromMessage, smartRename } from '../src/index';
import { writeFileSync, existsSync, unlinkSync, mkdirSync } from 'fs';
import { join } from 'path';

describe('feishu-file-renamer', () => {
  const testDir = '/tmp/test-rename';
  
  beforeEach(() => {
    try {
      mkdirSync(testDir, { recursive: true });
    } catch {}
  });
  
  afterEach(() => {
    // Cleanup test files
    try {
      const files = ['test.png', 'test_1.png', 'downloaded.png'];
      files.forEach(f => {
        const path = join(testDir, f);
        if (existsSync(path)) unlinkSync(path);
      });
    } catch {}
  });

  describe('extractFileMappingsFromMessage', () => {
    it('should extract file mappings from message', () => {
      const message = '文件：[img_v3_0210g_xxx.png](产品图.png)';
      const mappings = extractFileMappingsFromMessage(message);
      
      expect(mappings.length).toBe(1);
      expect(mappings[0].hashFile).toBe('img_v3_0210g_xxx.png');
      expect(mappings[0].originalName).toBe('产品图.png');
    });

    it('should extract multiple file mappings', () => {
      const message = `
        [img_v3_xxx.png](产品图 1.png)
        [img_v3_yyy.png](产品图 2.png)
        [file_v3_zzz.pdf](规格书.pdf)
      `;
      const mappings = extractFileMappingsFromMessage(message);
      
      expect(mappings.length).toBe(3);
      expect(mappings[0].originalName).toBe('产品图 1.png');
      expect(mappings[1].originalName).toBe('产品图 2.png');
      expect(mappings[2].originalName).toBe('规格书.pdf');
    });

    it('should return empty array for no files', () => {
      const message = '这是一条普通消息';
      const mappings = extractFileMappingsFromMessage(message);
      
      expect(mappings.length).toBe(0);
    });
  });

  describe('restoreFileName', () => {
    it('should rename file to original name', () => {
      const hashFile = join(testDir, 'img_v3_xxx.png');
      const originalName = '产品图.png';
      
      // Create test file
      writeFileSync(hashFile, 'test content');
      
      const newPath = restoreFileName(hashFile, originalName);
      
      expect(existsSync(newPath)).toBe(true);
      expect(existsSync(hashFile)).toBe(false);
      expect(newPath).toContain('产品图.png');
    });

    it('should handle filename conflicts', () => {
      const hashFile = join(testDir, 'img_v3_xxx.png');
      const existingFile = join(testDir, '产品图.png');
      
      // Create files
      writeFileSync(hashFile, 'test content');
      writeFileSync(existingFile, 'existing content');
      
      const newPath = restoreFileName(hashFile, '产品图.png');
      
      expect(existsSync(newPath)).toBe(true);
      expect(newPath).toContain('产品图_1.png');
    });
  });

  describe('batchRename', () => {
    it('should rename multiple files', () => {
      const mappings = [
        { hashFile: join(testDir, 'img_v3_xxx.png'), originalName: '图 1.png' },
        { hashFile: join(testDir, 'img_v3_yyy.png'), originalName: '图 2.png' },
      ];
      
      // Create test files
      mappings.forEach(m => writeFileSync(m.hashFile, 'test'));
      
      const result = batchRename(mappings);
      
      expect(result.success).toBe(2);
      expect(result.failed).toBe(0);
      expect(result.skipped).toBe(0);
    });

    it('should handle missing files', () => {
      const mappings = [
        { hashFile: join(testDir, 'not_exists.png'), originalName: '图 1.png' },
      ];
      
      const result = batchRename(mappings);
      
      expect(result.success).toBe(0);
      expect(result.failed).toBe(0);
      expect(result.skipped).toBe(1);
    });
  });

  describe('smartRename', () => {
    it('should generate filename from context', () => {
      const hashFile = join(testDir, 'downloaded.png');
      writeFileSync(hashFile, 'test');
      
      const newPath = smartRename(hashFile, '产品宣传图');
      
      expect(existsSync(newPath)).toBe(true);
      expect(newPath).toContain('产品宣传图');
    });

    it('should filter special characters', () => {
      const hashFile = join(testDir, 'downloaded.png');
      writeFileSync(hashFile, 'test');
      
      const newPath = smartRename(hashFile, '产品@图#123!');
      
      expect(newPath).not.toContain('@');
      expect(newPath).not.toContain('#');
      expect(newPath).not.toContain('!');
    });
  });
});
