/**
 * EventOrchestrator 主入口单元测试
 */

const {
  EventOrchestrator,
  EventSchemas,
  EventBus,
  OrchestrationState,
  LoggingMiddleware,
  RetryMiddleware
} = require('../src/index');

describe('EventOrchestrator', () => {
  let orchestrator;

  beforeEach(() => {
    orchestrator = new EventOrchestrator({ maxHistorySize: 100 });
  });

  afterEach(() => {
    orchestrator.clear();
  });

  test('应该创建编排器实例', () => {
    expect(orchestrator).toBeDefined();
    expect(orchestrator.eventBus).toBeInstanceOf(EventBus);
  });

  test('应该注册事件 Schema', () => {
    const schema = { name: 'string', required: ['name'] };
    orchestrator.registerSchema('test.event', schema);
    // 无错误即成功
  });

  test('应该订阅和发布事件', async () => {
    const handler = jest.fn();
    orchestrator.subscribe('test.event', handler);

    const result = await orchestrator.publish('test.event', { data: 'test' });

    expect(result.status).toBe('published');
    expect(handler).toHaveBeenCalledTimes(1);
  });

  test('应该取消订阅', async () => {
    const handler = jest.fn();
    const subscriberId = orchestrator.subscribe('test.event', handler);

    orchestrator.unsubscribe('test.event', subscriberId);
    await orchestrator.publish('test.event', { data: 'test' });

    expect(handler).not.toHaveBeenCalled();
  });

  test('应该创建编排任务', () => {
    const task = orchestrator.createTask('task-123', {
      name: 'Test Task',
      steps: ['step1', 'step2']
    });

    expect(task).toBeDefined();
    expect(task.taskId).toBe('task-123');
  });

  test('应该获取任务状态', async () => {
    orchestrator.createTask('task-123', { name: 'Test' });
    
    const status = orchestrator.getTaskStatus('task-123');
    expect(status.taskId).toBe('task-123');
    expect(status.state).toBe(OrchestrationState.PENDING);
  });

  test('应该返回未找到任务的错误', () => {
    const status = orchestrator.getTaskStatus('nonexistent');
    expect(status.error).toBe('Task not found');
  });

  test('应该获取所有任务状态', async () => {
    orchestrator.createTask('task-1', { name: 'Task 1' });
    orchestrator.createTask('task-2', { name: 'Task 2' });

    const allStatus = orchestrator.getAllTasksStatus();
    expect(Object.keys(allStatus).length).toBe(2);
    expect(allStatus['task-1']).toBeDefined();
    expect(allStatus['task-2']).toBeDefined();
  });

  test('应该获取事件历史', async () => {
    await orchestrator.publish('event.1', { data: 1 });
    await orchestrator.publish('event.2', { data: 2 });
    await orchestrator.publish('event.3', { data: 3 });

    const history = orchestrator.getEventHistory(10);
    expect(history.length).toBe(3);
  });

  test('应该获取订阅者统计', () => {
    orchestrator.subscribe('stat.event1', jest.fn());
    orchestrator.subscribe('stat.event1', jest.fn());
    orchestrator.subscribe('stat.event2', jest.fn());

    const stats = orchestrator.getSubscriberStats();
    expect(stats['stat.event1']).toBe(2);
    expect(stats['stat.event2']).toBe(1);
  });

  test('应该添加自定义中间件', () => {
    const middleware = new LoggingMiddleware({ logLevel: 'debug' });
    orchestrator.useMiddleware(middleware);
    // 无错误即成功
  });

  test('应该清空所有数据', async () => {
    await orchestrator.publish('event.1', { data: 1 });
    orchestrator.createTask('task-1', { name: 'Test' });

    orchestrator.clear();

    expect(orchestrator.getEventHistory().length).toBe(0);
    expect(Object.keys(orchestrator.getAllTasksStatus()).length).toBe(0);
  });

  test('应该导出状态', async () => {
    await orchestrator.publish('event.1', { data: 1 });
    orchestrator.createTask('task-1', { name: 'Test' });

    const state = orchestrator.exportState();

    expect(state.tasks).toBeDefined();
    expect(state.eventHistory).toBeDefined();
    expect(state.subscriberStats).toBeDefined();
    expect(state.exportedAt).toBeDefined();
  });
});

describe('EventSchemas', () => {
  test('应该定义技能执行事件 Schema', () => {
    expect(EventSchemas['skill.started']).toBeDefined();
    expect(EventSchemas['skill.completed']).toBeDefined();
    expect(EventSchemas['skill.failed']).toBeDefined();
  });

  test('应该定义任务编排事件 Schema', () => {
    expect(EventSchemas['task.created']).toBeDefined();
    expect(EventSchemas['task.started']).toBeDefined();
    expect(EventSchemas['task.completed']).toBeDefined();
    expect(EventSchemas['task.failed']).toBeDefined();
  });

  test('应该定义系统事件 Schema', () => {
    expect(EventSchemas['system.ready']).toBeDefined();
    expect(EventSchemas['system.shutdown']).toBeDefined();
  });

  test('Schema 应该有正确的结构', () => {
    const schema = EventSchemas['skill.completed'];
    expect(schema.skillId).toBe('string');
    expect(schema.taskId).toBe('string');
    expect(schema.result).toBe('object');
    expect(schema.duration).toBe('number');
  });
});

describe('集成测试', () => {
  test('应该完成完整的任务编排流程', async () => {
    const orchestrator = new EventOrchestrator();
    const events = [];

    // 订阅事件
    orchestrator.subscribe('task.started', (e) => events.push({ type: 'started', ...e }));
    orchestrator.subscribe('task.completed', (e) => events.push({ type: 'completed', ...e }));

    // 创建任务
    const task = orchestrator.createTask('integration-task', { name: 'Integration Test' });

    // 启动任务并发布事件
    await task.start();
    await orchestrator.publish('task.started', { taskId: 'integration-task', startedAt: Date.now() });

    // 完成任务并发布事件
    await task.complete({ result: 'success' });
    await orchestrator.publish('task.completed', { taskId: 'integration-task', completedAt: Date.now(), result: { success: true } });

    // 验证事件
    expect(events.length).toBe(2);
    expect(events[0].type).toBe('started');
    expect(events[1].type).toBe('completed');

    // 验证任务状态
    const status = orchestrator.getTaskStatus('integration-task');
    expect(status.state).toBe(OrchestrationState.COMPLETED);
    expect(status.isFinal).toBe(true);

    orchestrator.clear();
  });

  test('应该处理任务失败和重试', async () => {
    const orchestrator = new EventOrchestrator();

    // 创建任务
    const task = orchestrator.createTask('retry-task', { name: 'Retry Test' });

    // 启动任务
    await task.start();

    // 模拟失败
    await task.fail(new Error('Test failure'));

    // 验证可以重试
    let status = orchestrator.getTaskStatus('retry-task');
    expect(status.state).toBe(OrchestrationState.FAILED);
    expect(status.canRetry).toBe(true);

    // 重试（通过恢复状态）
    await task.resume();
    status = orchestrator.getTaskStatus('retry-task');
    expect(status.state).toBe(OrchestrationState.RUNNING);

    // 完成
    await task.complete({ result: 'success after retry' });
    status = orchestrator.getTaskStatus('retry-task');
    expect(status.state).toBe(OrchestrationState.COMPLETED);

    orchestrator.clear();
  });
});
