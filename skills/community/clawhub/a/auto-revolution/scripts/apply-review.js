#!/usr/bin/env node
/**
 * apply-review.js - 应用 Sonnet 审阅结果到任务文件
 * 
 * 用法：node apply-review.js <task-id> '<review-json>'
 * 
 * 或者从文件读取：node apply-review.js <task-id> --file <review.json>
 */

const fs = require('fs');
const path = require('path');

const TASKS_DIR = path.join(__dirname, '..', 'tasks');
const LOGS_DIR = path.join(__dirname, '..', 'logs');
const SCRIPTS_DIR = path.join(__dirname, '..');
const EVENTS_LOG = path.join(LOGS_DIR, 'events.log');

/**
 * 写入事件日志
 */
function logEvent(event, data = {}) {
  const entry = {
    timestamp: new Date().toISOString(),
    event,
    ...data
  };
  fs.appendFileSync(EVENTS_LOG, JSON.stringify(entry) + '\n');
  console.log(`📝 事件：${event}`, JSON.stringify(data));
  return entry;
}

/**
 * 读取任务文件
 */
function readTask(taskId) {
  const taskFile = path.join(TASKS_DIR, `${taskId}.json`);
  if (!fs.existsSync(taskFile)) {
    return null;
  }
  return JSON.parse(fs.readFileSync(taskFile, 'utf8'));
}

/**
 * 写入任务文件
 */
function writeTask(task) {
  const taskFile = path.join(TASKS_DIR, `${task.task_id}.json`);
  fs.writeFileSync(taskFile, JSON.stringify(task, null, 2));
}

// 主程序
const args = process.argv.slice(2);
const taskId = args[0];

if (!taskId) {
  console.log('用法：');
  console.log('  node apply-review.js <task-id> \'<review-json>\'');
  console.log('  node apply-review.js <task-id> --file <review.json>');
  console.log('  node apply-review.js <task-id> --stdin  # 从 stdin 读取 JSON');
  console.log('');
  console.log('示例：');
  console.log('  node apply-review.js task-010 --file review-result.json');
  console.log('  cat review-result.json | node apply-review.js task-010 --stdin');
  process.exit(0);
}

const task = readTask(taskId);

if (!task) {
  console.error(`❌ 任务不存在：${taskId}`);
  process.exit(1);
}

// 解析 review JSON
let review;

if (args.includes('--file')) {
  const fileIndex = args.indexOf('--file');
  const reviewFile = args[fileIndex + 1];
  
  if (!reviewFile) {
    console.error('❌ 缺少文件名');
    process.exit(1);
  }
  
  if (!fs.existsSync(reviewFile)) {
    console.error(`❌ 文件不存在：${reviewFile}`);
    process.exit(1);
  }
  
  try {
    review = JSON.parse(fs.readFileSync(reviewFile, 'utf8'));
  } catch (error) {
    console.error('❌ JSON 解析失败:', error.message);
    process.exit(1);
  }
} else if (args.includes('--stdin')) {
  // 从 stdin 读取 JSON（避免命令行引号转义问题）
  const input = fs.readFileSync(0, 'utf8');
  
  try {
    review = JSON.parse(input);
  } catch (error) {
    console.error('❌ JSON 解析失败:', error.message);
    process.exit(1);
  }
} else {
  // 从命令行参数读取 JSON
  const reviewJson = args.slice(1).join(' ');
  
  try {
    review = JSON.parse(reviewJson);
  } catch (error) {
    console.error('❌ JSON 解析失败:', error.message);
    console.error('提示：如果 JSON 包含引号，建议使用 --file 或 --stdin 方式');
    console.error('示例：node apply-review.js task-010 --file review.json');
    console.error('      cat review.json | node apply-review.js task-010 --stdin');
    process.exit(1);
  }
}

// 验证必要字段
if (!review.verdict) {
  console.error('❌ 缺少 verdict 字段');
  process.exit(1);
}

if (!['approve', 'revise', 'reject', 'complete'].includes(review.verdict)) {
  console.error(`❌ 无效的 verdict: ${review.verdict}`);
  process.exit(1);
}

console.log(`📝 应用审阅结果到 ${taskId}...`);
console.log(`Verdict: ${review.verdict}`);

// 更新任务
const oldStatus = task.status;
task.review = review;
task.updated_at = new Date().toISOString();

// 根据 verdict 更新状态
if (review.verdict === 'complete') {
  task.status = 'completed';
  task.completed_at = task.updated_at;
  console.log('✅ 任务完成！');
} else if (review.verdict === 'reject') {
  task.current_iteration = (task.current_iteration || 0) + 1;
  if (task.current_iteration >= task.max_iterations) {
    task.status = 'failed';
    console.log('❌ 达到最大迭代次数，任务失败');
  } else {
    task.status = 'pending';
    console.log('🔄 重新执行（iteration +1）');
  }
} else {
  // approve 或 revise → reviewed，等待 executor-agent 执行
  task.status = 'reviewed';
  console.log('⏳ 等待 executor-agent 执行');
}

// 记录到 history
task.history = task.history || [];
task.history.push({
  timestamp: task.updated_at,
  action: 'review_applied',
  verdict: review.verdict,
  confidence: review.confidence,
  feedback: review.feedback,
  model: 'advanced-model/sonnet'
});

writeTask(task);

logEvent('review_applied', {
  task_id: taskId,
  from: oldStatus,
  to: task.status,
  verdict: review.verdict,
  model: 'advanced-model/sonnet'
});

console.log('');
console.log('✅ 审阅结果已应用');
console.log(`   状态：${oldStatus} → ${task.status}`);
console.log(`   Feedback: ${review.feedback}`);

if (review.next_instructions) {
  console.log('');
  console.log('📋 Next Instructions:');
  console.log('-'.repeat(50));
  console.log(review.next_instructions);
  console.log('-'.repeat(50));
}

console.log('');
console.log('下一步：');
if (task.status === 'reviewed') {
  console.log('  运行 executor-agent 心跳执行指令：');
  console.log('  node scripts/iron-heartbeat.js');
} else if (task.status === 'pending') {
  console.log('  重新触发审阅：');
  console.log('  node scripts/trigger-review.js ' + taskId);
}
