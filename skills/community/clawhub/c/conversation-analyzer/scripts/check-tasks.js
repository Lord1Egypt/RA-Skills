#!/usr/bin/env node
/**
 * 未完成任务检查脚本
 * 检查未完成任务并发送 Feishu 通知
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');
const HEARTBEAT_FILE = path.join(WORKSPACE, 'HEARTBEAT.md');
const MEMORY_FILE = path.join(WORKSPACE, 'MEMORY.md');
const WORKING_FILE = path.join(WORKSPACE, 'WORKING.md');

/**
 * 读取文件内容
 */
function readFile(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      return fs.readFileSync(filePath, 'utf-8');
    }
  } catch (e) {
    console.error(`读取失败: ${filePath}`, e.message);
  }
  return '';
}

/**
 * 解析 HEARTBEAT.md 中的任务看板
 */
function parseHeartbeatTasks(content) {
  const tasks = [];
  const lines = content.split('\n');
  let inTable = false;
  
  for (const line of lines) {
    if (line.includes('| 任务ID |') || line.includes('| TaskID |')) {
      inTable = true;
      continue;
    }
    if (inTable && line.startsWith('|') && !line.includes('---')) {
      const cells = line.split('|').map(c => c.trim()).filter(c => c);
      if (cells.length >= 4 && cells[0] !== '任务ID' && cells[0] !== 'TaskID') {
        const status = cells[2];
        if (status !== 'Done' && status !== 'Aborted') {
          tasks.push({
            id: cells[0],
            name: cells[1],
            status: status,
            progress: cells[3],
            deadline: cells[4] || '',
            source: 'HEARTBEAT'
          });
        }
      }
    }
  }
  
  return tasks;
}

/**
 * 解析 WORKING.md 中的任务
 */
function parseWorkingTasks(content) {
  const tasks = [];
  // 简单匹配任务标题
  const taskMatches = content.match(/###?\s*(T\d+|任务\d+)[\s\S]*?(?=###?\s*(T\d+|任务\d+)|$)/g) || [];
  
  taskMatches.forEach(match => {
    const idMatch = match.match(/###?\s*(T\d+|任务\d+)/);
    const statusMatch = match.match(/状态[:：]\s*(\w+)/);
    
    if (idMatch) {
      const status = statusMatch ? statusMatch[1] : 'Unknown';
      if (status !== 'Done' && status !== 'Aborted') {
        tasks.push({
          id: idMatch[1],
          content: match.substring(0, 100),
          status: status,
          source: 'WORKING'
        });
      }
    }
  });
  
  return tasks;
}

/**
 * 检查 MEMORY.md 中标记为 NotNeeded 的任务
 */
function getNotNeededTasks(content) {
  const notNeeded = [];
  // 匹配标记为不需要完成的任务
  const matches = content.match(/任务[:：]\s*([^\n]+).*?不需要完成|NotNeeded[:：]\s*([^\n]+)/g) || [];
  
  matches.forEach(match => {
    const taskMatch = match.match(/任务[:：]\s*([^\n]+)/);
    if (taskMatch) {
      notNeeded.push(taskMatch[1].trim());
    }
  });
  
  return notNeeded;
}

/**
 * 主检查函数
 */
async function main() {
  console.log('✅ 未完成任务检查启动...\n');
  
  // 1. 读取文件
  const heartbeat = readFile(HEARTBEAT_FILE);
  const working = readFile(WORKING_FILE);
  const memory = readFile(MEMORY_FILE);
  
  // 2. 解析任务
  const heartbeatTasks = parseHeartbeatTasks(heartbeat);
  const workingTasks = parseWorkingTasks(working);
  const notNeededTasks = getNotNeededTasks(memory);
  
  console.log(`📊 HEARTBEAT.md 未完成任务: ${heartbeatTasks.length}`);
  console.log(`📊 WORKING.md 未完成任务: ${workingTasks.length}`);
  console.log(`📊 标记为不需要的任务: ${notNeededTasks.length}\n`);
  
  // 3. 过滤不需要的任务
  const allTasks = [...heartbeatTasks, ...workingTasks];
  const incompleteTasks = allTasks.filter(task => {
    return !notNeededTasks.some(nt => task.name?.includes(nt) || task.id?.includes(nt));
  });
  
  // 4. 输出结果
  if (incompleteTasks.length === 0) {
    console.log('✅ 未发现未完成的任务');
    console.log('\n📱 Feishu 通知内容：');
    console.log('   主题：任务检查完成');
    console.log('   内容：未发现未完成的任务');
    return {
      hasIncomplete: false,
      message: '未发现未完成的任务'
    };
  }
  
  console.log(`⚠️ 发现 ${incompleteTasks.length} 个未完成任务:\n`);
  incompleteTasks.forEach((task, i) => {
    console.log(`${i + 1}. [${task.status}] ${task.id}: ${task.name || task.content}`);
    if (task.deadline) {
      console.log(`   截止时间: ${task.deadline}`);
    }
  });
  
  console.log('\n📱 Feishu 通知内容：');
  console.log('   主题：未完成任务提醒');
  console.log(`   内容：发现 ${incompleteTasks.length} 个未完成任务，是否需要完成？`);
  console.log('   任务列表：');
  incompleteTasks.forEach(task => {
    console.log(`   - [${task.status}] ${task.id}: ${task.name || task.content.substring(0, 50)}`);
  });
  
  return {
    hasIncomplete: true,
    count: incompleteTasks.length,
    tasks: incompleteTasks,
    message: `发现 ${incompleteTasks.length} 个未完成任务，是否需要完成？`
  };
}

// 运行
main().then(result => {
  console.log('\n✅ 检查完成');
  process.exit(0);
}).catch(err => {
  console.error('❌ 检查失败:', err);
  process.exit(1);
});
