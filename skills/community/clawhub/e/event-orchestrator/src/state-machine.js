/**
 * State Machine - 状态机实现
 * 
 * 设计模式：状态机模式
 * 来源：DeerFlow 架构学习
 */

/**
 * 编排任务状态枚举
 */
const OrchestrationState = {
  PENDING: 'pending',
  RUNNING: 'running',
  PAUSED: 'paused',
  COMPLETED: 'completed',
  FAILED: 'failed',
  CANCELLED: 'cancelled'
};

/**
 * 状态转换规则
 */
const STATE_TRANSITIONS = {
  [OrchestrationState.PENDING]: [OrchestrationState.RUNNING, OrchestrationState.CANCELLED],
  [OrchestrationState.RUNNING]: [OrchestrationState.COMPLETED, OrchestrationState.FAILED, OrchestrationState.PAUSED],
  [OrchestrationState.PAUSED]: [OrchestrationState.RUNNING, OrchestrationState.CANCELLED],
  [OrchestrationState.COMPLETED]: [], // 终态
  [OrchestrationState.FAILED]: [OrchestrationState.RUNNING], // 允许重试
  [OrchestrationState.CANCELLED]: [] // 终态
};

/**
 * 状态机类
 */
class StateMachine {
  constructor(initialState = OrchestrationState.PENDING, options = {}) {
    this.state = initialState;
    this.history = [{ state: initialState, timestamp: Date.now() }];
    this.metadata = options.metadata || {};
    this.listeners = [];
  }

  /**
   * 获取当前状态
   */
  getState() {
    return this.state;
  }

  /**
   * 检查是否可以转换到目标状态
   */
  canTransitionTo(targetState) {
    const allowedTransitions = STATE_TRANSITIONS[this.state] || [];
    return allowedTransitions.includes(targetState);
  }

  /**
   * 状态转换
   */
  async transition(targetState, context = {}) {
    if (!this.canTransitionTo(targetState)) {
      throw new Error(
        `Invalid state transition: ${this.state} → ${targetState}. ` +
        `Allowed transitions: ${STATE_TRANSITIONS[this.state]?.join(', ') || 'none'}`
      );
    }

    const previousState = this.state;
    this.state = targetState;
    
    const historyEntry = {
      state: targetState,
      previousState,
      timestamp: Date.now(),
      context
    };
    
    this.history.push(historyEntry);

    // 通知监听器
    await this._notifyListeners(targetState, previousState, context);

    return {
      previousState,
      newState: targetState,
      timestamp: historyEntry.timestamp
    };
  }

  /**
   * 注册状态变化监听器
   */
  onStateChange(listener) {
    this.listeners.push(listener);
  }

  /**
   * 通知监听器
   */
  async _notifyListeners(newState, previousState, context) {
    for (const listener of this.listeners) {
      try {
        await listener(newState, previousState, context);
      } catch (error) {
        console.error('State change listener error:', error.message);
      }
    }
  }

  /**
   * 获取状态历史
   */
  getHistory() {
    return this.history;
  }

  /**
   * 获取状态持续时间
   */
  getStateDuration(state) {
    const entries = this.history.filter(h => h.state === state);
    if (entries.length === 0) return 0;

    const firstEntry = entries[0];
    const nextEntry = this.history.find(h => 
      h.timestamp > firstEntry.timestamp && h.state !== state
    );

    if (nextEntry) {
      return nextEntry.timestamp - firstEntry.timestamp;
    }

    // 如果是当前状态，计算到现在的时间
    if (this.state === state) {
      return Date.now() - firstEntry.timestamp;
    }

    return 0;
  }

  /**
   * 序列化状态机
   */
  serialize() {
    return {
      state: this.state,
      history: this.history,
      metadata: this.metadata,
      serializedAt: Date.now()
    };
  }

  /**
   * 从序列化数据恢复
   */
  static deserialize(data) {
    const machine = new StateMachine(data.state, { metadata: data.metadata });
    machine.history = data.history || [];
    return machine;
  }

  /**
   * 判断是否为终态
   */
  isFinalState() {
    return [OrchestrationState.COMPLETED, OrchestrationState.FAILED, OrchestrationState.CANCELLED].includes(this.state);
  }

  /**
   * 判断是否可以重试
   */
  canRetry() {
    return this.state === OrchestrationState.FAILED;
  }
}

/**
 * 编排任务类
 */
class OrchestrationTask {
  constructor(taskId, definition) {
    this.taskId = taskId;
    this.definition = definition;
    this.stateMachine = new StateMachine(OrchestrationState.PENDING, {
      metadata: { taskId, definition }
    });
    this.createdAt = Date.now();
    this.updatedAt = Date.now();
  }

  async start() {
    await this.stateMachine.transition(OrchestrationState.RUNNING, { action: 'start' });
    this.updatedAt = Date.now();
  }

  async complete(result = {}) {
    await this.stateMachine.transition(OrchestrationState.COMPLETED, { action: 'complete', result });
    this.updatedAt = Date.now();
  }

  async fail(error) {
    await this.stateMachine.transition(OrchestrationState.FAILED, { action: 'fail', error: error.message });
    this.updatedAt = Date.now();
  }

  async pause() {
    await this.stateMachine.transition(OrchestrationState.PAUSED, { action: 'pause' });
    this.updatedAt = Date.now();
  }

  async resume() {
    await this.stateMachine.transition(OrchestrationState.RUNNING, { action: 'resume' });
    this.updatedAt = Date.now();
  }

  async cancel() {
    await this.stateMachine.transition(OrchestrationState.CANCELLED, { action: 'cancel' });
    this.updatedAt = Date.now();
  }

  getStatus() {
    return {
      taskId: this.taskId,
      state: this.stateMachine.getState(),
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
      history: this.stateMachine.getHistory(),
      isFinal: this.stateMachine.isFinalState(),
      canRetry: this.stateMachine.canRetry()
    };
  }
}

module.exports = {
  OrchestrationState,
  STATE_TRANSITIONS,
  StateMachine,
  OrchestrationTask
};
