/**
 * 对话状态管理器（内存版 - 安全）
 * 用于管理 agentlove 技能的对话状态，支持回退、保存、加载等功能
 * 
 * 安全特性：
 * - 所有数据存储在内存中，会话结束即清除
 * - 不写入任何文件
 * - 不收集敏感凭证
 */

class StateManager {
  /**
   * 构造函数
   */
  constructor() {
    this.states = new Map(); // 内存存储
  }
  
  /**
   * 生成唯一的 session ID
   * @returns {string} - session ID
   */
  generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substring(2, 15)}`;
  }
  
  /**
   * 创建新的状态
   * @param {string} userId - 用户 ID
   * @returns {object} - 初始状态对象
   */
  createState(userId) {
    return {
      session_id: this.generateSessionId(),
      user_id: userId,
      current_step: 0,  // 从第 0 步（功能介绍）开始
      step_data: {},
      created_at: Date.now(),
      updated_at: Date.now()
    };
  }
  
  /**
   * 保存状态（内存）
   * @param {string} userId - 用户 ID
   * @param {object} state - 状态对象
   */
  saveState(userId, state) {
    this.states.set(userId, state);
  }
  
  /**
   * 加载状态（内存）
   * @param {string} userId - 用户 ID
   * @returns {object|null} - 状态对象，不存在则返回 null
   */
  loadState(userId) {
    return this.states.get(userId) || null;
  }
  
  /**
   * 初始化或获取状态
   * @param {string} userId - 用户 ID
   * @returns {object} - 状态对象
   */
  getOrCreateState(userId) {
    let state = this.loadState(userId);
    if (!state) {
      state = this.createState(userId);
      this.saveState(userId, state);
    }
    return state;
  }
  
  /**
   * 更新当前步骤
   * @param {string} userId - 用户 ID
   * @param {number} step - 步骤编号
   * @returns {object} - 更新后的状态
   */
  updateStep(userId, step) {
    const state = this.getOrCreateState(userId);
    state.current_step = step;
    state.updated_at = Date.now();
    this.saveState(userId, state);
    return state;
  }
  
  /**
   * 回退到上一步
   * @param {string} userId - 用户 ID
   * @returns {object} - {success, step, message}
   */
  goBack(userId) {
    const state = this.getOrCreateState(userId);
    if (state.current_step > 0) {
      state.current_step--;
      state.updated_at = Date.now();
      this.saveState(userId, state);
      return { 
        success: true, 
        step: state.current_step, 
        message: `已回退到第 ${state.current_step} 步` 
      };
    }
    return { 
      success: false, 
      step: 0, 
      message: '已经是第一步了，无法回退' 
    };
  }
  
  /**
   * 前进到下一步
   * @param {string} userId - 用户 ID
   * @returns {object} - {success, step, message}
   */
  goNext(userId) {
    const state = this.getOrCreateState(userId);
    // 最多到第 10 步（完成配置）
    if (state.current_step < 10) {
      state.current_step++;
      state.updated_at = Date.now();
      this.saveState(userId, state);
      return { 
        success: true, 
        step: state.current_step, 
        message: `已进入第 ${state.current_step} 步` 
      };
    }
    return { 
      success: false, 
      step: 10, 
      message: '已是最后一步' 
    };
  }
  
  /**
   * 保存步骤数据
   * @param {string} userId - 用户 ID
   * @param {number|string} step - 步骤编号
   * @param {object} data - 步骤数据
   */
  saveStepData(userId, step, data) {
    const state = this.getOrCreateState(userId);
    const stepKey = typeof step === 'number' ? `step_${step}` : step;
    state.step_data[stepKey] = {
      ...data,
      saved_at: Date.now()
    };
    state.updated_at = Date.now();
    this.saveState(userId, state);
  }
  
  /**
   * 获取步骤数据
   * @param {string} userId - 用户 ID
   * @param {number|string} step - 步骤编号
   * @returns {object|null} - 步骤数据
   */
  getStepData(userId, step) {
    const state = this.loadState(userId);
    if (state && state.step_data) {
      const stepKey = typeof step === 'number' ? `step_${step}` : step;
      return state.step_data[stepKey] || null;
    }
    return null;
  }
  
  /**
   * 获取所有会话（用于测试和管理）
   * @returns {Array} - 会话列表
   */
  getAllSessions() {
    return Array.from(this.states.entries()).map(([userId, state]) => ({
      user_id: userId,
      session_id: state.session_id,
      current_step: state.current_step,
      created_at: state.created_at,
      updated_at: state.updated_at
    }));
  }
  
  /**
   * 清除状态（会话结束）
   * @param {string} userId - 用户 ID
   * @returns {boolean} - 清除结果
   */
  clearState(userId) {
    return this.states.delete(userId);
  }
  
  /**
   * 获取状态摘要（用于日志）
   * @param {string} userId - 用户 ID
   * @returns {string} - 状态摘要
   */
  getStateSummary(userId) {
    const state = this.loadState(userId);
    if (state) {
      return `用户${userId} - 步骤${state.current_step}/10 - 会话${state.session_id}`;
    }
    return `用户${userId} - 无状态`;
  }
}

module.exports = StateManager;
