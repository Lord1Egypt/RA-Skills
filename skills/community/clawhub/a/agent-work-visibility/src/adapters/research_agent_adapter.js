/**
 * Research Agent Event Adapter
 * 
 * 将 Research Agent 的原始事件映射到 Visibility Skill 的标准化事件
 * 
 * 输入：Research Agent 原始事件
 * 输出：Visibility Skill 可处理的标准事件 + 人类可读动作
 */

const { BLOCKER_TYPE, USER_INPUT_TYPE } = require('../schema');

// ==================== 事件映射表 ====================

/**
 * 原始事件 → 标准化事件映射
 */
const EVENT_MAPPING = {
  // 任务生命周期
  'task_start': 'task_started',
  'task_replan': 'planning_started',
  'task_complete': 'task_completed',
  'task_failed': 'task_failed',
  
  // 阶段事件
  'phase_start': 'phase_started',
  'phase_complete': 'phase_completed',
  
  // 搜索相关
  'search_query_built': 'search_query_defined',
  'search_start': 'search_started',
  'search_complete': 'search_completed',
  
  // 网页抓取
  'page_fetch_start': 'page_fetch_started',
  'page_fetch_success': 'page_fetch_completed',
  'page_fetch_timeout': 'page_fetch_timeout',
  'page_fetch_error': 'page_fetch_failed',
  
  // 重试
  'retry_start': 'retry_attempt',
  'retry_success': 'retry_success',
  'retry_failed': 'retry_failed',
  
  // 数据提取
  'extraction_done': 'extraction_completed',
  'shortlist_done': 'shortlist_completed',
  
  // 分析比较
  'compare_start': 'comparison_started',
  'conflict_detected': 'info_conflict_detected',
  
  // 输出
  'draft_start': 'output_generating',
  'report_created': 'report_created',
  
  // 用户介入
  'user_input_required': 'user_input_requested'
};

/**
 * 标准化事件 → 人类可读动作翻译
 */
const ACTION_TRANSLATIONS = {
  'task_started': (data) => `任务已启动：${data.title || '未知任务'}`,
  'planning_started': () => '开始重新规划任务',
  'phase_started': (data) => `开始阶段：${data.phase || '未知阶段'}`,
  'phase_completed': (data) => `完成阶段：${data.phase || '未知阶段'}`,
  
  'search_query_defined': (data) => `已明确搜索范围：${data.query || '未指定'}`,
  'search_started': () => '开始搜索',
  'search_completed': (data) => `搜索完成：找到 ${data.resultCount || 0} 个结果`,
  
  'page_fetch_started': (data) => `正在读取网页：${data.url ? shortenUrl(data.url) : '未知'}`,
  'page_fetch_completed': (data) => `已读取 ${data.pageNumber || 1} 个网页`,
  'page_fetch_timeout': () => '网页加载超时，正在等待响应',
  'page_fetch_failed': (data) => `网页读取失败：${data.reason || '未知原因'}`,
  
  'retry_attempt': (data) => `第 ${data.attempt || 1} 次重试：${data.operation || '操作'}`,
  'retry_success': (data) => `重试成功：${data.operation || '操作'}`,
  'retry_failed': (data) => `重试失败：${data.operation || '操作'}`,
  
  'extraction_completed': (data) => `已提取 ${data.itemCount || 0} 个数据项`,
  'shortlist_completed': (data) => `已确定 ${data.count || 0} 个候选项目`,
  
  'comparison_started': (data) => `正在比较 ${data.itemCount || 2} 个项目`,
  'info_conflict_detected': () => '发现信息不一致，正在交叉验证',
  
  'output_generating': () => '正在生成输出',
  'report_created': (data) => `已生成报告：${data.pages || 1}页`,
  
  'user_input_requested': () => '需要用户决策',
  'task_completed': () => '任务已完成',
  'task_failed': (data) => `任务失败：${data.reason || '未知原因'}`
};

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

// ==================== 阻塞检测规则 ====================

/**
 * 事件 → 阻塞类型映射
 */
const BLOCKER_MAPPING = {
  'page_fetch_timeout': {
    type: BLOCKER_TYPE.API_TIMEOUT,
    level: 'low',  // 首次超时
    reason: '外部 API 响应超时'
  },
  'page_fetch_failed': {
    type: BLOCKER_TYPE.RESOURCE_UNAVAILABLE,
    level: 'medium',
    reason: '网页读取失败'
  },
  'retry_failed': (data) => ({
    type: BLOCKER_TYPE.API_TIMEOUT,
    level: data.attempt >= 3 ? 'medium' : 'low',
    reason: `多次重试失败（第${data.attempt || 1}次）`
  }),
  'auth_required': {
    type: BLOCKER_TYPE.AUTH_REQUIRED,
    level: 'medium',
    reason: '需要登录/授权'
  },
  'info_conflict_detected': {
    type: BLOCKER_TYPE.INFO_CONFLICT,
    level: 'low',  // 先自动交叉验证
    reason: '发现信息不一致'
  }
};

/**
 * 需要用户介入的事件
 */
const ASK_HUMAN_MAPPING = {
  'user_input_required': (data) => ({
    type: data.inputType || USER_INPUT_TYPE.DIRECTION_CHOICE,
    question: data.question || '需要您提供输入',
    options: data.options || []
  }),
  'scope_expansion_detected': (data) => ({
    type: USER_INPUT_TYPE.SCOPE_CONFIRMATION,
    question: `发现重要扩展内容：${data.description}，是否深入分析？`,
    options: ['是，深入分析', '否，保持原范围', '简要浏览即可']
  }),
  'direction_choice_needed': (data) => ({
    type: USER_INPUT_TYPE.DIRECTION_CHOICE,
    question: data.question || '发现多个可深入的方向，请优先选择：',
    options: data.directions?.map((d, i) => `${String.fromCharCode(65 + i)}: ${d}`) || []
  }),
  'conflict_requires_judgement': (data) => ({
    type: USER_INPUT_TYPE.JUDGEMENT_CALL,
    question: '发现关键信息冲突，请判断以哪个为准：',
    options: data.conflictingInfo?.map((info, i) => `${String.fromCharCode(65 + i)}: ${info}`) || []
  })
};

// ==================== Adapter 主类 ====================

class ResearchAgentAdapter {
  constructor(visibilityManager) {
    this.manager = visibilityManager;
    this.taskId = null;
    this.eventCount = 0;
    this.timeoutThreshold = 5000;      // 5 秒后显示 waiting
    this.blockerThreshold = 30000;     // 30 秒后显示 blocked
    this.retryCount = new Map();       // 跟踪重试次数
  }

  /**
   * 绑定任务
   */
  bindTask(taskId, taskTitle) {
    this.taskId = taskId;
    this.manager.createTask(taskId, taskTitle, 'research');
    return this;
  }

  /**
   * 处理原始事件（主入口）
   */
  handleEvent(rawEvent) {
    this.eventCount++;
    
    // 1. 标准化事件
    const normalizedEvent = this.normalizeEvent(rawEvent);
    
    // 2. 翻译为人类可读动作
    const humanAction = this.translateEvent(normalizedEvent, rawEvent.data);
    
    // 3. 检测是否需要更新状态
    this.updateVisibilityState(normalizedEvent, rawEvent.data);
    
    // 4. 检测阻塞
    const blocker = this.detectBlocker(normalizedEvent, rawEvent.data);
    if (blocker) {
      this.handleBlocker(blocker);
    }
    
    // 5. 检测是否需要 Ask Human
    const askHuman = this.detectAskHuman(normalizedEvent, rawEvent.data);
    if (askHuman) {
      this.handleAskHuman(askHuman);
    }
    
    return {
      normalized: normalizedEvent,
      humanAction: humanAction,
      blocker: blocker,
      askHuman: askHuman
    };
  }

  /**
   * 标准化事件
   */
  normalizeEvent(rawEvent) {
    const { type, data } = rawEvent;
    const normalizedType = EVENT_MAPPING[type] || type;
    
    return {
      type: normalizedType,
      data: data || {},
      timestamp: new Date().toISOString()
    };
  }

  /**
   * 翻译为人类可读动作
   */
  translateEvent(normalizedEvent, rawData) {
    const { type, data } = normalizedEvent;
    const translator = ACTION_TRANSLATIONS[type];
    
    if (!translator) {
      return `执行中：${type}`;
    }
    
    return translator(data || rawData);
  }

  /**
   * 更新 Visibility 状态
   */
  updateVisibilityState(normalizedEvent, rawData) {
    const { type, data } = normalizedEvent;
    
    switch (type) {
      case 'task_started':
        this.manager.log(this.taskId, `任务已启动：${data.title || '未知任务'}`);
        break;
        
      case 'phase_started':
        this.manager.startPhase(this.taskId, data.phase);
        break;
        
      case 'phase_completed':
        this.manager.completePhase(this.taskId, data.phase, data.summary);
        break;
        
      case 'search_query_defined':
        this.manager.log(this.taskId, `已明确搜索范围：${data.query || '未指定'}`);
        break;
        
      case 'page_fetch_started':
        this.manager.log(this.taskId, `正在读取网页：${data.url ? shortenUrl(data.url) : '未知'}`);
        break;
        
      case 'page_fetch_completed':
        this.manager.log(this.taskId, `已读取 ${data.pageNumber || 1} 个网页`);
        break;
        
      case 'extraction_completed':
        this.manager.log(this.taskId, `已提取 ${data.itemCount || 0} 个数据项`);
        break;
        
      case 'comparison_started':
        this.manager.log(this.taskId, `正在比较 ${data.itemCount || 2} 个项目`);
        break;
        
      case 'output_generating':
        this.manager.log(this.taskId, '正在生成输出');
        break;
        
      case 'report_created':
        this.manager.log(this.taskId, `已生成报告：${data.pages || 1}页`);
        break;
        
      case 'task_completed':
        this.manager.event(this.taskId, 'task_completed');
        break;
        
      case 'task_failed':
        this.manager.event(this.taskId, 'task_failed', { reason: data.reason });
        break;
    }
  }

  /**
   * 检测阻塞
   */
  detectBlocker(normalizedEvent, rawData) {
    const { type, data } = normalizedEvent;
    const rule = BLOCKER_MAPPING[type];
    
    if (!rule) {
      return null;
    }
    
    // 处理函数型规则
    const blocker = typeof rule === 'function' ? rule(data) : rule;
    
    // 重试次数跟踪
    if (type === 'retry_failed') {
      const currentCount = this.retryCount.get(this.taskId) || 0;
      this.retryCount.set(this.taskId, currentCount + 1);
      
      // 只有重试≥3 次才报告阻塞
      if (currentCount + 1 < 3) {
        return null;
      }
    }
    
    return blocker;
  }

  /**
   * 处理阻塞
   */
  handleBlocker(blocker) {
    this.manager.block(this.taskId, blocker.type, blocker.reason, blocker.level);
  }

  /**
   * 检测是否需要 Ask Human
   */
  detectAskHuman(normalizedEvent, rawData) {
    const { type, data } = normalizedEvent;
    const rule = ASK_HUMAN_MAPPING[type];
    
    if (!rule) {
      return null;
    }
    
    // 处理函数型规则
    const askHuman = typeof rule === 'function' ? rule(data) : rule;
    
    return askHuman;
  }

  /**
   * 处理 Ask Human
   */
  handleAskHuman(askHuman) {
    this.manager.ask(this.taskId, askHuman.type, askHuman.question, askHuman.options);
  }

  /**
   * 用户已响应
   */
  userResponded() {
    this.manager.respond(this.taskId);
  }

  /**
   * 获取当前快照
   */
  getSnapshot(full = false) {
    if (full) {
      return this.manager.getFullView(this.taskId);
    }
    return this.manager.getDefaultView(this.taskId);
  }

  /**
   * 获取 JSON 状态
   */
  getStatusJSON(full = false) {
    return this.manager.getStatusJSON(this.taskId, full);
  }
}

// ==================== 便捷函数 ====================

/**
 * 创建 Research Agent Adapter
 */
function createResearchAdapter(taskId, taskTitle) {
  const { TaskVisibilityManager } = require('../index');
  const manager = new TaskVisibilityManager();
  const adapter = new ResearchAgentAdapter(manager);
  adapter.bindTask(taskId, taskTitle);
  return adapter;
}

// ==================== 导出 ====================

module.exports = {
  ResearchAgentAdapter,
  createResearchAdapter,
  EVENT_MAPPING,
  ACTION_TRANSLATIONS,
  BLOCKER_MAPPING,
  ASK_HUMAN_MAPPING
};
