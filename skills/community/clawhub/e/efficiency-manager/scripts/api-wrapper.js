#!/usr/bin/env node
/**
 * Efficiency Manager API Wrapper
 * 
 * 提供可直接调用的 programmatic API，供 agent 通过 exec 调用
 * 复用 lib/storage.js, lib/analyzer.js, lib/reporter.js
 * 
 * 用法: node api-wrapper.js <action> [params...]
 * 
 * 首批暴露接口: add, report, list
 * 内部保留但不暴露: delete, config, analyze
 */

const path = require('path');

// 设置正确的 working directory 以找到 lib 模块
const SKILL_DIR = path.dirname(path.dirname(__filename));
process.chdir(SKILL_DIR);

const {
  initStorage,
  loadEvents,
  saveEvent,
  deleteEvent,
  loadConfig,
  saveConfig,
  getEventsByDateRange
} = require('../lib/storage');

const {
  generateReport,
  analyzeCategory,
  findBestTimeSlots
} = require('../lib/analyzer');

const {
  formatDailyReport,
  formatWeeklyReport,
  formatMonthlyReport,
  formatEventList
} = require('../lib/reporter');

// Simple UUID generator
function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

function getToday() {
  return new Date().toISOString().split('T')[0];
}

function formatTimeForStorage(date, time) {
  return `${date}T${time}:00`;
}

// 自动识别分类
function estimateCategory(description) {
  const desc = description.toLowerCase();
  if (desc.includes('代码') || desc.includes('code') || desc.includes('开发') || desc.includes('program')) return 'work';
  if (desc.includes('书') || desc.includes('学习') || desc.includes('study') || desc.includes('read')) return 'study';
  if (desc.includes('运动') || desc.includes('健身') || desc.includes('exercise') || desc.includes('gym')) return 'exercise';
  if (desc.includes('休息') || desc.includes('睡觉') || desc.includes('rest') || desc.includes('sleep')) return 'rest';
  if (desc.includes('娱乐') || desc.includes('游戏') || desc.includes('entertainment') || desc.includes('game')) return 'entertainment';
  if (desc.includes('家务') || desc.includes('打扫') || desc.includes('chores') || desc.includes('clean')) return 'chores';
  if (desc.includes('社交') || desc.includes('朋友') || desc.includes('social') || desc.includes('friend')) return 'social';
  return 'other';
}

// 输出 JSON 结果
function outputJSON(data) {
  console.log(JSON.stringify(data, null, 2));
}

// 输出错误
function outputError(message) {
  console.error(JSON.stringify({ error: message }));
  process.exit(1);
}

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const action = args[0];
  const params = {};
  
  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith('--')) {
        params[key] = next;
        i++;
      } else {
        params[key] = true;
      }
    } else if (arg.startsWith('-') && arg.length === 2) {
      const key = arg.slice(1);
      const next = args[i + 1];
      if (next && !next.startsWith('-')) {
        params[key] = next;
        i++;
      } else {
        params[key] = true;
      }
    }
  }
  
  return { action, params };
}

// ==================== Actions (首批暴露) ====================

// add: 添加事件
function actionAdd(params) {
  initStorage();
  
  const description = params.description || params.d;
  if (!description) {
    outputError('Missing required parameter: description (or -d)');
  }
  
  const category = params.category || params.c || estimateCategory(description);
  const date = params.date || getToday();
  const from = params.from || params.start;
  const to = params.to || params.end;
  const notes = params.notes || params.n || '';
  
  if (!from || !to) {
    outputError('Missing required parameter: from/start and to/end times (HH:MM format)');
  }
  
  const startTime = formatTimeForStorage(date, from);
  const endTime = formatTimeForStorage(date, to);
  
  const event = saveEvent({
    id: uuidv4(),
    description,
    category,
    startTime,
    endTime,
    status: 'completed',
    notes
  });
  
  const duration = (new Date(event.endTime) - new Date(event.startTime)) / (1000 * 60 * 60);
  
  outputJSON({
    success: true,
    action: 'add',
    event: {
      id: event.id,
      description: event.description,
      category: event.category,
      startTime: event.startTime,
      endTime: event.endTime,
      duration: Math.round(duration * 10) / 10,
      notes: event.notes
    }
  });
}

// report: 生成报告
function actionReport(params) {
  initStorage();
  
  const type = params.type || params.t || 'today';
  const dateArg = params.date || null;
  
  let period, date;
  
  if (type === 'today') {
    period = 'daily';
    date = getToday();
  } else if (type === 'week' || type === 'weekly') {
    period = 'weekly';
    date = dateArg || getToday();
  } else if (type === 'month' || type === 'monthly') {
    period = 'monthly';
    date = dateArg || getToday().slice(0, 7);
  } else if (type.match(/^\d{4}-\d{2}-\d{2}$/)) {
    period = 'daily';
    date = type;
  } else {
    outputError('Invalid report type. Use: today, week, month, or YYYY-MM-DD');
  }
  
  const report = generateReport(period, date);
  
  // 同时返回结构化数据和格式化文本
  let formatted;
  if (period === 'daily') {
    formatted = formatDailyReport(report);
  } else if (period === 'weekly') {
    formatted = formatWeeklyReport(report);
  } else {
    formatted = formatMonthlyReport(report);
  }
  
  outputJSON({
    success: true,
    action: 'report',
    period,
    date,
    summary: report.summary,
    categoryBreakdown: report.categoryBreakdown,
    bestTimeSlots: report.bestTimeSlots,
    suggestions: report.suggestions,
    formatted
  });
}

// list: 列出事件（已修复旧数据兼容性）
function actionList(params) {
  initStorage();
  
  const query = {};
  if (params.category || params.c) query.category = params.category || params.c;
  if (params.date || params.d) query.date = params.date || params.d;
  if (params.startDate) query.startDate = params.startDate;
  if (params.endDate) query.endDate = params.endDate;
  
  const events = loadEvents(query);
  const formatted = formatEventList(events);
  
  outputJSON({
    success: true,
    action: 'list',
    count: events.length,
    events: events.slice(0, 50), // 限制返回数量
    formatted
  });
}

// ==================== Actions (内部保留，不暴露) ====================

// analyze: 分析效率（内部保留，不暴露给外部入口）
function actionAnalyze(params) {
  initStorage();
  
  const category = params.category || params.c;
  
  if (category) {
    const analysis = analyzeCategory(category);
    outputJSON({
      success: true,
      action: 'analyze',
      category,
      analysis
    });
  } else {
    // 分析所有分类
    const allEvents = loadEvents();
    const categories = [...new Set(allEvents.map(e => e.category))];
    const analyses = categories.map(cat => analyzeCategory(cat));
    const bestSlots = findBestTimeSlots(allEvents);
    
    outputJSON({
      success: true,
      action: 'analyze',
      scope: 'all',
      categories: analyses,
      bestTimeSlots: bestSlots
    });
  }
}

// delete: 删除事件（内部保留，不暴露给外部入口）
function actionDelete(params) {
  initStorage();
  
  const id = params.id || params.i;
  if (!id) {
    outputError('Missing required parameter: id (or -i)');
  }
  
  const success = deleteEvent(id);
  outputJSON({
    success,
    action: 'delete',
    id,
    message: success ? 'Event deleted' : 'Event not found'
  });
}

// config: 获取/设置配置（内部保留，不暴露给外部入口）
function actionConfig(params) {
  initStorage();
  
  if (params.set && params.value) {
    const config = loadConfig();
    config[params.set] = params.value;
    saveConfig(config);
    outputJSON({
      success: true,
      action: 'config',
      set: params.set,
      value: params.value
    });
  } else {
    const config = loadConfig();
    outputJSON({
      success: true,
      action: 'config',
      config
    });
  }
}

// ==================== Main ====================

const { action, params } = parseArgs();

// 首批暴露的接口列表
const EXPOSED_ACTIONS = ['add', 'report', 'list'];
// 内部保留但不暴露的接口
const INTERNAL_ACTIONS = ['analyze', 'delete', 'config'];

if (!action) {
  console.log(`
Efficiency Manager API Wrapper

Usage: efficiency-api <action> [options]

首批暴露接口 (Exposed):
  add       Add a new event
            --description, -d    Event description
            --category, -c       Category (work/study/exercise/etc)
            --from, --start      Start time (HH:MM)
            --to, --end          End time (HH:MM)
            --date               Date (YYYY-MM-DD, default: today)
            --notes, -n          Optional notes

  report    Generate efficiency report
            --type, -t           Report type: today/week/month/YYYY-MM-DD
            --date               Specific date for weekly/monthly

  list      List events
            --category, -c       Filter by category
            --date, -d           Filter by date
            --startDate          Start date for range
            --endDate            End date for range

内部保留接口 (Internal only):
  analyze   Analyze efficiency (not exposed)
  delete    Delete an event (not exposed)
  config    Get/set configuration (not exposed)

Examples:
  efficiency-api add -d "写代码" -c work --from 09:00 --to 11:00
  efficiency-api report -t today
  efficiency-api list --category work --date 2026-03-25
`);
  process.exit(0);
}

// 检查是否是首批暴露的接口
if (EXPOSED_ACTIONS.includes(action)) {
  switch (action) {
    case 'add':
      actionAdd(params);
      break;
    case 'report':
      actionReport(params);
      break;
    case 'list':
      actionList(params);
      break;
  }
} else if (INTERNAL_ACTIONS.includes(action)) {
  // 内部接口可以通过直接调用 api-wrapper.js 使用，但不暴露给 efficiency-api
  switch (action) {
    case 'analyze':
      actionAnalyze(params);
      break;
    case 'delete':
      actionDelete(params);
      break;
    case 'config':
      actionConfig(params);
      break;
  }
} else {
  outputError(`Unknown action: ${action}. Available: ${EXPOSED_ACTIONS.join(', ')}`);
}
