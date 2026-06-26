/**
 * TopicScope — 话题作用域隔离
 *
 * 解决的问题：话题A的上下文 不应该 渗透到话题B
 *
 * 设计原则（来自用户反馈）：
 * - 记忆的连续性 = 基本认知的联系，不是所有内容的联系
 * - 两个完全无关的话题，不需要任何联想
 * - 新话题来 → 干净的处理空间，不需要携带旧话题的上下文
 *
 * API:
 *   TopicScope.push('话题名')   → 进入话题，上下文隔离
 *   TopicScope.pop()            → 退出话题，恢复之前上下文
 *   TopicScope.store('key', val) → 只存在当前话题的存储里
 *   TopicScope.get('key')       → 只从当前话题读取
 *   TopicScope.clear()          → 清空当前话题所有存储（但不删除话题历史）
 *   TopicScope.current          → 当前话题名
 */

class TopicScope {
  constructor(options = {}) {
    // { topicName: { store: {}, timestamp } }
    this._topics = new Map();
    this._stack = [];           // 话题栈，记录进入顺序
    this._current = null;        // 当前话题名
    this._context = {};          // 当前话题的"工作上下文"（模拟AI当前在处理什么）
    // 桥接到 MeaningfulMemory — push 时自动更新记忆的 topic 标签
    this._memoryBridge = options.memoryBridge || null;
  }

  /**
   * 注入 MeaningfulMemory 实例，建立桥接
   * @param {object} memory - MeaningfulMemory 实例
   */
  setMemoryBridge(memory) {
    this._memoryBridge = memory;
    return this;
  }

  /**
   * 进入话题（push）
   * @param {string} topic - 话题名
   * @param {object} initialContext - 进入话题时的初始上下文（可选）
   */
  push(topic, initialContext = {}) {
    // 保存当前话题的上下文（如果存在）
    if (this._current !== null) {
      const currentData = this._topics.get(this._current);
      if (currentData) {
        currentData.context = { ...this._context };
        currentData.store = { ...currentData.store };
      }
    }

    // 进入新话题
    if (!this._topics.has(topic)) {
      // 新话题：干净存储
      this._topics.set(topic, {
        store: {},
        context: {},
        createdAt: Date.now()
      });
    } else {
      // 已有话题：恢复之前保存的上下文
      const saved = this._topics.get(topic);
      this._context = { ...saved.context };
    }

    // 初始化上下文（如果有初始内容）
    if (Object.keys(initialContext).length > 0) {
      this._context = { ...this._context, ...initialContext };
    }

    this._current = topic;
    if (!this._stack.includes(topic)) {
      this._stack.push(topic);
    }

    // 桥接到 MeaningfulMemory — 每次 push 自动同步当前 topic
    if (this._memoryBridge) {
      this._memoryBridge.setCurrentTopic(topic);
    }

    return this;
  }

  /**
   * 退出话题（pop）
   * 保存当前话题状态，然后恢复上一个
   */
  pop() {
    if (this._stack.length <= 1) {
      // 已经是最顶层，不能pop
      return this;
    }

    // 保存当前话题
    if (this._current !== null) {
      const currentData = this._topics.get(this._current);
      if (currentData) {
        currentData.context = { ...this._context };
      }
    }

    // 弹出当前，恢复上一个
    this._stack.pop();
    this._current = this._stack[this._stack.length - 1] || null;

    if (this._current !== null) {
      const saved = this._topics.get(this._current);
      if (saved) {
        this._context = { ...saved.context };
      }
    } else {
      this._context = {};
    }

    return this;
  }

  /**
   * 在当前话题里存储数据
   */
  store(key, value) {
    if (this._current === null) return this;
    const topicData = this._topics.get(this._current);
    if (topicData) {
      topicData.store[key] = value;
    }
    return this;
  }

  /**
   * 从当前话题读取数据
   */
  get(key) {
    if (this._current === null) return undefined;
    const topicData = this._topics.get(this._current);
    return topicData ? topicData.store[key] : undefined;
  }

  /**
   * 把数据存入当前话题的工作上下文
   * context 和 store 的区别：
   * - store: 话题的"知识库"（问答记录等）
   * - context: 话题的"当前处理状态"（AI正在处理的内容）
   */
  setContext(key, value) {
    this._context[key] = value;
    return this;
  }

  getContext(key) {
    return this._context[key];
  }

  /**
   * 清空当前话题的工作上下文（但保留store）
   * 用于"新问题进入同一话题"时重置
   */
  clearContext() {
    this._context = {};
    return this;
  }

  /**
   * 清空当前话题所有存储（完全重置）
   */
  clearAll() {
    if (this._current === null) return this;
    this._topics.set(this._current, {
      store: {},
      context: {},
      createdAt: Date.now()
    });
    this._context = {};
    return this;
  }

  get current() { return this._current; }
  get stack() { return [...this._stack]; }

  /**
   * 获取所有话题概览（不含详细内容）
   */
  getTopics() {
    return Array.from(this._topics.entries()).map(([name, data]) => ({
      name,
      storeKeys: Object.keys(data.store),
      hasContext: Object.keys(data.context).length > 0
    }));
  }

  /**
   * 诊断：打印当前状态
   */
  diagnose(label = '') {
    console.log(`\n=== TopicScope 诊断${label ? ' — ' + label : ''} ===`);
    console.log(`当前话题: ${this._current}`);
    console.log(`话题栈: [${this._stack.join(' → ')}]`);
    console.log(`当前上下文:`, JSON.stringify(this._context));
    for (const [name, data] of this._topics) {
      console.log(`话题[${name}] store:`, Object.keys(data.store));
    }
    return this;
  }
}

module.exports = { TopicScope };
