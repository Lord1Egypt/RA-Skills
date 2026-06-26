/**
 * Agent Work Visibility - Schema Definitions
 * 
 * 定义任务状态的核心数据结构
 */

// ==================== 任务整体状态 ====================

const OVERALL_STATUS = {
  PENDING: 'pending',       // 等待开始
  PLANNING: 'planning',     // 规划中
  RUNNING: 'running',       // 执行中
  WAITING: 'waiting',       // 等待外部响应（正常）
  BLOCKED: 'blocked',       // 被阻塞（需要关注）
  REVIEWING: 'reviewing',   // 复核中
  COMPLETED: 'completed',   // 已完成
  FAILED: 'failed'          // 失败
};

// ==================== 阶段状态 ====================

const PHASE_STATUS = {
  PENDING: 'pending',       // 等待中
  IN_PROGRESS: 'in_progress', // 进行中
  COMPLETED: 'completed',   // 已完成
  BLOCKED: 'blocked',       // 被阻塞
  SKIPPED: 'skipped'        // 已跳过
};

// ==================== 阻塞级别 ====================

const BLOCKER_LEVEL = {
  NONE: 'none',     // 无阻塞
  LOW: 'low',       // 轻微阻塞（可自动恢复）
  MEDIUM: 'medium', // 中等阻塞（可能需要用户关注）
  HIGH: 'high'      // 严重阻塞（需要用户介入）
};

// ==================== 阻塞类型 ====================

const BLOCKER_TYPE = {
  API_TIMEOUT: 'api_timeout',           // API/网页超时
  AUTH_REQUIRED: 'auth_required',       // 需要登录/授权
  INFO_CONFLICT: 'info_conflict',       // 信息冲突
  MISSING_INPUT: 'missing_input',       // 缺少关键输入
  SCOPE_EXPANSION: 'scope_expansion',   // 任务范围扩大
  RATE_LIMITED: 'rate_limited',         // 触发速率限制
  RESOURCE_UNAVAILABLE: 'resource_unavailable' // 资源不可用
};

// ==================== 用户介入类型 ====================

const USER_INPUT_TYPE = {
  SCOPE_CLARIFICATION: 'scope_clarification',   // 需要澄清搜索范围
  DIRECTION_CHOICE: 'direction_choice',         // 需要选择方向
  AUTH_REQUIRED: 'auth_required',               // 需要登录/授权
  SCOPE_CONFIRMATION: 'scope_confirmation',     // 需要确认范围扩大
  JUDGEMENT_CALL: 'judgement_call',             // 需要在冲突信息中判断
  CONTINUE_OR_STOP: 'continue_or_stop'          // 需要确认是否继续
};

// ==================== 任务状态对象 ====================

/**
 * 创建新的任务状态对象
 */
function createTaskState(taskId, taskTitle, taskType = 'research') {
  const now = new Date().toISOString();
  
  return {
    // 基础信息
    task_id: taskId,
    task_title: taskTitle,
    task_type: taskType,
    
    // 整体状态
    overall_status: OVERALL_STATUS.PENDING,
    current_phase: null,
    progress_percent: 0,
    
    // 阻塞状态
    blocker_status: BLOCKER_LEVEL.NONE,
    blocker_reason: null,
    blocker_type: null,
    blocker_since: null,
    
    // 用户介入
    needs_user_input: false,
    user_input_type: null,
    user_question: null,
    user_options: [],
    
    // 行动指引
    current_action: null,       // 当前在做什么
    why_not_done: null,         // 为什么还没完成
    next_action: null,          // 下一步做什么
    recommended_user_action: null, // 推荐用户操作
    
    // 时间戳
    started_at: now,
    updated_at: now,
    completed_at: null,
    
    // 阶段列表（固定 5 阶段）
    phases: [],
    
    // 动作日志（最近 10 条）
    action_log: [],
    
    // 重试记录
    retry_log: []
  };
}

// ==================== 阶段对象 ====================

/**
 * 创建阶段对象
 */
function createPhase(phaseName, weight, order) {
  return {
    phase_name: phaseName,
    phase_status: PHASE_STATUS.PENDING,
    phase_progress: 0,          // 0-100
    phase_weight: weight,       // 权重（用于计算总进度）
    order: order,
    summary: null,
    started_at: null,
    completed_at: null,
    blocked_reason: null
  };
}

// ==================== 动作日志对象 ====================

/**
 * 创建动作日志条目（用户可读的自然语言）
 */
function createLogEntry(message, level = 'info') {
  return {
    timestamp: new Date().toISOString(),
    message: message,           // 用户可读的自然语言
    level: level,               // info | warning | error | retry
    raw_event: null             // 可选：底层原始事件
  };
}

// ==================== 重试记录对象 ====================

/**
 * 创建重试记录
 */
function createRetryEntry(operation, attempt, reason) {
  return {
    timestamp: new Date().toISOString(),
    operation: operation,
    attempt: attempt,
    reason: reason,
    success: false
  };
}

// ==================== 用户介入请求对象 ====================

/**
 * 创建用户介入请求
 */
function createUserInputRequest(question, options, inputType = USER_INPUT_TYPE.DIRECTION_CHOICE) {
  return {
    needs_user_input: true,
    user_input_type: inputType,
    user_question: question,
    user_options: options,
    created_at: new Date().toISOString()
  };
}

// ==================== 导出 ====================

module.exports = {
  // 枚举
  OVERALL_STATUS,
  PHASE_STATUS,
  BLOCKER_LEVEL,
  BLOCKER_TYPE,
  USER_INPUT_TYPE,
  
  // 创建函数
  createTaskState,
  createPhase,
  createLogEntry,
  createRetryEntry,
  createUserInputRequest
};
