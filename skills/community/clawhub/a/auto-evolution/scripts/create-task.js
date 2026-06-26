#!/usr/bin/env node

/**
 * Auto Revolution Task Creator
 * 创建任务并自动评估复杂度，决定使用手动或自动 Subtask 模式
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const TASKS_DIR = path.join(__dirname, '../tasks');

// 创建 readline 接口
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// 提示函数
function prompt(question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
    });
  });
}

// 复杂度评分
async function assessComplexity() {
  console.log('\n📊 任务复杂度评估（1-5 分）\n');
  
  const codeLines = parseInt(await prompt('1. 代码量预估:\n   1=<100 行，2=100-200 行，3=200-500 行，4=500-1000 行，5=>1000 行\n   评分：'), 10);
  const files = parseInt(await prompt('2. 修改文件数:\n   1=1-2 个，2=3-5 个，3=5-10 个，4=10-20 个，5=>20 个\n   评分：'), 10);
  const risk = parseInt(await prompt('3. 风险等级:\n   1=文档/测试，2=小功能，3=功能改进，4=核心功能，5=架构变更\n   评分：'), 10);
  const dependencies = parseInt(await prompt('4. 依赖复杂度:\n   1=无依赖，2=1-2 个依赖，3=3-5 个依赖，4=跨模块，5=跨系统\n   评分：'), 10);
  const innovation = parseInt(await prompt('5. 创新程度:\n   1=常规修复，2=小改进，3=功能增强，4=新功能，5=创新功能\n   评分：'), 10);
  
  const total = codeLines + files + risk + dependencies + innovation;
  
  let mode, taskType;
  if (total <= 10) {
    mode = 'manual';
    taskType = '简单任务';
  } else if (total >= 18) {
    mode = 'auto';
    taskType = '复杂任务';
  } else {
    const choice = await prompt(`\n总分 ${total} 分，属于中等任务。\n请选择模式：\n   1=manual（手动 Subtask，推荐）\n   2=auto（自动 Subtask）\n   选择（1/2）：`);
    mode = choice === '2' ? 'auto' : 'manual';
    taskType = mode === 'auto' ? '复杂任务' : '简单任务';
  }
  
  return {
    code_lines: codeLines,
    files: files,
    risk: risk,
    dependencies: dependencies,
    innovation: innovation,
    total: total,
    mode: mode,
    task_type: taskType
  };
}

// 生成任务 ID
function generateTaskId() {
  const files = fs.readdirSync(TASKS_DIR);
  const ids = files
    .filter(f => f.match(/task-\d+\.json/))
    .map(f => parseInt(f.match(/task-(\d+)\.json/)[1], 10));
  return Math.max(0, ...ids) + 1;
}

// 创建手动 Subtask
async function createManualSubtasks() {
  console.log('\n📝 创建 Subtasks（输入空行结束）\n');
  
  const subtasks = [];
  let index = 0;
  
  while (true) {
    const title = await prompt(`Subtask ${index} 标题（空行结束）：`);
    if (!title) break;
    
    const description = await prompt('描述：');
    
    subtasks.push({
      id: index,
      title: title,
      description: description
    });
    
    index++;
  }
  
  return subtasks;
}

// 生成任务 JSON
function generateTaskJson(taskId, title, description, complexity, subtasks, reviewerModel) {
  const task = {
    task_id: taskId,
    title: title,
    description: description,
    status: 'pending',
    priority: 'P1',
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
    current_iteration: 0,
    max_iterations: 3,
    depends_on: [],
    reference_files: [],
    subtasks: subtasks,
    history: [],
    result: null
  };
  
  if (complexity.mode === 'auto') {
    task.complexity = complexity;
    task.reviewer = {
      model: reviewerModel || 'anthropic/claude-sonnet-4-6',
      instructions: '请分析此任务并生成详细的 subtasks'
    };
    task.status = 'pending_review';
  } else {
    task.complexity = complexity;
  }
  
  return task;
}

// 主函数
async function main() {
  console.log('🤖 Auto Revolution Task Creator\n');
  
  // 确保任务目录存在
  if (!fs.existsSync(TASKS_DIR)) {
    fs.mkdirSync(TASKS_DIR, { recursive: true });
  }
  
  // 基本信息
  const title = await prompt('任务标题：');
  const description = await prompt('任务描述：');
  
  // 复杂度评估
  const complexity = await assessComplexity();
  
  console.log(`\n✅ 任务类型：${complexity.task_type}`);
  console.log(`✅ 模式：${complexity.mode === 'manual' ? '手动 Subtask' : '自动 Subtask'}\n`);
  
  // 创建 Subtasks
  let subtasks = [];
  if (complexity.mode === 'manual') {
    subtasks = await createManualSubtasks();
  }
  
  // Reviewer 模型（仅复杂任务）
  let reviewerModel;
  if (complexity.mode === 'auto') {
    reviewerModel = await prompt('Reviewer 模型（默认：anthropic/claude-sonnet-4-6）：') || 'anthropic/claude-sonnet-4-6';
  }
  
  // 生成任务
  const taskId = generateTaskId();
  const taskJson = generateTaskJson(taskId, title, description, complexity, subtasks, reviewerModel);
  
  // 保存任务
  const taskFile = path.join(TASKS_DIR, `task-${taskId}.json`);
  fs.writeFileSync(taskFile, JSON.stringify(taskJson, null, 2), 'utf8');
  
  console.log(`\n✅ 任务创建成功！`);
  console.log(`📁 文件位置：${taskFile}`);
  console.log(`📊 复杂度评分：${complexity.total}/25`);
  console.log(`🤖 模式：${complexity.mode === 'manual' ? '手动 Subtask' : '自动 Subtask'}`);
  console.log(`📝 Subtasks 数量：${subtasks.length}`);
  
  if (complexity.mode === 'auto') {
    console.log(`\n⏳ 下一步：启动 Reviewer 分析任务并生成详细 Subtasks`);
    console.log(`   命令：node scripts/start-reviewer.js ${taskId}`);
  } else {
    console.log(`\n⏳ 下一步：启动 Executor 执行任务`);
    console.log(`   命令：node scripts/start-executor.js ${taskId}`);
  }
  
  rl.close();
}

// 运行
main().catch(console.error);
