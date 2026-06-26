/**
 * 动态模型路由技能 - 工具函数测试
 */

import { describe, test, expect } from '@jest/globals';
import {
  generateId,
  estimateTokens,
  detectLanguage,
  calculateComplexity,
  complexityToCategory,
  identifyCategories,
  validateConfig,
  mergeConfig,
  sleep,
  retry,
  calculateAverage,
  calculateStandardDeviation,
  clamp,
  formatBytes,
  formatTime,
} from '../src/utils/index.js';

describe('工具函数库', () => {
  describe('generateId', () => {
    test('生成唯一ID', () => {
      const id1 = generateId('task_');
      const id2 = generateId('task_');
      
      expect(id1).toMatch(/^task_\d+_[a-z0-9]{9}$/);
      expect(id2).toMatch(/^task_\d+_[a-z0-9]{9}$/);
      expect(id1).not.toBe(id2);
    });
    
    test('生成不带前缀的ID', () => {
      const id = generateId();
      expect(id).toMatch(/^\d+_[a-z0-9]{9}$/);
    });
  });
  
  describe('estimateTokens', () => {
    test('估算英文文本token数', () => {
      const text = 'Hello world, this is a test.';
      const tokens = estimateTokens(text);
      expect(tokens).toBeGreaterThan(5);
      expect(tokens).toBeLessThan(10);
    });
    
    test('估算中文文本token数', () => {
      const text = '你好世界，这是一个测试。';
      const tokens = estimateTokens(text);
      expect(tokens).toBeGreaterThan(4);
      expect(tokens).toBeLessThan(8);
    });
    
    test('估算混合文本token数', () => {
      const text = 'Hello 世界，this is a 测试。';
      const tokens = estimateTokens(text);
      expect(tokens).toBeGreaterThan(6);
      expect(tokens).toBeLessThan(12);
    });
    
    test('空文本返回0', () => {
      expect(estimateTokens('')).toBe(0);
      expect(estimateTokens('   ')).toBe(0);
    });
  });
  
  describe('detectLanguage', () => {
    test('检测中文', () => {
      expect(detectLanguage('这是一个中文测试')).toBe('zh');
      expect(detectLanguage('中文')).toBe('zh');
    });
    
    test('检测英文', () => {
      expect(detectLanguage('This is an English test')).toBe('en');
      expect(detectLanguage('English')).toBe('en');
    });
    
    test('检测混合语言', () => {
      expect(detectLanguage('这是中文 and English')).toBe('mixed');
      expect(detectLanguage('Hello 世界')).toBe('mixed');
    });
    
    test('检测其他语言', () => {
      expect(detectLanguage('123456')).toBe('other');
      expect(detectLanguage('!@#$%^')).toBe('other');
      expect(detectLanguage('')).toBe('other');
    });
  });
  
  describe('calculateComplexity', () => {
    test('计算简单文本复杂度', () => {
      const text = '你好';
      const complexity = calculateComplexity(text);
      expect(complexity).toBeGreaterThanOrEqual(0);
      expect(complexity).toBeLessThan(0.3);
    });
    
    test('计算中等文本复杂度', () => {
      const text = '请帮我写一个简单的函数，实现两个数字相加。';
      const complexity = calculateComplexity(text);
      expect(complexity).toBeGreaterThanOrEqual(0.3);
      expect(complexity).toBeLessThan(0.7);
    });
    
    test('计算复杂文本复杂度', () => {
      const text = `实现一个快速排序算法，要求：
      1. 支持泛型
      2. 时间复杂度O(n log n)
      3. 包含详细的注释
      4. 提供单元测试`;
      const complexity = calculateComplexity(text);
      expect(complexity).toBeGreaterThanOrEqual(0.7);
      expect(complexity).toBeLessThanOrEqual(1);
    });
    
    test('计算包含代码的文本复杂度', () => {
      const text = '```python\ndef hello():\n    print("world")\n```';
      const complexity = calculateComplexity(text);
      expect(complexity).toBeGreaterThan(0.3);
    });
  });
  
  describe('complexityToCategory', () => {
    test('简单复杂度', () => {
      expect(complexityToCategory(0.1)).toBe('simple');
      expect(complexityToCategory(0.29)).toBe('simple');
    });
    
    test('中等复杂度', () => {
      expect(complexityToCategory(0.3)).toBe('medium');
      expect(complexityToCategory(0.5)).toBe('medium');
      expect(complexityToCategory(0.69)).toBe('medium');
    });
    
    test('复杂复杂度', () => {
      expect(complexityToCategory(0.7)).toBe('complex');
      expect(complexityToCategory(0.9)).toBe('complex');
      expect(complexityToCategory(1)).toBe('complex');
    });
  });
  
  describe('identifyCategories', () => {
    test('识别编程类别', () => {
      const text = '写一个Python函数';
      const categories = identifyCategories(text);
      expect(categories).toContain('coding');
    });
    
    test('识别写作类别', () => {
      const text = '请帮我润色这篇文章';
      const categories = identifyCategories(text);
      expect(categories).toContain('writing');
    });
    
    test('识别分析类别', () => {
      const text = '分析这个数据集';
      const categories = identifyCategories(text);
      expect(categories).toContain('analysis');
    });
    
    test('识别推理类别', () => {
      const text = '这个问题的解决方案是什么';
      const categories = identifyCategories(text);
      expect(categories).toContain('reasoning');
    });
    
    test('通用类别', () => {
      const text = '你好';
      const categories = identifyCategories(text);
      expect(categories).toContain('general');
    });
  });
  
  describe('validateConfig', () => {
    test('验证有效配置', () => {
      const validConfig = {
        enabled: true,
        learningEnabled: true,
        defaultStrategy: 'balanced',
        complexityThresholds: {
          simple: 0.3,
          medium: 0.7,
        },
        scoringWeights: {
          capabilityMatch: 0.4,
          costEfficiency: 0.3,
          performance: 0.2,
          reliability: 0.1,
        },
        providers: {
          autoDiscover: true,
          refreshInterval: 3600,
        },
        learning: {
          feedbackCollection: true,
          optimizationInterval: 86400,
          minSamplesForOptimization: 100,
        },
      };
      
      expect(() => validateConfig(validConfig)).not.toThrow();
    });
    
    test('验证缺失字段', () => {
      const invalidConfig = {
        enabled: true,
        // 缺少其他字段
      };
      
      expect(() => validateConfig(invalidConfig)).toThrow();
    });
    
    test('验证无效复杂度阈值', () => {
      const invalidConfig = {
        enabled: true,
        learningEnabled: true,
        defaultStrategy: 'balanced',
        complexityThresholds: {
          simple: 0.8, // 大于medium
          medium: 0.3,
        },
        scoringWeights: {
          capabilityMatch: 0.4,
          costEfficiency: 0.3,
          performance: 0.2,
          reliability: 0.1,
        },
        providers: {
          autoDiscover: true,
          refreshInterval: 3600,
        },
        learning: {
          feedbackCollection: true,
          optimizationInterval: 86400,
          minSamplesForOptimization: 100,
        },
      };
      
      expect(() => validateConfig(invalidConfig)).toThrow();
    });
  });
  
  describe('mergeConfig', () => {
    test('合并配置', () => {
      const defaultConfig = {
        a: 1,
        b: { c: 2, d: 3 },
        e: [1, 2, 3],
      };
      
      const userConfig = {
        a: 10,
        b: { d: 30 },
        f: 'new',
      };
      
      const merged = mergeConfig(userConfig, defaultConfig);
      
      expect(merged.a).toBe(10);
      expect(merged.b.c).toBe(2); // 保持默认
      expect(merged.b.d).toBe(30); // 被覆盖
      expect(merged.e).toEqual([1, 2, 3]); // 保持默认
      expect(merged.f).toBe('new'); // 新增
    });
  });
  
  describe('sleep', () => {
    test('休眠指定时间', async () => {
      const start = Date.now();
      await sleep(50);
      const end = Date.now();
      const duration = end - start;
      
      expect(duration).toBeGreaterThanOrEqual(40);
      expect(duration).toBeLessThan(100);
    });
  });
  
  describe('retry', () => {
    test('成功执行不重试', async () => {
      let callCount = 0;
      const fn = async () => {
        callCount++;
        return 'success';
      };
      
      const result = await retry(fn);
      expect(result).toBe('success');
      expect(callCount).toBe(1);
    });
    
    test('失败后重试成功', async () => {
      let callCount = 0;
      const fn = async () => {
        callCount++;
        if (callCount < 3) {
          throw new Error('暂时失败');
        }
        return 'success';
      };
      
      const result = await retry(fn, 3);
      expect(result).toBe('success');
      expect(callCount).toBe(3);
    });
    
    test('重试次数用尽后抛出错误', async () => {
      let callCount = 0;
      const fn = async () => {
        callCount++;
        throw new Error('总是失败');
      };
      
      await expect(retry(fn, 2)).rejects.toThrow('总是失败');
      expect(callCount).toBe(2);
    });
  });
  
  describe('数学函数', () => {
    test('calculateAverage', () => {
      expect(calculateAverage([1, 2, 3, 4, 5])).toBe(3);
      expect(calculateAverage([10])).toBe(10);
      expect(calculateAverage([])).toBe(0);
    });
    
    test('calculateStandardDeviation', () => {
      expect(calculateStandardDeviation([1, 2, 3, 4, 5])).toBeCloseTo(1.414, 2);
      expect(calculateStandardDeviation([10])).toBe(0);
      expect(calculateStandardDeviation([])).toBe(0);
    });
    
    test('clamp', () => {
      expect(clamp(5, 0, 10)).toBe(5);
      expect(clamp(-5, 0, 10)).toBe(0);
      expect(clamp(15, 0, 10)).toBe(10);
    });
  });
  
  describe('格式化函数', () => {
    test('formatBytes', () => {
      expect(formatBytes(0)).toBe('0 Bytes');
      expect(formatBytes(1024)).toBe('1 KB');
      expect(formatBytes(1024 * 1024)).toBe('1 MB');
      expect(formatBytes(1024 * 1024 * 1024)).toBe('1 GB');
    });
    
    test('formatTime', () => {
      expect(formatTime(500)).toBe('500ms');
      expect(formatTime(1500)).toBe('1.50s');
      expect(formatTime(61000)).toBe('1.02m');
      expect(formatTime(3661000)).toBe('1.02h');
    });
  });
});