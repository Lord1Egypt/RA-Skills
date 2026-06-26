#!/usr/bin/env node
/**
 * Error Monitor — OpenClaw 错误日志监控
 * 
 * 功能：
 * 1. 扫描 /tmp/openclaw/openclaw-YYYY-MM-DD.log JSON 日志
 * 2. 提取 ERROR 级别日志（logLevelId: 5）
 * 3. 去重：同一错误类型 1 小时内只记录一次
 * 4. 追加到 ~/.openclaw/workspace/error.md
 * 
 * 用法:
 *   node monitor-error.js              # 检查最近 5 分钟
 *   node monitor-error.js --all        # 检查今日全部
 *   node monitor-error.js --json       # JSON 输出
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const ERROR_FILE = path.join(WORKSPACE, 'error.md');
const LOG_FILE = `/tmp/openclaw/openclaw-${new Date().toISOString().slice(0, 10)}.log`;
const DEDUP_FILE = path.join(WORKSPACE, '.error-dedup.json');
const WINDOW_MS = 5 * 60 * 1000;  // 5 分钟窗口
const DEDUP_MS = 60 * 60 * 1000;  // 1 小时去重

// ============================================================================
// 工具函数
// ============================================================================

function loadDedup() {
  try {
    return JSON.parse(fs.readFileSync(DEDUP_FILE, 'utf8'));
  } catch {
    return {};
  }
}

function saveDedup(dedup) {
  // 清理过期的
  const now = Date.now();
  const cleaned = {};
  for (const [key, time] of Object.entries(dedup)) {
    if (now - time < DEDUP_MS) cleaned[key] = time;
  }
  fs.writeFileSync(DEDUP_FILE, JSON.stringify(cleaned, null, 2));
}

function hashError(err) {
  // 生成错误指纹：子系统 + 错误类型
  let subsystem = err.subsystem || err.channel || 'unknown';
  let errorType = '';
  
  if (err.message?.includes('fetch failed')) errorType = 'fetch_failed';
  else if (err.message?.includes('timeout')) errorType = 'timeout';
  else if (err.message?.includes('ECONNABORTED')) errorType = 'conn_aborted';
  else if (err.message?.includes('ws') && err.message?.includes('fail')) errorType = 'ws_failed';
  else if (err.message?.includes('EACCES') || err.message?.includes('permission')) errorType = 'permission';
  else if (err.message?.includes('EADDRINUSE')) errorType = 'port_in_use';
  else if (err.message?.includes('ENOENT')) errorType = 'file_not_found';
  else if (err.message?.includes('memory') || err.message?.includes('OOM')) errorType = 'memory';
  else if (err.message?.includes('DeprecationWarning')) errorType = 'deprecation';
  else errorType = 'unknown';
  
  return `${subsystem}:${errorType}`;
}

function parseLogLine(line) {
  try {
    const obj = JSON.parse(line);
    const logLevelId = obj._meta?.logLevelId || 0;
    const logLevelName = obj._meta?.logLevelName || 'INFO';
    
    // 只收集 ERROR 级别 (logLevelId: 5)
    if (logLevelId !== 5) return null;
    
    // 合并消息
    let message = '';
    const parts = [];
    for (const key of Object.keys(obj)) {
      if (key === '_meta' || key === 'time') continue;
      parts.push(typeof obj[key] === 'string' ? obj[key] : JSON.stringify(obj[key]));
    }
    message = parts.join(' | ');
    
    // 提取子系统
    let subsystem = '';
    if (typeof obj[0] === 'string') {
      const subMatch = obj[0].match(/gateway\/channels\/([^/]+)/);
      if (subMatch) subsystem = subMatch[1];
      else if (obj[0].includes('subsystem')) {
        try {
          const subObj = JSON.parse(obj[0]);
          subsystem = subObj.subsystem || '';
        } catch {}
      }
    }
    
    return {
      timestamp: obj.time || '',
      subsystem,
      message: message.slice(0, 500),
      level: logLevelName,
      hash: '',
    };
  } catch {
    return null;
  }
}

// ============================================================================
// 核心逻辑
// ============================================================================

function scanErrors() {
  const now = Date.now();
  const cutoff = now - WINDOW_MS;
  const jsonMode = process.argv.includes('--json');
  const allMode = process.argv.includes('--all');
  
  // 检查日志文件
  if (!fs.existsSync(LOG_FILE)) {
    if (jsonMode) {
      console.log(JSON.stringify({ errors: [], message: '今日日志不存在' }));
    } else {
      console.log(`📭 今日日志文件不存在：${LOG_FILE}`);
      console.log('NO_REPLY');
    }
    return;
  }
  
  // 读取日志
  const content = fs.readFileSync(LOG_FILE, 'utf8');
  const lines = content.split('\n').filter(l => l.trim());
  
  const errors = [];
  const dedup = loadDedup();
  
  for (const line of lines) {
    const entry = parseLogLine(line);
    if (!entry) continue;
    
    // 时间过滤
    if (!allMode) {
      const entryTime = new Date(entry.timestamp).getTime();
      if (entryTime < cutoff) continue;
    }
    
    // 去重
    entry.hash = hashError(entry);
    if (dedup[entry.hash] && now - dedup[entry.hash] < DEDUP_MS) {
      continue; // 已记录过，跳过
    }
    
    errors.push(entry);
    dedup[entry.hash] = now;
  }
  
  saveDedup(dedup);
  
  // 输出
  if (errors.length === 0) {
    if (jsonMode) {
      console.log(JSON.stringify({ errors: [], message: '无新错误' }));
    } else {
      console.log(`✅ 无新错误（${allMode ? '全量扫描' : '最近 5 分钟'}）`);
      console.log('NO_REPLY');
    }
    return;
  }
  
  if (jsonMode) {
    console.log(JSON.stringify({ errors, count: errors.length }, null, 2));
    return;
  }
  
  // 追加到 error.md
  const lines_out = [];
  lines_out.push(`## ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })} 自动扫描`);
  lines_out.push('');
  lines_out.push(`**扫描时间**: ${new Date().toISOString()}`);
  lines_out.push(`**扫描范围**: ${allMode ? '今日全量' : '最近 5 分钟'}`);
  lines_out.push(`**发现错误**: ${errors.length} 条`);
  lines_out.push('');
  lines_out.push('| 时间 | 子系统 | 错误类型 | 描述 |');
  lines_out.push('|------|--------|----------|------|');
  
  for (const err of errors) {
    const time = err.timestamp.slice(11, 19);
    const shortMsg = err.message.slice(0, 80).replace(/\|/g, '\\|');
    const errorType = err.hash.split(':')[1] || 'unknown';
    lines_out.push(`| ${time} | ${err.subsystem || '-'} | ${errorType} | ${shortMsg} |`);
  }
  
  lines_out.push('');
  lines_out.push('---');
  lines_out.push('');
  
  fs.appendFileSync(ERROR_FILE, '\n' + lines_out.join('\n'));
  
  // 输出报告
  console.log(`⚠️ 发现 ${errors.length} 条新错误:`);
  console.log('');
  for (const err of errors) {
    console.log(`  🔴 [${err.subsystem || 'system'}] ${err.hash.split(':')[1]}`);
    console.log(`     ${err.message.slice(0, 100)}`);
    console.log('');
  }
  
  console.log('✅ 已追加到 error.md');
}

scanErrors();
