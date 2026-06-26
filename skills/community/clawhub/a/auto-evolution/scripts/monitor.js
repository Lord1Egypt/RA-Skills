#!/usr/bin/env node

/**
 * Monitor — detects stuck tasks, cleans orphaned locks, reports anomalies.
 * 
 * Run on a timer (e.g. every 10 min via cron or heartbeat).
 * Can be run by any agent — no specific agent identity required.
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || process.env.WORKSPACE || path.join(require('os').homedir(), '.openclaw', 'agents', 'main', 'workspace');
const TASKS_DIR = process.env.EVOLUTION_TASKS_DIR || path.join(WORKSPACE, 'evolution', 'tasks');
const STUCK_THRESHOLD_MS = 10 * 60 * 1000; // 10 min

function main() {
  console.log(`\n🛡️ Monitor @ ${new Date().toISOString()}`);
  
  if (!fs.existsSync(TASKS_DIR)) {
    console.log(`📁 Tasks directory not found: ${TASKS_DIR}`);
    return;
  }
  
  let issues = [];
  
  // 1. Clean expired locks
  const lockFiles = fs.readdirSync(TASKS_DIR).filter(f => f.endsWith('.lock'));
  for (const lockName of lockFiles) {
    const lockPath = path.join(TASKS_DIR, lockName);
    try {
      const lockData = JSON.parse(fs.readFileSync(lockPath, 'utf8'));
      const age = Date.now() - lockData.timestamp;
      if (age > STUCK_THRESHOLD_MS) {
        fs.unlinkSync(lockPath);
        issues.push(`🔓 Cleaned expired lock: ${lockName} (${Math.round(age / 60000)}min old)`);
      }
    } catch (err) {
      fs.unlinkSync(lockPath);
      issues.push(`🔓 Cleaned corrupt lock: ${lockName}`);
    }
  }
  
  // 2. Detect stuck tasks
  const files = fs.readdirSync(TASKS_DIR).filter(f => f.endsWith('.json') && f.startsWith('task-'));
  
  for (const file of files) {
    try {
      const data = JSON.parse(fs.readFileSync(path.join(TASKS_DIR, file), 'utf8'));
      
      if (['reviewing', 'executing'].includes(data.status)) {
        const updatedAt = new Date(data.updated_at).getTime();
        const age = Date.now() - updatedAt;
        
        if (age > STUCK_THRESHOLD_MS) {
          data.status = 'pending';
          data.updated_at = new Date().toISOString();
          if (!data.history) data.history = [];
          data.history.push({
            timestamp: data.updated_at,
            action: 'monitor_auto_reset',
            role: 'monitor',
            notes: `Task stuck in ${data.status} for ${Math.round(age / 60000)}min, reset to pending`
          });
          fs.writeFileSync(path.join(TASKS_DIR, file), JSON.stringify(data, null, 2));
          issues.push(`🔄 Reset stuck task: ${data.task_id} (${Math.round(age / 60000)}min)`);
        }
      }
      
      // 3. Detect consecutive failures
      const recentHistory = (data.history || []).slice(-3);
      const allFailed = recentHistory.length >= 3 && recentHistory.every(h => h.result === 'failure');
      if (allFailed) {
        issues.push(`🚨 Task ${data.task_id} failed 3 times in a row — needs manual intervention`);
      }
      
    } catch (err) {
      issues.push(`⚠️ Failed to read ${file}: ${err.message}`);
    }
  }
  
  // 4. Status report
  const taskStatuses = files.map(f => {
    try {
      const d = JSON.parse(fs.readFileSync(path.join(TASKS_DIR, f), 'utf8'));
      return `${d.task_id}: ${d.status} (iter ${d.current_iteration || 0})`;
    } catch { return `${f}: error`; }
  });
  
  console.log(`📋 Tasks:\n  ${taskStatuses.join('\n  ')}`);
  
  if (issues.length > 0) {
    console.log(`\n⚠️ ${issues.length} issue(s):`);
    issues.forEach(i => console.log(`  ${i}`));
  } else {
    console.log('\n✅ All clear');
  }
}

main();
