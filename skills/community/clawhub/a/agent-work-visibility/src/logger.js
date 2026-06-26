/**
 * Agent Work Visibility - Action Logger
 * 
 * 记录用户可读的自然语言动作日志
 * 核心原则：底层事件必须翻译成用户看得懂的话
 */

const { createLogEntry } = require('./schema');

// ==================== 日志配置 ====================

const MAX_LOG_ENTRIES = 10;  // 最多保留最近 10 条

// ==================== 事件翻译器 ====================

/**
 * 将底层系统事件翻译为用户可读的自然语言
 */
function translateEventToMessage(eventType, eventData = {}) {
  const translations = {
    // 任务启动
    'task_started': `任务已启动：${eventData.title || '未知任务'}`,
    'planning_started': '开始制定执行计划',
    'plan_created': `已生成计划：${eventData.stepCount || '?'}个步骤`,
    
    // 搜索相关
    'search_started': '开始搜索',
    'search_query_defined': `已明确搜索范围：${eventData.query || '未指定'}`,
    'search_completed': `搜索完成：找到 ${eventData.resultCount || 0} 个结果`,
    
    // 网页读取
    'page_fetch_started': `正在读取网页：${eventData.url ? shortenUrl(eventData.url) : '未知'}`,
    'page_fetch_completed': `已读取 ${eventData.pageNumber || 1} 个网页`,
    'page_fetch_timeout': '网页加载超时，正在重试',
    'page_fetch_failed': `网页读取失败：${eventData.reason || '未知原因'}`,
    
    // 数据提取
    'extraction_started': '开始提取数据',
    'extraction_completed': `已提取 ${eventData.itemCount || 0} 个数据项`,
    'extraction_partial': `部分提取成功：${eventData.successCount || 0}/${eventData.totalCount || '?'}`,
    
    // 数据分析
    'analysis_started': '开始分析数据',
    'comparison_started': `正在比较 ${eventData.itemCount || 2} 个项目`,
    'cross_validation_started': '发现信息不一致，正在交叉验证',
    'pattern_found': `发现关键模式：${eventData.pattern || '未指定'}`,
    
    // 重试
    'retry_attempt': `第 ${eventData.attempt || 1} 次重试：${eventData.operation || '操作'}`,
    'retry_success': `重试成功：${eventData.operation || '操作'}`,
    'retry_failed': `重试失败：${eventData.operation || '操作'}`,
    
    // 输出
    'output_generating': '正在生成输出',
    'output_completed': '输出已完成',
    'report_created': `已生成报告：${eventData.pages || 1}页`,
    
    // 阻塞
    'blocked_api_timeout': '外部 API 响应超时',
    'blocked_auth_required': '需要登录/授权才能继续',
    'blocked_info_conflict': '发现信息冲突，需要判断',
    'blocked_missing_input': '缺少关键输入，无法继续',
    'blocked_scope_expansion': '任务范围扩大，需要确认',
    
    // 用户介入
    'user_input_requested': '需要用户决策',
    'user_input_provided': '用户已提供输入',
    
    // 完成
    'task_completed': '任务已完成',
    'task_failed': `任务失败：${eventData.reason || '未知原因'}`
  };
  
  return translations[eventType] || `执行中：${eventType}`;
}

/**
 * 缩短 URL 用于显示
 */
function shortenUrl(url) {
  if (!url) return '';
  try {
    const urlObj = new URL(url);
    return urlObj.hostname + urlObj.pathname.slice(0, 30);
  } catch {
    return url.slice(0, 50);
  }
}

// ==================== 日志操作 ====================

/**
 * 添加动作日志
 */
function addLogEntry(taskState, message, level = 'info', rawEvent = null) {
  const entry = createLogEntry(message, level);
  if (rawEvent) {
    entry.raw_event = rawEvent;
  }
  
  taskState.action_log.unshift(entry);  // 新日志放在最前面
  
  // 保持最多 MAX_LOG_ENTRIES 条
  if (taskState.action_log.length > MAX_LOG_ENTRIES) {
    taskState.action_log = taskState.action_log.slice(0, MAX_LOG_ENTRIES);
  }
  
  taskState.updated_at = new Date().toISOString();
  
  return entry;
}

/**
 * 记录系统事件（自动翻译为用户可读消息）
 */
function recordEvent(taskState, eventType, eventData = {}, level = 'info') {
  const message = translateEventToMessage(eventType, eventData);
  return addLogEntry(taskState, message, level, { type: eventType, data: eventData });
}

/**
 * 记录重试
 */
function recordRetry(taskState, operation, attempt, reason, success = false) {
  const retryEntry = {
    timestamp: new Date().toISOString(),
    operation: operation,
    attempt: attempt,
    reason: reason,
    success: success
  };
  
  taskState.retry_log.unshift(retryEntry);
  
  // 同时添加到动作日志
  if (success) {
    addLogEntry(taskState, `重试成功：${operation}`, 'info');
  } else {
    addLogEntry(taskState, `重试失败：${operation}（第${attempt}次）`, 'warning');
  }
  
  return retryEntry;
}

/**
 * 获取最近动作日志（用于默认视图）
 */
function getRecentLogs(taskState, limit = 5) {
  return taskState.action_log.slice(0, limit).map(entry => ({
    timestamp: entry.timestamp,
    message: entry.message,
    level: entry.level
  }));
}

/**
 * 获取当前正在做什么（用于默认视图）
 */
function getCurrentAction(taskState) {
  if (taskState.action_log.length === 0) {
    return '准备中...';
  }
  
  const latest = taskState.action_log[0];
  
  // 如果是进行中的动作，直接返回
  if (latest.message.includes('正在') || latest.message.includes('开始')) {
    return latest.message;
  }
  
  // 否则根据当前阶段推断
  if (taskState.current_phase) {
    return `正在进行：${taskState.current_phase}`;
  }
  
  return latest.message;
}

/**
 * 清除日志
 */
function clearLogs(taskState) {
  taskState.action_log = [];
  taskState.retry_log = [];
  taskState.updated_at = new Date().toISOString();
}

// ==================== 导出 ====================

module.exports = {
  MAX_LOG_ENTRIES,
  translateEventToMessage,
  addLogEntry,
  recordEvent,
  recordRetry,
  getRecentLogs,
  getCurrentAction,
  clearLogs
};
