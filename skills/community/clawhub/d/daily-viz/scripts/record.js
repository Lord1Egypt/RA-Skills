#!/usr/bin/env node
/**
 * Daily Viz - 记录模块
 */

const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(process.env.HOME, '.daily-viz', 'data');
const DATA_FILE = path.join(DATA_DIR, 'records.json');

if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

if (!fs.existsSync(DATA_FILE)) {
  fs.writeFileSync(DATA_FILE, JSON.stringify({ records: [] }, null, 2));
}

function loadData() {
  return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
}

function saveData(data) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

function record(data) {
  const db = loadData();
  const record = {
    id: Date.now(),
    date: new Date().toISOString(),
    ...data
  };
  db.records.push(record);
  saveData(db);
  return record;
}

// 解析参数
const input = process.argv.slice(2).join(' ');
if (!input) {
  console.log('用法: record.js <数据>');
  console.log('示例: record.js 心情:开心 运动:30分钟');
  process.exit(1);
}

const data = {};

// 改进的解析逻辑
const regex = /([^:]+):([^\s]+)/g;
let match;
while ((match = regex.exec(input)) !== null) {
  data[match[1]] = match[2];
}

if (Object.keys(data).length === 0) {
  data.note = input;
}

const record_entry = record(data);
console.log('✅ 记录成功！');
console.log(`📅 ${new Date(record_entry.date).toLocaleString()}`);
Object.entries(data).forEach(([key, value]) => {
  console.log(`   ${key}: ${value}`);
});
