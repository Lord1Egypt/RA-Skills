/**
 * Design System 配置加载器单元测试
 */

import { DesignSystemConfigLoader } from '../design-system-config';

describe('DesignSystemConfigLoader', () => {
  let loader: DesignSystemConfigLoader;

  beforeEach(() => {
    loader = DesignSystemConfigLoader.getInstance();
  });

  describe('match', () => {
    it('should match user specified design system', () => {
      const result = loader.match('使用 linear 风格生成页面');

      expect(result.matchedBy).toBe('user_specified');
      expect(result.designSystem).toBe('linear');
      expect(result.confidence).toBe(1.0);
    });

    it('should match keyword "支付" to stripe', () => {
      const result = loader.match('生成一个支付系统的后台管理页面');

      expect(result.matchedBy).toBe('keyword');
      expect(result.designSystem).toBe('stripe');
      expect(result.confidence).toBe(0.8);
    });

    it('should match keyword "ai" to claude', () => {
      const result = loader.match('创建一个 AI 聊天机器人界面');

      expect(result.matchedBy).toBe('keyword');
      expect(result.designSystem).toBe('claude');
      expect(result.confidence).toBe(0.8);
    });

    it('should match alias "苹果" to apple', () => {
      const result = loader.match('按苹果风格设计移动端页面');

      expect(result.matchedBy).toBe('user_specified');
      expect(result.designSystem).toBe('apple');
    });

    it('should use default when no match', () => {
      const result = loader.match('生成一个普通页面');

      expect(result.matchedBy).toBe('default');
      expect(result.designSystem).toBe('linear');
      expect(result.confidence).toBe(0.5);
    });

    it('should respect exclude rules', () => {
      const result = loader.match('不要 stripe 风格，生成支付页面');

      // 应该排除 stripe，使用默认或其他匹配
      expect(result.designSystem).not.toBe('stripe');
    });
  });

  describe('resolveAlias', () => {
    it('should resolve "lin" to linear', () => {
      const result = loader.resolveAlias('lin');
      expect(result).toBe('linear');
    });

    it('should resolve "苹果" to apple', () => {
      const result = loader.resolveAlias('苹果');
      expect(result).toBe('apple');
    });

    it('should return null for unknown alias', () => {
      const result = loader.resolveAlias('unknown');
      expect(result).toBeNull();
    });
  });

  describe('getDefault', () => {
    it('should return default design system', () => {
      const result = loader.getDefault();
      expect(result).toBe('linear');
    });
  });

  describe('getAllDesignSystems', () => {
    it('should return all design systems metadata', () => {
      const systems = loader.getAllDesignSystems();

      expect(systems).toHaveProperty('linear');
      expect(systems).toHaveProperty('stripe');
      expect(systems).toHaveProperty('vercel');
      expect(systems.linear).toHaveProperty('name');
      expect(systems.linear).toHaveProperty('primaryColor');
    });
  });

  describe('getVersion', () => {
    it('should return config version', () => {
      const version = loader.getVersion();
      expect(version).toMatch(/^\d+\.\d+\.\d+$/);
    });
  });
});
