/**
 * Context Engine 单元测试
 *
 * 测试智能上下文分析引擎的核心功能
 */

import { ContextEngine } from '../../src/core/context-engine.js';

describe('ContextEngine', () => {
  let contextEngine;

  beforeEach(() => {
    contextEngine = new ContextEngine({
      enableAI: false,
      maxHistoryLength: 5
    });
  });

  describe('构造函数', () => {
    test('应该使用默认配置创建实例', () => {
      const engine = new ContextEngine();
      expect(engine.config).toBeDefined();
      expect(engine.config.enableAI).toBe(false);
      expect(engine.config.maxHistoryLength).toBe(10);
    });

    test('应该使用自定义配置创建实例', () => {
      const customConfig = {
        enableAI: true,
        maxHistoryLength: 20,
        scenarioWeights: {
          share: 2.0,
          backup: 1.0
        }
      };

      const engine = new ContextEngine(customConfig);
      expect(engine.config.enableAI).toBe(true);
      expect(engine.config.maxHistoryLength).toBe(20);
      expect(engine.config.scenarioWeights.share).toBe(2.0);
    });
  });

  describe('analyzeContext方法', () => {
    test('应该成功分析基本文件传输上下文', async () => {
      const context = {
        filePath: '/path/to/document.pdf',
        fileName: 'document.pdf',
        fileSize: 1024 * 1024, // 1MB
        fileType: 'application/pdf',
        caption: '团队周报',
        chatInfo: {
          isGroupChat: true,
          chatType: 'group'
        },
        userInfo: {
          id: 'user123',
          name: '测试用户'
        },
        history: ['早上好', '这是本周的周报']
      };

      const result = await contextEngine.analyzeContext(context);

      expect(result).toBeDefined();
      expect(result.scenario).toBeDefined();
      expect(result.urgency).toBeDefined();
      expect(result.recommendedTargets).toBeInstanceOf(Array);
      expect(result.metadata).toBeDefined();
      expect(result.isGroupChat).toBe(true);
      expect(result.chatType).toBe('group');
      expect(result.fileCategory).toBe('document');
      expect(result.timestamp).toBeDefined();
      expect(result.confidence).toBeGreaterThan(0);
      expect(result.confidence).toBeLessThanOrEqual(1);
    });

    test('应该处理缺少可选字段的上下文', async () => {
      const minimalContext = {
        filePath: '/path/to/image.jpg',
        fileName: 'image.jpg',
        fileSize: 500 * 1024, // 500KB
        fileType: 'image/jpeg'
      };

      const result = await contextEngine.analyzeContext(minimalContext);

      expect(result).toBeDefined();
      expect(result.scenario).toBe('share');
      expect(result.isGroupChat).toBe(false);
      expect(result.chatType).toBe('private');
      expect(result.confidence).toBeGreaterThan(0);
    });

    test('应该处理未知文件类型', async () => {
      const context = {
        filePath: '/path/to/unknown.xyz',
        fileName: 'unknown.xyz',
        fileSize: 1024,
        fileType: 'application/unknown'
      };

      const result = await contextEngine.analyzeContext(context);

      expect(result).toBeDefined();
      expect(result.scenario).toBe('share');
      // 未知类型默认归为 document
      expect(result.fileCategory).toBe('document');
    });

    test('应该处理大文件场景', async () => {
      const context = {
        filePath: '/path/to/large-video.mp4',
        fileName: 'large-video.mp4',
        fileSize: 200 * 1024 * 1024, // 200MB
        fileType: 'video/mp4',
        chatInfo: { isGroupChat: false }
      };

      const result = await contextEngine.analyzeContext(context);

      expect(result).toBeDefined();
      expect(result.scenario).toBe('share'); // video/mp4 maps to share
    });
  });

  describe('场景识别', () => {
    test('应该正确识别文档协作场景', async () => {
      const context = {
        filePath: '/path/to/project-plan.docx',
        fileName: 'project-plan.docx',
        fileSize: 2 * 1024 * 1024,
        fileType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        caption: '项目计划草案',
        chatInfo: {
          isGroupChat: true,
          chatType: 'group'
        },
        history: ['我们需要制定项目计划', '这是初步草案']
      };

      const result = await contextEngine.analyzeContext(context);

      expect(result.scenario).toBe('collaborate');
      expect(result.urgency).toBe('high');
      expect(result.recommendedTargets).toContain('collaborators');
      expect(result.recommendedTargets).toContain('team_chat');
    });

    test('应该正确识别图片分享场景', async () => {
      const context = {
        filePath: '/path/to/vacation.jpg',
        fileName: 'vacation.jpg',
        fileSize: 3 * 1024 * 1024,
        fileType: 'image/jpeg',
        caption: '度假照片',
        chatInfo: {
          isGroupChat: false,
          chatType: 'private'
        }
      };

      const result = await contextEngine.analyzeContext(context);

      expect(result.scenario).toBe('share');
      expect(result.recommendedTargets).toContain('current_chat');
      expect(result.recommendedTargets).toContain('related_chats');
    });

    test('应该正确识别压缩包归档场景', async () => {
      const context = {
        filePath: '/path/to/backup.zip',
        fileName: 'backup.zip',
        fileSize: 50 * 1024 * 1024,
        fileType: 'application/zip',
        caption: '数据库备份',
        history: ['需要备份数据库', '这是最新的备份文件']
      };

      const result = await contextEngine.analyzeContext(context);

      expect(result.scenario).toBe('archive');
      expect(result.urgency).toBe('low');
      expect(result.recommendedTargets).toContain('archive_folder');
    });
  });

  describe('紧急程度评估', () => {
    test('应该根据场景设置基础紧急程度', async () => {
      const collaborateContext = {
        filePath: '/path/to/doc.docx',
        fileName: 'doc.docx',
        fileSize: 1024,
        fileType: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        chatInfo: { isGroupChat: true }
      };

      const archiveContext = {
        filePath: '/path/to/backup.zip',
        fileName: 'backup.zip',
        fileSize: 1024,
        fileType: 'application/zip'
      };

      const collaborateResult = await contextEngine.analyzeContext(collaborateContext);
      const archiveResult = await contextEngine.analyzeContext(archiveContext);

      expect(collaborateResult.urgency).toBe('high');
      expect(archiveResult.urgency).toBe('low');
    });
  });

  describe('错误处理', () => {
    test('应该在分析失败时返回降级结果', async () => {
      // 触发 getFallbackAnalysis：让 determineScenario 内部抛错
      // 通过破坏内部状态来模拟
      const brokenEngine = new ContextEngine();
      brokenEngine.fileTypeToScenario = null; // 让 fileTypeToScenario[x] 抛 TypeError

      const result = await brokenEngine.analyzeContext({
        fileType: 'application/pdf',
        fileSize: 1024
      });

      expect(result).toBeDefined();
      expect(result.scenario).toBe('share');
      expect(result.confidence).toBe(0.5);
      expect(result.metadata.isFallback).toBe(true);
    });
  });

  describe('getStatus方法', () => {
    test('应该返回引擎状态信息', () => {
      const status = contextEngine.getStatus();

      expect(status).toBeDefined();
      expect(status.version).toBe('0.2.0-beta');
      expect(status.config).toBeDefined();
      expect(status.scenarios).toBeInstanceOf(Array);
      expect(status.scenarios).toContain('share');
      expect(status.scenarios).toContain('collaborate');
      expect(status.fileTypes).toBeInstanceOf(Array);
      expect(status.isOperational).toBe(true);
    });
  });

  describe('文件分类', () => {
    test('应该正确分类各种文件类型', () => {
      const testCases = [
        { mimeType: 'image/jpeg', expected: 'image' },
        { mimeType: 'video/mp4', expected: 'video' },
        { mimeType: 'text/plain', expected: 'document' },
        { mimeType: 'application/pdf', expected: 'document' },
        { mimeType: 'application/zip', expected: 'archive' },
        { mimeType: 'text/javascript', expected: 'code' },
        { mimeType: 'application/json', expected: 'code' },
        // 未知类型默认归为 document
        { mimeType: 'application/octet-stream', expected: 'document' },
      ];

      testCases.forEach(({ mimeType, expected }) => {
        const category = contextEngine.categorizeFile(mimeType);
        expect(category).toBe(expected);
      });
    });
  });

  describe('置信度计算', () => {
    test('应该为完整上下文提供高置信度', async () => {
      const completeContext = {
        filePath: '/path/to/file.pdf',
        fileName: 'file.pdf',
        fileSize: 1024,
        fileType: 'application/pdf',
        caption: '详细说明',
        chatInfo: { isGroupChat: true, chatType: 'group' },
        history: ['相关讨论1', '相关讨论2'],
        userInfo: { id: 'user1' }
      };

      const result = await contextEngine.analyzeContext(completeContext);
      // base 0.5 + fileType match 0.2 + chatInfo 0.1 + caption 0.1 + history 0.1 = 1.0
      expect(result.confidence).toBeGreaterThanOrEqual(0.9);
    });

    test('应该为不完整上下文提供较低置信度', async () => {
      const incompleteContext = {
        filePath: '/path/to/file.xyz',
        fileName: 'file.xyz',
        fileSize: 1024,
        fileType: 'application/unknown'
      };

      const result = await contextEngine.analyzeContext(incompleteContext);
      // base 0.5, no other bonuses
      expect(result.confidence).toBeLessThan(0.8);
    });
  });

  describe('用户意图提取', () => {
    test('应该从 caption 中提取分享意图', () => {
      const intent = contextEngine.extractUserIntent({
        caption: '分享一下这个文件'
      });
      expect(intent).toBe('share');
    });

    test('应该从 caption 中提取备份意图', () => {
      const intent = contextEngine.extractUserIntent({
        caption: '帮我备份一下'
      });
      expect(intent).toBe('backup');
    });

    test('应该对无关内容返回 unknown', () => {
      const intent = contextEngine.extractUserIntent({
        caption: '这个文件看看'
      });
      expect(intent).toBe('unknown');
    });
  });
});
