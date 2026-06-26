/**
 * State Debouncing Machine (V2)
 * 
 * 状态缓冲状态机 - 解决状态抖动问题
 * 
 * 规则：
 * - 请求发起 0-10s: Running（正常执行）
 * - 10-30s: Waiting（等待中，不显示 blocked）
 * - >30s: Blocked（真正阻塞）
 * 
 * 阻塞时长累积计数，让用户看到"已卡住 45 秒"
 */

const { BLOCKER_LEVEL, BLOCKER_TYPE } = require('../src/schema');

// ==================== 状态阈值配置 ====================

const STATE_THRESHOLDS = {
  WAITING_THRESHOLD_MS: 10000,   // 10 秒后进入 waiting
  BLOCKED_THRESHOLD_MS: 30000,   // 30 秒后进入 blocked
  ESCALATION_INTERVAL_MS: 30000  // 每 30 秒升级一次阻塞级别
};

// ==================== 阻塞状态跟踪器 ====================

class BlockerTracker {
  constructor() {
    this.trackers = new Map();  // taskId -> tracker
  }

  /**
   * 开始跟踪任务的阻塞状态
   */
  startTracking(taskId, blockerType, reason, initialLevel = BLOCKER_LEVEL.LOW) {
    const now = Date.now();
    
    this.trackers.set(taskId, {
      blockerType: blockerType,
      reason: reason,
      initialLevel: initialLevel,
      currentLevel: initialLevel,
      startTime: now,
      lastEscalationTime: now,
      state: 'waiting',  // running -> waiting -> blocked
      durationMs: 0
    });
    
    return this.getTracker(taskId);
  }

  /**
   * 更新阻塞状态（计算持续时间）
   */
  update(taskId) {
    const tracker = this.trackers.get(taskId);
    if (!tracker) {
      return null;
    }
    
    const now = Date.now();
    tracker.durationMs = now - tracker.startTime;
    
    // 状态转换逻辑
    if (tracker.durationMs < STATE_THRESHOLDS.WAITING_THRESHOLD_MS) {
      tracker.state = 'running';
    } else if (tracker.durationMs < STATE_THRESHOLDS.BLOCKED_THRESHOLD_MS) {
      tracker.state = 'waiting';
    } else {
      tracker.state = 'blocked';
      
      // 阻塞级别升级（每 30 秒升级一次）
      if (now - tracker.lastEscalationTime >= STATE_THRESHOLDS.ESCALATION_INTERVAL_MS) {
        tracker.currentLevel = this.escalateLevel(tracker.currentLevel);
        tracker.lastEscalationTime = now;
      }
    }
    
    return this.getTracker(taskId);
  }

  /**
   * 升级阻塞级别
   */
  escalateLevel(currentLevel) {
    switch (currentLevel) {
      case BLOCKER_LEVEL.LOW:
        return BLOCKER_LEVEL.MEDIUM;
      case BLOCKER_LEVEL.MEDIUM:
        return BLOCKER_LEVEL.HIGH;
      default:
        return BLOCKER_LEVEL.HIGH;
    }
  }

  /**
   * 获取跟踪器快照
   */
  getTracker(taskId) {
    const tracker = this.trackers.get(taskId);
    if (!tracker) {
      return null;
    }
    
    return {
      blockerType: tracker.blockerType,
      reason: tracker.reason,
      level: tracker.currentLevel,
      state: tracker.state,
      durationMs: tracker.durationMs,
      durationSeconds: Math.floor(tracker.durationMs / 1000),
      durationText: this.formatDuration(tracker.durationMs)
    };
  }

  /**
   * 清除跟踪器
   */
  clear(taskId) {
    this.trackers.delete(taskId);
  }

  /**
   * 格式化持续时间
   */
  formatDuration(ms) {
    const seconds = Math.floor(ms / 1000);
    
    if (seconds < 60) {
      return `${seconds}秒`;
    } else if (seconds < 3600) {
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return secs > 0 ? `${mins}分${secs}秒` : `${mins}分钟`;
    } else {
      const hours = Math.floor(seconds / 3600);
      const mins = Math.floor((seconds % 3600) / 60);
      return mins > 0 ? `${hours}小时${mins}分` : `${hours}小时`;
    }
  }

  /**
   * 获取所有跟踪的任务
   */
  getAllTaskIds() {
    return Array.from(this.trackers.keys());
  }
}

// ==================== 状态机主类 ====================

class StateDebouncingMachine {
  constructor() {
    this.blockerTracker = new BlockerTracker();
    this.taskStates = new Map();  // taskId -> { lastEventTime, eventCount }
  }

  /**
   * 记录事件（用于防抖动）
   */
  recordEvent(taskId, eventType) {
    const now = Date.now();
    
    if (!this.taskStates.has(taskId)) {
      this.taskStates.set(taskId, {
        lastEventTime: now,
        eventCount: 0,
        consecutiveTimeouts: 0
      });
    }
    
    const state = this.taskStates.get(taskId);
    state.lastEventTime = now;
    state.eventCount++;
    
    // 统计连续超时
    if (eventType.includes('timeout') || eventType.includes('error')) {
      state.consecutiveTimeouts++;
    } else {
      state.consecutiveTimeouts = 0;
    }
    
    return state;
  }

  /**
   * 开始阻塞跟踪
   */
  startBlocker(taskId, blockerType, reason, level = BLOCKER_LEVEL.LOW) {
    this.recordEvent(taskId, 'blocker_start');
    return this.blockerTracker.startTracking(taskId, blockerType, reason, level);
  }

  /**
   * 更新阻塞状态
   */
  updateBlocker(taskId) {
    return this.blockerTracker.update(taskId);
  }

  /**
   * 获取阻塞状态（带防抖动）
   */
  getBlockerStatus(taskId) {
    const tracker = this.blockerTracker.update(taskId);
    if (!tracker) {
      return { hasBlocker: false };
    }
    
    return {
      hasBlocker: true,
      blockerType: tracker.blockerType,
      reason: tracker.reason,
      level: tracker.level,
      state: tracker.state,  // running | waiting | blocked
      durationMs: tracker.durationMs,
      durationSeconds: tracker.durationSeconds,
      durationText: tracker.durationText,
      shouldShowBlocked: tracker.state === 'blocked'
    };
  }

  /**
   * 清除阻塞
   */
  clearBlocker(taskId) {
    this.blockerTracker.clear(taskId);
    const state = this.taskStates.get(taskId);
    if (state) {
      state.consecutiveTimeouts = 0;
    }
  }

  /**
   * 获取任务健康度（0-100）
   */
  getHealthScore(taskId) {
    const state = this.taskStates.get(taskId);
    const blocker = this.blockerTracker.getTracker(taskId);
    
    let score = 100;
    
    // 阻塞扣分
    if (blocker) {
      const durationSeconds = blocker.durationSeconds;
      
      // 根据阻塞时长扣分
      if (durationSeconds > 60) {
        score -= 40;  // 超过 1 分钟扣 40 分
      } else if (durationSeconds > 30) {
        score -= 20;  // 超过 30 秒扣 20 分
      } else if (durationSeconds > 10) {
        score -= 10;  // 超过 10 秒扣 10 分
      }
      
      // 根据阻塞级别扣分
      if (blocker.level === BLOCKER_LEVEL.HIGH) {
        score -= 30;
      } else if (blocker.level === BLOCKER_LEVEL.MEDIUM) {
        score -= 15;
      }
    }
    
    // 连续超时扣分
    if (state && state.consecutiveTimeouts > 0) {
      score -= Math.min(state.consecutiveTimeouts * 10, 30);
    }
    
    // 长时间无事件扣分
    if (state && state.lastEventTime) {
      const idleMs = Date.now() - state.lastEventTime;
      if (idleMs > 60000) {  // 超过 1 分钟无事件
        score -= 20;
      } else if (idleMs > 30000) {  // 超过 30 秒无事件
        score -= 10;
      }
    }
    
    return Math.max(0, Math.min(100, score));
  }

  /**
   * 获取健康度文本描述
   */
  getHealthText(taskId) {
    const score = this.getHealthScore(taskId);
    
    if (score >= 80) {
      return { text: '健康', icon: '🟢', level: 'good' };
    } else if (score >= 60) {
      return { text: '轻微延迟', icon: '🟡', level: 'fair' };
    } else if (score >= 40) {
      return { text: '注意', icon: '🟠', level: 'warning' };
    } else {
      return { text: '严重阻塞', icon: '🔴', level: 'critical' };
    }
  }

  /**
   * 清除所有状态
   */
  clearAll() {
    this.taskStates.clear();
    this.blockerTracker = new BlockerTracker();
  }
}

// ==================== 导出 ====================

module.exports = {
  STATE_THRESHOLDS,
  BlockerTracker,
  StateDebouncingMachine
};
