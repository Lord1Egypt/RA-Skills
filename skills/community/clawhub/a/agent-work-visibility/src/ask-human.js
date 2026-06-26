/**
 * Agent Work Visibility - Ask Human
 * 
 * 用户介入队列系统
 * 核心原则：明确告诉用户"现在该不该你介入，以及你该做什么"
 */

const { USER_INPUT_TYPE, createUserInputRequest } = require('./schema');

// ==================== 介入请求模板 ====================

/**
 * 预定义的用户介入请求模板
 */
const INPUT_TEMPLATES = {
  // 需要补充搜索范围
  [USER_INPUT_TYPE.SCOPE_CLARIFICATION]: {
    question: '请补充或调整搜索范围',
    options: null,  // 自由文本输入
    hint: '可以指定关键词、数据源、或排除条件'
  },
  
  // 需要选择方向
  [USER_INPUT_TYPE.DIRECTION_CHOICE]: {
    question: '发现多个可深入的方向，请优先选择：',
    options: [],  // 需要动态填充
    hint: '选择一个方向，或要求全部分析'
  },
  
  // 需要登录/授权
  [USER_INPUT_TYPE.AUTH_REQUIRED]: {
    question: '需要登录/授权才能继续访问以下资源：',
    options: ['已登录，继续', '跳过此资源', '更换数据源'],
    hint: '请先完成登录，或选择跳过'
  },
  
  // 需要确认范围扩大
  [USER_INPUT_TYPE.SCOPE_CONFIRMATION]: {
    question: '发现重要扩展内容，是否深入分析？',
    options: ['是，深入分析', '否，保持原范围', '简要浏览即可'],
    hint: '深入分析会增加执行时间'
  },
  
  // 需要在冲突信息中判断
  [USER_INPUT_TYPE.JUDGEMENT_CALL]: {
    question: '发现信息冲突，请判断以哪个为准：',
    options: [],  // 需要动态填充冲突选项
    hint: '可以指定判断依据，或要求进一步验证'
  },
  
  // 需要确认是否继续
  [USER_INPUT_TYPE.CONTINUE_OR_STOP]: {
    question: '任务执行时间较长，是否继续？',
    options: ['继续执行', '暂停并保存进度', '终止任务'],
    hint: '当前已完成部分进度不会丢失'
  }
};

// ==================== 介入请求操作 ====================

/**
 * 创建用户介入请求（V2 增强版 - 支持 context）
 */
function requestUserInput(taskState, inputType, customQuestion = null, customOptions = null, context = null) {
  const template = INPUT_TEMPLATES[inputType];
  
  if (!template) {
    throw new Error(`未知的介入类型：${inputType}`);
  }
  
  const question = customQuestion || template.question;
  const options = customOptions || template.options;
  
  // 创建介入请求（V2 增加 context 字段）
  const request = {
    ...createUserInputRequest(question, options, inputType),
    context: context || generateDefaultContext(taskState, inputType)
  };
  
  // 更新任务状态
  taskState.needs_user_input = true;
  taskState.user_input_type = inputType;
  taskState.user_question = question;
  taskState.user_options = options || [];
  taskState.user_context = request.context;  // V2 新增
  taskState.overall_status = 'waiting';
  taskState.updated_at = new Date().toISOString();
  
  // 如果有 hint，添加到推荐操作
  if (template.hint) {
    taskState.recommended_user_action = template.hint;
  }
  
  return request;
}

/**
 * 生成默认 context（为什么需要你）
 */
function generateDefaultContext(taskState, inputType) {
  const context = {
    current_phase: taskState.current_phase,
    progress_percent: taskState.progress_percent,
    items_collected: 0,
    blocker_status: taskState.blocker_status
  };
  
  // 根据介入类型补充具体 context
  switch (inputType) {
    case 'direction_choice':
      context.reason = '发现多个可深入的方向，需要您指定优先级';
      context.alternatives = taskState.user_options || [];
      break;
      
    case 'scope_confirmation':
      context.reason = '任务范围显著扩大，需要您确认是否继续';
      context.original_scope = '原定范围';
      context.expanded_scope = '发现扩展内容';
      break;
      
    case 'auth_required':
      context.reason = '需要登录/授权才能访问所需资源';
      context.resource = '受限资源';
      context.auth_type = 'login';
      break;
      
    case 'judgement_call':
      context.reason = '发现关键信息冲突，需要您裁决';
      context.conflict_type = 'information_mismatch';
      break;
      
    case 'scope_clarification':
      context.reason = '搜索结果不足，需要您补充搜索范围';
      context.current_results = 0;
      context.min_results = 3;
      break;
      
    default:
      context.reason = '需要您的输入才能继续';
  }
  
  return context;
}

/**
 * 快速创建方向选择请求
 */
function requestDirectionChoice(taskState, directions) {
  const options = directions.map((d, i) => {
    if (typeof d === 'string') {
      return `${String.fromCharCode(65 + i)}: ${d}`;
    }
    return d;  // 已经是格式化好的选项
  });
  
  return requestUserInput(
    taskState,
    USER_INPUT_TYPE.DIRECTION_CHOICE,
    '发现多个可深入的方向，请优先选择：',
    options
  );
}

/**
 * 快速创建冲突判断请求
 */
function requestJudgementCall(taskState, conflictingInfo) {
  const options = conflictingInfo.map((info, i) => {
    return `${String.fromCharCode(65 + i)}: ${info}`;
  });
  
  return requestUserInput(
    taskState,
    USER_INPUT_TYPE.JUDGEMENT_CALL,
    '发现信息冲突，请判断以哪个为准：',
    options
  );
}

/**
 * 快速创建范围确认请求
 */
function requestScopeConfirmation(taskState, expansionDescription) {
  return requestUserInput(
    taskState,
    USER_INPUT_TYPE.SCOPE_CONFIRMATION,
    `发现重要扩展内容：${expansionDescription}，是否深入分析？`,
    ['是，深入分析', '否，保持原范围', '简要浏览即可']
  );
}

/**
 * 快速创建继续/停止请求（长任务超时提醒）
 */
function requestContinueOrStop(taskState, elapsedTime, completedPercent) {
  return requestUserInput(
    taskState,
    USER_INPUT_TYPE.CONTINUE_OR_STOP,
    `任务已执行 ${formatTime(elapsedTime)}，当前进度 ${completedPercent}%，是否继续？`,
    ['继续执行', '暂停并保存进度', '终止任务']
  );
}

/**
 * 用户已提供输入，清除介入状态
 */
function clearUserInputRequest(taskState) {
  taskState.needs_user_input = false;
  taskState.user_input_type = null;
  taskState.user_question = null;
  taskState.user_options = [];
  taskState.recommended_user_action = null;
  
  // 恢复执行状态
  taskState.overall_status = 'running';
  taskState.updated_at = new Date().toISOString();
}

/**
 * 检查是否需要用户介入
 */
function needsUserInput(taskState) {
  return taskState.needs_user_input === true;
}

/**
 * 获取介入请求摘要（用于默认视图）
 */
function getUserInputSummary(taskState) {
  if (!needsUserInput(taskState)) {
    return { needs_input: false };
  }
  
  return {
    needs_input: true,
    input_type: taskState.user_input_type,
    question: taskState.user_question,
    options: taskState.user_options,
    hint: taskState.recommended_user_action
  };
}

/**
 * 格式化时间（秒 -> 可读格式）
 */
function formatTime(seconds) {
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

// ==================== 导出 ====================

module.exports = {
  INPUT_TEMPLATES,
  USER_INPUT_TYPE,
  requestUserInput,
  requestDirectionChoice,
  requestJudgementCall,
  requestScopeConfirmation,
  requestContinueOrStop,
  clearUserInputRequest,
  needsUserInput,
  getUserInputSummary
};
