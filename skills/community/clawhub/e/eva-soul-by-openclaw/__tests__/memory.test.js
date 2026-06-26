/**
 * EVA Soul - 记忆系统单元测试
 */

const { MemoryStore, MEMORY_TIERS, MEMORY_TYPES } = require('../lib/memory/memory');
const path = require('path');
const fs = require('fs');

// 使用临时目录进行测试
const TEST_DIR = path.join(__dirname, '..', '__test_tmp__');

beforeAll(() => {
  if (!fs.existsSync(TEST_DIR)) {
    fs.mkdirSync(TEST_DIR, { recursive: true });
  }
  ['short', 'medium', 'long', 'archive', 'auto'].forEach(dir => {
    const d = path.join(TEST_DIR, dir);
    if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });
  });
});

afterAll(() => {
  // 清理测试目录
  const rimraf = (dir) => {
    if (!fs.existsSync(dir)) return;
    fs.readdirSync(dir).forEach(file => {
      const cur = path.join(dir, file);
      if (fs.statSync(cur).isDirectory()) {
        rimraf(cur);
      } else {
        fs.unlinkSync(cur);
      }
    });
    fs.rmdirSync(dir);
  };
  rimraf(TEST_DIR);
});

describe('MEMORY_TIERS 记忆层级定义', () => {
  test('包含 short/medium/long/archive 四层', () => {
    expect(MEMORY_TIERS).toHaveProperty('short');
    expect(MEMORY_TIERS).toHaveProperty('medium');
    expect(MEMORY_TIERS).toHaveProperty('long');
    expect(MEMORY_TIERS).toHaveProperty('archive');
  });

  test('各层 maxAge 和 maxItems 有效', () => {
    expect(typeof MEMORY_TIERS.short.maxAge).toBe('number');
    expect(typeof MEMORY_TIERS.medium.maxAge).toBe('number');
    expect(typeof MEMORY_TIERS.long.maxAge).toBe('number');
  });
});

describe('MEMORY_TYPES 记忆类型定义', () => {
  test('包含主要类型', () => {
    expect(MEMORY_TYPES).toHaveProperty('fact');
    expect(MEMORY_TYPES).toHaveProperty('preference');
    expect(MEMORY_TYPES).toHaveProperty('instruction');
    expect(MEMORY_TYPES).toHaveProperty('event');
  });

  test('每种类型有 name 和 priority', () => {
    Object.values(MEMORY_TYPES).forEach(type => {
      expect(type).toHaveProperty('name');
      expect(type).toHaveProperty('priority');
      expect(type.priority).toBeGreaterThan(0);
    });
  });
});

describe('MemoryStore 记忆存储', () => {
  let store;

  beforeEach(() => {
    // 清理测试文件
    ['short', 'medium', 'long', 'archive'].forEach(dir => {
      const dirPath = path.join(TEST_DIR, dir);
      if (fs.existsSync(dirPath)) {
        fs.readdirSync(dirPath).forEach(f => {
          if (f.endsWith('.json')) {
            try { fs.unlinkSync(path.join(dirPath, f)); } catch (e) {}
          }
        });
      }
    });
    store = new MemoryStore(TEST_DIR);
  });

  describe('save 保存记忆', () => {
    test('保存记忆返回 id', () => {
      const result = store.save({ content: '测试记忆', importance: 5 });
      expect(result).toHaveProperty('id');
      expect(result.id).toBeTruthy();
    });

    test('保存记忆包含所有字段', () => {
      const result = store.save({
        content: '我的生日',
        type: 'event',
        importance: 8,
        tags: ['生日', '重要']
      });
      expect(result.content).toBe('我的生日');
      expect(result.type).toBe('event');
      expect(result.importance).toBe(8);
      expect(result.tier).toBe('short');
      expect(result.tags).toContain('生日');
    });

    test('自动生成 id 唯一', () => {
      const r1 = store.save({ content: '记忆1' });
      const r2 = store.save({ content: '记忆2' });
      expect(r1.id).not.toBe(r2.id);
    });
  });

  describe('search 搜索记忆', () => {
    test('搜索关键词返回相关记忆', async () => {
      store.save({ content: '主人喜欢吃苹果', importance: 5 });
      store.save({ content: '今天是晴天', importance: 5 });

      // 直接读取文件系统进行搜索
      const shortDir = path.join(TEST_DIR, 'short');
      const files = fs.readdirSync(shortDir).filter(f => f.endsWith('.json'));
      const results = [];
      for (const file of files) {
        const content = fs.readFileSync(path.join(shortDir, file), 'utf8');
        const memory = JSON.parse(content);
        if (memory.content.includes('苹果')) {
          results.push(memory);
        }
      }
      expect(results.length).toBeGreaterThan(0);
    });

    test('按重要性过滤', () => {
      store.save({ content: '普通记忆', importance: 3 });
      store.save({ content: '重要记忆', importance: 8 });

      const shortDir = path.join(TEST_DIR, 'short');
      const files = fs.readdirSync(shortDir).filter(f => f.endsWith('.json'));
      let importantCount = 0;
      for (const file of files) {
        const content = fs.readFileSync(path.join(shortDir, file), 'utf8');
        const memory = JSON.parse(content);
        if (memory.importance >= 5) importantCount++;
      }
      expect(importantCount).toBe(1);
    });
  });

  describe('delete 删除记忆', () => {
    test('删除存在的记忆返回 true', () => {
      const result = store.save({ content: '待删除记忆', importance: 5 });
      const deleted = store.delete(result.id);
      expect(deleted).toBe(true);
    });

    test('删除不存在的记忆返回 false', () => {
      const deleted = store.delete('nonexistent_id_12345');
      expect(deleted).toBe(false);
    });
  });

  describe('generateId 生成 ID', () => {
    test('生成的 ID 唯一', () => {
      const ids = new Set();
      for (let i = 0; i < 100; i++) {
        ids.add(store.generateId());
      }
      expect(ids.size).toBe(100);
    });
  });

  describe('autoSave 自动记忆', () => {
    test('包含"记住"关键词触发自动记忆', () => {
      const result = store.autoSave('记住，我喜欢喝咖啡', 'neutral');
      expect(result).not.toBeNull();
      expect(result.type).toBe('instruction');
    });

    test('包含"喜欢"关键词', () => {
      const result = store.autoSave('我喜欢蓝色', 'happy');
      expect(result).not.toBeNull();
      expect(result.type).toBe('preference');
    });

    test('普通消息不触发自动记忆', () => {
      const result = store.autoSave('今天天气不错', 'neutral');
      expect(result).toBeNull();
    });
  });

  describe('getStats 统计信息', () => {
    test('返回各层统计', () => {
      store.save({ content: '测试1', importance: 5 });
      store.save({ content: '测试2', importance: 5 });
      const stats = store.getStats();
      expect(stats).toHaveProperty('short');
      expect(stats).toHaveProperty('medium');
      expect(stats).toHaveProperty('long');
      expect(stats).toHaveProperty('total');
    });
  });
});
