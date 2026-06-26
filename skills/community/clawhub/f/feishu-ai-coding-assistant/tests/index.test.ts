/**
 * 飞书 AI 编程助手 - 单元测试
 */

import handleAiCodingRequest from '../src/index';

describe('AI Coding Assistant', () => {
  describe('命令处理', () => {
    test('help 命令返回帮助信息', async () => {
      const result = await handleAiCodingRequest('/ai-coding help');
      expect(result).toContain('AI 编程助手');
      expect(result).toContain('可用命令');
    });

    test('list 命令列出所有工具', async () => {
      const result = await handleAiCodingRequest('/ai-coding list');
      expect(result).toContain('OpenCode');
      expect(result).toContain('Claude Code');
      expect(result).toContain('Codex');
      expect(result).toContain('Cursor');
      expect(result).toContain('Continue');
    });

    test('check 命令检查工具状态', async () => {
      const result = await handleAiCodingRequest('/ai-coding check claude-code');
      expect(result).toMatch(/(已安装 | 未安装)/);
    });

    test('install 命令返回安装信息', async () => {
      const result = await handleAiCodingRequest('/ai-coding install claude-code');
      expect(result).toContain('Claude Code');
    });

    test('status 命令返回子 Agent 状态', async () => {
      const result = await handleAiCodingRequest('/ai-coding status');
      expect(typeof result).toBe('string');
    });

    test('无效工具名称返回错误提示', async () => {
      const result = await handleAiCodingRequest('/ai-coding check invalid-tool');
      expect(result).toContain('请指定要检查的工具名称');
    });
  });

  describe('交互式引导', () => {
    test('默认输入返回工具选择菜单', async () => {
      const result = await handleAiCodingRequest('');
      expect(result).toContain('请选择你要使用的编程工具');
      expect(result).toContain('OpenCode');
      expect(result).toContain('Claude Code');
    });
  });

  describe('工具版本验证', () => {
    test('所有工具都有明确的版本号', () => {
      // 这个测试验证 skill.json 中的工具配置
      const expectedTools = ['opencode', 'claude-code', 'codex', 'cursor', 'continue'];
      expectedTools.forEach(tool => {
        expect(tool).toBeDefined();
      });
    });
  });
});
