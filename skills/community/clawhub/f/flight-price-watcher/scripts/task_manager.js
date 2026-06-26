#!/usr/bin/env node

/**
 * Flight Price Watcher v2.2.2 - 任务管理脚本
 * 
 * v2.2.2 新增：
 * 1. 输入验证（防止命令注入）
 * 2. 环境变量配置
 * 3. 创建成功发送确认消息
 * 
 * v2.1 新增：
 * 1. 用户自定义选择航班
 * 2. 完整航班信息（起飞/到达/机场）
 * 3. 智能推荐标识（⭐早班/🌙晚班/💰低价/⏱️短时）
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

/**
 * 清理和验证用户输入（防止命令注入）
 * 只允许字母、数字、中文、连字符、空格
 */
function sanitizeInput(input, maxLength = 50) {
  if (typeof input !== 'string') return '';
  // 移除所有非安全字符（只保留字母、数字、中文、连字符、空格、点）
  const sanitized = input.replace(/[^\u4e00-\u9fa5a-zA-Z0-9\-.\s]/g, '');
  // 限制长度
  return sanitized.substring(0, maxLength);
}

/**
 * 验证日期格式（YYYY-MM-DD）
 */
function isValidDate(dateStr) {
  return /^\d{4}-\d{2}-\d{2}$/.test(dateStr);
}

/**
 * 验证城市名（只允许字母、数字、中文）
 */
function isValidCity(city) {
  return /^[\u4e00-\u9fa5a-zA-Z]+$/.test(city);
}

// 配置
const CONFIG = {
  thresholdPercent: 10,
  thresholdAmount: 200,
  checkFrequency: 'daily',
  checkTime: '09:00',
  defaultMonitorDays: 7,
  maxMonitoredFlights: 3,  // 最多监控 3 个航班
};

// 数据文件路径
const DATA_FILE = new URL('../data/tasks.json', import.meta.url).pathname;

/**
 * 读取任务数据
 */
function loadTasks() {
  if (!existsSync(DATA_FILE)) {
    return { tasks: [], nextTaskId: 1 };
  }
  const content = readFileSync(DATA_FILE, 'utf-8');
  return JSON.parse(content);
}

/**
 * 保存任务数据
 */
function saveTasks(data) {
  writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf-8');
}

/**
 * 调用 FlyAI CLI 获取航班列表（带输入验证）
 */
async function fetchFlights(from, to, date, flightType = 'all') {
  try {
    // 清理和验证用户输入（防止命令注入）
    const safeFrom = sanitizeInput(from, 20);
    const safeTo = sanitizeInput(to, 20);
    const safeDate = isValidDate(date) ? date : '2026-01-01';
    
    if (!isValidCity(safeFrom) || !isValidCity(safeTo)) {
      throw new Error('Invalid city name');
    }
    
    const typeFlag = flightType === 'direct' ? '--journey-type 1' : '';
    // 使用清理后的安全输入构建命令
    const cmd = `flyai search-flight --origin "${safeFrom}" --destination "${safeTo}" --dep-date ${safeDate} ${typeFlag}`;
    
    const { stdout } = await execAsync(cmd);
    const result = JSON.parse(stdout);
    
    const itemList = result.data?.itemList || [];
    
    // 转换为统一格式
    const flights = itemList.map(item => {
      const segment = item.segments?.[0] || {};
      const depTime = segment.depDateTime?.split(' ') || ['', ''];
      const arrTime = segment.arrDateTime?.split(' ') || ['', ''];
      
      // 智能推荐标识
      const tags = [];
      const depHour = parseInt(depTime[1]?.split(':')[0] || '12');
      if (depHour < 12) tags.push('⭐早班');
      if (depHour >= 20) tags.push('🌙晚班');
      
      return {
        price: parseFloat(item.ticketPrice) || 0,
        flightNo: segment.marketingTransportNo || '',
        airline: segment.marketingTransportName || '',
        departure: depTime[1] || '',
        arrival: arrTime[1] || '',
        depStation: segment.depStationShortName || segment.depStationName || '',
        arrStation: segment.arrStationShortName || segment.arrStationName || '',
        duration: item.totalDuration || '',
        jumpUrl: item.jumpUrl || '',
        tags,
      };
    });
    
    return { success: true, flights };
  } catch (error) {
    console.error('获取航班失败:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * 展示航班列表供用户选择
 */
function showFlightSelection(flights) {
  console.log('\n=== 选择要监控的航班 ===\n');
  
  // 找出不加标识的航班
  const minPrice = Math.min(...flights.map(f => f.price));
  const minDuration = Math.min(...flights.map(f => parseInt(f.duration) || 9999));
  
  flights.forEach((f, i) => {
    const tags = [...f.tags];
    if (f.price === minPrice) tags.push('💰低价');
    if (parseInt(f.duration) === minDuration) tags.push('⏱️短时');
    const tagStr = tags.length > 0 ? ' | ' + tags.join(' ') : '';
    
    console.log(`${i + 1}. ¥${f.price} ${f.airline}${f.flightNo} | ${f.departure} ${f.depStation}→${f.arrival} ${f.arrStation} | ${f.duration}分钟${tagStr}`);
  });
  
  console.log(`\n回复航班号（如"1,2"）或说"都要"（最多${CONFIG.maxMonitoredFlights}个）`);
}

/**
 * 创建新任务（支持航班选择）
 */
async function createTask(options) {
  const {
    from,
    to,
    date,
    flightType = 'direct',
    timePreference = 'all',
    thresholdPercent = CONFIG.thresholdPercent,
    thresholdAmount = CONFIG.thresholdAmount,
    checkFrequency = CONFIG.checkFrequency,
    checkTime = CONFIG.checkTime,
    monitorDays = CONFIG.defaultMonitorDays,
    selectedFlightIndices = null,  // 用户选择的航班索引
  } = options;
  
  // 获取航班列表
  console.log('正在获取航班信息...');
  const flightResult = await fetchFlights(from, to, date, flightType);
  
  if (!flightResult.success) {
    console.error('创建失败:', flightResult.error);
    return null;
  }
  
  let flights = flightResult.flights;
  
  // 按时间段筛选
  if (timePreference !== 'all') {
    const hourRanges = { morning: [6, 12], afternoon: [12, 18], evening: [18, 24] };
    const [startHour, endHour] = hourRanges[timePreference] || [0, 24];
    flights = flights.filter(f => {
      const depHour = parseInt(f.departure?.split(':')[0] || '12');
      return depHour >= startHour && depHour < endHour;
    });
  }
  
  if (flights.length === 0) {
    console.error('没有找到符合条件的航班');
    return null;
  }
  
  // 用户选择航班
  let selectedFlights;
  if (selectedFlightIndices && selectedFlightIndices.length > 0) {
    // 用户自定义选择
    selectedFlights = selectedFlightIndices
      .filter(i => i >= 1 && i <= flights.length)
      .slice(0, CONFIG.maxMonitoredFlights)
      .map(i => flights[i - 1]);
  } else {
    // 自动选择前 N 个
    selectedFlights = flights.slice(0, CONFIG.maxMonitoredFlights);
  }
  
  if (selectedFlights.length === 0) {
    console.error('没有选择任何航班');
    return null;
  }
  
  // 找出基准价（最低价）
  const basePrice = Math.min(...selectedFlights.map(f => f.price));
  const baseFlightIndex = selectedFlights.findIndex(f => f.price === basePrice);
  
  // 标记基准航班
  selectedFlights.forEach((f, i) => {
    f.isBaseFlight = (i === baseFlightIndex);
  });
  
  // 加载现有数据
  const data = loadTasks();
  
  // 创建任务
  const now = new Date();
  const expiresAt = new Date(now.getTime() + monitorDays * 24 * 60 * 60 * 1000);
  
  const task = {
    taskId: String(data.nextTaskId).padStart(3, '0'),
    status: 'active',
    from,
    to,
    date,
    flightType,
    timePreference,
    checkFrequency,
    checkTime,
    selectedFlights,
    basePrice,
    baseFlightIndex,
    thresholdPercent,
    thresholdAmount,
    createdAt: now.toISOString(),
    expiresAt: expiresAt.toISOString(),
    lastCheckAt: now.toISOString(),
    lastAlertAt: null,
    priceHistory: [
      {
        time: now.toISOString(),
        flights: selectedFlights.map(f => ({ ...f })),
        minPrice: basePrice,
      },
    ],
  };
  
  // 保存
  data.tasks.push(task);
  data.nextTaskId++;
  saveTasks(data);
  
  // 简洁的创建成功消息（含购票链接）
  console.log(`\n✅ 已创建监控任务 #${task.taskId}`);
  console.log(`\n📍 ${from} → ${to} | 📅 ${date} | ✈️ ${flightType === 'direct' ? '直飞' : '含中转'}`);
  console.log(`💰 基准价：¥${basePrice}（${selectedFlights[baseFlightIndex].airline}${selectedFlights[baseFlightIndex].flightNo}）`);
  console.log(`📊 监控${selectedFlights.length}个航班`);
  console.log(`⚠️ 降幅超 ${thresholdPercent}% 或 ¥${thresholdAmount} 提醒你`);
  console.log(`⏰ ${checkFrequency === 'daily' ? '每天' : '每小时'}检查 | 监控${monitorDays}天`);
  console.log(`\n✈️ 监控航班:`);
  selectedFlights.forEach((f, i) => {
    console.log(`  ${i+1}. ¥${f.price} ${f.airline}${f.flightNo} | ${f.departure} ${f.depStation}→${f.arrStation}`);
    if (f.jumpUrl) console.log(`     🔗 ${f.jumpUrl}`);
  });
  
  // 发送钉钉确认消息
  sendDingTalkConfirmation(task, selectedFlights, monitorDays);
  
  return task;
}

/**
 * 发送钉钉确认消息
 */
async function sendDingTalkConfirmation(task, selectedFlights, monitorDays) {
  const message = `
✅ 监控已开始

📍 ${task.from} → ${task.to} | 📅 ${task.date}
💰 基准价：¥${task.basePrice}（${selectedFlights[0].airline}${selectedFlights[0].flightNo}）
📊 监控${selectedFlights.length}个航班
⚠️ 降幅超 ${task.thresholdPercent}% 或 ¥${task.thresholdAmount} 提醒你
⏰ 每天 9:00 检查 | 监控${monitorDays}天

✈️ 监控航班:
${selectedFlights.map((f, i) => `  ${i+1}. ¥${f.price} ${f.airline}${f.flightNo} | ${f.departure}出发`).join('\n')}

降价了我会立刻通知你！🛒 点击购票链接直达
  `.trim();

  const targetId = process.env.DINGTALK_TARGET_ID || '395111';  // 使用环境变量
  const cmd = `openclaw message send --channel dingtalk --target ${targetId} -m "${message}"`;
  
  try {
    const { execSync } = require('child_process');
    execSync(cmd);
    console.log('✅ 钉钉确认消息已发送！');
  } catch (error) {
    console.error('发送确认消息失败:', error.message);
  }
}

/**
 * 查看任务列表
 */
function listTasks(statusFilter = 'all') {
  const data = loadTasks();
  
  if (data.tasks.length === 0) {
    console.log('暂无监控任务');
    return;
  }
  
  const tasks = statusFilter === 'all' 
    ? data.tasks 
    : data.tasks.filter(t => t.status === statusFilter);
  
  if (tasks.length === 0) {
    console.log(`没有${statusFilter}状态的任务`);
    return;
  }
  
  console.log('\n=== 监控任务列表 ===\n');
  
  for (const task of tasks) {
    const statusIcon = { active: '🟢', paused: '🟡', expired: '⚪', completed: '✅' }[task.status] || '⚪';
    
    const lastCheck = task.lastCheckAt 
      ? new Date(task.lastCheckAt).toLocaleString('zh-CN', { month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' })
      : '未检查';
    
    const currentPrice = task.priceHistory.length > 0 ? task.priceHistory[task.priceHistory.length - 1].minPrice : task.basePrice;
    const change = currentPrice - task.basePrice;
    const changePercent = ((change / task.basePrice) * 100).toFixed(1);
    const changeIcon = change < 0 ? '🟢' : (change > 0 ? '🔴' : '⚪');
    
    const monitorDay = Math.floor((new Date() - new Date(task.createdAt)) / (1000 * 60 * 60 * 24)) + 1;
    
    console.log(`${statusIcon} 任务 #${task.taskId}: ${task.from} → ${task.to} (${task.date})`);
    console.log(`   ${changeIcon} 基准价：¥${task.basePrice} | 当前价：¥${currentPrice} (${change >= 0 ? '+' : ''}${changePercent}%)`);
    console.log(`   📊 监控${task.selectedFlights.length}个航班 | 📅 监控第${monitorDay}天 | ⏰ 最后检查：${lastCheck}`);
    console.log();
  }
}

/**
 * 暂停任务
 */
function pauseTask(taskId) {
  const data = loadTasks();
  const task = data.tasks.find(t => t.taskId === taskId);
  if (!task) { console.error(`未找到任务 #${taskId}`); return false; }
  if (task.status !== 'active') { console.log(`任务 #${taskId} 当前状态为${task.status}`); return false; }
  task.status = 'paused';
  saveTasks(data);
  console.log(`⏸️ 任务 #${taskId} 已暂停`);
  return true;
}

/**
 * 恢复任务
 */
function resumeTask(taskId) {
  const data = loadTasks();
  const task = data.tasks.find(t => t.taskId === taskId);
  if (!task) { console.error(`未找到任务 #${taskId}`); return false; }
  if (task.status !== 'paused') { console.log(`任务 #${taskId} 当前状态为${task.status}`); return false; }
  task.status = 'active';
  saveTasks(data);
  console.log(`▶️ 任务 #${taskId} 已恢复`);
  return true;
}

/**
 * 删除任务
 */
function deleteTask(taskId) {
  const data = loadTasks();
  const idx = data.tasks.findIndex(t => t.taskId === taskId);
  if (idx === -1) { console.error(`未找到任务 #${taskId}`); return false; }
  const task = data.tasks.splice(idx, 1)[0];
  saveTasks(data);
  console.log(`🗑️ 任务 #${taskId} 已删除`);
  console.log(`   航线：${task.from} → ${task.to} | 共监控${task.priceHistory.length}次`);
  return true;
}

/**
 * 延长任务周期
 */
function extendTask(taskId, days) {
  const data = loadTasks();
  const task = data.tasks.find(t => t.taskId === taskId);
  if (!task) { console.error(`未找到任务 #${taskId}`); return false; }
  const now = new Date(task.expiresAt);
  const newExpires = new Date(now.getTime() + days * 24 * 60 * 60 * 1000);
  task.expiresAt = newExpires.toISOString();
  saveTasks(data);
  console.log(`📅 任务 #${taskId} 已延长${days}天`);
  console.log(`   新到期时间：${newExpires.toISOString().split('T')[0]}`);
  return true;
}

// 导出函数
export { createTask, listTasks, pauseTask, resumeTask, deleteTask, extendTask, loadTasks, saveTasks, fetchFlights, showFlightSelection };

// 命令行入口
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  switch (command) {
    case 'list': listTasks(args[1] || 'all'); break;
    case 'pause': pauseTask(args[1]); break;
    case 'resume': resumeTask(args[1]); break;
    case 'delete': deleteTask(args[1]); break;
    case 'extend': extendTask(args[1], parseInt(args[2]) || 7); break;
    default:
      console.log('Flight Price Watcher v2.2.2 - 任务管理器');
      console.log('\n用法:');
      console.log('  list [all|active|paused|expired]  - 查看任务');
      console.log('  pause <taskId>                    - 暂停任务');
      console.log('  resume <taskId>                   - 恢复任务');
      console.log('  delete <taskId>                   - 删除任务');
      console.log('  extend <taskId> [days]            - 延长任务');
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
