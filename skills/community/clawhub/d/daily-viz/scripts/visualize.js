#!/usr/bin/env node
/**
 * Daily Viz - 可视化模块
 * 生成数据图表和报告
 */

const fs = require('fs');
const path = require('path');

const DATA_FILE = path.join(process.env.HOME, '.daily-viz', 'data', 'records.json');

// 简单的 ASCII 图表生成
function generateBarChart(data, title, width = 40) {
  const max = Math.max(...Object.values(data));
  const min = Math.min(...Object.values(data));
  const range = max - min || 1;
  
  console.log(`\n📊 ${title}`);
  console.log('─'.repeat(width + 15));
  
  Object.entries(data).forEach(([label, value]) => {
    const barLength = Math.round(((value - min) / range) * width);
    const bar = '█'.repeat(barLength) + '░'.repeat(width - barLength);
    console.log(`${label.padEnd(8)} │${bar}│ ${value}`);
  });
  
  console.log('─'.repeat(width + 15));
}

// 生成周报告
function generateWeeklyReport() {
  if (!fs.existsSync(DATA_FILE)) {
    console.log('暂无数据，请先使用 /记录 添加一些数据');
    return;
  }
  
  const db = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  const records = db.records;
  
  if (records.length === 0) {
    console.log('暂无数据');
    return;
  }
  
  // 统计心情
  const moodCounts = {};
  records.forEach(r => {
    if (r.心情) {
      moodCounts[r.心情] = (moodCounts[r.心情] || 0) + 1;
    }
  });
  
  if (Object.keys(moodCounts).length > 0) {
    generateBarChart(moodCounts, '心情分布');
  }
  
  // 统计运动
  const exerciseData = {};
  records.slice(-7).forEach((r, i) => {
    if (r.运动) {
      const day = ['日', '一', '二', '三', '四', '五', '六'][new Date(r.date).getDay()];
      const value = parseInt(r.运动) || 0;
      exerciseData[day] = value;
    }
  });
  
  if (Object.keys(exerciseData).length > 0) {
    generateBarChart(exerciseData, '近7天运动时长(分钟)');
  }
  
  console.log(`\n📈 总计记录: ${records.length} 条`);
}

// 主函数
const args = process.argv.slice(2);
const command = args[0] || 'week';

switch (command) {
  case 'week':
    generateWeeklyReport();
    break;
  default:
    console.log('用法: visualize.js [week|month]');
}
