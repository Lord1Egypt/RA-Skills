/**
 * Smart Action Logger (V2)
 * 
 * 动态文案引擎
 * 
 * 优先级逻辑：
 * 1. 优先使用最新 action_log（具体动作）
 * 2. 若无动作，显示 phase_name（抽象阶段）
 * 3. Next-Step Predictor：为 Research 5 阶段预设默认下一步文案
 */

const { PHASE_STATUS } = require('../src/schema');

// ==================== Next-Step 预设文案 ====================

/**
 * Research 5 阶段的默认下一步文案
 */
const NEXT_STEP_TEMPLATES = {
  '理解任务': [
    '明确搜索关键词和数据源',
    '确认任务目标和范围',
    '识别关键信息需求'
  ],
  '制定搜索计划': [
    '确定关键词和优先级',
    '选择主要数据源',
    '设计搜索策略'
  ],
  '收集信息': [
    '继续抓取网页数据',
    '提取关键信息',
    '整理收集的数据'
  ],
  '分析与比较': [
    '交叉验证信息来源',
    '对比关键差异',
    '识别模式和趋势'
  ],
  '形成输出': [
    '生成结论摘要',
    '格式化输出报告',
    '完成最终审核'
  ]
};

/**
 * 根据阶段和进度智能选择下一步文案
 */
function predictNextStep(phaseName, phaseProgress = 0) {
  const templates = NEXT_STEP_TEMPLATES[phaseName];
  if (!templates || templates.length === 0) {
    return '继续执行当前阶段';
  }
  
  // 根据进度选择不同文案
  if (phaseProgress < 30) {
    return templates[0];  // 早期
  } else if (phaseProgress < 70) {
    return templates[1] || templates[0];  // 中期
  } else {
    return templates[2] || templates[templates.length - 1];  // 后期
  }
}

// ==================== 文案质量检查 ====================

/**
 * 检查文案是否太空
 */
function isTooVague(text) {
  if (!text) return true;
  
  const vaguePatterns = [
    /^正在处理/,
    /^执行中/,
    /^继续/,
    /^进行中/,
    /^处理中/
  ];
  
  return vaguePatterns.some(pattern => pattern.test(text));
}

/**
 * 检查文案是否太技术
 */
function isTooTechnical(text) {
  if (!text) return false;
  
  const technicalPatterns = [
    /timeout/i,
    /event\s*queue/i,
    /parser\s*fallback/i,
    /span\s*\d+/i,
    /error\s*code/i,
    /http\s*\d+/i,
    /\b(api|rpc|grpc|tcp|ip)\b/i
  ];
  
  return technicalPatterns.some(pattern => pattern.test(text));
}

/**
 * 将技术文案翻译为用户语言
 */
function translateTechnicalToHuman(text) {
  const translations = {
    'timeout': '请求超时',
    'event queue blocked': '处理队列等待中',
    'parser fallback triggered': '备用解析方案已启动',
    '401': '需要登录授权',
    '403': '权限不足',
    '404': '页面不存在',
    '429': '请求过于频繁',
    '500': '服务器内部错误',
    '502': '网关错误',
    '503': '服务暂时不可用'
  };
  
  let result = text;
  for (const [tech, human] of Object.entries(translations)) {
    result = result.replace(new RegExp(tech, 'gi'), human);
  }
  
  return result;
}

// ==================== 智能动作日志 ====================

class SmartActionLogger {
  constructor() {
    this.logs = new Map();  // taskId -> [logs]
    this.maxLogsPerTask = 10;
  }

  /**
   * 添加动作日志
   */
  add(taskId, message, level = 'info', metadata = null) {
    if (!this.logs.has(taskId)) {
      this.logs.set(taskId, []);
    }
    
    const log = {
      timestamp: new Date().toISOString(),
      message: message,
      level: level,
      metadata: metadata
    };
    
    this.logs.get(taskId).unshift(log);
    
    // 保持最多 maxLogsPerTask 条
    if (this.logs.get(taskId).length > this.maxLogsPerTask) {
      this.logs.get(taskId).pop();
    }
    
    return log;
  }

  /**
   * 获取最新动作（用于"当前在做什么"）
   */
  getLatestAction(taskId, fallbackToPhase = true) {
    const taskLogs = this.logs.get(taskId);
    
    if (!taskLogs || taskLogs.length === 0) {
      return null;
    }
    
    // 返回最新日志
    return taskLogs[0].message;
  }

  /**
   * 获取最近动作列表（用于展开视图）
   */
  getRecentActions(taskId, limit = 5) {
    const taskLogs = this.logs.get(taskId);
    
    if (!taskLogs) {
      return [];
    }
    
    return taskLogs.slice(0, limit).map(log => ({
      timestamp: log.timestamp,
      message: log.message,
      level: log.level
    }));
  }

  /**
   * 清空日志
   */
  clear(taskId) {
    if (taskId) {
      this.logs.delete(taskId);
    } else {
      this.logs.clear();
    }
  }
}

// ==================== 文案生成器 ====================

class ActionTextGenerator {
  constructor(smartLogger) {
    this.logger = smartLogger || new SmartActionLogger();
  }

  /**
   * 生成"当前在做什么"文案
   * 
   * 优先级：
   * 1. 最新 action_log（具体动作）
   * 2. phase_name + 进度（抽象阶段）
   * 3. 默认文案
   */
  getCurrentAction(taskId, currentPhase = null, phaseProgress = 0) {
    // 1. 优先使用最新 action_log
    const latestAction = this.logger.getLatestAction(taskId);
    if (latestAction && !isTooVague(latestAction)) {
      return latestAction;
    }
    
    // 2. 使用阶段名 + 进度
    if (currentPhase) {
      const progressText = phaseProgress > 0 ? ` (${phaseProgress}%)` : '';
      return `正在进行：${currentPhase}${progressText}`;
    }
    
    // 3. 默认文案
    return '准备中...';
  }

  /**
   * 生成"为什么还没完成"文案
   */
  getWhyNotDone(taskId, blockerStatus = null, currentPhase = null) {
    // 如果有阻塞
    if (blockerStatus && blockerStatus.hasBlocker) {
      if (blockerStatus.state === 'waiting') {
        return `等待响应中（已${blockerStatus.durationText}）`;
      } else if (blockerStatus.state === 'blocked') {
        return `${blockerStatus.reason}（已${blockerStatus.durationText}）`;
      }
    }
    
    // 正常执行中
    if (currentPhase) {
      return '任务正在正常执行中';
    }
    
    return '任务正在处理中';
  }

  /**
   * 生成"下一步"文案
   */
  getNextAction(taskId, currentPhase = null, phaseProgress = 0, customNextAction = null) {
    // 1. 优先使用自定义 next_action
    if (customNextAction && !isTooVague(customNextAction)) {
      return customNextAction;
    }
    
    // 2. 使用预设模板
    if (currentPhase) {
      return predictNextStep(currentPhase, phaseProgress);
    }
    
    // 3. 默认文案
    return '继续执行';
  }

  /**
   * 生成健康度指示器
   */
  getHealthIndicator(healthScore) {
    if (healthScore >= 80) {
      return { icon: '🟢', text: '健康', color: 'green' };
    } else if (healthScore >= 60) {
      return { icon: '🟡', text: '轻微延迟', color: 'yellow' };
    } else if (healthScore >= 40) {
      return { icon: '🟠', text: '注意', color: 'orange' };
    } else {
      return { icon: '🔴', text: '严重阻塞', color: 'red' };
    }
  }

  /**
   * 生成状态图标
   */
  getStatusIcon(status, needsUserInput = false, hasBlocker = false) {
    if (needsUserInput) {
      return '⚠️';
    }
    
    if (hasBlocker) {
      return '🔴';
    }
    
    switch (status) {
      case 'completed':
        return '✅';
      case 'failed':
        return '❌';
      case 'blocked':
        return '🔴';
      case 'waiting':
        return '🟡';
      case 'running':
        return '🟢';
      default:
        return '⚪';
    }
  }
}

// ==================== 导出 ====================

module.exports = {
  NEXT_STEP_TEMPLATES,
  predictNextStep,
  isTooVague,
  isTooTechnical,
  translateTechnicalToHuman,
  SmartActionLogger,
  ActionTextGenerator
};
