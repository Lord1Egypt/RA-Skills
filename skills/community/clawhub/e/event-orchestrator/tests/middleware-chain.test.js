/**
 * Middleware Chain 单元测试
 */

const {
  LoggingMiddleware,
  ValidationMiddleware,
  RetryMiddleware,
  RateLimitMiddleware,
  MiddlewareChainExecutor
} = require('../src/middleware-chain');

describe('LoggingMiddleware', () => {
  test('应该创建日志中间件实例', () => {
    const middleware = new LoggingMiddleware();
    expect(middleware).toBeDefined();
  });

  test('应该记录事件日志', async () => {
    const logger = { info: jest.fn() };
    const middleware = new LoggingMiddleware({ logger });

    const event = {
      id: 'test-123',
      name: 'test.event',
      timestamp: Date.now(),
      metadata: { correlationId: 'corr-123' }
    };

    const result = await middleware.handle(event);

    expect(result).toBe(true);
    expect(logger.info).toHaveBeenCalled();
  });

  test('应该支持 debug 日志级别', async () => {
    const logger = { debug: jest.fn() };
    const middleware = new LoggingMiddleware({ logLevel: 'debug', logger });

    const event = {
      id: 'test-123',
      name: 'test.event',
      timestamp: Date.now(),
      metadata: { correlationId: 'corr-123' },
      payload: { data: 'test' }
    };

    await middleware.handle(event);

    expect(logger.debug).toHaveBeenCalled();
  });
});

describe('ValidationMiddleware', () => {
  test('应该创建验证中间件实例', () => {
    const validator = jest.fn().mockResolvedValue(true);
    const middleware = new ValidationMiddleware(validator);
    expect(middleware).toBeDefined();
  });

  test('应该通过有效事件', async () => {
    const validator = jest.fn().mockResolvedValue(true);
    const middleware = new ValidationMiddleware(validator);

    const event = { name: 'test.event' };
    const result = await middleware.handle(event);

    expect(result).toBe(true);
    expect(validator).toHaveBeenCalledWith(event);
  });

  test('应该阻止无效事件', async () => {
    const validator = jest.fn().mockResolvedValue(false);
    const middleware = new ValidationMiddleware(validator);

    const event = { name: 'test.event' };
    const result = await middleware.handle(event);

    expect(result).toBe(false);
  });

  test('应该处理验证器错误', async () => {
    const validator = jest.fn().mockRejectedValue(new Error('Validation failed'));
    const middleware = new ValidationMiddleware(validator);

    const event = { name: 'test.event' };
    const result = await middleware.handle(event);

    expect(result).toBe(false);
  });
});

describe('RetryMiddleware', () => {
  test('应该创建重试中间件实例', () => {
    const middleware = new RetryMiddleware();
    expect(middleware).toBeDefined();
    expect(middleware.maxRetries).toBe(3);
  });

  test('应该允许未达到最大重试次数的事件', async () => {
    const middleware = new RetryMiddleware({ maxRetries: 3 });
    const event = {
      name: 'test.event',
      metadata: { retryCount: 1 }
    };

    const result = await middleware.handle(event);
    expect(result).toBe(true);
  });

  test('应该阻止超过最大重试次数的事件', async () => {
    const middleware = new RetryMiddleware({ maxRetries: 3 });
    const event = {
      name: 'test.event',
      metadata: { retryCount: 3 }
    };

    const result = await middleware.handle(event);
    expect(result).toBe(false);
  });

  test('应该成功重试', async () => {
    const middleware = new RetryMiddleware({ maxRetries: 3, retryDelay: 10 });
    const handler = jest.fn()
      .mockRejectedValueOnce(new Error('First attempt failed'))
      .mockResolvedValueOnce('success');

    const event = { name: 'test.event' };
    const result = await middleware.retry(event, handler);

    expect(result).toBe('success');
    expect(handler).toHaveBeenCalledTimes(2);
  });

  test('应该在达到最大重试次数后抛出错误', async () => {
    const middleware = new RetryMiddleware({ maxRetries: 2, retryDelay: 10 });
    const handler = jest.fn().mockRejectedValue(new Error('Always fails'));

    const event = { name: 'test.event' };

    await expect(middleware.retry(event, handler)).rejects.toThrow('Always fails');
    expect(handler).toHaveBeenCalledTimes(2);
  });
});

describe('RateLimitMiddleware', () => {
  test('应该创建速率限制中间件实例', () => {
    const middleware = new RateLimitMiddleware();
    expect(middleware).toBeDefined();
    expect(middleware.maxEvents).toBe(100);
  });

  test('应该允许未达到限制的事件', async () => {
    const middleware = new RateLimitMiddleware({ maxEvents: 5, windowMs: 1000 });
    const event = { name: 'test.event' };

    const result = await middleware.handle(event);
    expect(result).toBe(true);
  });

  test('应该阻止超过限制的事件', async () => {
    const middleware = new RateLimitMiddleware({ maxEvents: 3, windowMs: 10000 });
    
    for (let i = 0; i < 3; i++) {
      await middleware.handle({ name: 'limit.event' });
    }

    const result = await middleware.handle({ name: 'limit.event' });
    expect(result).toBe(false);
  });
});

describe('MiddlewareChainExecutor', () => {
  test('应该创建执行器实例', () => {
    const executor = new MiddlewareChainExecutor();
    expect(executor).toBeDefined();
  });

  test('应该执行中间件链', async () => {
    const executor = new MiddlewareChainExecutor();
    const middleware1 = { handle: jest.fn().mockResolvedValue(true) };
    const middleware2 = { handle: jest.fn().mockResolvedValue(true) };

    executor.use(middleware1);
    executor.use(middleware2);

    const event = { name: 'test.event' };
    const result = await executor.execute(event);

    expect(result.stopped).toBe(false);
    expect(middleware1.handle).toHaveBeenCalledWith(event);
    expect(middleware2.handle).toHaveBeenCalledWith(event);
  });

  test('应该在中间件返回 false 时停止', async () => {
    const executor = new MiddlewareChainExecutor();
    const middleware1 = { handle: jest.fn().mockResolvedValue(true) };
    const middleware2 = { handle: jest.fn().mockResolvedValue(false) };
    const middleware3 = { handle: jest.fn().mockResolvedValue(true) };

    executor.use(middleware1);
    executor.use(middleware2);
    executor.use(middleware3);

    const event = { name: 'test.event' };
    const result = await executor.execute(event);

    expect(result.stopped).toBe(true);
    expect(middleware1.handle).toHaveBeenCalled();
    expect(middleware2.handle).toHaveBeenCalled();
    expect(middleware3.handle).not.toHaveBeenCalled();
  });

  test('应该处理中间件错误并继续', async () => {
    const executor = new MiddlewareChainExecutor();
    const middleware1 = { handle: jest.fn().mockRejectedValue(new Error('Error')) };
    const middleware2 = { handle: jest.fn().mockResolvedValue(true) };

    executor.use(middleware1);
    executor.use(middleware2);

    const event = { name: 'test.event' };
    const result = await executor.execute(event);

    expect(result.stopped).toBe(false);
    expect(middleware2.handle).toHaveBeenCalled();
  });
});
