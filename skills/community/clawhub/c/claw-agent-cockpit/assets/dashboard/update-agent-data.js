#!/usr/bin/env node
/**
 * Agent 数据自动更新脚本
 * 每 3 分钟自动更新 agent-data.json 文件
 * 
 * 状态判断逻辑：
 * - ok (正常运行): 任务进行中 (<100% 进度)
 * - rest (休息中): 任务已完成 (100%) 且 ≤24 小时未活动
 * - idle (待业 ing): 任务已完成且 ≥24 小时但 <7 天未活动
 * - lost (失联): ≥7 天未活动
 */

const fs = require('fs');
const path = require('path');
const { updateQuota } = require('./quota-tracker');

const DATA_FILE = path.join(__dirname, 'agent-data.json');
const UPDATE_INTERVAL = 180000; // 3 分钟

function updateAgentData() {
  console.log('📡 正在更新 Agent 数据...');
  
  try {
    const existing = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
    const now = Date.now();
    
    const updated = existing.map(agent => {
      const minutesAgo = (now - agent.lastActive) / 60000;
      const hoursAgo = minutesAgo / 60;
      const daysAgo = hoursAgo / 24;
      let newStatus = agent.status;
      let newStatusText = null;
      
      // 失联：≥7 天未活动
      if (daysAgo >= 7) {
        newStatus = 'lost';
        newStatusText = `${daysAgo.toFixed(1)}天未活动`;
      }
      // 待业 ing: 任务已完成且 ≥24 小时但 <7 天
      else if (agent.progress >= 100 && hoursAgo >= 24 && daysAgo < 7) {
        newStatus = 'idle';
        newStatusText = `待业 ing (${hoursAgo.toFixed(0)}小时未活动)`;
      }
      // 休息中：任务已完成且 ≤24 小时
      else if (agent.progress >= 100 && hoursAgo < 24) {
        newStatus = 'rest';
        newStatusText = '任务已完成，待命中';
      }
      // 正常运行：任务进行中 (<100%)
      else if (agent.progress < 100) {
        newStatus = 'ok';
        newStatusText = null;
      }
      
      return {
        ...agent,
        status: newStatus,
        statusText: newStatusText,
        restReason: newStatus === 'rest' ? newStatusText : null,
        idleReason: newStatus === 'idle' ? newStatusText : null,
        lostReason: newStatus === 'lost' ? newStatusText : null,
      };
    });
    
    fs.writeFileSync(DATA_FILE, JSON.stringify(updated, null, 2));
    
    // 统计状态
    const stats = {
      ok: updated.filter(a => a.status === 'ok').length,
      rest: updated.filter(a => a.status === 'rest').length,
      idle: updated.filter(a => a.status === 'idle').length,
      lost: updated.filter(a => a.status === 'lost').length,
    };
    
    console.log(`✅ 数据已更新：${updated.length}个 Agent (正常:${stats.ok} 休息:${stats.rest} 待业:${stats.idle} 失联:${stats.lost})`);
    return updated;
    
  } catch (e) {
    console.error('❌ 更新失败:', e.message);
    return [];
  }
}

// 首次更新
updateAgentData();
updateQuota();

// 定时更新
setInterval(() => {
  updateAgentData();
  updateQuota();
}, UPDATE_INTERVAL);

console.log(`🔄 自动更新服务已启动（每 ${UPDATE_INTERVAL / 1000}秒更新一次）`);
