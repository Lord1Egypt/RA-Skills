/**
 * EVA Soul - 状态管理单元测试
 */

jest.mock('fs', () => {
  const _mem = {};
  return {
    existsSync: jest.fn((path) => path in _mem),
    readFileSync: jest.fn((path) => {
      if (path in _mem) return _mem[path];
      throw new Error('ENOENT');
    }),
    writeFileSync: jest.fn((path, data) => { _mem[path] = data; }),
    unlinkSync: jest.fn(),
    mkdirSync: jest.fn()
  };
});
jest.mock('../lib/core/config', () => ({
  expandPath: (p) => p
}));

const {
  DEFAULT_STATE,
  createState,
  updateEmotion,
  updatePersonality,
  recordInteraction,
  incrementSession,
  setSleepState,
  recordToolUsage,
  getStateSummary
} = require('../lib/core/state');

describe('DEFAULT_STATE 默认状态', () => {
  test('包含所有必需字段', () => {
    expect(DEFAULT_STATE).toHaveProperty('currentEmotion');
    expect(DEFAULT_STATE).toHaveProperty('personality');
    expect(DEFAULT_STATE).toHaveProperty('emotionHistory');
    expect(DEFAULT_STATE).toHaveProperty('sessionCount');
    expect(DEFAULT_STATE).toHaveProperty('isSleeping');
    expect(DEFAULT_STATE).toHaveProperty('toolUsage');
  });

  test('初始情感为 neutral', () => {
    expect(DEFAULT_STATE.currentEmotion).toBe('neutral');
  });

  test('初始性格为 gentle', () => {
    expect(DEFAULT_STATE.personality).toBe('gentle');
  });

  test('初始睡眠状态为 false', () => {
    expect(DEFAULT_STATE.isSleeping).toBe(false);
  });
});

describe('createState 创建新状态', () => {
  test('返回包含 initializedAt 的状态对象', () => {
    const state = createState();
    expect(state).toHaveProperty('initializedAt');
    expect(state.initializedAt).toBeTruthy();
  });

  test('继承所有 DEFAULT_STATE 字段', () => {
    const state = createState();
    Object.keys(DEFAULT_STATE).forEach(key => {
      expect(state).toHaveProperty(key);
    });
  });
});

describe('updateEmotion 更新情感', () => {
  test('更新当前情感', () => {
    const state = createState();
    const result = updateEmotion(state, 'happy');
    expect(result.currentEmotion).toBe('happy');
  });

  test('记录情感历史', () => {
    const state = createState();
    const result = updateEmotion(state, 'sad');
    expect(result.emotionHistory.length).toBeGreaterThan(0);
    const lastEntry = result.emotionHistory[result.emotionHistory.length - 1];
    expect(lastEntry.from).toBe('neutral');
    expect(lastEntry.to).toBe('sad');
  });

  test('保留最近50条历史', () => {
    const state = createState();
    for (let i = 0; i < 60; i++) {
      updateEmotion(state, 'happy');
    }
    expect(state.emotionHistory.length).toBeLessThanOrEqual(50);
  });
});

describe('updatePersonality 更新性格', () => {
  test('更新性格', () => {
    const state = createState();
    const result = updatePersonality(state, 'cute');
    expect(result.personality).toBe('cute');
  });

  test('保留修饰符', () => {
    const state = createState();
    const modifiers = { playfulness: 0.8 };
    const result = updatePersonality(state, 'cute', modifiers);
    expect(result.personalityModifiers.playfulness).toBe(0.8);
  });
});

describe('recordInteraction 记录交互', () => {
  test('更新最后交互时间', () => {
    const state = createState();
    const result = recordInteraction(state);
    expect(result.lastInteraction).toBeTruthy();
  });

  test('增加总交互次数', () => {
    const state = createState();
    const before = state.totalInteractions;
    recordInteraction(state);
    expect(state.totalInteractions).toBe(before + 1);
  });

  test('记录消息摘要', () => {
    const state = createState();
    recordInteraction(state, '主人问我问题');
    expect(state.lastInteractionMessage).toBe('主人问我问题');
  });
});

describe('incrementSession 增加会话数', () => {
  test('增加 sessionCount', () => {
    const state = createState();
    incrementSession(state);
    expect(state.sessionCount).toBe(1);
    incrementSession(state);
    expect(state.sessionCount).toBe(2);
  });

  test('设置 sessionStartTime', () => {
    const state = createState();
    incrementSession(state);
    expect(state.sessionStartTime).toBeTruthy();
  });
});

describe('setSleepState 睡眠/唤醒', () => {
  test('设置为睡眠', () => {
    const state = createState();
    const result = setSleepState(state, true);
    expect(result.isSleeping).toBe(true);
    expect(result.sleepStartTime).toBeTruthy();
  });

  test('唤醒', () => {
    const state = createState();
    setSleepState(state, true);
    const result = setSleepState(state, false);
    expect(result.isSleeping).toBe(false);
    expect(result.lastWakeTime).toBeTruthy();
  });
});

describe('recordToolUsage 工具使用记录', () => {
  test('记录工具使用次数', () => {
    const state = createState();
    recordToolUsage(state, 'eva_memory');
    expect(state.toolUsage['eva_memory']).toBe(1);
    recordToolUsage(state, 'eva_memory');
    expect(state.toolUsage['eva_memory']).toBe(2);
  });

  test('新工具从0开始', () => {
    const state = createState();
    recordToolUsage(state, 'eva_decide');
    expect(state.toolUsage['eva_decide']).toBe(1);
  });
});

describe('getStateSummary 获取状态摘要', () => {
  test('返回必要字段', () => {
    const state = createState();
    state.sessionCount = 5;
    const summary = getStateSummary(state);
    expect(summary).toHaveProperty('emotion');
    expect(summary).toHaveProperty('personality');
    expect(summary).toHaveProperty('sessionCount');
    expect(summary).toHaveProperty('uptime');
  });

  test('sessionCount 正确', () => {
    const state = createState();
    state.sessionCount = 42;
    const summary = getStateSummary(state);
    expect(summary.sessionCount).toBe(42);
  });
});
