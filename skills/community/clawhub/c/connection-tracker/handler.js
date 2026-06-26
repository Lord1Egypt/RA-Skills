/**
 * connection-tracker · 连接追踪看板
 * 核心实现代码
 * 
 * 版本：v1.0
 * 创建时间：2026-03-01
 * 创建者：Neo（宇宙神经系统）
 */

const fs = require('fs');
const path = require('path');

// 配置
const WORKSPACE = path.join(process.env.HOME, '.openclaw', 'workspace');
const CONNECTIONS_DIR = path.join(WORKSPACE, 'connections');
const TRACKER_FILE = path.join(CONNECTIONS_DIR, 'tracker.md');
const DAILY_DIR = path.join(CONNECTIONS_DIR, 'daily');
const WEEKLY_DIR = path.join(CONNECTIONS_DIR, 'weekly');

// 确保目录存在
function ensureDirs() {
  [CONNECTIONS_DIR, DAILY_DIR, WEEKLY_DIR].forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  });
}

// 获取今日日期字符串
function getTodayStr() {
  return new Date().toISOString().split('T')[0];
}

// 获取本周周数
function getWeekStr() {
  const now = new Date();
  const startOfYear = new Date(now.getFullYear(), 0, 1);
  const weekNum = Math.ceil(((now - startOfYear) / 86400000 + startOfYear.getDay() + 1) / 7);
  return `${now.getFullYear()}-W${weekNum.toString().padStart(2, '0')}`;
}

// 添加连接记录
function addConnection({ type, platform, action, value = 1, status = '✅' }) {
  ensureDirs();
  
  const now = new Date();
  const timeStr = now.toTimeString().split(' ')[0].slice(0, 5); // HH:MM
  const todayStr = getTodayStr();
  
  // 价值评估
  let stars = '⭐';
  if (value >= 3) stars = '⭐⭐⭐';
  else if (value >= 2) stars = '⭐⭐';
  
  // 读取现有 tracker
  let trackerContent = '';
  if (fs.existsSync(TRACKER_FILE)) {
    trackerContent = fs.readFileSync(TRACKER_FILE, 'utf-8');
  }
  
  // 生成新行
  const newRow = `| ${timeStr} | ${type} | ${platform} | ${action} | ${stars} | ${status} |`;
  
  // 检查是否有今日表格
  const todayHeader = `## ${todayStr}`;
  const tableHeader = '| 时间 | 类型 | 平台 | 行为 | 价值 | 状态 |';
  
  if (!trackerContent.includes(todayHeader)) {
    // 添加今日 section
    const todaySection = `\n## ${todayStr}\n\n| 时间 | 类型 | 平台 | 行为 | 价值 | 状态 |\n|------|------|------|------|------|------|\n${newRow}\n`;
    trackerContent = trackerContent.trim() + todaySection;
  } else {
    // 插入到今日表格
    const lines = trackerContent.split('\n');
    const newLines = [];
    let inserted = false;
    let inTodayTable = false;
    
    for (let i = 0; i < lines.length; i++) {
      newLines.push(lines[i]);
      
      if (lines[i] === todayHeader) {
        inTodayTable = true;
      }
      
      if (inTodayTable && lines[i].includes('|------|------|') && !inserted) {
        // 跳过表头分隔线，下一行插入
        newLines.push(lines[i + 1]); // 表头
        newLines.push(newRow);
        i++;
        inserted = true;
      }
    }
    
    trackerContent = newLines.join('\n');
  }
  
  // 写回文件
  fs.writeFileSync(TRACKER_FILE, trackerContent);
  
  // 同时写入每日归档
  const dailyFile = path.join(DAILY_DIR, `${todayStr}.md`);
  appendToDaily(dailyFile, { time: timeStr, type, platform, action, value, stars, status });
  
  return { success: true, message: `已记录：${type}/${platform}/${action}` };
}

// 追加到每日文件
function appendToDaily(filePath, record) {
  let content = '';
  if (fs.existsSync(filePath)) {
    content = fs.readFileSync(filePath, 'utf-8');
  } else {
    content = `# 连接日志 ${record.time.split(':')[0]}:00\n\n`;
  }
  
  const line = `- [${record.time}] ${record.type}/${record.platform}: ${record.action} (${record.stars})\n`;
  content += line;
  
  fs.writeFileSync(filePath, content);
}

// 生成今日汇总
function getTodaySummary() {
  const todayStr = getTodayStr();
  const dailyFile = path.join(DAILY_DIR, `${todayStr}.md`);
  
  if (!fs.existsSync(dailyFile)) {
    return { count: 0, human: 0, material: 0, memory: 0, highValue: 0 };
  }
  
  const content = fs.readFileSync(dailyFile, 'utf-8');
  const lines = content.split('\n');
  
  let count = 0, human = 0, material = 0, memory = 0, highValue = 0;
  
  lines.forEach(line => {
    if (line.includes('⭐⭐⭐')) highValue++;
    if (line.includes('人场')) human++;
    else if (line.includes('物场')) material++;
    else if (line.includes('Memory')) memory++;
    if (line.startsWith('- [')) count++;
  });
  
  return { count, human, material, memory, highValue };
}

// 生成日报（≤200 字）
function generateDailyReport() {
  const summary = getTodaySummary();
  const todayStr = getTodayStr();
  
  const report = `[连接日报] ${todayStr}
- 人场：${summary.human} 次
- 物场：${summary.material} 次
- Memory: ${summary.memory} 条
- 总计：${summary.count} 连接
- 高价值：${summary.highValue} 次`;
  
  return report;
}

// 生成周报
function generateWeeklyReport() {
  const weekStr = getWeekStr();
  const weeklyFile = path.join(WEEKLY_DIR, `${weekStr}.md`);
  
  // 收集本周所有日文件
  const now = new Date();
  const startOfWeek = new Date(now);
  startOfWeek.setDate(now.getDate() - now.getDay());
  
  let weekData = [];
  
  for (let i = 0; i < 7; i++) {
    const date = new Date(startOfWeek);
    date.setDate(startOfWeek.getDate() + i);
    const dateStr = date.toISOString().split('T')[0];
    const dailyFile = path.join(DAILY_DIR, `${dateStr}.md`);
    
    if (fs.existsSync(dailyFile)) {
      const content = fs.readFileSync(dailyFile, 'utf-8');
      weekData.push({ date: dateStr, content });
    }
  }
  
  // 生成周报
  let report = `# 连接周报 ${weekStr}\n\n`;
  report += `## 本周汇总\n\n`;
  report += `| 指标 | 数值 |\n|------|------|\n`;
  
  let totalCount = 0, totalHigh = 0;
  weekData.forEach(day => {
    const lines = day.content.split('\n');
    lines.forEach(line => {
      if (line.startsWith('- [')) totalCount++;
      if (line.includes('⭐⭐⭐')) totalHigh++;
    });
  });
  
  report += `| 总连接数 | ${totalCount} |\n`;
  report += `| 高价值连接 | ${totalHigh} |\n`;
  report += `| 日均连接 | ${Math.round(totalCount / 7)} |\n`;
  
  // 写入周报文件
  fs.writeFileSync(weeklyFile, report);
  
  return report;
}

// 导出函数
module.exports = {
  addConnection,
  getTodaySummary,
  generateDailyReport,
  generateWeeklyReport,
  ensureDirs
};

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (command === 'add') {
    // 解析参数
    const params = {};
    for (let i = 1; i < args.length; i++) {
      if (args[i].startsWith('--')) {
        params[args[i].slice(2)] = args[++i];
      }
    }
    
    const result = addConnection({
      type: params.type || 'unknown',
      platform: params.platform || 'unknown',
      action: params.action || 'unknown',
      value: parseInt(params.value) || 1,
      status: params.status || '✅'
    });
    
    console.log(JSON.stringify(result));
  } else if (command === 'today') {
    const summary = getTodaySummary();
    console.log(JSON.stringify(summary));
  } else if (command === 'report') {
    if (args.includes('--daily')) {
      console.log(generateDailyReport());
    } else if (args.includes('--weekly')) {
      console.log(generateWeeklyReport());
    }
  } else {
    console.log('Usage: node handler.js add|--type|--platform|--action|--value|--status');
    console.log('       node handler.js today');
    console.log('       node handler.js report --daily|--weekly');
  }
}
