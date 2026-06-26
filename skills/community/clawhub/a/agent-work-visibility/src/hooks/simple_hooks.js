/**
 * Simple Hooks for Agent Work Visibility
 * 
 * 轻量级通知钩子（非完整通知系统）
 * 支持内部事件触发回调
 */

// ==================== 钩子类型 ====================

const HOOK_TYPES = {
  ON_BLOCKED: 'on_blocked',
  ON_BLOCKER_CLEARED: 'on_blocker_cleared',
  ON_USER_INPUT_REQUIRED: 'on_user_input_required',
  ON_USER_INPUT_RESOLVED: 'on_user_input_resolved',
  ON_TASK_COMPLETED: 'on_task_completed',
  ON_TASK_FAILED: 'on_task_failed',
  ON_PHASE_CHANGED: 'on_phase_changed',
  ON_PROGRESS_UPDATED: 'on_progress_updated'
};

// ==================== 钩子管理器 ====================

class HookManager {
  constructor() {
    this.hooks = new Map();
  }

  /**
   * 注册钩子
   */
  on(hookType, callback) {
    if (!this.hooks.has(hookType)) {
      this.hooks.set(hookType, []);
    }
    this.hooks.get(hookType).push(callback);
    return this;
  }

  /**
   * 触发钩子
   */
  trigger(hookType, data = {}) {
    const callbacks = this.hooks.get(hookType) || [];
    
    for (const callback of callbacks) {
      try {
        callback(data);
      } catch (error) {
        console.error(`Hook ${hookType} 执行失败:`, error);
      }
    }
  }

  /**
   * 移除钩子
   */
  off(hookType, callback) {
    if (!this.hooks.has(hookType)) {
      return;
    }
    
    if (callback) {
      const callbacks = this.hooks.get(hookType);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    } else {
      this.hooks.delete(hookType);
    }
  }

  /**
   * 清空所有钩子
   */
  clear() {
    this.hooks.clear();
  }
}

// ==================== 集成到 Visibility Manager ====================

/**
 * 为 TaskVisibilityManager 添加钩子支持
 */
function withHooks(manager) {
  const hookManager = new HookManager();
  
  // 保存原始方法
  const originalBlock = manager.block.bind(manager);
  const originalUnblock = manager.unblock.bind(manager);
  const originalAsk = manager.ask.bind(manager);
  const originalRespond = manager.respond.bind(manager);
  const originalCompletePhase = manager.completePhase.bind(manager);
  const originalUpdatePhaseProgress = manager.updatePhaseProgress.bind(manager);
  
  // 包装方法以触发钩子
  manager.block = function(taskId, blockerType, reason, level) {
    const result = originalBlock(taskId, blockerType, reason, level);
    hookManager.trigger(HOOK_TYPES.ON_BLOCKED, { taskId, blockerType, reason, level });
    return result;
  };
  
  manager.unblock = function(taskId) {
    const result = originalUnblock(taskId);
    hookManager.trigger(HOOK_TYPES.ON_BLOCKER_CLEARED, { taskId });
    return result;
  };
  
  manager.ask = function(taskId, inputType, question, options) {
    const result = originalAsk(taskId, inputType, question, options);
    hookManager.trigger(HOOK_TYPES.ON_USER_INPUT_REQUIRED, { taskId, inputType, question, options });
    return result;
  };
  
  manager.respond = function(taskId) {
    const result = originalRespond(taskId);
    hookManager.trigger(HOOK_TYPES.ON_USER_INPUT_RESOLVED, { taskId });
    return result;
  };
  
  manager.completePhase = function(taskId, phaseName, summary) {
    const result = originalCompletePhase(taskId, phaseName, summary);
    hookManager.trigger(HOOK_TYPES.ON_PHASE_CHANGED, { taskId, phase: phaseName, status: 'completed' });
    return result;
  };
  
  manager.updatePhaseProgress = function(taskId, phaseName, progress, currentAction) {
    const result = originalUpdatePhaseProgress(taskId, phaseName, progress, currentAction);
    hookManager.trigger(HOOK_TYPES.ON_PROGRESS_UPDATED, { taskId, phase: phaseName, progress });
    return result;
  };
  
  // 添加钩子注册方法
  manager.on = hookManager.on.bind(hookManager);
  manager.off = hookManager.off.bind(hookManager);
  manager.trigger = hookManager.trigger.bind(hookManager);
  
  return manager;
}

// ==================== 预设钩子处理器 ====================

/**
 * 日志钩子处理器（记录到控制台）
 */
function createLoggingHook(prefix = '[Visibility]') {
  return {
    on_blocked: (data) => {
      console.log(`${prefix} 🔴 阻塞：${data.taskId} - ${data.reason} (${data.level})`);
    },
    on_blocker_cleared: (data) => {
      console.log(`${prefix} 🟢 阻塞解除：${data.taskId}`);
    },
    on_user_input_required: (data) => {
      console.log(`${prefix} 🙋 需要用户介入：${data.taskId}`);
      console.log(`   问题：${data.question}`);
      if (data.options?.length > 0) {
        console.log(`   选项：${data.options.join(', ')}`);
      }
    },
    on_user_input_resolved: (data) => {
      console.log(`${prefix} ✅ 用户已响应：${data.taskId}`);
    },
    on_task_completed: (data) => {
      console.log(`${prefix} 🎉 任务完成：${data.taskId}`);
    },
    on_task_failed: (data) => {
      console.log(`${prefix} ❌ 任务失败：${data.taskId} - ${data.reason}`);
    },
    on_phase_changed: (data) => {
      console.log(`${prefix} 📍 阶段变更：${data.taskId} - ${data.phase} (${data.status})`);
    },
    on_progress_updated: (data) => {
      console.log(`${prefix} 📊 进度更新：${data.taskId} - ${data.phase} ${data.progress}%`);
    }
  };
}

/**
 * 注册预设钩子到 manager
 */
function registerLoggingHooks(manager, prefix) {
  const hooks = createLoggingHook(prefix);
  
  for (const [event, handler] of Object.entries(hooks)) {
    manager.on(event, handler);
  }
  
  return manager;
}

// ==================== 导出 ====================

module.exports = {
  HOOK_TYPES,
  HookManager,
  withHooks,
  createLoggingHook,
  registerLoggingHooks
};
