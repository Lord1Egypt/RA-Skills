#!/usr/bin/env node

/**
 * Agent Work Visibility - CLI Monitor
 * 
 * Usage:
 *   agent-visibility create <task-id> <title> [type]
 *   agent-visibility status <task-id> [--full]
 *   agent-visibility phase <task-id> <phase> <action> [--progress N]
 *   agent-visibility block <task-id> <type> <reason> [--level low|medium|high]
 *   agent-visibility ask <task-id> <type> <question> [--options A,B,C]
 *   agent-visibility list
 *   agent-visibility clear <task-id>
 *   agent-visibility clear --all
 */

const { TaskVisibilityManager } = require('../lib/index');
const path = require('path');
const fs = require('fs');

// ==================== 状态文件管理 ====================

const STATE_FILE = path.join(__dirname, '../.visibility-state.json');

function loadState() {
  if (fs.existsSync(STATE_FILE)) {
    const data = fs.readFileSync(STATE_FILE, 'utf8');
    return JSON.parse(data);
  }
  return { tasks: {} };
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), 'utf8');
}

// ==================== 命令处理 ====================

const commands = {
  create: (args) => {
    const [taskId, title, type = 'research'] = args;
    
    if (!taskId || !title) {
      console.error('Usage: agent-visibility create <task-id> <title> [type]');
      process.exit(1);
    }
    
    const state = loadState();
    const manager = new TaskVisibilityManager();
    
    // 从现有状态恢复
    if (state.tasks[taskId]) {
      console.log(`⚠️  任务 ${taskId} 已存在`);
      console.log(manager.getDefaultView(taskId));
      return;
    }
    
    // 创建新任务
    manager.createTask(taskId, title, type);
    state.tasks[taskId] = manager.getTask(taskId);
    saveState(state);
    
    console.log(`✅ 任务已创建：${taskId}`);
    console.log('');
    console.log(manager.getDefaultView(taskId));
  },

  status: (args) => {
    const taskId = args[0];
    const full = args.includes('--full');
    
    if (!taskId) {
      console.error('Usage: agent-visibility status <task-id> [--full]');
      process.exit(1);
    }
    
    const state = loadState();
    if (!state.tasks[taskId]) {
      console.error(`❌ 任务不存在：${taskId}`);
      process.exit(1);
    }
    
    const manager = new TaskVisibilityManager();
    // 恢复状态
    manager.tasks.set(taskId, state.tasks[taskId]);
    
    if (full) {
      console.log(manager.getFullView(taskId));
    } else {
      console.log(manager.getDefaultView(taskId));
    }
  },

  phase: (args) => {
    const taskId = args[0];
    const phaseName = args[1];
    const action = args[2];
    
    if (!taskId || !phaseName || !action) {
      console.error('Usage: agent-visibility phase <task-id> <phase> <action> [--progress N]');
      console.error('Actions: start | update | complete');
      process.exit(1);
    }
    
    const state = loadState();
    if (!state.tasks[taskId]) {
      console.error(`❌ 任务不存在：${taskId}`);
      process.exit(1);
    }
    
    const manager = new TaskVisibilityManager();
    manager.tasks.set(taskId, state.tasks[taskId]);
    
    const progressMatch = args.find(a => a.startsWith('--progress='));
    const progress = progressMatch ? parseInt(progressMatch.split('=')[1]) : null;
    
    switch (action) {
      case 'start':
        manager.startPhase(taskId, phaseName);
        console.log(`✅ 阶段已启动：${phaseName}`);
        break;
        
      case 'update':
        if (progress === null) {
          console.error('需要指定 --progress=N');
          process.exit(1);
        }
        manager.updatePhaseProgress(taskId, phaseName, progress);
        console.log(`✅ 进度已更新：${phaseName} ${progress}%`);
        break;
        
      case 'complete':
        const summary = args.find(a => a.startsWith('--summary='))?.split('=')[1] || null;
        manager.completePhase(taskId, phaseName, summary);
        console.log(`✅ 阶段已完成：${phaseName}`);
        break;
        
      default:
        console.error(`未知操作：${action}`);
        process.exit(1);
    }
    
    state.tasks[taskId] = manager.getTask(taskId);
    saveState(state);
    console.log('');
    console.log(manager.getDefaultView(taskId));
  },

  block: (args) => {
    const taskId = args[0];
    const blockerType = args[1];
    const reason = args[2];
    
    if (!taskId || !blockerType || !reason) {
      console.error('Usage: agent-visibility block <task-id> <type> <reason> [--level low|medium|high]');
      process.exit(1);
    }
    
    const state = loadState();
    if (!state.tasks[taskId]) {
      console.error(`❌ 任务不存在：${taskId}`);
      process.exit(1);
    }
    
    const manager = new TaskVisibilityManager();
    manager.tasks.set(taskId, state.tasks[taskId]);
    
    const levelMatch = args.find(a => a.startsWith('--level='));
    const level = levelMatch ? levelMatch.split('=')[1] : 'low';
    
    manager.block(taskId, blockerType, reason, level);
    
    state.tasks[taskId] = manager.getTask(taskId);
    saveState(state);
    
    console.log(`⚠️  阻塞已报告：${reason}`);
    console.log('');
    console.log(manager.getDefaultView(taskId));
  },

  ask: (args) => {
    const taskId = args[0];
    const inputType = args[1];
    const question = args[2];
    
    if (!taskId || !inputType || !question) {
      console.error('Usage: agent-visibility ask <task-id> <type> <question> [--options A,B,C]');
      process.exit(1);
    }
    
    const state = loadState();
    if (!state.tasks[taskId]) {
      console.error(`❌ 任务不存在：${taskId}`);
      process.exit(1);
    }
    
    const manager = new TaskVisibilityManager();
    manager.tasks.set(taskId, state.tasks[taskId]);
    
    const optionsMatch = args.find(a => a.startsWith('--options='));
    const options = optionsMatch ? optionsMatch.split('=')[1].split(',') : [];
    
    manager.ask(taskId, inputType, question, options);
    
    state.tasks[taskId] = manager.getTask(taskId);
    saveState(state);
    
    console.log(`🙋 用户介入请求已创建`);
    console.log('');
    console.log(manager.getDefaultView(taskId));
  },

  list: () => {
    const state = loadState();
    const taskIds = Object.keys(state.tasks);
    
    if (taskIds.length === 0) {
      console.log('暂无任务');
      return;
    }
    
    console.log(`当前任务 (${taskIds.length}个):\n`);
    
    for (const taskId of taskIds) {
      const task = state.tasks[taskId];
      const icon = task.needs_user_input ? '⚠️' : 
                   task.blocker_status !== 'none' ? '🔴' :
                   task.overall_status === 'completed' ? '✅' :
                   task.overall_status === 'failed' ? '❌' : '🟢';
      
      console.log(`${icon} ${taskId}: ${task.task_title}`);
      console.log(`   状态：${task.overall_status} | 阶段：${task.current_phase || '-'} | 进度：${task.progress_percent}%`);
      console.log('');
    }
  },

  clear: (args) => {
    const state = loadState();
    
    if (args.includes('--all')) {
      state.tasks = {};
      saveState(state);
      console.log('✅ 已清空所有任务');
      return;
    }
    
    const taskId = args[0];
    if (!taskId) {
      console.error('Usage: agent-visibility clear <task-id> | --all');
      process.exit(1);
    }
    
    if (!state.tasks[taskId]) {
      console.error(`❌ 任务不存在：${taskId}`);
      process.exit(1);
    }
    
    delete state.tasks[taskId];
    saveState(state);
    console.log(`✅ 任务已清除：${taskId}`);
  },

  help: () => {
    console.log(`
Agent Work Visibility CLI v2.0.0

Usage:
  agent-visibility <command> [arguments]

Commands:
  create <task-id> <title> [type]           创建新任务
  status <task-id> [--full]                 查看任务状态
  phase <task-id> <phase> <action>          管理阶段
  block <task-id> <type> <reason> [--level] 报告阻塞
  ask <task-id> <type> <question>           请求用户介入
  list                                      列出所有任务
  clear <task-id> | --all                   清除任务
  help                                      显示帮助

Examples:
  agent-visibility create task-001 "调研 AI 项目" research
  agent-visibility status task-001 --full
  agent-visibility phase task-001 收集信息 start
  agent-visibility phase task-001 收集信息 update --progress=50
  agent-visibility phase task-001 收集信息 complete --summary="已收集 10 个数据"
  agent-visibility block task-001 api_timeout "API 响应超时" --level=medium
  agent-visibility ask task-001 direction_choice "优先看哪个方向？" --options="A,B,C"
  agent-visibility list
  agent-visibility clear task-001
  agent-visibility clear --all
`);
  }
};

// ==================== 主程序 ====================

const command = process.argv[2] || 'help';
const args = process.argv.slice(3);

if (commands[command]) {
  commands[command](args);
} else {
  console.error(`未知命令：${command}`);
  console.log('运行 agent-visibility help 查看帮助');
  process.exit(1);
}
