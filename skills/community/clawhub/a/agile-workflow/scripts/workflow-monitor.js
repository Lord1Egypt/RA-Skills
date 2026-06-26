#!/usr/bin/env node
/**
 * 敏捷工作流定时监控器
 * 
 * 功能：
 * 1. 每 10 分钟检查一次工作流状态
 * 2. 检查任务列表、任务分配、任务执行情况
 * 3. 检查各 Agent 的真实状态
 * 4. 发现问题自动修复
 * 5. 确保未完成所有任务前不闲置、不阻塞
 * 
 * 用法：node workflow-monitor.js <项目目录>
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const PROJECT_DIR = process.argv[2] || process.env.OPENCLAW_PROJECT_DIR || '.';
const LOG_FILE = path.join(path.dirname(PROJECT_DIR), 'logs/workflow-monitor.log');
const STATE_FILE = path.join(PROJECT_DIR, '.task-state.json');

// 配置
const CONFIG = {
  lockFileThreshold: 120000,      // 锁文件超过 2 分钟清理
  taskTimeout: 600000,            // 任务超过 10 分钟超时
  idleThreshold: 300000,          // 空闲超过 5 分钟触发任务
  maxConcurrentFailures: 5        // 连续失败阈值
};

// 确保日志目录
const logDir = path.dirname(LOG_FILE);
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

/**
 * 记录日志
 */
function log(message, level = 'INFO') {
  const timestamp = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  const logLine = `[${timestamp}] [${level}] ${message}\n`;
  console.log(logLine.trim());
  fs.appendFileSync(LOG_FILE, logLine);
}

/**
 * 加载任务状态
 */
function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
  } catch (e) {
    log('加载任务状态失败：' + e.message, 'ERROR');
    return null;
  }
}

/**
 * 保存任务状态
 */
function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

/**
 * 获取 Agent 状态
 */
async function getAgentStatus() {
  const agents = ['novel_writer', 'novel_architect', 'novel_editor'];
  const status = [];
  
  for (const agentId of agents) {
    const agentStatus = {
      id: agentId,
      pid: null,
      running: false,
      hasLock: false,
      lockAge: 0,
      health: 'unknown'
    };
    
    // 检查进程
    try {
      const procResult = await new Promise((resolve) => {
        exec(`ps aux | grep "${agentId}" | grep -v grep | grep -v "workflow-monitor" | head -1`, (error, stdout) => {
          resolve(stdout.trim());
        });
      });
      
      if (procResult) {
        const match = procResult.match(/\s+(\d+)\s+/);
        agentStatus.pid = match ? parseInt(match[1]) : null;
        agentStatus.running = true;
      }
    } catch (e) {
      // 忽略
    }
    
    // 检查锁文件
    const sessionDir = path.join('/home/ubutu/.openclaw/agents', agentId, 'sessions');
    if (fs.existsSync(sessionDir)) {
      const files = fs.readdirSync(sessionDir);
      const lockFiles = files.filter(f => f.endsWith('.lock'));
      
      if (lockFiles.length > 0) {
        agentStatus.hasLock = true;
        try {
          const lockStats = fs.statSync(path.join(sessionDir, lockFiles[0]));
          agentStatus.lockAge = Date.now() - lockStats.mtimeMs;
        } catch (e) {
          // 忽略
        }
      }
    }
    
    // 判断健康状态
    if (!agentStatus.running) {
      agentStatus.health = 'idle';
    } else if (agentStatus.hasLock && agentStatus.lockAge > CONFIG.lockFileThreshold) {
      agentStatus.health = 'stuck';
    } else {
      agentStatus.health = 'busy';
    }
    
    status.push(agentStatus);
  }
  
  return status;
}

/**
 * 清理锁文件
 */
async function cleanupLockFiles() {
  const agents = ['novel_writer', 'novel_architect', 'novel_editor', 'main'];
  let cleaned = 0;
  
  for (const agent of agents) {
    const sessionDir = path.join('/home/ubutu/.openclaw/agents', agent, 'sessions');
    if (!fs.existsSync(sessionDir)) continue;
    
    const files = fs.readdirSync(sessionDir);
    for (const file of files) {
      if (file.endsWith('.lock')) {
        const lockPath = path.join(sessionDir, file);
        try {
          const stats = fs.statSync(lockPath);
          const age = Date.now() - stats.mtimeMs;
          
          if (age > CONFIG.lockFileThreshold) {
            fs.unlinkSync(lockPath);
            log(`🧹 清理锁文件：${file} (年龄：${Math.round(age/1000)}s)`, 'INFO');
            cleaned++;
          }
        } catch (e) {
          // 忽略
        }
      }
    }
  }
  
  return cleaned;
}

/**
 * 重置超时任务
 */
function resetTimeoutTasks(state) {
  let resetCount = 0;
  const now = Date.now();
  
  for (const [tid, tstate] of Object.entries(state)) {
    if (tstate.status === 'running' && tstate.updatedAt) {
      const lastUpdate = new Date(tstate.updatedAt).getTime();
      const duration = now - lastUpdate;
      
      if (duration > CONFIG.taskTimeout) {
        tstate.status = 'pending';
        tstate.updatedAt = new Date().toISOString();
        delete tstate.startedAt;
        delete tstate.completedAt;
        log(`⚠️ 重置超时任务：${tid} (运行 ${Math.round(duration/1000)}s)`, 'WARN');
        resetCount++;
      }
    }
  }
  
  return resetCount;
}

/**
 * 修复缺失 agent 字段的任务
 */
function fixMissingAgents(state) {
  let fixed = 0;
  
  for (const [tid, tstate] of Object.entries(state)) {
    if (!tstate.agent) {
      if (tid.includes('writing')) tstate.agent = 'novel_writer';
      else if (tid.includes('outline')) tstate.agent = 'novel_architect';
      else if (tid.includes('review')) tstate.agent = 'novel_architect';
      else tstate.agent = 'novel_architect';
      fixed++;
    }
  }
  
  return fixed;
}

/**
 * 重启调度器
 */
function restartScheduler() {
  log('🔄 重启调度器...', 'INFO');
  
  exec('pkill -f "task-scheduler.js" && sleep 2 && rm -f ' + PROJECT_DIR + '/.scheduler.pid && cd /home/ubutu/.openclaw/workspace && nohup node skills/agile-workflow/core/task-scheduler.js ' + PROJECT_DIR + ' daemon 30000 > /tmp/scheduler-monitor.log 2>&1 &', (error, stdout) => {
    if (error) {
      log('❌ 重启调度器失败：' + error.message, 'ERROR');
    } else {
      log('✅ 调度器已重启', 'INFO');
    }
  });
}

/**
 * 触发任务检查
 */
function triggerTaskCheck() {
  log('🔍 触发任务检查...', 'INFO');
  
  exec('cd /home/ubutu/.openclaw/workspace && node skills/agile-workflow/core/task-scheduler.js ' + PROJECT_DIR + ' check > /tmp/task-check.log 2>&1', (error, stdout) => {
    if (error) {
      log('❌ 任务检查失败：' + error.message, 'ERROR');
    }
  });
}

/**
 * 主检查函数
 */
async function checkAndHeal() {
  log('=== 开始工作流健康检查 ===', 'INFO');
  
  const state = loadState();
  if (!state) {
    log('❌ 无法加载任务状态，跳过检查', 'ERROR');
    return;
  }
  
  // 统计任务状态
  const total = Object.keys(state).length;
  const completed = Object.values(state).filter(s => s.status === 'completed').length;
  const running = Object.values(state).filter(s => s.status === 'running').length;
  const pending = Object.values(state).filter(s => s.status === 'pending').length;
  const failed = Object.values(state).filter(s => s.status === 'failed').length;
  
  log(`📊 任务状态：总计 ${total} | 完成 ${completed} | 运行 ${running} | 待执行 ${pending} | 失败 ${failed}`, 'INFO');
  
  // 获取 Agent 状态
  const agentStatus = await getAgentStatus();
  log('🤖 Agent 状态:', 'INFO');
  for (const agent of agentStatus) {
    log(`   ${agent.id}: ${agent.health} (PID: ${agent.pid || '-'})${agent.hasLock ? ' | 🔒 锁文件 ' + Math.round(agent.lockAge/1000) + 's' : ''}`, 'INFO');
  }
  
  // 问题诊断和修复
  let issuesFound = 0;
  let issuesFixed = 0;
  
  // 1. 清理锁文件
  const cleanedLocks = await cleanupLockFiles();
  if (cleanedLocks > 0) {
    issuesFound++;
    issuesFixed++;
    log(`✅ 清理 ${cleanedLocks} 个锁文件`, 'INFO');
  }
  
  // 2. 重置超时任务
  const resetTasks = resetTimeoutTasks(state);
  if (resetTasks > 0) {
    issuesFound++;
    issuesFixed++;
    saveState(state);
    log(`✅ 重置 ${resetTasks} 个超时任务`, 'INFO');
  }
  
  // 3. 修复缺失 agent 字段
  const fixedAgents = fixMissingAgents(state);
  if (fixedAgents > 0) {
    issuesFound++;
    issuesFixed++;
    saveState(state);
    log(`✅ 修复 ${fixedAgents} 个任务的 agent 字段`, 'INFO');
  }
  
  // 4. 检查是否有待执行任务但无运行中任务（闲置检测）
  if (pending > 0 && running === 0) {
    issuesFound++;
    log('⚠️ 有待执行任务但无运行中任务，触发任务分配...', 'WARN');
    triggerTaskCheck();
    issuesFixed++;
  }
  
  // 5. 检查调度器是否运行
  const schedulerRunning = await new Promise((resolve) => {
    exec('pgrep -f "task-scheduler.js.*daemon"', (error, stdout) => {
      resolve(!error && stdout.trim().length > 0);
    });
  });
  
  if (!schedulerRunning) {
    issuesFound++;
    log('❌ 调度器未运行，重启中...', 'ERROR');
    restartScheduler();
    issuesFixed++;
  }
  
  // 6. 检查是否所有任务完成
  if (completed === total) {
    log('🎉 所有任务已完成！', 'INFO');
  }
  
  // 总结
  log(`=== 检查完成：发现 ${issuesFound} 个问题，修复 ${issuesFixed} 个 ===`, 'INFO');
}

// 主程序
log('🚀 工作流监控器启动', 'INFO');
log(`📁 项目目录：${PROJECT_DIR}`, 'INFO');
log(`⏱️  检查间隔：10 分钟`, 'INFO');

// 立即执行一次
checkAndHeal().catch(e => {
  log('❌ 检查失败：' + e.message, 'ERROR');
});

// 每 10 分钟检查一次
setInterval(() => {
  checkAndHeal().catch(e => {
    log('❌ 定期检查失败：' + e.message, 'ERROR');
  });
}, 600000); // 10 分钟

log('✅ 监控器已启动，每 10 分钟自动检查', 'INFO');
