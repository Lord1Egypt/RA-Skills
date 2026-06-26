/**
 * EventBus 单元测试
 * 
 * 测试覆盖：事件发布/订阅、中间件、历史记录
 */

const { EventBus, EventValidator } = require('../src/event-bus');

describe('EventBus', () => {
  let eventBus;

  beforeEach(() => {
    eventBus = new EventBus({ maxHistorySize: 100 });
  });

  afterEach(() => {
    eventBus.clearHistory();
  });

  describe('订阅与发布', () => {
    test('应该成功订阅和发布事件', async () => {
      const handler = jest.fn();
      const subscriberId = eventBus.subscribe('test.event', handler);

      expect(subscriberId).toBeDefined();
      expect(typeof subscriberId).toBe('string');

      const result = await eventBus.publish('test.event', { data: 'test' });

      expect(result.status).toBe('published');
      expect(result.eventId).toBeDefined();
      expect(handler).toHaveBeenCalledTimes(1);
      expect(handler).toHaveBeenCalledWith(expect.objectContaining({
        name: 'test.event',
        payload: { data: 'test' }
      }));
    });

    test('应该支持多个订阅者', async () => {
      const handler1 = jest.fn();
      const handler2 = jest.fn();

      eventBus.subscribe('multi.event', handler1);
      eventBus.subscribe('multi.event', handler2);

      await eventBus.publish('multi.event', { data: 'test' });

      expect(handler1).toHaveBeenCalledTimes(1);
      expect(handler2).toHaveBeenCalledTimes(1);
    });

    test('应该支持 once 订阅（一次性）', async () => {
      const handler = jest.fn();
      eventBus.subscribe('once.event', handler, { once: true });

      await eventBus.publish('once.event', { data: 'first' });
      await eventBus.publish('once.event', { data: 'second' });

      expect(handler).toHaveBeenCalledTimes(1);
    });

    test('应该支持取消订阅', async () => {
      const handler = jest.fn();
      const subscriberId = eventBus.subscribe('cancel.event', handler);

      expect(eventBus.unsubscribe('cancel.event', subscriberId)).toBe(true);

      await eventBus.publish('cancel.event', { data: 'test' });

      expect(handler).not.toHaveBeenCalled();
    });
  });

  describe('事件过滤器', () => {
    test('应该支持事件过滤', async () => {
      const handler = jest.fn();
      const filter = (payload) => payload.value > 5;

      eventBus.subscribe('filtered.event', handler, { filter });

      await eventBus.publish('filtered.event', { value: 3 }); // 不满足过滤
      await eventBus.publish('filtered.event', { value: 7 }); // 满足过滤

      expect(handler).toHaveBeenCalledTimes(1);
    });
  });

  describe('事件历史', () => {
    test('应该记录事件历史', async () => {
      await eventBus.publish('history.event1', { data: 1 });
      await eventBus.publish('history.event2', { data: 2 });
      await eventBus.publish('history.event3', { data: 3 });

      const history = eventBus.getHistory();

      expect(history.length).toBe(3);
      expect(history[0].name).toBe('history.event1');
      expect(history[2].name).toBe('history.event3');
    });

    test('应该支持按事件名过滤历史', async () => {
      await eventBus.publish('type.a', { data: 1 });
      await eventBus.publish('type.b', { data: 2 });
      await eventBus.publish('type.a', { data: 3 });

      const history = eventBus.getHistory(100, 'type.a');

      expect(history.length).toBe(2);
      expect(history.every(e => e.name === 'type.a')).toBe(true);
    });

    test('应该限制历史记录大小', async () => {
      const smallBus = new EventBus({ maxHistorySize: 5 });

      for (let i = 0; i < 10; i++) {
        await smallBus.publish(`event.${i}`, { index: i });
      }

      const history = smallBus.getHistory();
      expect(history.length).toBe(5);
      expect(history[0].name).toBe('event.5'); // 最早的被移除
    });
  });

  describe('事件验证', () => {
    test('应该验证事件 Schema', async () => {
      eventBus.registerSchema('validated.event', {
        name: 'string',
        age: 'number',
        required: ['name']
      });

      // 有效事件
      await expect(eventBus.publish('validated.event', { name: 'John', age: 30 }))
        .resolves.toMatchObject({ status: 'published' });

      // 缺少必填字段
      await expect(eventBus.publish('validated.event', { age: 30 }))
        .rejects.toThrow('Missing required field: name');

      // 类型错误
      await expect(eventBus.publish('validated.event', { name: 123, age: 30 }))
        .rejects.toThrow('Invalid type');
    });
  });

  describe('订阅者统计', () => {
    test('应该返回订阅者统计', () => {
      eventBus.subscribe('stat.event1', jest.fn());
      eventBus.subscribe('stat.event1', jest.fn());
      eventBus.subscribe('stat.event2', jest.fn());

      const stats = eventBus.getSubscriberStats();

      expect(stats['stat.event1']).toBe(2);
      expect(stats['stat.event2']).toBe(1);
    });
  });
});

describe('EventValidator', () => {
  test('应该创建验证器实例', () => {
    const validator = new EventValidator();
    expect(validator).toBeDefined();
  });

  test('应该注册和验证 Schema', () => {
    const validator = new EventValidator();
    
    validator.registerSchema('test.event', {
      name: 'string',
      required: ['name']
    });

    expect(validator.validate('test.event', { name: 'John' })).toBe(true);
    expect(() => validator.validate('test.event', {})).toThrow();
  });
});
