#!/usr/bin/env node
/**
 * Focus Tree - 格式化操作 FOCUS.md 和 FOCUS-LOG.md
 * 确保文件格式统一，不依赖其他存储
 */

import fs from 'fs';
import path from 'path';

const FOCUS_PATH = path.join(process.cwd(), 'FOCUS.md');
const FOCUS_LOG_PATH = path.join(process.cwd(), 'FOCUS-LOG.md');

const args = process.argv.slice(2);
const command = args[0];

// 生成统一格式的 FOCUS.md
function generateFocus(focusPoint, todos = [], context = '', status = 'active') {
  const now = new Date().toLocaleString('zh-CN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit', 
    hour: '2-digit', 
    minute: '2-digit',
    timeZone: 'Asia/Shanghai'
  }).replace(/\//g, '-');
  
  const stateIcons = { active: '🟢', paused: '⏸️', blocked: '🔴' };
  
  let output = `# FOCUS.md - 当前聚焦\n\n`;
  output += `🎯 **Focus Point**: ${focusPoint || '无'}\n\n`;
  output += `**Started:** ${new Date().toISOString().split('T')[0]}\n`;
  output += `**Status:** ${stateIcons[status] || '🟢'} ${status}\n\n`;
  
  if (todos.length > 0) {
    output += `📝 TODOs\n`;
    todos.forEach(todo => {
      const icon = todo.done ? '✅' : '☐';
      output += `${icon} ${todo.content}\n`;
    });
    output += `\n`;
  }
  
  output += `📖 Context\n`;
  output += context || '无\n';
  output += `\n---\n*最后更新: ${now}*\n`;
  
  return output;
}

// 解析现有 FOCUS.md
function parseFocus() {
  if (!fs.existsSync(FOCUS_PATH)) return null;
  
  const content = fs.readFileSync(FOCUS_PATH, 'utf8');
  const lines = content.split('\n');
  
  const result = {
    focusPoint: '',
    status: 'active',
    started: '',
    todos: [],
    context: ''
  };
  
  let inContext = false;
  
  for (const line of lines) {
    const focusMatch = line.match(/^🎯 \*\*Focus Point\*\*[:\s]*(.+)/);
    if (focusMatch) result.focusPoint = focusMatch[1].trim();
    
    const statusMatch = line.match(/active|paused|blocked/);
    if (line.includes('Status:') && statusMatch) result.status = statusMatch[0];
    
    const todoMatch = line.match(/^[✅☐]\s+(.+)/);
    if (todoMatch) {
      result.todos.push({
        done: line.startsWith('✅'),
        content: todoMatch[1].trim()
      });
    }
    
    if (line.startsWith('📖 Context')) {
      inContext = true;
      continue;
    }
    if (inContext && line.startsWith('---')) inContext = false;
    if (inContext && !line.startsWith('📖')) {
      result.context += line + '\n';
    }
  }
  
  result.context = result.context.trim() || '无';
  return result;
}

// 归档到 FOCUS-LOG.md
function archive(outcome) {
  const data = parseFocus();
  if (!data || !data.focusPoint || data.focusPoint === '无') {
    console.error('❌ No valid Focus Point found');
    process.exit(1);
  }
  
  const completed = new Date().toISOString();
  const completedDate = completed.split('T')[0];
  const allCompleted = data.todos.length > 0 && data.todos.every(t => t.done);
  const statusEmoji = allCompleted ? '✅' : '⏸️';
  const archiveType = allCompleted ? 'COMPLETED' : 'ARCHIVED';
  
  const entry = `\n## ${statusEmoji} ${data.focusPoint} — ${archiveType} ${completedDate}\n**Started:** ${data.started || completedDate}\n**Outcome:** ${outcome || '任务完成'}\n**Status:** ${allCompleted ? '全部完成' : '未完成'}\n`;
  
  if (!fs.existsSync(FOCUS_LOG_PATH)) {
    fs.writeFileSync(FOCUS_LOG_PATH, '# Focus Log\n');
  }
  fs.appendFileSync(FOCUS_LOG_PATH, entry);
  
  // 清空 FOCUS.md
  fs.writeFileSync(FOCUS_PATH, generateFocus('无', [], '', 'active'));
  
  console.log(`${statusEmoji} Archived: ${data.focusPoint}`);
}

// 命令处理
switch (command) {
  case 'init':
    const focusPoint = args.slice(1).join(' ') || '新项目';
    fs.writeFileSync(FOCUS_PATH, generateFocus(focusPoint, [], '', 'active'));
    console.log('✅ FOCUS.md created:', focusPoint);
    break;
    
  case 'add-todo':
    const data = parseFocus();
    if (!data) {
      console.error('❌ No FOCUS.md found. Run "init" first.');
      process.exit(1);
    }
    data.todos.push({ done: false, content: args.slice(1).join(' ') });
    fs.writeFileSync(FOCUS_PATH, generateFocus(data.focusPoint, data.todos, data.context, data.status));
    console.log('✅ Todo added');
    break;
    
  case 'done':
    const idx = parseInt(args[1]) - 1;
    const d = parseFocus();
    if (!d || !d.todos[idx]) {
      console.error('❌ Todo not found');
      process.exit(1);
    }
    d.todos[idx].done = true;
    fs.writeFileSync(FOCUS_PATH, generateFocus(d.focusPoint, d.todos, d.context, d.status));
    console.log('✅ Todo marked done');
    break;
    
  case 'status':
    const newStatus = args[1];
    if (!['active', 'paused', 'blocked'].includes(newStatus)) {
      console.error('❌ Invalid status');
      process.exit(1);
    }
    const s = parseFocus();
    if (!s) {
      console.error('❌ No FOCUS.md found');
      process.exit(1);
    }
    fs.writeFileSync(FOCUS_PATH, generateFocus(s.focusPoint, s.todos, s.context, newStatus));
    console.log('✅ Status updated:', newStatus);
    break;
    
  case 'archive':
    archive(args.slice(1).join(' '));
    break;
    
  default:
    console.log(`
🎯 Focus Tree

Usage: node scripts/focus.mjs <command> [options]

Commands:
  init "Focus Point"    初始化 FOCUS.md
  add-todo "task"       添加 TODO
  done <n>              标记第 n 个任务完成
  status <state>        设置状态 (active/paused/blocked)
  archive "outcome"     归档到 FOCUS-LOG.md

All operations ensure consistent file formatting.
`);
}