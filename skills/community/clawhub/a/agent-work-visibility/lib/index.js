/**
 * Agent Work Visibility v2.0
 * 
 * Unified entry point for V2 features:
 * - State Debouncing Machine
 * - Smart Action Logger
 * - Enhanced Ask-Human Protocol
 * - Health Indicators
 */

// V1 Core (backward compatible)
const { 
  TaskVisibilityManager,
  OVERALL_STATUS,
  PHASE_STATUS,
  BLOCKER_LEVEL,
  BLOCKER_TYPE,
  USER_INPUT_TYPE,
  createTaskState
} = require('../src/index');

// V2 Core
const { 
  StateDebouncingMachine,
  BlockerTracker,
  STATE_THRESHOLDS
} = require('./state_machine');

const {
  SmartActionLogger,
  ActionTextGenerator,
  NEXT_STEP_TEMPLATES,
  predictNextStep,
  isTooVague,
  isTooTechnical,
  translateTechnicalToHuman
} = require('./smart_logger');

// ==================== V2 Enhanced Manager ====================

class VisibilityManagerV2 extends TaskVisibilityManager {
  constructor(options = {}) {
    super();
    
    // V2 components
    this.stateMachine = new StateDebouncingMachine();
    this.smartLogger = new SmartActionLogger();
    this.textGenerator = new ActionTextGenerator(this.smartLogger);
    
    // Options
    this.options = {
      enableDebouncing: options.enableDebouncing !== false,
      enableSmartLogging: options.enableSmartLogging !== false,
      enableHealthScore: options.enableHealthScore !== false,
      ...options
    };
  }

  /**
   * 创建任务（V2 增强）
   */
  createTask(taskId, taskTitle, taskType = 'research') {
    const task = super.createTask(taskId, taskTitle, taskType);
    
    // V2: 初始化状态机跟踪
    if (this.options.enableDebouncing) {
      this.stateMachine.recordEvent(taskId, 'task_created');
    }
    
    // V2: 记录初始动作
    if (this.options.enableSmartLogging) {
      this.smartLogger.add(taskId, `任务已创建：${taskTitle}`, 'info');
    }
    
    return task;
  }

  /**
   * 报告阻塞（V2 带状态缓冲）
   */
  block(taskId, blockerType, reason, level = 'low') {
    // V2: 使用状态机跟踪阻塞
    if (this.options.enableDebouncing) {
      const tracker = this.stateMachine.startBlocker(taskId, blockerType, reason, level);
      
      // 根据状态机决定实际阻塞级别
      const status = this.stateMachine.getBlockerStatus(taskId);
      if (!status.shouldShowBlocked) {
        // 在 waiting 状态，记录但不显示 blocked
        this.smartLogger.add(taskId, `等待响应中（${status.durationText}）`, 'warning');
        return { ...tracker, state: 'waiting' };
      }
      
      // 真正 blocked
      level = status.level;
    }
    
    // V1 兼容
    const result = super.block(taskId, blockerType, reason, level);
    
    // V2: 记录阻塞日志
    if (this.options.enableSmartLogging) {
      this.smartLogger.add(taskId, `遇到阻塞：${reason}`, 'warning');
    }
    
    return result;
  }

  /**
   * 清除阻塞（V2）
   */
  unblock(taskId) {
    // V2: 清除状态机跟踪
    if (this.options.enableDebouncing) {
      this.stateMachine.clearBlocker(taskId);
    }
    
    return super.unblock(taskId);
  }

  /**
   * 记录动作（V2 智能日志）
   */
  log(taskId, message, level = 'info') {
    // V2: 检查文案质量
    if (this.options.enableSmartLogging) {
      if (isTooVague(message)) {
        console.warn(`⚠️  文案可能太空洞："${message}"`);
      }
      if (isTooTechnical(message)) {
        const translated = translateTechnicalToHuman(message);
        console.warn(`⚠️  文案可能太技术，建议："${translated}"`);
      }
      
      this.smartLogger.add(taskId, message, level);
    }
    
    return super.log(taskId, message, level);
  }

  /**
   * 获取默认视图（V2 增强）
   */
  getDefaultView(taskId) {
    const task = this.getTask(taskId);
    if (!task) {
      throw new Error(`任务不存在：${taskId}`);
    }
    
    // V2: 计算健康度
    if (this.options.enableHealthScore) {
      task.health_score = this.stateMachine.getHealthScore(taskId);
    }
    
    // V2: 使用智能文案生成器
    if (this.options.enableSmartLogging) {
      task.current_action = this.textGenerator.getCurrentAction(
        taskId, 
        task.current_phase, 
        task.progress_percent
      );
      
      // V2: 预测下一步
      if (!task.next_action) {
        task.next_action = predictNextStep(task.current_phase, task.progress_percent);
      }
    }
    
    // 更新任务状态
    this.tasks.set(taskId, task);
    
    return require('../src/renderer').renderDefaultView(task);
  }

  /**
   * 获取健康度（V2 新增）
   */
  getHealth(taskId) {
    if (!this.options.enableHealthScore) {
      return null;
    }
    
    const score = this.stateMachine.getHealthScore(taskId);
    const healthText = this.stateMachine.getHealthText(taskId);
    
    return {
      score: score,
      text: healthText.text,
      icon: healthText.icon,
      level: healthText.level
    };
  }

  /**
   * 获取阻塞详情（V2 带持续时间）
   */
  getBlockerDetails(taskId) {
    if (!this.options.enableDebouncing) {
      return null;
    }
    
    return this.stateMachine.getBlockerStatus(taskId);
  }

  /**
   * 获取最近动作（V2 智能日志）
   */
  getRecentActions(taskId, limit = 5) {
    if (!this.options.enableSmartLogging) {
      return this.getTask(taskId)?.action_log?.slice(0, limit) || [];
    }
    
    return this.smartLogger.getRecentActions(taskId, limit);
  }
}

// ==================== 工厂函数 ====================

/**
 * 创建 Visibility Manager（V2）
 */
function createVisibilityManager(options = {}) {
  return new VisibilityManagerV2(options);
}

/**
 * 快速创建 Research 任务（V2）
 */
function createResearchTask(taskId, taskTitle, options = {}) {
  const manager = createVisibilityManager(options);
  const task = manager.createTask(taskId, taskTitle, 'research');
  
  // 自动开始第一阶段
  manager.startPhase(taskId, '理解任务');
  
  return { manager, task };
}

// ==================== 导出 ====================

module.exports = {
  // V2 Manager
  VisibilityManagerV2,
  createVisibilityManager,
  createResearchTask,
  
  // V1 兼容导出
  TaskVisibilityManager,
  OVERALL_STATUS,
  PHASE_STATUS,
  BLOCKER_LEVEL,
  BLOCKER_TYPE,
  USER_INPUT_TYPE,
  createTaskState,
  
  // V2 组件
  StateDebouncingMachine,
  BlockerTracker,
  STATE_THRESHOLDS,
  SmartActionLogger,
  ActionTextGenerator,
  NEXT_STEP_TEMPLATES,
  
  // V2 工具函数
  predictNextStep,
  isTooVague,
  isTooTechnical,
  translateTechnicalToHuman,
  
  // 向后兼容
  ...require('../src/index')
};
