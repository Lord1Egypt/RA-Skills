#!/usr/bin/env node

/**
 * 飞书任务处理器 - 增强版
 * 处理单个任务并发送进度反馈
 * 
 * 功能：
 * - 智能任务解析
 * - 错误容错处理
 * - 自动重试机制
 * - 详细日志记录
 * 
 * 用法：node process_task.js "<任务文本>" <taskId> <messageId>
 */

const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);
const path = require('path');
const fs = require('fs');

// ============ 配置 ============
const CONFIG = {
  // 最大重试次数
  maxRetries: parseInt(process.env.FEISHU_MAX_RETRIES) || 3,
  
  // 重试延迟（毫秒）
  retryDelay: parseInt(process.env.FEISHU_RETRY_DELAY) || 1000,
  
  // 子任务处理延迟（毫秒）
  taskDelay: parseInt(process.env.FEISHU_TASK_DELAY) || 500,
  
  // 是否启用详细日志
  verbose: process.env.FEISHU_VERBOSE === 'true',
  
  // 日志文件路径
  logFile: path.join(__dirname, '..', '.tasks.log')
};

// ============ 参数解析 ============
const taskText = process.argv[2] || '';
const taskId = process.argv[3] || `task_${Date.now()}`;
const messageId = process.argv[4] || 'unknown';

if (!taskText) {
  console.error('❌ 缺少任务文本');
  console.error('用法：node process_task.js "<任务文本>" <taskId> <messageId>');
  process.exit(1);
}

// ============ 工具函数 ============

/**
 * 日志记录
 */
function log(level, message, data = null) {
  const timestamp = new Date().toISOString();
  const logEntry = `[${timestamp}] [Task #${taskId}] [${level.toUpperCase()}] ${message}${data ? ' ' + JSON.stringify(data) : ''}`;
  console.log(logEntry);
  
  try {
    fs.appendFileSync(CONFIG.logFile, logEntry + '\n');
  } catch (error) {
    // 忽略日志写入错误
  }
}

/**
 * 延迟函数
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 发送飞书反馈消息（带重试）
 */
async function sendFeedback(message, retryCount = 0) {
  try {
    // 转义特殊字符
    const escaped = message
      .replace(/\\/g, '\\\\')
      .replace(/"/g, '\\"')
      .replace(/\n/g, '\\n')
      .replace(/\r/g, '');
    
    const cmd = `openclaw message send --channel feishu --message "${escaped}"`;
    await execAsync(cmd);
    log('info', '发送反馈', { messageLength: message.length });
    return true;
  } catch (error) {
    if (retryCount < CONFIG.maxRetries) {
      log('warn', `发送失败，重试 ${retryCount + 1}/${CONFIG.maxRetries}`, { error: error.message });
      await sleep(CONFIG.retryDelay * (retryCount + 1));
      return sendFeedback(message, retryCount + 1);
    }
    log('error', '发送反馈失败（已达最大重试次数）', { error: error.message });
    return false;
  }
}

/**
 * 安全执行子任务（带错误处理）
 */
async function safeExecute(handler, fallback = null) {
  try {
    return await handler();
  } catch (error) {
    log('error', '执行失败', { error: error.message });
    if (fallback) {
      return fallback(error);
    }
    throw error;
  }
}

// ============ 任务解析 ============

/**
 * 智能任务解析器
 * 识别不同类型的任务结构
 */
function parseTask(text) {
  const lines = text.split('\n').filter(line => line.trim());
  
  if (lines.length === 0) {
    return {
      mainTask: text,
      subtasks: [text],
      type: 'simple'
    };
  }
  
  // 识别带编号/符号的子任务
  const numberedPattern = /^[\d]+[\.\)]\s*/;
  const dashPattern = /^[-–—•*]\s*/;
  const letterPattern = /^[A-Z][\.\)]\s*/;
  
  const subtasks = lines.filter(line => 
    numberedPattern.test(line) || 
    dashPattern.test(line) ||
    letterPattern.test(line)
  );
  
  // 识别任务类型
  let type = 'simple';
  const lowerText = text.toLowerCase();
  
  if (lowerText.includes('创建') || lowerText.includes('build') || lowerText.includes('create')) {
    type = 'create';
  } else if (lowerText.includes('分析') || lowerText.includes('analyze')) {
    type = 'analyze';
  } else if (lowerText.includes('计算') || lowerText.includes('calculate')) {
    type = 'calculate';
  } else if (lowerText.includes('查询') || lowerText.includes('search') || lowerText.includes('find')) {
    type = 'query';
  }
  
  return {
    mainTask: lines[0] || text,
    subtasks: subtasks.length > 0 ? subtasks : lines,
    type,
    metadata: {
      lineCount: lines.length,
      charCount: text.length,
      estimatedDuration: lines.length * CONFIG.taskDelay
    }
  };
}

/**
 * 根据任务类型生成处理策略
 */
function getTaskStrategy(type) {
  const strategies = {
    create: {
      steps: ['设计结构', '创建内容', '验证输出'],
      icon: '🛠️'
    },
    analyze: {
      steps: ['收集数据', '分析处理', '生成结论'],
      icon: '🔍'
    },
    calculate: {
      steps: ['准备数据', '执行计算', '验证结果'],
      icon: '🧮'
    },
    query: {
      steps: ['构建查询', '执行搜索', '整理结果'],
      icon: '🔎'
    },
    simple: {
      steps: ['处理任务'],
      icon: '⚙️'
    }
  };
  
  return strategies[type] || strategies.simple;
}

// ============ 任务执行 ============

/**
 * 执行单个子任务
 * 此处应集成具体业务逻辑或大模型 API
 */
async function executeSubtask(subtask, index, total) {
  log('info', `执行子任务 ${index + 1}/${total}`, { subtask: subtask.substring(0, 50) });
  
  // 模拟处理延迟（实际应替换为真实逻辑）
  await sleep(CONFIG.taskDelay);
  
  // TODO: 集成具体处理逻辑
  // 示例：根据任务类型调用不同的处理器
  // - 创建类任务：调用文件生成 API
  // - 分析类任务：调用大模型分析
  // - 计算类任务：执行计算逻辑
  // - 查询类任务：调用搜索 API
  
  return { success: true, index };
}

/**
 * 处理任务主流程
 */
async function processTask() {
  const startTime = Date.now();
  
  log('info', '开始处理任务', { 
    taskId, 
    messageId, 
    taskPreview: taskText.substring(0, 100) 
  });
  
  try {
    // 解析任务
    const parsed = parseTask(taskText);
    const total = parsed.subtasks.length;
    const strategy = getTaskStrategy(parsed.type);
    
    log('info', '任务解析完成', { 
      type: parsed.type, 
      subtasks: total,
      estimatedDuration: parsed.metadata.estimatedDuration 
    });
    
    // 发送开始反馈
    await sendFeedback(
      `📋 任务收到，开始处理...\n` +
      `任务 ID: #${taskId}\n` +
      `类型：${strategy.icon} ${parsed.type}\n` +
      `共 ${total} 个子任务\n` +
      `主任务：${parsed.mainTask.substring(0, 60)}${parsed.mainTask.length > 60 ? '...' : ''}`
    );
    
    // 处理每个子任务
    const results = [];
    let successCount = 0;
    let failCount = 0;
    
    for (let i = 0; i < total; i++) {
      const progress = Math.round(((i + 1) / total) * 100);
      const subtask = parsed.subtasks[i];
      const preview = subtask.replace(/^[\d\-\*•]+[\.\)]\s*/, '').substring(0, 50);
      
      // 发送开始处理反馈
      await sendFeedback(`⏳ 进度 ${progress}% - 正在处理：${preview}...`);
      
      // 执行子任务（带错误处理）
      const result = await safeExecute(
        () => executeSubtask(subtask, i, total),
        (error) => ({ success: false, index: i, error: error.message })
      );
      
      results.push(result);
      
      if (result.success) {
        successCount++;
        await sendFeedback(`✅ 完成 ${progress}% - ${preview}...`);
      } else {
        failCount++;
        await sendFeedback(`⚠️ 失败 ${progress}% - ${preview}: ${result.error}`);
      }
    }
    
    // 计算执行时间
    const duration = ((Date.now() - startTime) / 1000).toFixed(2);
    
    // 发送完成通知
    const statusIcon = failCount === 0 ? '🎉' : '⚠️';
    const statusText = failCount === 0 ? '全部完成' : `完成 ${successCount}/${total}`;
    
    await sendFeedback(
      `${statusIcon} 任务完成！\n` +
      `任务 ID: #${taskId}\n` +
      `状态：${statusText}\n` +
      `成功：${successCount} | 失败：${failCount}\n` +
      `耗时：${duration}秒\n` +
      `进度：100%`
    );
    
    log('info', '任务处理完成', { 
      duration, 
      success: successCount, 
      fail: failCount 
    });
    
    // 返回结果
    return {
      taskId,
      success: failCount === 0,
      successCount,
      failCount,
      total,
      duration: parseFloat(duration),
      results
    };
    
  } catch (error) {
    log('error', '任务处理异常', { error: error.message, stack: error.stack });
    
    await sendFeedback(
      `❌ 任务处理失败\n` +
      `任务 ID: #${taskId}\n` +
      `错误：${error.message}\n` +
      `请联系管理员或重试`
    );
    
    process.exit(1);
  }
}

// ============ 启动执行 ============

log('info', '任务处理器启动', { 
  taskId, 
  argv: process.argv.slice(2).join(' ') 
});

processTask()
  .then(result => {
    log('info', '处理器退出', { success: result.success });
    process.exit(result.success ? 0 : 1);
  })
  .catch(error => {
    log('error', '处理器异常退出', { error: error.message });
    process.exit(1);
  });
