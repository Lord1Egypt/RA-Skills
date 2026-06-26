#!/usr/bin/env node
/**
 * Error Auto Fix — 错误自动修复
 * 
 * 功能：
 * 1. 分析 OpenClaw 日志中的 ERROR 级别错误
 * 2. 识别错误类型
 * 3. 提供修复建议（提示手动）
 * 
 * 修复策略：
 * - Gateway 连接错误 → 提示用户手动重启
 * - 端口占用 → 只读检查
 * - 会话异常 → 只读检查
 * 
 * 注意：缓存清理、权限修复属于 dev/test/rule 子代理的操作范畴，
 * 不属于系统错误监控技能的职责。
 * 
 * 用法:
 *   node auto-fix.js
 *   node auto-fix.js --dry-run    # 只报告不执行
 *   node auto-fix.js --json       # JSON 输出
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const ERROR_FILE = path.join(WORKSPACE, 'error.md');
const LOG_FILE = `/tmp/openclaw/openclaw-${new Date().toISOString().slice(0, 10)}.log`;
const FIX_LOG = path.join(WORKSPACE, '.fix-log.json');

// ============================================================================
// 修复策略定义
// ============================================================================

const FIX_STRATEGIES = [
  {
    id: 'gateway_restart',
    name: 'Gateway 重启（提示手动）',
    match: (errors) => {
      return errors.some(e => 
        e.includes('gateway') || 
        e.includes('ws') || 
        e.includes('WebSocket') ||
        e.includes('connect') ||
        e.includes('fetch failed')
      );
    },
    action: () => {
      return '⚠️ 检测到 Gateway 连接错误，请手动执行: openclaw gateway restart（或 systemctl --user restart openclaw-gateway.service）';
    },
  },
  {
    id: 'port_release',
    name: '端口释放（只读检查）',
    match: (errors) => {
      return errors.some(e =>
        e.includes('EADDRINUSE') ||
        e.includes('port') && e.includes('in use') ||
        e.includes('address already in use')
      );
    },
    action: () => {
      try {
        const output = execSync('ss -tlnp 2>/dev/null | grep node | awk \'{print $4}\' | grep -oP ":\\K\\d+"', { encoding: 'utf8' });
        const ports = output.trim().split('\n').filter(Boolean);
        if (ports.length > 0) {
          return `发现 node 监听端口: ${ports.join(', ')}（无需强制释放，属正常监听）`;
        }
        return '无端口占用问题';
      } catch {
        return '端口检查失败';
      }
    },
  },
  {
    id: 'session_cleanup',
    name: '会话清理（只读检查）',
    match: (errors) => {
      return errors.some(e =>
        e.includes('session') ||
        e.includes('INVALID_REQUEST') ||
        e.includes('not found')
      );
    },
    action: () => {
      try {
        execSync('openclaw sessions cleanup --dry-run 2>/dev/null', { timeout: 10000 });
        return '会话清理已检查';
      } catch {
        return '会话清理检查失败';
      }
    },
  },
];

// ============================================================================
// 工具函数
// ============================================================================

function loadFixLog() {
  try {
    return JSON.parse(fs.readFileSync(FIX_LOG, 'utf8'));
  } catch {
    return { fixes: [], lastRun: null };
  }
}

function saveFixLog(log) {
  log.lastRun = new Date().toISOString();
  fs.writeFileSync(FIX_LOG, JSON.stringify(log, null, 2));
}

function getRecentErrors() {
  if (!fs.existsSync(LOG_FILE)) return [];
  
  const content = fs.readFileSync(LOG_FILE, 'utf8');
  const lines = content.split('\n').filter(l => l.trim());
  const now = Date.now();
  const cutoff = now - 60 * 60 * 1000; // 最近 1 小时
  
  const errors = [];
  for (const line of lines) {
    try {
      const obj = JSON.parse(line);
      if (obj._meta?.logLevelId !== 5) continue;
      
      const time = new Date(obj.time).getTime();
      if (time < cutoff) continue;
      
      let message = '';
      for (const key of Object.keys(obj)) {
        if (key === '_meta' || key === 'time') continue;
        message += typeof obj[key] === 'string' ? obj[key] + ' ' : JSON.stringify(obj[key]) + ' ';
      }
      errors.push(message.trim());
    } catch {}
  }
  
  return errors;
}

// ============================================================================
// 核心逻辑
// ============================================================================

function autoFix() {
  const dryRun = process.argv.includes('--dry-run');
  const jsonMode = process.argv.includes('--json');
  
  const errors = getRecentErrors();
  
  if (errors.length === 0) {
    if (jsonMode) {
      console.log(JSON.stringify({ message: '无待修复错误', fixes: [] }));
    } else {
      console.log('✅ 无待修复错误');
      console.log('NO_REPLY');
    }
    return;
  }
  
  const fixLog = loadFixLog();
  const applied = [];
  
  for (const strategy of FIX_STRATEGIES) {
    if (strategy.match(errors)) {
      const result = {
        id: strategy.id,
        name: strategy.name,
        status: dryRun ? 'dry-run' : 'pending',
        message: '',
      };
      
      if (dryRun) {
        result.message = `[DRY RUN] 将执行: ${strategy.name}`;
      } else {
        try {
          result.message = strategy.action();
          result.status = 'success';
        } catch (e) {
          result.status = 'failed';
          result.message = e.message || '修复失败';
        }
      }
      
      applied.push(result);
    }
  }
  
  // 记录修复历史
  fixLog.fixes.push({
    timestamp: new Date().toISOString(),
    errorCount: errors.length,
    fixes: applied,
  });
  
  // 只保留最近 100 条
  if (fixLog.fixes.length > 100) {
    fixLog.fixes = fixLog.fixes.slice(-100);
  }
  
  saveFixLog(fixLog);
  
  // 输出
  if (jsonMode) {
    console.log(JSON.stringify({
      errors: errors.length,
      fixes: applied,
    }, null, 2));
    return;
  }
  
  if (applied.length === 0) {
    console.log('✅ 无匹配的自动修复策略');
    console.log('NO_REPLY');
    return;
  }
  
  console.log(`🔧 执行了 ${applied.length} 个修复操作:`);
  console.log('');
  for (const fix of applied) {
    const icon = fix.status === 'success' ? '✅' : fix.status === 'failed' ? '❌' : '🔵';
    console.log(`${icon} [${fix.name}] ${fix.message}`);
  }
  
  console.log('');
  console.log('✅ 自动修复完成');
}

autoFix();
