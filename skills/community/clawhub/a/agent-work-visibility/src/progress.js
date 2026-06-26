/**
 * Agent Work Visibility - Progress Calculation
 * 
 * 进度计算模块
 * 核心原则：百分比只是辅助，文字解释优先
 */

const { PHASE_STATUS } = require('./schema');

// ==================== 进度计算 ====================

/**
 * 计算总体进度（加权完成度）
 * 
 * 公式：progress = Σ(phase_weight × phase_completion / 100)
 * 
 * Research 阶段权重：
 * - 理解任务：10%
 * - 制定搜索计划：15%
 * - 收集信息：30%
 * - 分析与比较：30%
 * - 形成输出：15%
 */
function calculateProgress(taskState) {
  if (!taskState.phases || taskState.phases.length === 0) {
    return 0;
  }
  
  let totalProgress = 0;
  let totalWeight = 0;
  
  for (const phase of taskState.phases) {
    const weight = phase.phase_weight || 0;
    const completion = getPhaseCompletion(phase);
    
    totalProgress += weight * completion;
    totalWeight += weight;
  }
  
  // 归一化到 0-100
  if (totalWeight === 0) {
    return 0;
  }
  
  // totalProgress / totalWeight 得到 0-1 的值，需要乘以 100
  return Math.round((totalProgress / totalWeight) * 100);
}

/**
 * 获取单个阶段的完成度（0-1）
 */
function getPhaseCompletion(phase) {
  switch (phase.phase_status) {
    case PHASE_STATUS.COMPLETED:
      return 1.0;
    case PHASE_STATUS.SKIPPED:
      return 1.0;  // 跳过也算完成
    case PHASE_STATUS.IN_PROGRESS:
      // 进行中的阶段，使用 phase_progress（0-100）
      return (phase.phase_progress || 0) / 100;
    case PHASE_STATUS.BLOCKED:
      // 被阻塞的阶段，按当前进度计算
      return (phase.phase_progress || 0) / 100;
    case PHASE_STATUS.PENDING:
    default:
      return 0;
  }
}

/**
 * 更新任务总体进度
 */
function updateTaskProgress(taskState) {
  taskState.progress_percent = calculateProgress(taskState);
  taskState.updated_at = new Date().toISOString();
  return taskState.progress_percent;
}

// ==================== 进度解释 ====================

/**
 * 生成进度的文字解释（用于默认视图）
 */
function getProgressExplanation(taskState) {
  const progress = taskState.progress_percent;
  const currentPhase = taskState.current_phase;
  
  // 根据进度范围给出不同解释
  if (progress === 0) {
    return '任务刚开始，正在准备';
  } else if (progress < 20) {
    return `早期阶段：${currentPhase || '准备中'}`;
  } else if (progress < 50) {
    return `进行中：${currentPhase || '执行中'}，进度正常`;
  } else if (progress < 80) {
    return `中后期：${currentPhase || '执行中'}，进展顺利`;
  } else if (progress < 100) {
    return `收尾阶段：${currentPhase || '最后整理'}，即将完成`;
  } else {
    return '任务已完成';
  }
}

/**
 * 判断进度是否异常（长时间无进展）
 */
function isProgressStalled(taskState, thresholdMinutes = 5) {
  if (!taskState.started_at) {
    return false;
  }
  
  const now = new Date();
  const started = new Date(taskState.started_at);
  const elapsedMinutes = (now - started) / 1000 / 60;
  
  // 如果执行时间超过阈值但进度仍为 0
  if (elapsedMinutes > thresholdMinutes && taskState.progress_percent === 0) {
    return true;
  }
  
  // 检查最近更新时间
  if (taskState.updated_at) {
    const updated = new Date(taskState.updated_at);
    const sinceUpdateMinutes = (now - updated) / 1000 / 60;
    
    // 超过阈值时间无更新且未完成
    if (sinceUpdateMinutes > thresholdMinutes && taskState.progress_percent < 100) {
      return true;
    }
  }
  
  return false;
}

/**
 * 获取阶段进度详情（用于展开视图）
 */
function getPhaseProgressDetails(taskState) {
  return taskState.phases.map(phase => ({
    name: phase.phase_name,
    status: phase.phase_status,
    progress: phase.phase_progress,
    weight: phase.phase_weight,
    summary: phase.summary,
    completed: phase.phase_status === PHASE_STATUS.COMPLETED || phase.phase_status === PHASE_STATUS.SKIPPED
  }));
}

/**
 * 格式化进度显示（用于 UI）
 */
function formatProgressDisplay(progress) {
  // 生成进度条
  const bars = Math.floor(progress / 10);
  const emptyBars = 10 - bars;
  
  return {
    percent: progress,
    bar: '█'.repeat(bars) + '░'.repeat(emptyBars),
    text: `${progress}%`
  };
}

/**
 * 预估剩余时间（简单版本）
 */
function estimateRemainingTime(taskState) {
  if (!taskState.started_at || taskState.progress_percent === 0) {
    return null;
  }
  
  const now = new Date();
  const started = new Date(taskState.started_at);
  const elapsedSeconds = (now - started) / 1000;
  const progress = taskState.progress_percent;
  
  if (progress >= 100) {
    return { seconds: 0, text: '已完成' };
  }
  
  // 简单线性预估
  const totalEstimated = elapsedSeconds / (progress / 100);
  const remaining = totalEstimated - elapsedSeconds;
  
  if (remaining < 0) {
    return { seconds: 0, text: '即将完成' };
  }
  
  return {
    seconds: Math.round(remaining),
    text: formatDuration(Math.round(remaining))
  };
}

/**
 * 格式化持续时间
 */
function formatDuration(seconds) {
  if (seconds < 60) {
    return `约${seconds}秒`;
  } else if (seconds < 3600) {
    const mins = Math.round(seconds / 60);
    return `约${mins}分钟`;
  } else {
    const hours = Math.round(seconds / 3600);
    return `约${hours}小时`;
  }
}

// ==================== 导出 ====================

module.exports = {
  calculateProgress,
  getPhaseCompletion,
  updateTaskProgress,
  getProgressExplanation,
  isProgressStalled,
  getPhaseProgressDetails,
  formatProgressDisplay,
  estimateRemainingTime
};
