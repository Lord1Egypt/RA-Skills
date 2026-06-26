/**
 * Snapshot History Manager
 * 
 * 保存任务过程中的关键 snapshot
 * 便于后续复盘和验证
 */

const fs = require('fs');
const path = require('path');

// ==================== 配置 ====================

const DEFAULT_ARTIFACTS_DIR = path.join(__dirname, '../../artifacts/phase2');

// ==================== Snapshot 历史管理器 ====================

class SnapshotHistoryManager {
  constructor(artifactsDir = null) {
    this.artifactsDir = artifactsDir || DEFAULT_ARTIFACTS_DIR;
    this.snapshots = new Map();  // taskId -> [snapshots]
    
    // 确保目录存在
    if (!fs.existsSync(this.artifactsDir)) {
      fs.mkdirSync(this.artifactsDir, { recursive: true });
    }
  }

  /**
   * 记录 snapshot
   */
  record(taskId, snapshotType, snapshot, metadata = {}) {
    if (!this.snapshots.has(taskId)) {
      this.snapshots.set(taskId, []);
    }
    
    const record = {
      type: snapshotType,
      timestamp: new Date().toISOString(),
      snapshot: snapshot,
      metadata: metadata
    };
    
    this.snapshots.get(taskId).push(record);
    
    // 自动保存到文件
    this.saveToFile(taskId, snapshotType, snapshot, metadata);
    
    return record;
  }

  /**
   * 保存到文件
   */
  saveToFile(taskId, snapshotType, snapshot, metadata = {}) {
    const taskDir = path.join(this.artifactsDir, taskId);
    
    if (!fs.existsSync(taskDir)) {
      fs.mkdirSync(taskDir, { recursive: true });
    }
    
    const filename = `snapshot_${snapshotType}.json`;
    const filepath = path.join(taskDir, filename);
    
    const content = {
      taskId: taskId,
      snapshotType: snapshotType,
      timestamp: new Date().toISOString(),
      metadata: metadata,
      snapshot: snapshot
    };
    
    fs.writeFileSync(filepath, JSON.stringify(content, null, 2), 'utf8');
  }

  /**
   * 获取任务的所有 snapshot
   */
  getTaskHistory(taskId) {
    return this.snapshots.get(taskId) || [];
  }

  /**
   * 获取特定类型的 snapshot
   */
  getSnapshot(taskId, snapshotType) {
    const history = this.getTaskHistory(taskId);
    return history.find(s => s.type === snapshotType);
  }

  /**
   * 获取最新 snapshot
   */
  getLatestSnapshot(taskId) {
    const history = this.getTaskHistory(taskId);
    return history.length > 0 ? history[history.length - 1] : null;
  }

  /**
   * 导出任务历史为文本报告
   */
  exportTaskReport(taskId, outputPath = null) {
    const history = this.getTaskHistory(taskId);
    
    if (history.length === 0) {
      return `任务 ${taskId} 无历史记录`;
    }
    
    const lines = [];
    lines.push(`# 任务历史报告：${taskId}`);
    lines.push('');
    lines.push(`生成时间：${new Date().toLocaleString('zh-CN')}`);
    lines.push(`Snapshot 数量：${history.length}`);
    lines.push('');
    lines.push('─────────────────────────────────────────────');
    lines.push('');
    
    for (const record of history) {
      lines.push(`## ${record.type}`);
      lines.push(`时间：${new Date(record.timestamp).toLocaleString('zh-CN')}`);
      
      if (record.metadata && Object.keys(record.metadata).length > 0) {
        lines.push(`元数据：${JSON.stringify(record.metadata)}`);
      }
      
      lines.push('');
      
      // 如果是文本 snapshot，直接输出
      if (typeof record.snapshot === 'string') {
        lines.push(record.snapshot);
      } else if (typeof record.snapshot === 'object') {
        // JSON snapshot，输出关键字段
        const s = record.snapshot;
        if (s.task_title) lines.push(`任务：${s.task_title}`);
        if (s.overall_status) lines.push(`状态：${s.overall_status}`);
        if (s.current_phase) lines.push(`阶段：${s.current_phase}`);
        if (s.progress_percent !== undefined) lines.push(`进度：${s.progress_percent}%`);
        if (s.current_action) lines.push(`当前：${s.current_action}`);
        if (s.why_not_done) lines.push(`原因：${s.why_not_done}`);
        if (s.needs_user_input) lines.push(`需要用户：${s.needs_user_input ? '是' : '否'}`);
      }
      
      lines.push('');
      lines.push('─────────────────────────────────────────────');
      lines.push('');
    }
    
    const report = lines.join('\n');
    
    if (outputPath) {
      fs.writeFileSync(outputPath, report, 'utf8');
    }
    
    return report;
  }

  /**
   * 清空历史
   */
  clear(taskId) {
    if (taskId) {
      this.snapshots.delete(taskId);
      
      // 删除文件
      const taskDir = path.join(this.artifactsDir, taskId);
      if (fs.existsSync(taskDir)) {
        fs.rmSync(taskDir, { recursive: true, force: true });
      }
    } else {
      this.snapshots.clear();
    }
  }

  /**
   * 获取所有任务 ID
   */
  getAllTaskIds() {
    return Array.from(this.snapshots.keys());
  }

  /**
   * 统计信息
   */
  getStats() {
    const taskIds = this.getAllTaskIds();
    let totalSnapshots = 0;
    
    for (const taskId of taskIds) {
      totalSnapshots += this.getTaskHistory(taskId).length;
    }
    
    return {
      totalTasks: taskIds.length,
      totalSnapshots: totalSnapshots,
      tasks: taskIds
    };
  }
}

// ==================== 与 Visibility Manager 集成 ====================

/**
 * 为 TaskVisibilityManager 添加 snapshot 历史记录
 */
function withSnapshotHistory(manager, artifactsDir = null) {
  const historyManager = new SnapshotHistoryManager(artifactsDir);
  
  // 保存原始方法
  const originalCreateTask = manager.createTask.bind(manager);
  const originalCompletePhase = manager.completePhase.bind(manager);
  const originalBlock = manager.block.bind(manager);
  const originalAsk = manager.ask.bind(manager);
  const originalRespond = manager.respond.bind(manager);
  
  // 包装方法以自动记录 snapshot
  manager.createTask = function(taskId, taskTitle, taskType) {
    const result = originalCreateTask(taskId, taskTitle, taskType);
    historyManager.record(taskId, 'init', manager.getStatusJSON(taskId, false), {
      taskTitle: taskTitle,
      taskType: taskType
    });
    return result;
  };
  
  manager.completePhase = function(taskId, phaseName, summary) {
    const result = originalCompletePhase(taskId, phaseName, summary);
    historyManager.record(taskId, `phase_${phaseName}`, manager.getStatusJSON(taskId, false), {
      phase: phaseName,
      summary: summary
    });
    return result;
  };
  
  manager.block = function(taskId, blockerType, reason, level) {
    const result = originalBlock(taskId, blockerType, reason, level);
    historyManager.record(taskId, 'blocked', manager.getStatusJSON(taskId, true), {
      blockerType: blockerType,
      reason: reason,
      level: level
    });
    return result;
  };
  
  manager.ask = function(taskId, inputType, question, options) {
    const result = originalAsk(taskId, inputType, question, options);
    historyManager.record(taskId, 'ask_human', manager.getStatusJSON(taskId, true), {
      inputType: inputType,
      question: question,
      options: options
    });
    return result;
  };
  
  manager.respond = function(taskId) {
    const result = originalRespond(taskId);
    historyManager.record(taskId, 'user_responded', manager.getStatusJSON(taskId, false));
    return result;
  };
  
  // 添加完成任务的 snapshot
  const originalEvent = manager.event.bind(manager);
  manager.event = function(taskId, eventType, eventData, level) {
    const result = originalEvent(taskId, eventType, eventData, level);
    
    if (eventType === 'task_completed' || eventType === 'task_failed') {
      historyManager.record(
        taskId, 
        eventType === 'task_completed' ? 'completed' : 'failed',
        manager.getStatusJSON(taskId, true),
        eventData
      );
    }
    
    return result;
  };
  
  // 暴露历史管理方法
  manager.getSnapshotHistory = historyManager.getTaskHistory.bind(historyManager);
  manager.getSnapshot = historyManager.getSnapshot.bind(historyManager);
  manager.getLatestSnapshot = historyManager.getLatestSnapshot.bind(historyManager);
  manager.exportTaskReport = historyManager.exportTaskReport.bind(historyManager);
  manager.getHistoryStats = () => historyManager.getStats();
  
  // 保存历史管理器引用
  manager._historyManager = historyManager;
  
  return manager;
}

// ==================== 便捷函数 ====================

/**
 * 创建带历史记录的 Visibility Manager
 */
function createManagerWithHistory(artifactsDir = null) {
  const { TaskVisibilityManager } = require('../index');
  const manager = new TaskVisibilityManager();
  return withSnapshotHistory(manager, artifactsDir);
}

// ==================== 导出 ====================

module.exports = {
  SnapshotHistoryManager,
  withSnapshotHistory,
  createManagerWithHistory,
  DEFAULT_ARTIFACTS_DIR
};
