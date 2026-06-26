#!/usr/bin/env node

/**
 * Flight Price Watcher v2.2.2 - 价格监控主逻辑
 * 
 * v2.2.2 新增：
 * 1. 输入验证（防止命令注入）
 * 2. 环境变量配置
 * 3. 完整安全文档
 * 
 * v2.2.0 新增：
 * 1. 创建成功确认消息
 * 2. 首次检查确认消息
 * 3. 每日汇总报告
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
  const sanitized = input.replace(/[^\u4e00-\u9fa5a-zA-Z0-9\-.\s]/g, '');
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
};

// 数据文件路径
const DATA_FILE = new URL('../data/tasks.json', import.meta.url).pathname;

/**
 * 读取任务数据
 */
function loadTasks() {
  if (!existsSync(DATA_FILE)) return { tasks: [], nextTaskId: 1 };
  return JSON.parse(readFileSync(DATA_FILE, 'utf-8'));
}

/**
 * 保存任务数据
 */
function saveTasks(data) {
  writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf-8');
}

/**
 * 检测 FlyAI CLI 是否已安装
 */
async function checkFlyAIInstalled() {
  try {
    const { stdout } = await execAsync('flyai --help');
    return stdout.includes('Fliggy travel CLI');
  } catch (error) {
    return false;
  }
}

/**
 * 调用 FlyAI CLI 获取最新价格（带输入验证）
 */
async function fetchPrice(from, to, date, flightType = 'all') {
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
    
    // 获取航班详情（含购票链接）
    const flights = itemList.slice(0, 10).map(item => {
      const segment = item.segments?.[0] || {};
      const depTime = segment.depDateTime?.split(' ') || ['', ''];
      const arrTime = segment.arrDateTime?.split(' ') || ['', ''];
      
      return {
        price: parseFloat(item.ticketPrice) || 0,
        flightNo: segment.marketingTransportNo || '',
        airline: segment.marketingTransportName || '',
        departure: depTime[1] || '',
        arrival: arrTime[1] || '',
        depStation: segment.depStationShortName || segment.depStationName || '',
        arrStation: segment.arrStationShortName || segment.arrStationName || '',
        duration: item.totalDuration || '',
        jumpUrl: item.jumpUrl || '',  // 购票链接
      };
    });
    
    const prices = flights.map(f => f.price).filter(p => p > 0);
    
    return { success: true, flights, minPrice: prices.length > 0 ? Math.min(...prices) : Infinity };
  } catch (error) {
    console.error('获取价格失败:', error.message);
    return { success: false, error: error.message };
  }
}

/**
 * 计算波动
 */
function calculateChange(current, base) {
  const diff = current - base;
  const percent = ((diff / base) * 100).toFixed(1);
  return { diff, percent: parseFloat(percent), isDrop: diff < 0, isRise: diff > 0 };
}

/**
 * 判断是否触发提醒
 */
function shouldAlert(change, thresholdPercent, thresholdAmount) {
  return Math.abs(change.percent) >= thresholdPercent || Math.abs(change.diff) >= thresholdAmount;
}

/**
 * 判断是否历史最低
 */
function isHistoricalLow(currentPrice, priceHistory) {
  if (priceHistory.length === 0) return false;
  return currentPrice < Math.min(...priceHistory.map(p => p.minPrice));
}

/**
 * 计算监控天数
 */
function getMonitorDay(task) {
  return Math.floor((new Date() - new Date(task.createdAt)) / (1000 * 60 * 60 * 24)) + 1;
}

/**
 * 生成醒目提醒消息（包含所有航班信息）
 */
function generateAlertMessage(task, currentFlights, priceChange, isLowest) {
  const monitorDay = getMonitorDay(task);
  const dropIcon = '🟢';
  const riseIcon = '🔴';
  
  // 找出降价航班
  const dropFlights = currentFlights.filter(f => {
    const baseFlight = task.selectedFlights.find(bf => bf.flightNo === f.flightNo);
    if (!baseFlight) return false;
    const change = calculateChange(f.price, baseFlight.price);
    return shouldAlert(change, task.thresholdPercent, task.thresholdAmount);
  });
  
  // 主标题
  const title = dropFlights.length > 0 ? '大降价！' : '涨价了！';
  const icon = dropFlights.length > 0 ? dropIcon : riseIcon;
  
  // 构建消息
  let message = `${icon} ${title}${task.from} → ${task.to}\n\n`;
  
  // 降价航班详情
  if (dropFlights.length > 0) {
    dropFlights.forEach(f => {
      const baseFlight = task.selectedFlights.find(bf => bf.flightNo === f.flightNo);
      const change = calculateChange(f.price, baseFlight.price);
      const isBest = f.price === Math.min(...dropFlights.map(df => df.price));
      
      message += `💰 ¥${f.price}（${change.isDrop ? '↓' : '↑'}¥${Math.abs(change.diff)}，${Math.abs(change.percent)}%）${change.isDrop ? '📉' : '📈'}\n`;
      message += `✈️ ${f.airline}${f.flightNo}\n`;
      message += `🕐 ${f.departure} ${f.depStation} → ${f.arrival} ${f.arrStation}（${f.duration}分钟）\n`;
      if (isBest && change.isDrop) message += `🏆 监控期间最低价！\n`;
      message += '\n';
    });
  } else {
    // 涨价时显示当前最低价航班
    const minFlight = currentFlights.reduce((min, f) => f.price < min.price ? f : min);
    const baseFlight = task.selectedFlights.find(bf => bf.flightNo === minFlight.flightNo);
    const change = baseFlight ? calculateChange(minFlight.price, baseFlight.price) : { percent: 0, diff: 0 };
    
    message += `💰 ¥${minFlight.price}（${change.isDrop ? '↓' : '↑'}¥${Math.abs(change.diff)}，${Math.abs(change.percent)}%）📈\n`;
    message += `✈️ ${minFlight.airline}${minFlight.flightNo}\n`;
    message += `🕐 ${minFlight.departure} ${minFlight.depStation} → ${minFlight.arrival} ${minFlight.arrStation}\n\n`;
  }
  
  // 基准价信息（帮助用户回忆）
  message += `📊 基准价：¥${task.basePrice}（监控第${monitorDay}天）\n\n`;
  
  // 其他监控航班（即使未触发阈值）
  const otherFlights = currentFlights.filter(f => !dropFlights.find(df => df.flightNo === f.flightNo));
  if (otherFlights.length > 0) {
    message += `其他监控航班：\n`;
    otherFlights.forEach(f => {
      const baseFlight = task.selectedFlights.find(bf => bf.flightNo === f.flightNo);
      if (!baseFlight) return;
      const change = calculateChange(f.price, baseFlight.price);
      const changeText = change.isDrop ? `↓¥${Math.abs(change.diff)}` : (change.isRise ? `↑¥${change.diff}` : '无波动');
      message += `  • ${f.airline}${f.flightNo} | ${f.departure}出发 | ¥${f.price}（${changeText}）\n`;
    });
    message += '\n';
  }
  
  // 建议文案
  const suggestion = dropFlights.length > 0 
    ? '✅ 建议入手！' 
    : '⚠️ 之前有更低价，建议尽快入手！';
  message += suggestion;
  
  // 购票链接（使用 Markdown 超链接格式，支持钉钉点击跳转）
  const bestFlight = dropFlights.length > 0 ? dropFlights[0] : currentFlights[0];
  if (bestFlight?.jumpUrl) {
    message += `\n\n🛒 [点击购票 →](${bestFlight.jumpUrl})`;
  }
  
  return message;
}

/**
 * 发送钉钉消息
 */
async function sendDingTalkAlert(task, currentFlights, priceChange, isLowest) {
  const message = generateAlertMessage(task, currentFlights, priceChange, isLowest);
  const targetId = process.env.DINGTALK_TARGET_ID || '395111';  // 使用环境变量
  const cmd = `openclaw message send --channel dingtalk --target ${targetId} -m "${message}"`;
  
  try {
    await execAsync(cmd);
    console.log(`已发送提醒：任务 #${task.taskId}`);
  } catch (error) {
    console.error('发送消息失败:', error.message);
  }
}

/**
 * 检查单个任务
 */
async function checkTask(task) {
  console.log(`检查任务 #${task.taskId}: ${task.from} → ${task.to}`);
  
  const now = new Date();
  const isFirstCheck = task.priceHistory.length <= 1;
  const result = await fetchPrice(task.from, task.to, task.date, task.flightType);
  
  if (!result.success) {
    console.error(`任务 #${task.taskId} 获取价格失败`);
    return;
  }
  
  // 匹配监控的航班
  const currentFlights = task.selectedFlights.map(base => {
    const current = result.flights.find(f => f.flightNo === base.flightNo);
    return current || { ...base, price: base.price };  // 找不到就用上次价格
  });
  
  const minPrice = Math.min(...currentFlights.map(f => f.price));
  const priceChange = calculateChange(minPrice, task.basePrice);
  
  // 记录历史
  task.priceHistory.push({ time: now.toISOString(), flights: currentFlights, minPrice });
  if (task.priceHistory.length > 100) task.priceHistory = task.priceHistory.slice(-100);
  
  // 判断是否历史最低
  const isLowest = isHistoricalLow(minPrice, task.priceHistory.slice(0, -1));
  
  // 首次检查确认
  if (isFirstCheck) {
    await sendFirstCheckConfirmation(task, minPrice, priceChange);
  }
  
  // 判断是否触发提醒
  const thresholdPercent = task.thresholdPercent || CONFIG.thresholdPercent;
  const thresholdAmount = task.thresholdAmount || CONFIG.thresholdAmount;
  
  if (shouldAlert(priceChange, thresholdPercent, thresholdAmount)) {
    const lastAlertTime = task.lastAlertAt ? new Date(task.lastAlertAt) : null;
    const hoursSinceLastAlert = lastAlertTime ? (now - lastAlertTime) / (1000 * 60 * 60) : Infinity;
    
    if (hoursSinceLastAlert >= 24) {
      await sendDingTalkAlert(task, currentFlights, priceChange, isLowest);
      task.lastAlertAt = now.toISOString();
    } else {
      console.log(`任务 #${task.taskId} 触发阈值，但距离上次提醒仅${hoursSinceLastAlert.toFixed(1)}小时，跳过`);
    }
  } else {
    console.log(`任务 #${task.taskId} 波动${priceChange.percent}%，未达阈值`);
  }
  
  task.lastCheckAt = now.toISOString();
  return task;
}

/**
 * 发送首次检查确认消息
 */
async function sendFirstCheckConfirmation(task, currentPrice, priceChange) {
  const percent = priceChange.percent >= 0 ? `+${priceChange.percent}%` : `${priceChange.percent}%`;
  const icon = priceChange.isDrop ? '🟢' : (priceChange.isRise ? '🔴' : '⚪');
  
  const message = `
✅ 首次检查完成

📍 ${task.from} → ${task.to} | 📅 ${task.date}
💰 当前价：¥${currentPrice}（${percent}）
📊 基准价：¥${task.basePrice}
⚠️ 降幅超 ${task.thresholdPercent}% 或 ¥${task.thresholdAmount} 提醒你
🔔 监控正常运行中...
  `.trim();

  const targetId = process.env.DINGTALK_TARGET_ID || '395111';
  const cmd = `openclaw message send --channel dingtalk --target ${targetId} -m "${message}"`;
  
  try {
    await execAsync(cmd);
    console.log(`已发送首次检查确认：任务 #${task.taskId}`);
  } catch (error) {
    console.error('发送首次检查消息失败:', error.message);
  }
}

/**
 * 检查任务是否到期
 */
function isTaskExpired(task) {
  return new Date() > new Date(task.expiresAt);
}

/**
 * 主函数
 */
async function main() {
  console.log('=== Flight Price Watcher v2.1 ===');
  console.log(`检查时间：${new Date().toISOString()}`);
  
  const data = loadTasks();
  const activeTasks = data.tasks.filter(t => t.status === 'active');
  
  if (activeTasks.length === 0) {
    console.log('没有活跃的监控任务');
    return;
  }
  
  console.log(`共有 ${activeTasks.length} 个活跃任务`);
  
  for (const task of activeTasks) {
    if (isTaskExpired(task)) {
      console.log(`任务 #${task.taskId} 已到期，自动暂停`);
      task.status = 'expired';
      continue;
    }
    await checkTask(task);
  }
  
  saveTasks(data);
  console.log('=== 检查完成 ===');
}

/**
 * 主函数（带每日汇总）
 */
async function mainWithSummary() {
  console.log('=== Flight Price Watcher v2.2.2 ===');
  console.log(`检查时间：${new Date().toISOString()}`);
  
  const data = loadTasks();
  const activeTasks = data.tasks.filter(t => t.status === 'active');
  
  if (activeTasks.length === 0) {
    console.log('没有活跃的监控任务');
    return;
  }
  
  console.log(`共有 ${activeTasks.length} 个活跃任务`);
  
  for (const task of activeTasks) {
    if (isTaskExpired(task)) {
      console.log(`任务 #${task.taskId} 已到期，自动暂停`);
      task.status = 'expired';
      continue;
    }
    await checkTask(task);
  }
  
  saveTasks(data);
  
  // 发送每日汇总（每天只发送一次）
  const now = new Date();
  const lastSummary = data.lastDailySummary ? new Date(data.lastDailySummary) : new Date(0);
  const hoursSinceSummary = (now - lastSummary) / (1000 * 60 * 60);
  
  if (hoursSinceSummary >= 24) {
    await sendDailySummary(data);
    data.lastDailySummary = now.toISOString();
    saveTasks(data);
  }
  
  console.log('=== 检查完成 ===');
}

/**
 * 发送每日汇总报告
 */
async function sendDailySummary(data) {
  const activeTasks = data.tasks.filter(t => t.status === 'active');
  if (activeTasks.length === 0) return;
  
  const today = new Date().toISOString().split('T')[0];
  const todayChecks = activeTasks.filter(t => {
    const lastCheck = t.lastCheckAt ? new Date(t.lastCheckAt).toISOString().split('T')[0] : '';
    return lastCheck === today;
  });
  
  if (todayChecks.length === 0) return;
  
  let message = `📊 监控日报 ${today}\n\n`;
  message += `今日检查 ${todayChecks.length} 个任务：\n\n`;
  
  for (const task of todayChecks) {
    const currentPrice = task.priceHistory.length > 0 ? task.priceHistory[task.priceHistory.length - 1].minPrice : task.basePrice;
    const change = currentPrice - task.basePrice;
    const percent = ((change / task.basePrice) * 100).toFixed(1);
    const icon = change < 0 ? '🟢' : (change > 0 ? '🔴' : '⚪');
    const changeText = change >= 0 ? `+${percent}%` : `${percent}%`;
    
    message += `${icon} #${task.taskId} ${task.from}→${task.to}\n`;
    message += `   ¥${task.basePrice} → ¥${currentPrice}（${changeText}）\n\n`;
  }
  
  message += `降价了我会立刻通知你！`;
  
  const targetId = process.env.DINGTALK_TARGET_ID || '395111';
  const cmd = `openclaw message send --channel dingtalk --target ${targetId} -m "${message}"`;
  
  try {
    await execAsync(cmd);
    console.log('已发送每日汇总报告');
  } catch (error) {
    console.error('发送每日汇总失败:', error.message);
  }
}

/**
 * 主函数
 */
async function main() {
  console.log('=== Flight Price Watcher v2.1 ===');
  console.log(`检查时间：${new Date().toISOString()}`);
  
  const data = loadTasks();
  const activeTasks = data.tasks.filter(t => t.status === 'active');
  
  if (activeTasks.length === 0) {
    console.log('没有活跃的监控任务');
    return;
  }
  
  console.log(`共有 ${activeTasks.length} 个活跃任务`);
  
  for (const task of activeTasks) {
    if (isTaskExpired(task)) {
      console.log(`任务 #${task.taskId} 已到期，自动暂停`);
      task.status = 'expired';
      continue;
    }
    await checkTask(task);
  }
  
  saveTasks(data);
  
  // 发送每日汇总（每天只发送一次）
  const now = new Date();
  const lastSummary = data.lastDailySummary ? new Date(data.lastDailySummary) : new Date(0);
  const hoursSinceSummary = (now - lastSummary) / (1000 * 60 * 60);
  
  if (hoursSinceSummary >= 24) {
    await sendDailySummary(data);
    data.lastDailySummary = now.toISOString();
    saveTasks(data);
  }
  
  console.log('=== 检查完成 ===');
}

main().catch(console.error);
