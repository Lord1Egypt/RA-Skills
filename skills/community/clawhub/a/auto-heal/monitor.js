#!/usr/bin/env node

/**
 * Auto-Heal Monitor for OpenClaw
 * 全天自动监控和自动修复
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 配置
const CONFIG = {
  checkInterval: 60 * 1000,      // 检查间隔：60秒
  gatewayTimeout: 30 * 1000,     // gateway 响应超时：30秒
  memoryThreshold: 80,            // 内存阈值：80%
  zombieSessionAge: 30 * 60 * 1000, // 僵尸会话：30分钟无响应
  logFile: path.join(__dirname, 'logs', 'auto-heal.log'),
  stateFile: path.join(__dirname, 'state.json')
};

// 确保日志目录存在
const logDir = path.dirname(CONFIG.logFile);
if (!fs.existsSync(logDir)) {
  fs.mkdirSync(logDir, { recursive: true });
}

// 日志函数
function log(level, message) {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] [${level}] ${message}\n`;
  
  console.log(logLine.trim());
  
  // 写入日志文件
  fs.appendFileSync(CONFIG.logFile, logLine);
}

// 执行命令
function runCommand(cmd, timeout = 10000) {
  try {
    const result = execSync(cmd, { 
      encoding: 'utf8', 
      timeout,
      stdio: ['pipe', 'pipe', 'pipe']
    });
    return { success: true, output: result.trim() };
  } catch (error) {
    return { success: false, error: error.message, output: error.stdout?.trim() || '' };
  }
}

// 检查 Gateway 状态
async function checkGateway() {
  log('INFO', 'Checking gateway status...');
  
  const result = runCommand('openclaw gateway status', CONFIG.gatewayTimeout);
  
  if (!result.success) {
    log('WARN', `Gateway check failed: ${result.error}`);
    return { healthy: false, issue: 'gateway_not_responding' };
  }
  
  // 解析状态
  if (result.output.includes('running') || result.output.includes('online')) {
    log('INFO', 'Gateway is healthy');
    return { healthy: true };
  }
  
  log('WARN', `Gateway status unknown: ${result.output}`);
  return { healthy: false, issue: 'gateway_unknown_state' };
}

// 修复 Gateway
async function fixGateway() {
  log('INFO', 'Attempting to fix gateway...');
  
  // 尝试重启 gateway
  const result = runCommand('openclaw gateway restart', 30000);
  
  if (result.success) {
    log('INFO', 'Gateway restarted successfully');
    
    // 等待启动
    await sleep(5000);
    
    // 验证
    const check = await checkGateway();
    if (check.healthy) {
      log('INFO', 'Gateway is now healthy');
      return { fixed: true };
    }
  }
  
  log('ERROR', `Failed to fix gateway: ${result.error}`);
  return { fixed: false, error: result.error };
}

// 检查 Agent 会话
async function checkAgentSessions() {
  log('INFO', 'Checking agent sessions...');
  
  const result = runCommand('openclaw sessions list --json', 10000);
  
  if (!result.success) {
    log('WARN', `Failed to list sessions: ${result.error}`);
    return { healthy: false, issue: 'cannot_list_sessions' };
  }
  
  try {
    const sessions = JSON.parse(result.output);
    const zombieSessions = [];
    
    for (const session of sessions) {
      // 检查会话是否卡死（根据最后活动时间）
      if (session.lastActivity) {
        const lastActivity = new Date(session.lastActivity).getTime();
        const now = Date.now();
        
        if (now - lastActivity > CONFIG.zombieSessionAge && session.status === 'busy') {
          zombieSessions.push(session);
        }
      }
    }
    
    if (zombieSessions.length > 0) {
      log('WARN', `Found ${zombieSessions.length} zombie sessions`);
      return { healthy: false, issue: 'zombie_sessions', sessions: zombieSessions };
    }
    
    log('INFO', `All ${sessions.length} sessions are healthy`);
    return { healthy: true, sessionCount: sessions.length };
  } catch (error) {
    log('ERROR', `Failed to parse sessions: ${error.message}`);
    return { healthy: false, issue: 'parse_error' };
  }
}

// 修复僵尸会话
async function fixZombieSessions(sessions) {
  log('INFO', `Fixing ${sessions.length} zombie sessions...`);
  
  const results = [];
  
  for (const session of sessions) {
    log('INFO', `Killing zombie session: ${session.id}`);
    
    const result = runCommand(`openclaw sessions kill ${session.id}`, 5000);
    results.push({
      sessionId: session.id,
      success: result.success,
      error: result.error
    });
  }
  
  const successCount = results.filter(r => r.success).length;
  log('INFO', `Killed ${successCount}/${sessions.length} zombie sessions`);
  
  return { fixed: successCount > 0, results };
}

// 检查系统资源
async function checkResources() {
  log('INFO', 'Checking system resources...');
  
  // 检查内存使用
  const memResult = runCommand('ps -o pid,ppid,pcpu,pmem,command -p $(pgrep -f "openclaw") | tail -n +2');
  
  if (memResult.success) {
    const lines = memResult.output.split('\n').filter(l => l.trim());
    let totalMem = 0;
    
    for (const line of lines) {
      const parts = line.trim().split(/\s+/);
      if (parts.length >= 4) {
        const memPercent = parseFloat(parts[3]);
        if (!isNaN(memPercent)) {
          totalMem += memPercent;
        }
      }
    }
    
    log('INFO', `OpenClaw memory usage: ${totalMem.toFixed(1)}%`);
    
    if (totalMem > CONFIG.memoryThreshold) {
      log('WARN', `Memory usage ${totalMem.toFixed(1)}% exceeds threshold ${CONFIG.memoryThreshold}%`);
      return { healthy: false, issue: 'high_memory', memory: totalMem };
    }
  }
  
  return { healthy: true };
}

// 修复资源问题
async function fixResources() {
  log('INFO', 'Attempting to fix resource issues...');
  
  // 清理旧日志
  const cleanupResult = runCommand('find ~/.openclaw/logs -name "*.log" -mtime +7 -delete', 5000);
  if (cleanupResult.success) {
    log('INFO', 'Cleaned up old log files');
  }
  
  // 重启 gateway 释放内存
  const restartResult = await fixGateway();
  
  return restartResult;
}

// 主检查循环
async function healthCheck() {
  log('INFO', '=== Starting health check ===');
  
  const issues = [];
  
  // 1. 检查 Gateway
  const gatewayStatus = await checkGateway();
  if (!gatewayStatus.healthy) {
    issues.push({ component: 'gateway', ...gatewayStatus });
    
    // 自动修复
    const fix = await fixGateway();
    if (!fix.fixed) {
      log('ERROR', 'Failed to auto-fix gateway');
    }
  }
  
  // 2. 检查 Agent 会话
  const sessionStatus = await checkAgentSessions();
  if (!sessionStatus.healthy) {
    issues.push({ component: 'sessions', ...sessionStatus });
    
    // 自动修复僵尸会话
    if (sessionStatus.sessions) {
      await fixZombieSessions(sessionStatus.sessions);
    }
  }
  
  // 3. 检查资源
  const resourceStatus = await checkResources();
  if (!resourceStatus.healthy) {
    issues.push({ component: 'resources', ...resourceStatus });
    
    // 自动修复资源问题
    await fixResources();
  }
  
  // 保存状态
  const state = {
    lastCheck: new Date().toISOString(),
    issues: issues.length,
    details: issues
  };
  fs.writeFileSync(CONFIG.stateFile, JSON.stringify(state, null, 2));
  
  if (issues.length === 0) {
    log('INFO', '=== Health check passed ===');
  } else {
    log('WARN', `=== Health check found ${issues.length} issues, auto-fixed ===`);
  }
  
  return issues;
}

// 辅助函数
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 主循环
async function main() {
  log('INFO', 'Auto-Heal Monitor started');
  log('INFO', `Check interval: ${CONFIG.checkInterval / 1000}s`);
  
  // 立即执行一次检查
  await healthCheck();
  
  // 定时检查
  setInterval(async () => {
    await healthCheck();
  }, CONFIG.checkInterval);
}

// 检查是否是单次运行模式
if (process.argv.includes('--check-once')) {
  healthCheck().then(issues => {
    process.exit(issues.length > 0 ? 1 : 0);
  }).catch(error => {
    log('ERROR', `Check failed: ${error.message}`);
    process.exit(1);
  });
} else {
  // 启动持续监控
  main().catch(error => {
    log('ERROR', `Monitor crashed: ${error.message}`);
    process.exit(1);
  });
}
