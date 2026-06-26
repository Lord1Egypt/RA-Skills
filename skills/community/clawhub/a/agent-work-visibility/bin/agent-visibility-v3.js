#!/usr/bin/env node

/**
 * Agent Work Visibility CLI v3.0
 * 
 * 简化版：支持自定义阶段名称，适用于所有任务类型
 * 
 * Usage:
 *   agent-visibility-v3 create <task-id> <title> [type]
 *   agent-visibility-v3 status <task-id>
 *   agent-visibility-v3 update <task-id> <phase> <progress> [action]
 *   agent-visibility-v3 complete <task-id>
 *   agent-visibility-v3 block <task-id> <reason>
 *   agent-visibility-v3 clear <task-id>
 */

const path = require('path');
const fs = require('fs');

// ==================== 状态文件管理 ====================

const STATE_FILE = path.join(__dirname, '../.visibility-state-v3.json');

function loadState() {
  if (fs.existsSync(STATE_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
    } catch (e) {
      return { tasks: {} };
    }
  }
  return { tasks: {} };
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), 'utf8');
}

// ==================== 进度条生成器 ====================

function generateProgressBar(progress, width = 20) {
  const filled = Math.floor((progress / 100) * width);
  const empty = width - filled;
  return `[${'█'.repeat(filled)}${'░'.repeat(empty)}] ${progress}%`;
}

// ==================== 状态展示 ====================

function renderStatus(task) {
  const statusIcon = task.status === 'completed' ? '🟢' : task.blocked ? '🟡' : '🟢';
  const healthIcon = task.health >= 80 ? '🟢' : task.health >= 60 ? '🟡' : '🟠';
  const healthText = task.health >= 80 ? '健康' : task.health >= 60 ? '轻微延迟' : '注意';
  
  const elapsed = Math.floor((Date.now() - task.startTime) / 60000);
  
  let output = `${statusIcon} ${task.title}
━━━━━━━━━━━━━━━━━━━
进度：${generateProgressBar(task.progress)} (${task.currentStep}/${task.totalSteps})
━━━━━━━━━━━━━━━━━━━
健康度：${healthIcon} ${healthText} (${task.health}/100)
当前阶段：${task.phase}
正在做什么：${task.action}
已运行：${elapsed} 分钟`;

  if (task.blocked) {
    output += `\n为什么还没完成：${task.blockReason}`;
  }

  return output;
}

// ==================== 命令处理 ====================

const commands = {
  create: (args) => {
    const [taskId, title, type = 'research'] = args;
    
    if (!taskId || !title) {
      console.error('Usage: agent-visibility-v3 create <task-id> "<title>" [type]');
      process.exit(1);
    }
    
    const state = loadState();
    
    if (state.tasks[taskId]) {
      console.log(`⚠️  任务 ${taskId} 已存在`);
      console.log(renderStatus(state.tasks[taskId]));
      return;
    }
    
    // 创建任务
    state.tasks[taskId] = {
      id: taskId,
      title: title,
      type: type,
      status: 'running',
      progress: 0,
      currentStep: 1,
      totalSteps: 4,  // 默认 4 步
      phase: '初始化',
      action: '任务已启动',
      health: 100,
      blocked: false,
      blockReason: null,
      startTime: Date.now(),
      updatedAt: Date.now()
    };
    
    saveState(state);
    
    console.log(`✅ 任务已创建：${taskId}`);
    console.log('');
    console.log(renderStatus(state.tasks[taskId]));
  },

  status: (args) => {
    const [taskId] = args;
    const state = loadState();
    
    if (!taskId) {
      // 列出所有任务
      const ids = Object.keys(state.tasks);
      if (ids.length === 0) {
        console.log('暂无任务');
      } else {
        console.log('当前任务：');
        ids.forEach(id => {
          const t = state.tasks[id];
          console.log(`  ${t.status === 'completed' ? '✅' : '🟢'} ${id}: ${t.title} (${t.progress}%)`);
        });
      }
      return;
    }
    
    if (!state.tasks[taskId]) {
      console.error(`❌ 任务不存在：${taskId}`);
      process.exit(1);
    }
    
    console.log(renderStatus(state.tasks[taskId]));
  },

  update: (args) => {
    const [taskId, phase, progressStr, action] = args;
    
    if (!taskId || !phase || !progressStr) {
      console.error('Usage: agent-visibility-v3 update <task-id> <phase> <progress> [action]');
      process.exit(1);
    }
    
    const state = loadState();
    
    if (!state.tasks[taskId]) {
      console.error(`❌ 任务不存在：${taskId}`);
      process.exit(1);
    }
    
    const task = state.tasks[taskId];
    const progress = parseInt(progressStr, 10);
    
    if (isNaN(progress) || progress < 0 || progress > 100) {
      console.error('❌ 进度必须是 0-100 的数字');
      process.exit(1);
    }
    
    // 更新任务
    task.phase = phase;
    task.progress = progress;
    task.currentStep = Math.ceil((progress / 100) * task.totalSteps);
    task.action = action || `正在${phase}`;
    task.updatedAt = Date.now();
    
    // 健康度根据进度更新
    if (progress >= 100) {
      task.status = 'completed';
      task.health = 100;
    }
    
    saveState(state);
    
    console.log(`✅ 已更新：${taskId}`);
    console.log('');
    console.log(renderStatus(task));
  },

  complete: (args) => {
    const [taskId] = args;
    
    if (!taskId) {
      console.error('Usage: agent-visibility-v3 complete <task-id>');
      process.exit(1);
    }
    
    const state = loadState();
    
    if (!state.tasks[taskId]) {
      console.error(`❌ 任务不存在：${taskId}`);
      process.exit(1);
    }
    
    const task = state.tasks[taskId];
    task.status = 'completed';
    task.progress = 100;
    task.currentStep = task.totalSteps;
    task.phase = '已完成';
    task.action = '任务完成';
    task.health = 100;
    task.blocked = false;
    task.updatedAt = Date.now();
    
    saveState(state);
    
    console.log(`✅ 任务完成：${taskId}`);
    console.log('');
    console.log(renderStatus(task));
  },

  block: (args) => {
    const [taskId, reason] = args;
    
    if (!taskId || !reason) {
      console.error('Usage: agent-visibility-v3 block <task-id> "<reason>"');
      process.exit(1);
    }
    
    const state = loadState();
    
    if (!state.tasks[taskId]) {
      console.error(`❌ 任务不存在：${taskId}`);
      process.exit(1);
    }
    
    const task = state.tasks[taskId];
    task.blocked = true;
    task.blockReason = reason;
    task.health = Math.max(40, task.health - 20);
    task.updatedAt = Date.now();
    
    saveState(state);
    
    console.log(`⚠️  任务阻塞：${taskId}`);
    console.log('');
    console.log(renderStatus(task));
  },

  clear: (args) => {
    const [taskId] = args;
    const state = loadState();
    
    if (taskId === '--all') {
      state.tasks = {};
      saveState(state);
      console.log('✅ 已清除所有任务');
      return;
    }
    
    if (!taskId) {
      console.error('Usage: agent-visibility-v3 clear <task-id> | --all');
      process.exit(1);
    }
    
    if (!state.tasks[taskId]) {
      console.error(`❌ 任务不存在：${taskId}`);
      process.exit(1);
    }
    
    delete state.tasks[taskId];
    saveState(state);
    
    console.log(`✅ 已清除：${taskId}`);
  },

  help: () => {
    console.log(`
Agent Work Visibility CLI v3.0

Usage:
  agent-visibility-v3 <command> [arguments]

Commands:
  create <task-id> "<title>" [type]    创建新任务
  status [task-id]                     查看任务状态
  update <task-id> <phase> <progress>  更新进度
  complete <task-id>                   完成任务
  block <task-id> "<reason>"           报告阻塞
  clear <task-id> | --all              清除任务

Examples:
  agent-visibility-v3 create task-001 "查询 BNB MemeCoin Top3" api
  agent-visibility-v3 status task-001
  agent-visibility-v3 update task-001 "连接 API" 25 "正在获取数据"
  agent-visibility-v3 update task-001 "数据处理" 50 "正在解析结果"
  agent-visibility-v3 complete task-001
  agent-visibility-v3 block task-001 "API 响应超时"
  agent-visibility-v3 clear task-001
`);
  }
};

// ==================== 主入口 ====================

const args = process.argv.slice(2);
const command = args[0];

if (!command || !commands[command]) {
  commands.help();
  process.exit(1);
}

commands[command](args.slice(1));
