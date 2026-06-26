/**
 * Agent Work Visibility - Blocker Detection
 * 
 * 阻塞识别系统
 * 核心原则：不能只说 blocked，要告诉用户该做什么
 */

const { BLOCKER_LEVEL, BLOCKER_TYPE } = require('./schema');

// ==================== 阻塞识别规则 ====================

/**
 * 阻塞类型到级别的映射
 */
const BLOCKER_TYPE_TO_LEVEL = {
  [BLOCKER_TYPE.API_TIMEOUT]: BLOCKER_LEVEL.LOW,      // 通常可自动恢复
  [BLOCKER_TYPE.RATE_LIMITED]: BLOCKER_LEVEL.LOW,     // 等待后可恢复
  [BLOCKER_TYPE.RESOURCE_UNAVAILABLE]: BLOCKER_LEVEL.MEDIUM,
  [BLOCKER_TYPE.AUTH_REQUIRED]: BLOCKER_LEVEL.MEDIUM, // 需要用户操作
  [BLOCKER_TYPE.INFO_CONFLICT]: BLOCKER_LEVEL.MEDIUM, // 需要判断
  [BLOCKER_TYPE.MISSING_INPUT]: BLOCKER_LEVEL.HIGH,   // 必须用户输入
  [BLOCKER_TYPE.SCOPE_EXPANSION]: BLOCKER_LEVEL.HIGH  // 必须用户确认
};

/**
 * 阻塞类型到推荐用户操作的映射
 */
const BLOCKER_RECOMMENDATIONS = {
  [BLOCKER_TYPE.API_TIMEOUT]: {
    low: '可继续等待，系统会自动重试',
    medium: '等待时间较长，可考虑跳过此数据源',
    high: '多次重试失败，建议手动跳过或更换数据源'
  },
  [BLOCKER_TYPE.RATE_LIMITED]: {
    low: '正在等待速率限制解除，预计 1-2 分钟',
    medium: '速率限制时间较长，可考虑稍后继续',
    high: '多次触发限制，可能需要更换 IP 或稍后再试'
  },
  [BLOCKER_TYPE.AUTH_REQUIRED]: {
    low: '需要登录才能访问此资源',
    medium: '需要提供账号授权才能继续',
    high: '多个资源都需要授权，建议先完成登录'
  },
  [BLOCKER_TYPE.INFO_CONFLICT]: {
    low: '发现信息不一致，正在交叉验证',
    medium: '关键信息存在冲突，需要人工判断',
    high: '多处信息矛盾，无法自动判断，需要您决策'
  },
  [BLOCKER_TYPE.MISSING_INPUT]: {
    low: '缺少部分信息，将尝试其他方式获取',
    medium: '缺少关键信息，需要您补充',
    high: '缺少必要输入，无法继续执行'
  },
  [BLOCKER_TYPE.SCOPE_EXPANSION]: {
    low: '发现相关扩展内容，将简要浏览',
    medium: '发现重要扩展方向，需要确认是否深入',
    high: '任务范围显著扩大，需要您确认是否继续'
  },
  [BLOCKER_TYPE.RESOURCE_UNAVAILABLE]: {
    low: '部分资源暂时不可用，尝试其他方式',
    medium: '关键资源不可用，可能需要更换数据源',
    high: '主要数据源不可用，任务可能无法完成'
  }
};

/**
 * 阻塞类型到"为什么还没完成"的解释映射
 */
const BLOCKER_WHY_NOT_DONE = {
  [BLOCKER_TYPE.API_TIMEOUT]: '正在等待外部 API 响应，已自动重试',
  [BLOCKER_TYPE.RATE_LIMITED]: '触发速率限制，正在等待恢复',
  [BLOCKER_TYPE.AUTH_REQUIRED]: '需要登录/授权才能访问所需资源',
  [BLOCKER_TYPE.INFO_CONFLICT]: '发现信息不一致，正在交叉验证',
  [BLOCKER_TYPE.MISSING_INPUT]: '缺少关键输入，等待用户补充',
  [BLOCKER_TYPE.SCOPE_EXPANSION]: '发现扩展内容，等待确认是否深入',
  [BLOCKER_TYPE.RESOURCE_UNAVAILABLE]: '部分资源不可用，正在寻找替代方案'
};

// ==================== 阻塞操作 ====================

/**
 * 报告阻塞
 */
function reportBlocker(taskState, blockerType, reason = null, overrideLevel = null) {
  const level = overrideLevel || BLOCKER_TYPE_TO_LEVEL[blockerType] || BLOCKER_LEVEL.MEDIUM;
  const now = new Date().toISOString();
  
  taskState.blocker_status = level;
  taskState.blocker_type = blockerType;
  taskState.blocker_reason = reason || getDefaultReason(blockerType);
  taskState.blocker_since = now;
  
  // 更新整体状态为 blocked
  taskState.overall_status = 'blocked';
  
  // 设置推荐用户操作
  taskState.recommended_user_action = getRecommendation(blockerType, level);
  
  // 设置"为什么还没完成"
  taskState.why_not_done = BLOCKER_WHY_NOT_DONE[blockerType] || '遇到阻塞，正在处理';
  
  taskState.updated_at = now;
  
  return {
    blocker_status: level,
    blocker_type: blockerType,
    blocker_reason: taskState.blocker_reason,
    recommended_user_action: taskState.recommended_user_action
  };
}

/**
 * 获取阻塞的默认原因描述
 */
function getDefaultReason(blockerType) {
  const defaults = {
    [BLOCKER_TYPE.API_TIMEOUT]: '外部 API 响应超时',
    [BLOCKER_TYPE.RATE_LIMITED]: '触发速率限制',
    [BLOCKER_TYPE.AUTH_REQUIRED]: '需要登录/授权',
    [BLOCKER_TYPE.INFO_CONFLICT]: '信息存在冲突',
    [BLOCKER_TYPE.MISSING_INPUT]: '缺少关键输入',
    [BLOCKER_TYPE.SCOPE_EXPANSION]: '任务范围扩大',
    [BLOCKER_TYPE.RESOURCE_UNAVAILABLE]: '资源不可用'
  };
  return defaults[blockerType] || '未知阻塞';
}

/**
 * 获取推荐用户操作
 */
function getRecommendation(blockerType, level) {
  return BLOCKER_RECOMMENDATIONS[blockerType]?.[level] || '请等待系统自动处理';
}

/**
 * 清除阻塞状态
 */
function clearBlocker(taskState) {
  taskState.blocker_status = BLOCKER_LEVEL.NONE;
  taskState.blocker_type = null;
  taskState.blocker_reason = null;
  taskState.blocker_since = null;
  taskState.recommended_user_action = null;
  
  // 恢复整体状态（如果没有其他问题）
  if (!taskState.needs_user_input) {
    taskState.overall_status = 'running';
  }
  
  // 清除"为什么还没完成"
  if (taskState.why_not_done?.includes('阻塞') || taskState.why_not_done?.includes('等待')) {
    taskState.why_not_done = null;
  }
  
  taskState.updated_at = new Date().toISOString();
}

/**
 * 检查是否有活跃阻塞
 */
function hasActiveBlocker(taskState) {
  return taskState.blocker_status !== BLOCKER_LEVEL.NONE;
}

/**
 * 获取阻塞持续时间（秒）
 */
function getBlockerDuration(taskState) {
  if (!taskState.blocker_since) {
    return 0;
  }
  
  const now = new Date();
  const since = new Date(taskState.blocker_since);
  return Math.floor((now - since) / 1000);
}

/**
 * 判断阻塞是否升级（持续时间过长）
 */
function shouldEscalateBlocker(taskState) {
  if (!hasActiveBlocker(taskState)) {
    return false;
  }
  
  const duration = getBlockerDuration(taskState);
  
  // 根据当前级别和持续时间判断是否升级
  const escalationRules = {
    [BLOCKER_LEVEL.LOW]: 120,      // 2 分钟后升级
    [BLOCKER_LEVEL.MEDIUM]: 300,   // 5 分钟后升级
    [BLOCKER_LEVEL.HIGH]: 600      // 10 分钟后升级
  };
  
  const threshold = escalationRules[taskState.blocker_status] || 300;
  return duration > threshold;
}

/**
 * 获取阻塞摘要（用于默认视图）
 */
function getBlockerSummary(taskState) {
  if (!hasActiveBlocker(taskState)) {
    return { has_blocker: false };
  }
  
  const duration = getBlockerDuration(taskState);
  const durationText = formatDuration(duration);
  
  return {
    has_blocker: true,
    level: taskState.blocker_status,
    reason: taskState.blocker_reason,
    duration: durationText,
    recommendation: taskState.recommended_user_action
  };
}

/**
 * 格式化持续时间
 */
function formatDuration(seconds) {
  if (seconds < 60) {
    return `${seconds}秒`;
  } else if (seconds < 3600) {
    return `${Math.floor(seconds / 60)}分钟`;
  } else {
    return `${Math.floor(seconds / 3600)}小时`;
  }
}

// ==================== 导出 ====================

module.exports = {
  BLOCKER_TYPE_TO_LEVEL,
  BLOCKER_RECOMMENDATIONS,
  reportBlocker,
  clearBlocker,
  hasActiveBlocker,
  getBlockerDuration,
  shouldEscalateBlocker,
  getBlockerSummary
};
