/**
 * Agent Work Visibility - Main Entry
 * 
 * 统一 API 入口
 */

const { 
  createTaskState, 
  OVERALL_STATUS, 
  PHASE_STATUS, 
  BLOCKER_LEVEL, 
  BLOCKER_TYPE,
  USER_INPUT_TYPE 
} = require('./schema');

const {
  initResearchPhases,
  startPhase,
  updatePhaseProgress,
  completePhase,
  blockPhase,
  skipPhase,
  getCurrentPhase,
  getPhaseSummary
} = require('./phases');

const {
  addLogEntry,
  recordEvent,
  recordRetry,
  getRecentLogs,
  getCurrentAction,
  clearLogs
} = require('./logger');

const {
  reportBlocker,
  clearBlocker,
  hasActiveBlocker,
  getBlockerDuration,
  getBlockerSummary
} = require('./blocker');

const {
  requestUserInput,
  requestDirectionChoice,
  requestJudgementCall,
  requestScopeConfirmation,
  requestContinueOrStop,
  clearUserInputRequest,
  needsUserInput,
  getUserInputSummary
} = require('./ask-human');

const {
  calculateProgress,
  updateTaskProgress,
  getProgressExplanation,
  isProgressStalled,
  getPhaseProgressDetails,
  formatProgressDisplay,
  estimateRemainingTime
} = require('./progress');

const {
  renderDefaultView,
  renderFullView,
  renderJSON
} = require('./renderer');

// ==================== 任务管理器类 ====================

class TaskVisibilityManager {
  constructor() {
    this.tasks = new Map();
  }
  
  /**
   * 创建新任务
   */
  createTask(taskId, taskTitle, taskType = 'research') {
    const state = createTaskState(taskId, taskTitle, taskType);
    
    // 初始化阶段（Research 固定 5 阶段）
    if (taskType === 'research') {
      state.phases = initResearchPhases();
    }
    
    this.tasks.set(taskId, state);
    
    // 记录启动日志
    recordEvent(state, 'task_started', { title: taskTitle });
    
    return state;
  }
  
  /**
   * 获取任务状态
   */
  getTask(taskId) {
    return this.tasks.get(taskId) || null;
  }
  
  /**
   * 删除任务
   */
  deleteTask(taskId) {
    return this.tasks.delete(taskId);
  }
  
  /**
   * 开始阶段
   */
  startPhase(taskId, phaseName, summary = null) {
    const task = this.tasks.get(taskId);
    if (!task) throw new Error(`任务不存在：${taskId}`);
    
    const phase = startPhase(task, phaseName);
    updateTaskProgress(task);
    
    // 记录日志
    addLogEntry(task, `开始阶段：${phaseName}`);
    if (summary) {
      addLogEntry(task, summary);
    }
    
    // 更新整体状态
    task.overall_status = OVERALL_STATUS.RUNNING;
    
    return phase;
  }
  
  /**
   * 更新阶段进度
   */
  updatePhaseProgress(taskId, phaseName, progress, currentAction = null) {
    const task = this.tasks.get(taskId);
    if (!task) throw new Error(`任务不存在：${taskId}`);
    
    updatePhaseProgress(task, phaseName, progress);
    updateTaskProgress(task);
    
    // 可选：更新当前动作
    if (currentAction) {
      task.current_action = currentAction;
    }
    
    return task;
  }
  
  /**
   * 完成阶段
   */
  completePhase(taskId, phaseName, summary = null) {
    const task = this.tasks.get(taskId);
    if (!task) throw new Error(`任务不存在：${taskId}`);
    
    const result = completePhase(task, phaseName, summary);
    updateTaskProgress(task);
    
    // 记录日志
    addLogEntry(task, `完成阶段：${phaseName}`);
    
    // 如果有下一阶段，自动开始
    if (result.next) {
      addLogEntry(task, `进入下一阶段：${result.next.phase_name}`);
    } else {
      // 所有阶段完成
      task.overall_status = OVERALL_STATUS.COMPLETED;
      task.completed_at = new Date().toISOString();
      recordEvent(task, 'task_completed');
    }
    
    return result;
  }
  
  /**
   * 记录动作
   */
  log(taskId, message, level = 'info') {
    const task = this.tasks.get(taskId);
    if (!task) throw new Error(`任务不存在：${taskId}`);
    
    return addLogEntry(task, message, level);
  }
  
  /**
   * 记录系统事件（自动翻译）
   */
  event(taskId, eventType, eventData = {}, level = 'info') {
    const task = this.tasks.get(taskId);
    if (!task) throw new Error(`任务不存在：${taskId}`);
    
    return recordEvent(task, eventType, eventData, level);
  }
  
  /**
   * 报告阻塞
   */
  block(taskId, blockerType, reason = null, level = null) {
    const task = this.tasks.get(taskId);
    if (!task) throw new Error(`任务不存在：${taskId}`);
    
    const result = reportBlocker(task, blockerType, reason, level);
    
    // 记录日志
    addLogEntry(task, `遇到阻塞：${reason || blockerType}`, 'warning');
    
    return result;
  }
  
  /**
   * 清除阻塞
   */
  unblock(taskId) {
    const task = this.tasks.get(taskId);
    if (!task) throw new Error(`任务不存在：${taskId}`);
    
    clearBlocker(task);
    addLogEntry(task, '阻塞已解除');
    
    return task;
  }
  
  /**
   * 请求用户介入
   */
  ask(taskId, inputType, question = null, options = null) {
    const task = this.tasks.get(taskId);
    if (!task) throw new Error(`任务不存在：${taskId}`);
    
    return requestUserInput(task, inputType, question, options);
  }
  
  /**
   * 用户已响应，清除介入请求
   */
  respond(taskId) {
    const task = this.tasks.get(taskId);
    if (!task) throw new Error(`任务不存在：${taskId}`);
    
    clearUserInputRequest(task);
    addLogEntry(task, '用户已响应，继续执行');
    
    return task;
  }
  
  /**
   * 设置下一步动作
   */
  setNextAction(taskId, action) {
    const task = this.tasks.get(taskId);
    if (!task) throw new Error(`任务不存在：${taskId}`);
    
    task.next_action = action;
    task.updated_at = new Date().toISOString();
    
    return task;
  }
  
  /**
   * 获取默认视图（文本）
   */
  getDefaultView(taskId) {
    const task = this.tasks.get(taskId);
    if (!task) throw new Error(`任务不存在：${taskId}`);
    
    return renderDefaultView(task);
  }
  
  /**
   * 获取完整视图（文本）
   */
  getFullView(taskId) {
    const task = this.tasks.get(taskId);
    if (!task) throw new Error(`任务不存在：${taskId}`);
    
    return renderFullView(task);
  }
  
  /**
   * 获取状态 JSON
   */
  getStatusJSON(taskId, full = false) {
    const task = this.tasks.get(taskId);
    if (!task) throw new Error(`任务不存在：${taskId}`);
    
    return renderJSON(task, full);
  }
  
  /**
   * 检查任务是否健康（无长时间停滞）
   */
  isHealthy(taskId, thresholdMinutes = 5) {
    const task = this.tasks.get(taskId);
    if (!task) return false;
    
    return !isProgressStalled(task, thresholdMinutes);
  }
}

// ==================== 便捷函数 ====================

/**
 * 快速创建 Research 任务
 */
function createResearchTask(taskId, taskTitle) {
  const manager = new TaskVisibilityManager();
  const task = manager.createTask(taskId, taskTitle, 'research');
  
  // 自动开始第一阶段
  manager.startPhase(taskId, '理解任务');
  
  return { manager, task };
}

// ==================== 导出 ====================

module.exports = {
  // 类
  TaskVisibilityManager,
  
  // 便捷函数
  createResearchTask,
  
  // Schema 导出
  OVERALL_STATUS,
  PHASE_STATUS,
  BLOCKER_LEVEL,
  BLOCKER_TYPE,
  USER_INPUT_TYPE,
  createTaskState,
  
  // 模块导出
  phases: {
    initResearchPhases,
    startPhase,
    updatePhaseProgress,
    completePhase,
    blockPhase,
    skipPhase,
    getCurrentPhase,
    getPhaseSummary
  },
  logger: {
    addLogEntry,
    recordEvent,
    recordRetry,
    getRecentLogs,
    getCurrentAction
  },
  blocker: {
    reportBlocker,
    clearBlocker,
    hasActiveBlocker,
    getBlockerDuration,
    getBlockerSummary
  },
  askHuman: {
    requestUserInput,
    requestDirectionChoice,
    requestJudgementCall,
    requestScopeConfirmation,
    requestContinueOrStop,
    clearUserInputRequest,
    needsUserInput,
    getUserInputSummary
  },
  progress: {
    calculateProgress,
    updateTaskProgress,
    getProgressExplanation,
    isProgressStalled,
    getPhaseProgressDetails,
    formatProgressDisplay,
    estimateRemainingTime
  },
  renderer: {
    renderDefaultView,
    renderFullView,
    renderJSON
  }
};
