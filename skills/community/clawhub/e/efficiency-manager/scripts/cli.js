#!/usr/bin/env node

/**
 * Efficiency Manager CLI
 * 
 * Usage:
 *   efficiency add "description" --category work --from 09:00 --to 11:00
 *   efficiency report today
 *   efficiency analyze work
 *   efficiency plan "写代码2h" "开会1h"
 *   efficiency list
 *   efficiency config
 */

const readline = require('readline');

const {
  initStorage,
  loadEvents,
  saveEvent,
  deleteEvent,
  deleteAllEvents,
  loadConfig,
  saveConfig,
  DEFAULT_CATEGORIES
} = require('../lib/storage');

const {
  generateReport,
  analyzeCategory,
  findBestTimeSlots
} = require('../lib/analyzer');

const {
  scheduleTasks,
  parseTaskString,
  estimateCategory,
  parseDuration
} = require('../lib/scheduler');

const {
  formatDailyReport,
  formatWeeklyReport,
  formatMonthlyReport,
  formatEventList,
  formatSchedule,
  getCategoryName
} = require('../lib/reporter');

// Simple UUID generator (no external dependency)
function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

// Get today's date in YYYY-MM-DD format
function getToday() {
  return new Date().toISOString().split('T')[0];
}

// Parse command line arguments
function parseArgs(args) {
  const result = {
    command: null,
    args: [],
    options: {}
  };
  
  let i = 0;
  while (i < args.length) {
    const arg = args[i];
    
    if (arg.startsWith('--')) {
      // Option
      const key = arg.slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith('--')) {
        result.options[key] = next;
        i += 2;
      } else {
        result.options[key] = true;
        i++;
      }
    } else if (!result.command) {
      result.command = arg;
      i++;
    } else {
      result.args.push(arg);
      i++;
    }
  }
  
  return result;
}

// Create readline interface
function createRL() {
  return readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
}

// Ask user a question
function ask(rl, question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer.trim());
    });
  });
}

// Format time for storage
function formatTimeForStorage(date, time) {
  return `${date}T${time}:00`;
}

// Command handlers
async function handleAdd(args, options) {
  initStorage();
  
  let description, category, startTime, endTime, notes;
  
  if (args.length > 0) {
    // Quick add mode: "写代码" --from 09:00 --to 11:00 --category work
    description = args.join(' ');
    
    if (options.from && options.to) {
      const date = options.date || getToday();
      startTime = formatTimeForStorage(date, options.from);
      endTime = formatTimeForStorage(date, options.to);
    }
    
    category = options.category || estimateCategory(description);
    notes = options.notes || '';
  } else {
    // Interactive mode
    const rl = createRL();
    
    description = await ask(rl, '事件描述: ');
    if (!description) {
      console.log('❌ 描述不能为空');
      return;
    }
    
    category = await ask(rl, `分类 (${Object.keys(DEFAULT_CATEGORIES).join(', ')}): `);
    if (!DEFAULT_CATEGORIES[category]) {
      category = estimateCategory(description);
      console.log(`  → 自动识别为: ${category} (${getCategoryName(category)})`);
    }
    
    const date = await ask(rl, `日期 (${getToday()}): `) || getToday();
    const from = await ask(rl, '开始时间 (HH:MM): ');
    const to = await ask(rl, '结束时间 (HH:MM): ');
    
    if (!from || !to) {
      console.log('❌ 开始和结束时间必填');
      return;
    }
    
    startTime = formatTimeForStorage(date, from);
    endTime = formatTimeForStorage(date, to);
    notes = await ask(rl, '备注 (可选): ');
    
    rl.close();
  }
  
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
  console.log(`✅ 已记录: [${getCategoryName(category)}] ${description}，耗时 ${Math.round(duration * 10) / 10}h`);
}

function handleReport(args, options) {
  initStorage();
  
  const type = args[0] || options.type || 'today';
  const dateArg = args[1] || options.date || null;
  
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
    console.log('用法: efficiency report [today|week|month] [日期]');
    return;
  }
  
  const report = generateReport(period, date);
  
  if (period === 'daily') {
    console.log(formatDailyReport(report));
  } else if (period === 'weekly') {
    console.log(formatWeeklyReport(report));
  } else {
    console.log(formatMonthlyReport(report));
  }
}

function handleAnalyze(args, options) {
  initStorage();
  
  const category = options.all ? null : (args[0] || 'work');
  
  if (category) {
    const analysis = analyzeCategory(category);
    console.log(`\n📊 ${getCategoryName(category)} 效率分析\n`);
    console.log(`  总次数: ${analysis.totalCount}`);
    console.log(`  总时长: ${analysis.totalDuration}h`);
    console.log(`  平均时长: ${analysis.avgDuration}h`);
    console.log(`  最佳时长: ${analysis.bestDuration}h`);
    console.log(`  最差时长: ${analysis.worstDuration}h`);
    console.log(`  完成率: ${analysis.completionRate}%`);
    console.log(`  效率得分: ${analysis.efficiency}%`);
  } else {
    const categories = Object.keys(DEFAULT_CATEGORIES);
    console.log('\n📊 全部分类效率分析\n');
    
    categories.forEach(cat => {
      const analysis = analyzeCategory(cat);
      if (analysis.totalCount > 0) {
        console.log(`  ${getCategoryName(cat)}: ${analysis.efficiency}% (${analysis.totalCount}次, 平均${analysis.avgDuration}h)`);
      }
    });
    
    const bestSlots = findBestTimeSlots(loadEvents());
    if (bestSlots.length > 0) {
      console.log('\n⭐ 最佳效率时段:');
      bestSlots.forEach(slot => {
        console.log(`  ${getCategoryName(slot.category)}: ${slot.slotName} (${slot.efficiency}%)`);
      });
    }
  }
}

function handlePlan(args, options) {
  initStorage();
  
  if (args.length === 0) {
    console.log('用法: efficiency plan "任务1" "任务2" ...');
    console.log('示例: efficiency plan "写代码2h" "开会1h" "健身1h"');
    return;
  }
  
  const tasks = args.map(a => parseTaskString(a));
  const result = scheduleTasks(tasks);
  
  console.log(formatSchedule(result));
}

function handleList(args, options) {
  initStorage();
  
  const query = {};
  
  if (options.category) {
    query.category = options.category;
  }
  
  if (options.date) {
    query.date = options.date;
  }
  
  const events = loadEvents(query);
  console.log('\n📋 事件列表\n');
  console.log(formatEventList(events));
}

function handleDelete(args, options) {
  initStorage();
  
  if (options.all) {
    const rl = createRL();
    rl.question('确认删除所有事件? (yes/no): ', async (answer) => {
      if (answer.toLowerCase() === 'yes') {
        deleteAllEvents();
        console.log('✅ 已删除所有事件');
      } else {
        console.log('❌ 已取消');
      }
      rl.close();
    });
    return;
  }
  
  const id = args[0];
  if (!id) {
    console.log('用法: efficiency delete <event-id> 或 efficiency delete --all');
    return;
  }
  
  const success = deleteEvent(id);
  if (success) {
    console.log('✅ 已删除事件');
  } else {
    console.log('❌ 事件不存在');
  }
}

async function handleStart(args, options) {
  initStorage();
  
  let description, category;
  
  if (args.length > 0) {
    description = args.join(' ');
    category = options.category || estimateCategory(description);
  } else {
    const rl = createRL();
    description = await ask(rl, '开始任务: ');
    if (!description) {
      console.log('❌ 任务描述不能为空');
      return;
    }
    category = await ask(rl, `分类 (${Object.keys(DEFAULT_CATEGORIES).join(', ')}): `) || estimateCategory(description);
    rl.close();
  }
  
  const now = new Date().toISOString();
  const event = saveEvent({
    id: uuidv4(),
    description,
    category,
    startTime: now,
    endTime: null, // Not set yet
    status: 'ongoing',
    notes: ''
  });
  
  const startTime = now.replace('T', ' ').slice(0, 16);
  console.log(`⏱️ 开始计时: [${getCategoryName(category)}] ${description}`);
  console.log(`   开始时间: ${startTime}`);
  console.log(`   ID: ${event.id}`);
  console.log(`   输入 "efficiency end ${event.id}" 或 "efficiency end ${description}" 完成任务`);
}

function handleEnd(args, options) {
  initStorage();
  
  if (args.length === 0) {
    // List ongoing events
    const events = loadEvents().filter(e => e.status === 'ongoing');
    if (events.length === 0) {
      console.log('没有进行中的任务');
      return;
    }
    console.log('\n⏳ 进行中的任务:\n');
    events.forEach(e => {
      const start = e.startTime.replace('T', ' ').slice(0, 16);
      console.log(`  ID: ${e.id}`);
      console.log(`  任务: ${e.description}`);
      console.log(`  开始: ${start}`);
      console.log(`  分类: ${getCategoryName(e.category)}\n`);
    });
    console.log('用法: efficiency end <任务描述或ID>');
    return;
  }
  
  const query = args.join(' ');
  const events = loadEvents().filter(e => e.status === 'ongoing');
  
  // Try to find by ID first
  let event = events.find(e => e.id === query);
  
  // Try to find by description (partial match)
  if (!event) {
    event = events.find(e => e.description.toLowerCase().includes(query.toLowerCase()));
  }
  
  // If still not found, show suggestions
  if (!event) {
    console.log(`未找到任务: "${query}"`);
    console.log('\n进行中的任务:');
    events.forEach(e => {
      console.log(`  - ${e.description} (ID: ${e.id})`);
    });
    return;
  }
  
  // End the event
  const now = new Date().toISOString();
  event = saveEvent({
    ...event,
    endTime: now,
    status: 'completed'
  });
  
  const duration = (new Date(event.endTime) - new Date(event.startTime)) / (1000 * 60);
  const startTime = event.startTime.replace('T', ' ').slice(0, 16);
  const endTime = event.endTime.replace('T', ' ').slice(0, 16);
  
  console.log(`✅ 任务完成: ${event.description}`);
  console.log(`   分类: ${getCategoryName(event.category)}`);
  console.log(`   开始: ${startTime}`);
  console.log(`   结束: ${endTime}`);
  console.log(`   耗时: ${Math.round(duration)} 分钟`);
}

function handleConfig(args, options) {
  initStorage();
  const config = loadConfig();
  
  if (options.set && args.length >= 1) {
    const key = options.set;
    const value = args[0];
    
    config[key] = value;
    saveConfig(config);
    console.log(`✅ 已设置 ${key} = ${value}`);
    return;
  }
  
  if (args[0] && args[1]) {
    // "config set key value" format
    config[args[0]] = args[1];
    saveConfig(config);
    console.log(`✅ 已设置 ${args[0]} = ${args[1]}`);
    return;
  }
  
  // Show config
  console.log('\n⚙️ 当前配置\n');
  console.log(`  dayStartTime: ${config.dayStartTime}`);
  console.log(`  dayEndTime: ${config.dayEndTime}`);
  console.log(`  reportTime: ${config.reportTime}`);
  console.log(`  benchmarkSource: ${config.benchmarkSource}`);
}

// Main entry point
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
📦 Efficiency Manager v1.0.0

用法:
  efficiency add "描述" --from 09:00 --to 11:00 --category work
  efficiency start "任务描述" [--category work]    # 开始计时
  efficiency end "任务描述" 或 "任务ID"             # 结束计时
  efficiency report [today|week|month] [日期]
  efficiency analyze [category|--all]
  efficiency plan "任务1" "任务2" ...
  efficiency list [--category work] [--date 2026-03-21]
  efficiency delete <event-id>
  efficiency config [show|set key value]

示例:
  efficiency add "写代码" --from 09:00 --to 11:00 --category work
  efficiency start "写代码"
  efficiency end "写代码"
  efficiency report today
  efficiency analyze work
  efficiency plan "写代码2h" "开会1h" "健身1h"
`);
    return;
  }
  
  const parsed = parseArgs(args);
  const command = parsed.command;
  const cmdArgs = parsed.args;
  const options = parsed.options;
  
  try {
    switch (command) {
      case 'add':
        await handleAdd(cmdArgs, options);
        break;
      case 'start':
        await handleStart(cmdArgs, options);
        break;
      case 'end':
        handleEnd(cmdArgs, options);
        break;
      case 'report':
        handleReport(cmdArgs, options);
        break;
      case 'analyze':
        handleAnalyze(cmdArgs, options);
        break;
      case 'plan':
        handlePlan(cmdArgs, options);
        break;
      case 'list':
        handleList(cmdArgs, options);
        break;
      case 'delete':
      case 'del':
        handleDelete(cmdArgs, options);
        break;
      case 'config':
        handleConfig(cmdArgs, options);
        break;
      default:
        console.log(`❌ 未知命令: ${command}`);
        console.log('运行 efficiency 查看帮助');
    }
  } catch (e) {
    console.error('❌ 错误:', e.message);
  }
}

main();
