/**
 * Agent Health Monitor
 * Monitors agent health status and detects failures
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * Get all running sessions
 */
function getRunningSessions() {
  const sessions = [];
  
  try {
    const output = execSync('openclaw sessions list --json 2>/dev/null || echo "[]"', {
      encoding: 'utf-8',
      timeout: 5000
    });
    
    const parsed = JSON.parse(output);
    return Array.isArray(parsed) ? parsed : [];
  } catch (e) {
    // Try alternative method
    try {
      const sessionsPath = path.join(process.env.HOME, '.openclaw', 'agents');
      if (fs.existsSync(sessionsPath)) {
        const agents = fs.readdirSync(sessionsPath);
        for (const agent of agents) {
          const sessionPath = path.join(sessionsPath, agent, 'sessions');
          if (fs.existsSync(sessionPath)) {
            const files = fs.readdirSync(sessionPath).filter(f => f.endsWith('.jsonl'));
            sessions.push({
              agent,
              sessions: files.length,
              active: files.filter(f => {
                const stat = fs.statSync(path.join(sessionPath, f));
                return Date.now() - stat.mtimeMs < 300000; // Active in last 5 min
              }).length
            });
          }
        }
      }
    } catch (e2) {
      // Ignore
    }
  }
  
  return sessions;
}

/**
 * Check if a process is running
 */
function isProcessRunning(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * Get system resource usage
 */
function getResourceUsage() {
  try {
    const output = execSync('cat /proc/loadavg 2>/dev/null || echo "0 0 0"', {
      encoding: 'utf-8',
      timeout: 2000
    });
    
    const loads = output.trim().split(' ').slice(0, 3).map(Number);
    
    const memOutput = execSync('cat /proc/meminfo 2>/dev/null | grep -E "MemTotal|MemAvailable"', {
      encoding: 'utf-8',
      timeout: 2000
    });
    
    const memLines = memOutput.trim().split('\n');
    const memTotal = parseInt(memLines[0]?.split(':')[1]?.trim().split(' ')[0] || '0');
    const memAvailable = parseInt(memLines[1]?.split(':')[1]?.trim().split(' ')[0] || '0');
    
    return {
      loadAvg: {
        '1m': loads[0],
        '5m': loads[1],
        '15m': loads[2]
      },
      memory: {
        totalMB: Math.round(memTotal / 1024),
        availableMB: Math.round(memAvailable / 1024),
        usedPercent: memTotal > 0 ? Math.round((1 - memAvailable / memTotal) * 100) : 0
      }
    };
  } catch (e) {
    return {
      loadAvg: { '1m': 0, '5m': 0, '15m': 0 },
      memory: { totalMB: 0, availableMB: 0, usedPercent: 0 }
    };
  }
}

/**
 * Check wrapper status
 */
function getWrapperStatus() {
  try {
    const wrapperPath = path.join(process.env.HOME, '.openclaw', 'workspace', 'skills', 'feishu-evolver-wrapper');
    const output = execSync(`cd ${wrapperPath} && node lifecycle.js status 2>/dev/null || echo "unknown"`, {
      encoding: 'utf-8',
      timeout: 5000
    });
    
    const isRunning = output.includes('RUNNING');
    const pidMatch = output.match(/PID\s+(\d+)/);
    
    return {
      status: isRunning ? 'running' : 'stopped',
      pid: pidMatch ? parseInt(pidMatch[1]) : null
    };
  } catch (e) {
    return { status: 'unknown', pid: null };
  }
}

/**
 * Main health check function
 */
async function checkHealth() {
  const sessions = getRunningSessions();
  const resources = getResourceUsage();
  const wrapper = getWrapperStatus();
  
  // Determine overall health
  let healthStatus = 'healthy';
  const issues = [];
  
  // Check wrapper
  if (wrapper.status !== 'running') {
    healthStatus = 'degraded';
    issues.push('Wrapper not running');
  }
  
  // Check memory
  if (resources.memory.usedPercent > 90) {
    healthStatus = 'critical';
    issues.push('Memory usage critical');
  } else if (resources.memory.usedPercent > 80) {
    if (healthStatus === 'healthy') healthStatus = 'degraded';
    issues.push('High memory usage');
  }
  
  // Check load
  if (resources.loadAvg['1m'] > 4) {
    if (healthStatus === 'healthy') healthStatus = 'degraded';
    issues.push('High system load');
  }
  
  // Count sessions
  const totalSessions = sessions.reduce((sum, s) => sum + s.sessions, 0);
  const activeSessions = sessions.reduce((sum, s) => sum + s.active, 0);
  
  return {
    timestamp: new Date().toISOString(),
    status: healthStatus,
    issues,
    sessions: {
      total: totalSessions,
      active: activeSessions,
      inactive: totalSessions - activeSessions,
      byAgent: sessions
    },
    wrapper,
    resources,
    summary: {
      healthy: healthStatus === 'healthy',
      warningCount: issues.length,
      activeAgents: sessions.filter(s => s.active > 0).length
    }
  };
}

/**
 * Get failed agents
 */
async function getFailedAgents() {
  const health = await checkHealth();
  const failed = [];
  
  if (health.wrapper.status !== 'running') {
    failed.push({
      type: 'wrapper',
      reason: 'Not running',
      severity: 'critical'
    });
  }
  
  for (const agent of health.sessions.byAgent) {
    if (agent.sessions > 0 && agent.active === 0) {
      failed.push({
        type: 'agent',
        name: agent.agent,
        reason: 'No active sessions',
        severity: 'warning'
      });
    }
  }
  
  return failed;
}

/**
 * Start continuous monitoring
 */
function startMonitoring(intervalMs = 30000, callback = null) {
  const monitor = async () => {
    const health = await checkHealth();
    if (callback) {
      callback(health);
    } else {
      console.log(JSON.stringify({
        timestamp: health.timestamp,
        status: health.status,
        issues: health.issues.length
      }));
    }
  };
  
  monitor(); // Initial check
  return setInterval(monitor, intervalMs);
}

module.exports = {
  checkHealth,
  getFailedAgents,
  getRunningSessions,
  getResourceUsage,
  getWrapperStatus,
  startMonitoring
};
