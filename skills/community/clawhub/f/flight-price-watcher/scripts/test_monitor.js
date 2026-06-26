#!/usr/bin/env node

/**
 * Flight Price Watcher - 测试模式
 * 每 2 分钟检查一次，连续检查 3 次
 */

import { readFileSync, writeFileSync } from 'fs';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// 测试配置
const TEST_CONFIG = {
  checkInterval: 2 * 60 * 1000,  // 2 分钟
  checkCount: 3,  // 检查 3 次
  taskId: '004',  // 测试任务 ID
};

const DATA_FILE = new URL('../data/tasks.json', import.meta.url).pathname;

/**
 * 调用 FlyAI CLI 获取价格
 */
async function fetchPrice(from, to, date, flightType = 'direct') {
  try {
    const typeFlag = flightType === 'direct' ? '--journey-type 1' : '';
    const cmd = `flyai search-flight --origin "${from}" --destination "${to}" --dep-date ${date} ${typeFlag}`;
    
    const { stdout } = await execAsync(cmd);
    const result = JSON.parse(stdout);
    const itemList = result.data?.itemList || [];
    
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
        jumpUrl: item.jumpUrl || '',
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
 * 发送钉钉消息
 */
async function sendDingTalkAlert(task, currentPrice, change, flight) {
  const percent = ((change / task.basePrice) * 100).toFixed(1);
  
  const message = `
🟢 大降价！${task.from} → ${task.to}

💰 ¥${currentPrice}（↓¥${Math.abs(change)}，-${percent}%）📉
✈️ ${flight.airline}${flight.flightNo}
🕐 ${flight.departure} ${flight.depStation} → ${flight.arrStation}（${flight.duration}分钟）
🏆 监控期间最低价！

📊 基准价：¥${task.basePrice}（监控第 1 天）

✅ 强烈建议入手！

🛒 [点击购票 →](${flight.jumpUrl})
  `.trim();

  const cmd = `openclaw message send --channel dingtalk --target 395111 -m "${message}"`;
  
  try {
    await execAsync(cmd);
    console.log('✅ 钉钉消息已发送！');
  } catch (error) {
    console.error('发送消息失败:', error.message);
  }
}

/**
 * 检查任务
 */
async function checkTask(task, checkNum) {
  console.log(`\n⏰ 第${checkNum}次检查（${new Date().toLocaleTimeString('zh-CN', {hour: '2-digit', minute:'2-digit', second:'2-digit'})}）`);
  
  const result = await fetchPrice(task.from, task.to, task.date, task.flightType);
  
  if (!result.success) {
    console.error('获取价格失败');
    return;
  }
  
  const currentPrice = result.minPrice;
  const change = currentPrice - task.basePrice;
  const percent = ((change / task.basePrice) * 100).toFixed(1);
  
  console.log(`当前价：¥${currentPrice}（${change >= 0 ? '+' : ''}¥${change}，${percent}%）`);
  
  // 记录价格历史
  task.priceHistory.push({
    time: new Date().toISOString(),
    flights: result.flights,
    minPrice: currentPrice,
  });
  
  // 判断是否触发阈值
  const thresholdPercent = task.thresholdPercent || 10;
  const thresholdAmount = task.thresholdAmount || 200;
  
  if (change < 0 && (Math.abs(percent) >= thresholdPercent || Math.abs(change) >= thresholdAmount)) {
    console.log(`✅ 已触发阈值（-${Math.abs(percent)}% < -${thresholdPercent}% 或 ¥${Math.abs(change)} >= ¥${thresholdAmount}）`);
    
    // 发送提醒
    const bestFlight = result.flights.find(f => f.price === currentPrice) || result.flights[0];
    await sendDingTalkAlert(task, currentPrice, change, bestFlight);
    
    task.lastAlertAt = new Date().toISOString();
  } else {
    console.log('❌ 未触发阈值');
  }
  
  task.lastCheckAt = new Date().toISOString();
  
  // 保存数据
  const data = JSON.parse(readFileSync(DATA_FILE, 'utf-8'));
  const taskIndex = data.tasks.findIndex(t => t.taskId === task.taskId);
  data.tasks[taskIndex] = task;
  writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf-8');
}

/**
 * 主函数
 */
async function main() {
  console.log('=== Flight Price Watcher - 测试模式 ===');
  console.log(`每${TEST_CONFIG.checkInterval / 1000 / 60}分钟检查一次，连续检查${TEST_CONFIG.checkCount}次`);
  
  const data = JSON.parse(readFileSync(DATA_FILE, 'utf-8'));
  const task = data.tasks.find(t => t.taskId === TEST_CONFIG.taskId);
  
  if (!task) {
    console.error('未找到任务 #' + TEST_CONFIG.taskId);
    return;
  }
  
  console.log(`\n📍 任务 #${task.taskId}: ${task.from} → ${task.to} (${task.date})`);
  console.log(`💰 基准价：¥${task.basePrice}`);
  console.log(`⚠️ 阈值：${task.thresholdPercent}% 或 ¥${task.thresholdAmount}`);
  
  // 连续检查 3 次
  for (let i = 1; i <= TEST_CONFIG.checkCount; i++) {
    await checkTask(task, i);
    
    if (i < TEST_CONFIG.checkCount) {
      console.log(`⏳ 等待${TEST_CONFIG.checkInterval / 1000 / 60}分钟后进行下一次检查...`);
      await new Promise(resolve => setTimeout(resolve, TEST_CONFIG.checkInterval));
    }
  }
  
  console.log('\n=== 测试完成 ===');
  console.log(`\n📊 价格历史:`);
  task.priceHistory.forEach((p, i) => {
    console.log(`  第${i+1}次：¥${p.minPrice}`);
  });
}

// 运行
main().catch(console.error);
