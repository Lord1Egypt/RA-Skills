/**
 * State Machine 单元测试
 */

const {
  OrchestrationState,
  STATE_TRANSITIONS,
  StateMachine,
  OrchestrationTask
} = require('../src/state-machine');

describe('OrchestrationState', () => {
  test('应该定义所有状态', () => {
    expect(OrchestrationState.PENDING).toBe('pending');
    expect(OrchestrationState.RUNNING).toBe('running');
    expect(OrchestrationState.PAUSED).toBe('paused');
    expect(OrchestrationState.COMPLETED).toBe('completed');
    expect(OrchestrationState.FAILED).toBe('failed');
    expect(OrchestrationState.CANCELLED).toBe('cancelled');
  });
});

describe('STATE_TRANSITIONS', () => {
  test('应该定义有效的状态转换', () => {
    expect(STATE_TRANSITIONS.pending).toContain('running');
    expect(STATE_TRANSITIONS.pending).toContain('cancelled');
    expect(STATE_TRANSITIONS.running).toContain('completed');
    expect(STATE_TRANSITIONS.running).toContain('failed');
    expect(STATE_TRANSITIONS.running).toContain('paused');
    expect(STATE_TRANSITIONS.paused).toContain('running');
    expect(STATE_TRANSITIONS.paused).toContain('cancelled');
    expect(STATE_TRANSITIONS.failed).toContain('running'); // 允许重试
  });
});

describe('StateMachine', () => {
  let machine;

  beforeEach(() => {
    machine = new StateMachine();
  });

  test('应该创建初始状态为 pending 的状态机', () => {
    expect(machine.getState()).toBe(OrchestrationState.PENDING);
  });

  test('应该支持自定义初始状态', () => {
    const customMachine = new StateMachine(OrchestrationState.RUNNING);
    expect(customMachine.getState()).toBe(OrchestrationState.RUNNING);
  });

  test('应该检查状态转换是否有效', () => {
    expect(machine.canTransitionTo(OrchestrationState.RUNNING)).toBe(true);
    expect(machine.canTransitionTo(OrchestrationState.COMPLETED)).toBe(false);
  });

  test('应该执行有效的状态转换', async () => {
    const result = await machine.transition(OrchestrationState.RUNNING);

    expect(result.previousState).toBe(OrchestrationState.PENDING);
    expect(result.newState).toBe(OrchestrationState.RUNNING);
    expect(machine.getState()).toBe(OrchestrationState.RUNNING);
  });

  test('应该拒绝无效的状态转换', async () => {
    await expect(machine.transition(OrchestrationState.COMPLETED))
      .rejects.toThrow('Invalid state transition');
  });

  test('应该记录状态历史', async () => {
    await machine.transition(OrchestrationState.RUNNING);
    await machine.transition(OrchestrationState.COMPLETED);

    const history = machine.getHistory();
    expect(history.length).toBe(3); // initial + 2 transitions
    expect(history[1].state).toBe(OrchestrationState.RUNNING);
    expect(history[2].state).toBe(OrchestrationState.COMPLETED);
  });

  test('应该通知状态变化监听器', async () => {
    const listener = jest.fn();
    machine.onStateChange(listener);

    await machine.transition(OrchestrationState.RUNNING, { action: 'start' });

    expect(listener).toHaveBeenCalledWith(
      OrchestrationState.RUNNING,
      OrchestrationState.PENDING,
      { action: 'start' }
    );
  });

  test('应该计算状态持续时间', async () => {
    await machine.transition(OrchestrationState.RUNNING);
    await new Promise(resolve => setTimeout(resolve, 150));
    await machine.transition(OrchestrationState.COMPLETED);

    const duration = machine.getStateDuration(OrchestrationState.RUNNING);
    expect(duration).toBeGreaterThanOrEqual(100);
  });

  test('应该序列化状态机', () => {
    const serialized = machine.serialize();

    expect(serialized.state).toBe(OrchestrationState.PENDING);
    expect(serialized.history).toBeDefined();
    expect(serialized.serializedAt).toBeDefined();
  });

  test('应该从序列化数据恢复', () => {
    const original = new StateMachine(OrchestrationState.RUNNING, {
      metadata: { test: 'data' }
    });
    const serialized = original.serialize();

    const restored = StateMachine.deserialize(serialized);

    expect(restored.getState()).toBe(OrchestrationState.RUNNING);
    expect(restored.history.length).toBe(original.history.length);
  });

  test('应该判断是否为终态', async () => {
    expect(machine.isFinalState()).toBe(false);

    await machine.transition(OrchestrationState.RUNNING);
    expect(machine.isFinalState()).toBe(false);

    await machine.transition(OrchestrationState.COMPLETED);
    expect(machine.isFinalState()).toBe(true);
  });

  test('应该判断是否可以重试', async () => {
    expect(machine.canRetry()).toBe(false);

    await machine.transition(OrchestrationState.RUNNING);
    await machine.transition(OrchestrationState.FAILED);
    expect(machine.canRetry()).toBe(true);
  });
});

describe('OrchestrationTask', () => {
  let task;

  beforeEach(() => {
    task = new OrchestrationTask('task-123', {
      name: 'Test Task',
      steps: ['step1', 'step2']
    });
  });

  test('应该创建任务', () => {
    expect(task.taskId).toBe('task-123');
    expect(task.definition.name).toBe('Test Task');
  });

  test('应该启动任务', async () => {
    await task.start();
    expect(task.stateMachine.getState()).toBe(OrchestrationState.RUNNING);
  });

  test('应该完成任务', async () => {
    await task.start();
    await task.complete({ result: 'success' });

    expect(task.stateMachine.getState()).toBe(OrchestrationState.COMPLETED);
  });

  test('应该标记任务失败', async () => {
    await task.start();
    await task.fail(new Error('Test error'));

    expect(task.stateMachine.getState()).toBe(OrchestrationState.FAILED);
  });

  test('应该暂停和恢复任务', async () => {
    await task.start();
    await task.pause();

    expect(task.stateMachine.getState()).toBe(OrchestrationState.PAUSED);

    await task.resume();
    expect(task.stateMachine.getState()).toBe(OrchestrationState.RUNNING);
  });

  test('应该从暂停状态取消任务', async () => {
    await task.start();
    await task.pause();
    await task.cancel();

    expect(task.stateMachine.getState()).toBe(OrchestrationState.CANCELLED);
  });

  test('应该获取任务状态', async () => {
    await task.start();
    const status = task.getStatus();

    expect(status.taskId).toBe('task-123');
    expect(status.state).toBe(OrchestrationState.RUNNING);
    expect(status.createdAt).toBeDefined();
    expect(status.updatedAt).toBeDefined();
    expect(status.history).toBeDefined();
  });

  test('应该判断是否为终态', async () => {
    await task.start();
    let status = task.getStatus();
    expect(status.isFinal).toBe(false);

    await task.complete();
    status = task.getStatus();
    expect(status.isFinal).toBe(true);
  });

  test('应该判断是否可以重试', async () => {
    await task.start();
    let status = task.getStatus();
    expect(status.canRetry).toBe(false);

    await task.fail(new Error('Test'));
    status = task.getStatus();
    expect(status.canRetry).toBe(true);
  });
});
