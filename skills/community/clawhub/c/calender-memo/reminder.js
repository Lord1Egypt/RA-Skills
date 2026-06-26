// reminder.js - 带主动推送功能的提醒模块
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process'); // 用于执行外部命令

const MEMORY_FILE = path.join(__dirname, 'MEMORY.md');

// 加载日程数据（同前）
function loadEvents() { /* ... */ }

// 保存日程数据（同前）
function saveEvents(events) { /* ... */ }

// 真正发送推送消息的函数
function sendPushNotification(messageText) {
  // 使用 openclaw 命令通过 feishu 通道发送消息
  // 注意：--channel 指定通道，--recipient current 表示发送给当前用户
  const cmd = `openclaw message send --channel feishu --recipient current --text "${messageText.replace(/"/g, '\\"')}"`;
  
  exec(cmd, (error, stdout, stderr) => {
    if (error) {
      console.error(`推送失败: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`推送 stderr: ${stderr}`);
      return;
    }
    console.log(`推送成功: ${stdout}`);
  });
}

// 检查并推送需要提醒的日程
function checkReminders() {
  const events = loadEvents();
  const now = new Date();
  let hasNewReminders = false;

  events.forEach(event => {
    if (event.status !== 'upcoming' || event.reminded) return;

    const startTime = new Date(event.startTime);
    const offset = event.reminderOffset || 15;
    const diffMinutes = (startTime - now) / (1000 * 60);

    if (diffMinutes > 0 && diffMinutes <= offset) {
      // 真正发送推送！
      const message = `⏰ 提醒：${event.title} 将于 ${startTime.toLocaleString('zh-CN', { 
        month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' 
      })} 开始`;
      
      sendPushNotification(message);
      
      // 标记为已提醒
      event.reminded = true;
      hasNewReminders = true;
    }
  });

  if (hasNewReminders) {
    saveEvents(events);
  }
}

// 启动定时检查（每分钟一次）
let intervalId = null;
function startReminderChecker() {
  if (intervalId) return;
  intervalId = setInterval(() => {
    checkReminders();
  }, 60 * 1000);
}

function stopReminderChecker() {
  if (intervalId) {
    clearInterval(intervalId);
    intervalId = null;
  }
}

module.exports = {
  startReminderChecker,
  stopReminderChecker
  // 注意：不再需要 getPendingReminders，因为直接推送了
};