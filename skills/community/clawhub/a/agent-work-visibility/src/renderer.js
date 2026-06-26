/**
 * Agent Work Visibility - View Renderer
 * 
 * 视图渲染器
 * 核心原则：渐进披露，默认视图极简
 */

const { OVERALL_STATUS, BLOCKER_LEVEL, PHASE_STATUS } = require('./schema');
const { getBlockerSummary } = require('./blocker');
const { getUserInputSummary } = require('./ask-human');
const { getRecentLogs, getCurrentAction } = require('./logger');
const { getPhaseProgressDetails, formatProgressDisplay, estimateRemainingTime } = require('./progress');

// ==================== 状态文本映射 ====================

const STATUS_TEXT = {
  [OVERALL_STATUS.PENDING]: '等待中',
  [OVERALL_STATUS.PLANNING]: '规划中',
  [OVERALL_STATUS.RUNNING]: '运行中',
  [OVERALL_STATUS.WAITING]: '等待中',
  [OVERALL_STATUS.BLOCKED]: '已阻塞',
  [OVERALL_STATUS.REVIEWING]: '复核中',
  [OVERALL_STATUS.COMPLETED]: '已完成',
  [OVERALL_STATUS.FAILED]: '已失败'
};

const BLOCKER_TEXT = {
  [BLOCKER_LEVEL.NONE]: '无',
  [BLOCKER_LEVEL.LOW]: '轻微',
  [BLOCKER_LEVEL.MEDIUM]: '中等',
  [BLOCKER_LEVEL.HIGH]: '严重'
};

// ==================== 默认视图渲染 ====================

/**
 * 渲染默认视图（V2 极简，3 秒内看懂）
 * 
 * 只展示：
 * - 任务标题
 * - 健康度指示器
 * - 当前状态（带图标）
 * - 当前阶段
 * - 当前在做什么
 * - 为什么还没完成
 * - 下一步
 * - 是否需要你
 */
function renderDefaultView(taskState) {
  const lines = [];
  
  // 任务标题（带状态图标）
  const statusIcon = getStatusIcon(taskState.overall_status, taskState.needs_user_input, taskState.blocker_status !== 'none');
  lines.push(`${statusIcon} ${taskState.task_title}`);
  lines.push('');
  
  // 健康度指示器（V2 新增）
  const healthScore = taskState.health_score !== undefined ? taskState.health_score : calculateHealthScore(taskState);
  const healthIndicator = getHealthIndicator(healthScore);
  lines.push(`健康度：${healthIndicator.icon} ${healthIndicator.text}`);
  lines.push('');
  
  // 当前状态
  const statusText = STATUS_TEXT[taskState.overall_status] || taskState.overall_status;
  lines.push(`状态：${statusIcon} ${statusText}`);
  
  // 当前阶段
  if (taskState.current_phase) {
    lines.push(`阶段：${taskState.current_phase}`);
  }
  
  // 空行分隔
  lines.push('');
  
  // 当前在做什么（V2 优先使用具体动作）
  lines.push('📍 当前在做什么：');
  const currentAction = getCurrentAction(taskState);
  lines.push(`   ${currentAction}`);
  lines.push('');
  
  // 为什么还没完成（V2 显示累积时长）
  lines.push('⏳ 为什么还没完成：');
  const whyNotDone = getWhyNotDone(taskState);
  lines.push(`   ${whyNotDone || '任务正在正常执行中'}`);
  lines.push('');
  
  // 下一步（V2 使用预测文案）
  lines.push('➡️ 下一步：');
  lines.push(`   ${taskState.next_action || '继续执行当前阶段'}`);
  lines.push('');
  
  // 是否需要你（V2 显示 context）
  lines.push('🙋 是否需要你：');
  const userInputSummary = getUserInputSummary(taskState);
  if (userInputSummary.needs_input) {
    lines.push('   ⚠️ 需要您的介入！');
    lines.push('');
    lines.push(`   问题：${userInputSummary.question}`);
    
    // V2 显示 context
    if (userInputSummary.context && userInputSummary.context.reason) {
      lines.push(`   原因：${userInputSummary.context.reason}`);
    }
    
    if (userInputSummary.options && userInputSummary.options.length > 0) {
      lines.push('');
      lines.push('   选项：');
      userInputSummary.options.forEach((opt, i) => {
        lines.push(`     [${String.fromCharCode(65 + i)}] ${opt}`);
      });
    }
  } else {
    lines.push('   暂时不需要');
  }
  
  return lines.join('\n');
}

/**
 * 计算健康度分数（V2）
 */
function calculateHealthScore(taskState) {
  let score = 100;
  
  // 阻塞扣分
  if (taskState.blocker_status !== 'none') {
    score -= 20;
    if (taskState.blocker_status === 'medium') score -= 15;
    if (taskState.blocker_status === 'high') score -= 30;
  }
  
  // 需要用户介入扣分
  if (taskState.needs_user_input) {
    score -= 10;
  }
  
  // 失败状态
  if (taskState.overall_status === 'failed') {
    score = 0;
  }
  
  return Math.max(0, Math.min(100, score));
}

/**
 * 获取健康度指示器（V2）
 */
function getHealthIndicator(score) {
  if (score >= 80) {
    return { icon: '🟢', text: '健康', color: 'green' };
  } else if (score >= 60) {
    return { icon: '🟡', text: '轻微延迟', color: 'yellow' };
  } else if (score >= 40) {
    return { icon: '🟠', text: '注意', color: 'orange' };
  } else {
    return { icon: '🔴', text: '严重阻塞', color: 'red' };
  }
}

/**
 * 获取状态图标（V2）
 */
function getStatusIcon(status, needsUserInput = false, hasBlocker = false) {
  if (needsUserInput) return '⚠️';
  if (hasBlocker) return '🔴';
  
  switch (status) {
    case 'completed': return '✅';
    case 'failed': return '❌';
    case 'blocked': return '🔴';
    case 'waiting': return '🟡';
    case 'running': return '🟢';
    case 'planning': return '🔵';
    default: return '⚪';
  }
}

/**
 * 获取"为什么还没完成"的解释
 */
function getWhyNotDone(taskState) {
  // 如果有阻塞，优先显示阻塞原因
  const blockerSummary = getBlockerSummary(taskState);
  if (blockerSummary.has_blocker) {
    return `${blockerSummary.reason}（已持续${blockerSummary.duration}）`;
  }
  
  // 如果有用户介入请求
  if (taskState.needs_user_input) {
    return '等待用户输入';
  }
  
  // 如果已有预设解释
  if (taskState.why_not_done) {
    return taskState.why_not_done;
  }
  
  // 根据状态推断
  switch (taskState.overall_status) {
    case OVERALL_STATUS.RUNNING:
      return '任务正在正常执行中';
    case OVERALL_STATUS.WAITING:
      return '等待外部响应';
    case OVERALL_STATUS.PLANNING:
      return '正在制定执行计划';
    case OVERALL_STATUS.REVIEWING:
      return '正在复核结果';
    default:
      return null;
  }
}

// ==================== 展开视图渲染 ====================

/**
 * 渲染展开视图（详细信息）
 * 
 * 展示：
 * - 阶段列表
 * - 最近动作日志
 * - 重试记录
 * - 阻塞详情
 */
function renderFullView(taskState) {
  const lines = [];
  
  // 先输出默认视图
  lines.push(renderDefaultView(taskState));
  lines.push('');
  lines.push('━━━━━━━━━━━━━━━━━━━━━━━━');
  lines.push('【展开详情】');
  lines.push('');
  
  // 进度条
  const progressDisplay = formatProgressDisplay(taskState.progress_percent);
  lines.push(`【总体进度】`);
  lines.push(`${progressDisplay.bar} ${progressDisplay.text}`);
  
  // 预估剩余时间
  const remaining = estimateRemainingTime(taskState);
  if (remaining) {
    lines.push(`预计剩余：${remaining.text}`);
  }
  lines.push('');
  
  // 阶段进度
  lines.push('【阶段进度】');
  const phaseDetails = getPhaseProgressDetails(taskState);
  phaseDetails.forEach(phase => {
    const icon = getPhaseIcon(phase.status);
    const progressText = phase.status === PHASE_STATUS.IN_PROGRESS 
      ? ` - ${phase.progress}%` 
      : '';
    lines.push(`${icon} ${phase.name}${progressText}`);
  });
  lines.push('');
  
  // 最近动作
  lines.push('【最近动作】');
  const recentLogs = getRecentLogs(taskState, 10);
  if (recentLogs.length === 0) {
    lines.push('暂无动作记录');
  } else {
    recentLogs.forEach(log => {
      const levelIcon = getLevelIcon(log.level);
      lines.push(`${levelIcon} ${log.message}`);
    });
  }
  lines.push('');
  
  // 阻塞状态
  lines.push('【阻塞状态】');
  const blockerSummary = getBlockerSummary(taskState);
  if (blockerSummary.has_blocker) {
    lines.push(`级别：${blockerSummary.level}`);
    lines.push(`原因：${blockerSummary.reason}`);
    lines.push(`持续：${blockerSummary.duration}`);
    if (blockerSummary.recommendation) {
      lines.push(`建议：${blockerSummary.recommendation}`);
    }
  } else {
    lines.push('无阻塞');
  }
  lines.push('');
  
  // 重试记录
  if (taskState.retry_log && taskState.retry_log.length > 0) {
    lines.push('【重试记录】');
    taskState.retry_log.slice(0, 5).forEach(retry => {
      const icon = retry.success ? '✓' : '✗';
      lines.push(`${icon} ${retry.operation} - 第${retry.attempt}次：${retry.reason}`);
    });
    lines.push('');
  }
  
  // 时间信息
  lines.push('【时间信息】');
  lines.push(`开始：${formatTimestamp(taskState.started_at)}`);
  lines.push(`更新：${formatTimestamp(taskState.updated_at)}`);
  if (taskState.completed_at) {
    lines.push(`完成：${formatTimestamp(taskState.completed_at)}`);
  }
  
  return lines.join('\n');
}

/**
 * 获取阶段图标
 */
function getPhaseIcon(status) {
  switch (status) {
    case PHASE_STATUS.COMPLETED:
      return '✓';
    case PHASE_STATUS.IN_PROGRESS:
      return '⟳';
    case PHASE_STATUS.BLOCKED:
      return '⚠';
    case PHASE_STATUS.SKIPPED:
      return '○';
    case PHASE_STATUS.PENDING:
    default:
      return '○';
  }
}

/**
 * 获取日志级别图标
 */
function getLevelIcon(level) {
  switch (level) {
    case 'error':
      return '✗';
    case 'warning':
      return '⚠';
    case 'retry':
      return '↻';
    case 'info':
    default:
      return '•';
  }
}

/**
 * 格式化时间戳
 */
function formatTimestamp(isoString) {
  if (!isoString) return '-';
  const date = new Date(isoString);
  return date.toLocaleString('zh-CN', { 
    month: '2-digit', 
    day: '2-digit', 
    hour: '2-digit', 
    minute: '2-digit' 
  });
}

// ==================== JSON 输出 ====================

/**
 * 输出任务状态 JSON（用于 API/程序化访问）
 */
function renderJSON(taskState, full = false) {
  const base = {
    task_id: taskState.task_id,
    task_title: taskState.task_title,
    task_type: taskState.task_type,
    overall_status: taskState.overall_status,
    current_phase: taskState.current_phase,
    progress_percent: taskState.progress_percent,
    current_action: getCurrentAction(taskState),
    why_not_done: getWhyNotDone(taskState),
    next_action: taskState.next_action,
    needs_user_input: taskState.needs_user_input,
    user_question: taskState.user_question,
    user_options: taskState.user_options,
    started_at: taskState.started_at,
    updated_at: taskState.updated_at
  };
  
  if (full) {
    base.phases = getPhaseProgressDetails(taskState);
    base.action_log = getRecentLogs(taskState, 10);
    base.blocker = getBlockerSummary(taskState);
    base.retry_log = taskState.retry_log || [];
  }
  
  return base;
}

// ==================== 导出 ====================

module.exports = {
  renderDefaultView,
  renderFullView,
  renderJSON,
  STATUS_TEXT,
  BLOCKER_TEXT
};
