/**
 * Agent Work Visibility - Phase Model
 * 
 * Research Agent 固定 5 阶段模型
 */

const { createPhase, PHASE_STATUS } = require('./schema');

// ==================== Research 固定 5 阶段 ====================

/**
 * Research 任务的标准阶段定义
 * 
 * 权重分配原则：
 * - 收集信息 + 分析与比较 = 60%（核心工作）
 * - 制定计划 = 15%（重要但较快）
 * - 理解任务 + 形成输出 = 25%（首尾阶段）
 */
const RESEARCH_PHASES = [
  {
    name: '理解任务',
    weight: 10,
    order: 1,
    description: '解析用户需求，明确任务目标和范围'
  },
  {
    name: '制定搜索计划',
    weight: 15,
    order: 2,
    description: '设计搜索策略，确定关键词和数据源'
  },
  {
    name: '收集信息',
    weight: 30,
    order: 3,
    description: '执行搜索，抓取网页，提取数据'
  },
  {
    name: '分析与比较',
    weight: 30,
    order: 4,
    description: '整理信息，交叉验证，对比分析'
  },
  {
    name: '形成输出',
    weight: 15,
    order: 5,
    description: '生成结论，撰写报告，格式化输出'
  }
];

// ==================== 阶段初始化 ====================

/**
 * 初始化 Research 任务的 5 个阶段
 */
function initResearchPhases() {
  return RESEARCH_PHASES.map(p => createPhase(p.name, p.weight, p.order));
}

// ==================== 阶段操作 ====================

/**
 * 开始一个阶段
 */
function startPhase(taskState, phaseName) {
  const phase = taskState.phases.find(p => p.phase_name === phaseName);
  if (!phase) {
    throw new Error(`未知阶段：${phaseName}`);
  }
  
  // 完成前一个阶段（如果有）
  const previousPhase = taskState.phases.find(
    p => p.phase_status === PHASE_STATUS.IN_PROGRESS
  );
  if (previousPhase) {
    completePhase(taskState, previousPhase.phase_name);
  }
  
  // 开始新阶段
  phase.phase_status = PHASE_STATUS.IN_PROGRESS;
  phase.phase_progress = 0;
  phase.started_at = new Date().toISOString();
  
  taskState.current_phase = phaseName;
  taskState.updated_at = new Date().toISOString();
  
  return phase;
}

/**
 * 更新阶段进度（0-100）
 */
function updatePhaseProgress(taskState, phaseName, progress) {
  const phase = taskState.phases.find(p => p.phase_name === phaseName);
  if (!phase) {
    throw new Error(`未知阶段：${phaseName}`);
  }
  
  phase.phase_progress = Math.min(100, Math.max(0, progress));
  taskState.updated_at = new Date().toISOString();
  
  return phase;
}

/**
 * 完成一个阶段
 */
function completePhase(taskState, phaseName, summary = null) {
  const phase = taskState.phases.find(p => p.phase_name === phaseName);
  if (!phase) {
    throw new Error(`未知阶段：${phaseName}`);
  }
  
  phase.phase_status = PHASE_STATUS.COMPLETED;
  phase.phase_progress = 100;
  phase.completed_at = new Date().toISOString();
  phase.summary = summary;
  
  taskState.updated_at = new Date().toISOString();
  
  // 自动推进到下一个阶段
  const nextPhase = taskState.phases.find(p => p.order === phase.order + 1);
  if (nextPhase && nextPhase.phase_status === PHASE_STATUS.PENDING) {
    return { completed: phase, next: nextPhase };
  }
  
  return { completed: phase, next: null };
}

/**
 * 阻塞一个阶段
 */
function blockPhase(taskState, phaseName, reason) {
  const phase = taskState.phases.find(p => p.phase_name === phaseName);
  if (!phase) {
    throw new Error(`未知阶段：${phaseName}`);
  }
  
  phase.phase_status = PHASE_STATUS.BLOCKED;
  phase.blocked_reason = reason;
  taskState.updated_at = new Date().toISOString();
  
  return phase;
}

/**
 * 跳过/标记为不需要执行
 */
function skipPhase(taskState, phaseName, reason = null) {
  const phase = taskState.phases.find(p => p.phase_name === phaseName);
  if (!phase) {
    throw new Error(`未知阶段：${phaseName}`);
  }
  
  phase.phase_status = PHASE_STATUS.SKIPPED;
  phase.summary = reason || '根据任务情况跳过此阶段';
  taskState.updated_at = new Date().toISOString();
  
  return phase;
}

/**
 * 获取当前阶段
 */
function getCurrentPhase(taskState) {
  return taskState.phases.find(p => p.phase_status === PHASE_STATUS.IN_PROGRESS) || null;
}

/**
 * 获取阶段摘要（用于默认视图）
 */
function getPhaseSummary(taskState) {
  const currentPhase = getCurrentPhase(taskState);
  if (!currentPhase) {
    return null;
  }
  
  const phaseDef = RESEARCH_PHASES.find(p => p.name === currentPhase.phase_name);
  
  return {
    phase_name: currentPhase.phase_name,
    phase_progress: currentPhase.phase_progress,
    description: phaseDef?.description || '',
    summary: currentPhase.summary
  };
}

// ==================== 导出 ====================

module.exports = {
  RESEARCH_PHASES,
  initResearchPhases,
  startPhase,
  updatePhaseProgress,
  completePhase,
  blockPhase,
  skipPhase,
  getCurrentPhase,
  getPhaseSummary
};
