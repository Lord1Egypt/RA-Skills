#!/usr/bin/env node

/**
 * 自动快照服务
 * 在任务完成、主题切换或定时时自动创建快照
 */

const { createSnapshot, getConfig, saveConfig, CONFIG } = require('./index.js');
const fs = require('fs');
const path = require('path');

// 会话状态文件
const sessionFile = path.join(CONFIG.dataDir, 'session.json');

// 初始化会话
function initSession() {
  if (!fs.existsSync(CONFIG.dataDir)) {
    fs.mkdirSync(CONFIG.dataDir, { recursive: true });
  }
  
  if (!fs.existsSync(sessionFile)) {
    fs.writeFileSync(sessionFile, JSON.stringify({
      startTime: new Date().toISOString(),
      lastActivity: new Date().toISOString(),
      taskCount: 0,
      topic: 'default'
    }, null, 2));
  }
}

// 获取会话状态
function getSession() {
  try {
    return JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
  } catch (e) {
    return { startTime: new Date().toISOString(), lastActivity: new Date().toISOString(), taskCount: 0, topic: 'default' };
  }
}

// 保存会话状态
function saveSession(session) {
  fs.writeFileSync(sessionFile, JSON.stringify(session, null, 2));
}

// 任务完成时创建快照
function onTaskComplete(taskName, result) {
  const config = getConfig();
  if (!config.autoSnapshot) return;
  
  const session = getSession();
  session.taskCount++;
  session.lastActivity = new Date().toISOString();
  saveSession(session);
  
  createSnapshot(`任务完成: ${taskName}`, ['auto', 'task-complete', session.topic]);
}

// 主题切换时创建快照
function onTopicSwitch(newTopic, previousTopic) {
  const config = getConfig();
  if (!config.autoSnapshot) return;
  
  // 先为旧主题创建快照
  if (previousTopic) {
    createSnapshot(`主题切换: ${previousTopic} -> ${newTopic}`, ['auto', 'topic-switch', previousTopic]);
  }
  
  const session = getSession();
  session.topic = newTopic;
  session.lastActivity = new Date().toISOString();
  saveSession(session);
  
  console.log(`🔄 主题已切换至: ${newTopic}`);
}

// 定时快照
function startAutoSnapshot(intervalMinutes = 30) {
  const config = getConfig();
  if (!config.autoSnapshot) {
    console.log('⏸️ 自动快照已关闭');
    return;
  }
  
  const intervalMs = intervalMinutes * 60 * 1000;
  
  console.log(`⏰ 自动快照已启动，间隔: ${intervalMinutes} 分钟`);
  
  setInterval(() => {
    const session = getSession();
    const now = new Date();
    const lastActivity = new Date(session.lastActivity);
    const timeSinceLastActivity = now - lastActivity;
    
    // 只有在有活动时才创建快照
    if (timeSinceLastActivity < intervalMs * 2) {
      createSnapshot(`定时快照: ${session.topic}`, ['auto', 'scheduled', session.topic]);
    }
  }, intervalMs);
}

// 记录活动
function recordActivity() {
  const session = getSession();
  session.lastActivity = new Date().toISOString();
  saveSession(session);
}

// 获取当前主题
function getCurrentTopic() {
  const session = getSession();
  return session.topic;
}

// 显示会话状态
function showSession() {
  initSession();
  const session = getSession();
  
  console.log('📊 当前会话状态:\n');
  console.log(`  开始时间: ${session.startTime}`);
  console.log(`  最后活动: ${session.lastActivity}`);
  console.log(`  当前主题: ${session.topic}`);
  console.log(`  完成任务: ${session.taskCount}`);
}

// 解析命令行
function parseArgs() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  switch (command) {
    case 'task':
      if (!args[1]) {
        console.error('❌ 请指定任务名称');
        process.exit(1);
      }
      onTaskComplete(args[1], args[2] || '');
      break;
      
    case 'topic':
      if (!args[1]) {
        console.error('❌ 请指定新主题');
        process.exit(1);
      }
      const session = getSession();
      onTopicSwitch(args[1], session.topic);
      break;
      
    case 'start':
      const interval = parseInt(args[1]) || 30;
      startAutoSnapshot(interval);
      // 保持进程运行
      setInterval(() => {}, 1000);
      break;
      
    case 'activity':
      recordActivity();
      console.log('✅ 活动已记录');
      break;
      
    case 'status':
      showSession();
      break;
      
    default:
      console.log(`
自动快照服务

用法: node auto-snapshot.js <command> [options]

命令:
  task <name> [result]     任务完成时创建快照
  topic <new-topic>        切换主题并创建快照
  start [interval-min]     启动定时快照服务
  activity                 记录活动
  status                   显示会话状态
`);
  }
}

// 主入口
if (require.main === module) {
  initSession();
  parseArgs();
}

// 导出API
module.exports = {
  initSession,
  onTaskComplete,
  onTopicSwitch,
  startAutoSnapshot,
  recordActivity,
  getCurrentTopic,
  showSession
};
