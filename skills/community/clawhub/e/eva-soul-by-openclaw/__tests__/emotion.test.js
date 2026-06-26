/**
 * EVA Soul - 情感系统单元测试
 */

// Mock hooks 模块
jest.mock('../hooks/errorHandler', () => ({
  fetchWithRetry: jest.fn()
}));
jest.mock('../hooks/logger', () => ({
  debug: jest.fn(),
  info: jest.fn(),
  warn: jest.fn(),
  error: jest.fn()
}));
jest.mock('fs', () => ({
  existsSync: jest.fn(() => false),
  readFileSync: jest.fn(() => '{}'),
  writeFileSync: jest.fn()
}));

const {
  EMOTIONS,
  detectEmotion,
  getIntensityLevel,
  analyzeEmotionTrend,
  getEmotionData,
  getAllEmotions
} = require('../lib/emotion/emotion');

describe('EMOTIONS 数据结构', () => {
  test('EMOTIONS 包含所有基础情感类型', () => {
    const baseEmotions = ['happy', 'sad', 'angry', 'neutral', 'excited', 'tired', 'surprised', 'confused'];
    baseEmotions.forEach(emotion => {
      expect(EMOTIONS).toHaveProperty(emotion);
    });
  });

  test('每种情感有 keywords 数组', () => {
    Object.entries(EMOTIONS).forEach(([key, data]) => {
      expect(data).toHaveProperty('keywords');
      expect(Array.isArray(data.keywords)).toBe(true);
    });
  });

  test('每种情感有 intensity 值', () => {
    Object.entries(EMOTIONS).forEach(([key, data]) => {
      expect(data).toHaveProperty('intensity');
      expect(typeof data.intensity).toBe('number');
    });
  });
});

describe('detectEmotion 情感检测', () => {
  test('空文本返回 neutral', async () => {
    const result = await detectEmotion('');
    expect(result.emotion).toBe('neutral');
  });

  test('使用实际关键词检测开心', async () => {
    const result = await detectEmotion('我很开心！太好了！');
    expect(result.emotion).toBe('happy');
  });

  test('使用实际关键词检测悲伤', async () => {
    const result = await detectEmotion('我好难过，伤心');
    expect(result.emotion).toBe('sad');
  });

  test('使用实际关键词检测愤怒', async () => {
    const result = await detectEmotion('气死我了！愤怒！');
    expect(result.emotion).toBe('angry');
  });

  test('中性文本返回 neutral', async () => {
    const result = await detectEmotion('这是桌子上的书');
    expect(result.emotion).toBe('neutral');
  });

  test('返回结果包含 emotion 字段', async () => {
    const result = await detectEmotion('今天天气不错');
    expect(result).toHaveProperty('emotion');
    expect(typeof result.emotion).toBe('string');
  });

  test('检测兴奋情感', async () => {
    const result = await detectEmotion('太激动了！超棒！');
    expect(['excited', 'happy']).toContain(result.emotion);
  });
});

describe('getIntensityLevel 情感强度', () => {
  test('高强度返回 high', () => {
    expect(getIntensityLevel(0.75)).toBe('high');
  });

  test('中等强度返回 medium', () => {
    expect(getIntensityLevel(0.55)).toBe('medium');
  });

  test('低强度返回 low', () => {
    expect(getIntensityLevel(0.3)).toBe('low');
  });

  test('极高强度返回 very_high', () => {
    expect(getIntensityLevel(0.95)).toBe('very_high');
  });

  test('极低强度返回 very_low', () => {
    expect(getIntensityLevel(0.1)).toBe('very_low');
  });
});

describe('analyzeEmotionTrend 情感趋势分析', () => {
  test('空历史返回 stable 趋势', () => {
    const result = analyzeEmotionTrend([]);
    expect(result.trend).toBe('stable');
    expect(result.dominant).toBeNull();
  });

  test('单条历史返回 stable 趋势', () => {
    const history = [{ to: 'happy', time: new Date().toISOString() }];
    const result = analyzeEmotionTrend(history);
    expect(result.trend).toBe('stable');
  });

  test('多条历史返回趋势对象', () => {
    const history = [
      { from: 'neutral', to: 'happy', time: new Date(Date.now() - 60000).toISOString() },
      { from: 'happy', to: 'excited', time: new Date().toISOString() }
    ];
    const result = analyzeEmotionTrend(history);
    expect(result).toHaveProperty('trend');
    expect(result).toHaveProperty('dominant');
    expect(result).toHaveProperty('changes');
  });
});

describe('getEmotionData 获取情感数据', () => {
  test('获取已知情感数据', () => {
    const data = getEmotionData('happy');
    expect(data).toBeTruthy();
    expect(data.name).toBe('开心');
  });

  test('未知情感 fallback 到 neutral', () => {
    const data = getEmotionData('totally_unknown_xyz');
    expect(data).toBeTruthy();
    expect(data.name).toBe('平静');
  });
});

describe('getAllEmotions 获取所有情感', () => {
  test('返回所有情感类型列表', () => {
    const result = getAllEmotions();
    expect(Array.isArray(result)).toBe(true);
    expect(result.length).toBeGreaterThan(0);
    expect(result).toContain('happy');
    expect(result).toContain('sad');
    expect(result).toContain('neutral');
  });
});
