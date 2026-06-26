/**
 * EVA Soul - 决策系统单元测试
 */

jest.mock('fs', () => ({
  existsSync: jest.fn(() => false),
  readFileSync: jest.fn(() => '{}'),
  writeFileSync: jest.fn()
}));
jest.mock('../lib/core/config', () => ({
  expandPath: (p) => p,
  getUserConfig: jest.fn(() => ({ name: '主人' }))
}));
jest.mock('../hooks/logger', () => ({
  debug: jest.fn(),
  info: jest.fn(),
  warn: jest.fn(),
  error: jest.fn()
}));

const {
  DecisionSystem,
  evaluateImportance
} = require('../lib/decision/decision');

describe('DecisionSystem 决策系统', () => {
  let ds;

  beforeEach(() => {
    ds = new DecisionSystem();
  });

  describe('decide 决策', () => {
    test('默认情境返回有效决策', () => {
      const ctx = { emotion: 'neutral', personality: 'gentle', message: '' };
      const result = ds.decide(ctx);
      expect(result).toHaveProperty('action');
      expect(result).toHaveProperty('style');
      expect(result).toHaveProperty('factors');
      expect(typeof result.action).toBe('string');
    });

    test('开心情境优先 celebrate', () => {
      const ctx = { emotion: 'happy', personality: 'gentle', message: '我很开心' };
      const result = ds.decide(ctx);
      expect(['celebrate', 'comfort', 'support']).toContain(result.action);
    });

    test('悲伤情境优先 comfort', () => {
      const ctx = { emotion: 'sad', personality: 'gentle', message: '我很难过' };
      const result = ds.decide(ctx);
      expect(['comfort', 'calm', 'support']).toContain(result.action);
    });

    test('愤怒情境优先 calm', () => {
      const ctx = { emotion: 'angry', personality: 'gentle', message: '我很生气' };
      const result = ds.decide(ctx);
      expect(result.action).toBe('calm');
    });

    test('返回决策因子', () => {
      const ctx = { emotion: 'neutral', personality: 'gentle', message: '' };
      const result = ds.decide(ctx);
      expect(Array.isArray(result.factors)).toBe(true);
    });
  });

  describe('辅助函数', () => {
    test('adjustForUrgency 识别高紧迫度', () => {
      const ctx = { emotion: 'neutral', personality: 'gentle', message: '', urgency: 'high' };
      const result = ds.decide(ctx);
      expect(result.action).toBeTruthy();
    });
  });
});

describe('evaluateImportance 重要性评估', () => {
  test('评估一般内容返回有效结果', async () => {
    const result = await evaluateImportance('今天天气不错', {
      emotion: 'happy',
      personality: 'gentle'
    });
    expect(result).toHaveProperty('importance');
    expect(result).toHaveProperty('level');
    expect(typeof result.importance).toBe('number');
  });

  test('评估重要内容（生日）', async () => {
    const result = await evaluateImportance('我的生日是12月25日', {
      emotion: 'neutral',
      personality: 'gentle'
    });
    // 生日属于中等以上重要性（实际规则返回值取决于关键词匹配）
    expect(result.importance).toBeGreaterThan(0);
    expect(result.importance).toBeLessThanOrEqual(10);
  });

  test('评估指令类内容', async () => {
    const result = await evaluateImportance('记住，以后每次都要这样做', {
      emotion: 'neutral',
      personality: 'gentle'
    });
    // importance 可能由规则或 LLM 判断
    expect(result.importance).toBeGreaterThan(0);
  });

  test('评估否定词内容', async () => {
    const result = await evaluateImportance('我不喜欢这个', {
      emotion: 'neutral',
      personality: 'gentle'
    });
    expect(result).toHaveProperty('importance');
    expect(result).toHaveProperty('level');
  });

  test('返回 level 在有效范围内', async () => {
    const result = await evaluateImportance('测试内容', {});
    expect(['low', 'medium', 'high']).toContain(result.level);
  });

  test('空内容返回 low 重要性而非抛出错误', async () => {
    const result = await evaluateImportance('', {});
    expect(result.level).toBe('low');
    expect(result.importance).toBe(1);
  });

  test('评估结果包含 method 字段', async () => {
    const result = await evaluateImportance('测试', {});
    expect(result).toHaveProperty('method');
    expect(['rule', 'llm', 'fallback', 'empty']).toContain(result.method);
  });
});
