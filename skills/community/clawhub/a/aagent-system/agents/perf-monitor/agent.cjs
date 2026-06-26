#!/usr/bin/env node
/**
 * 📊 Performance Monitor - 性能监控与统计
 * 统计各数据源的拉取极限和超时
 */

const fs = require('fs'), path = require('path');
const DATA_DIR = path.join(__dirname, '..', '..', 'data');
const STATS_FILE = path.join(DATA_DIR, 'perf-stats.json');

const MARKETS = {
  'npm': { name: 'npm', baseUrl: 'registry.npmjs.com', timeout: 5000 },
  'cnpm': { name: 'cnpm', baseUrl: 'registry.npmmirror.com', timeout: 5000 },
  'github': { name: 'GitHub', baseUrl: 'api.github.com', timeout: 10000 },
  'mcp': { name: 'MCP Market', baseUrl: 'mcpmarket.com', timeout: 8000 }
};

let stats = {
  markets: {},
  updates: 0,
  started: new Date().toISOString()
};

// 初始化各市场统计
Object.keys(MARKETS).forEach(k => {
  stats.markets[k] = {
    name: MARKETS[k].name,
    requests: 0,
    success: 0,
    failed: 0,
    timeouts: 0,
    totalTime: 0,
    avgTime: 0,
    maxTime: 0,
    minTime: 99999,
    rate: 0, // 每分钟请求数
    lastUpdate: null
  };
});

function save() {
  fs.writeFileSync(STATS_FILE, JSON.stringify(stats, null, 2));
}

function log(msg) {
  console.log(`[PERF] ${msg}`);
}

// 记录请求结果
function record(market, success, timeMs, isTimeout = false) {
  if (!stats.markets[market]) return;
  
  const m = stats.markets[market];
  m.requests++;
  m.totalTime += timeMs;
  m.maxTime = Math.max(m.maxTime, timeMs);
  m.minTime = Math.min(m.minTime, timeMs);
  m.avgTime = m.totalTime / m.requests;
  m.lastUpdate = new Date().toISOString();
  
  if (success) m.success++;
  else {
    m.failed++;
    if (isTimeout) m.timeouts++;
  }
  
  // 计算速率 (每分钟)
  const elapsed = (Date.now() - new Date(stats.started).getTime()) / 60000;
  m.rate = Math.round(m.requests / elapsed);
  
  stats.updates++;
  if (stats.updates % 10 === 0) save();
}

// 获取统计
function getStats() {
  return stats;
}

// 资源检查
function checkResources() {
  const os = require('os');
  const cpuLoad = os.loadavg()[0] / os.cpus().length;
  const memUsed = 1 - os.freemem() / os.totalmem();
  
  return {
    cpuLoad: (cpuLoad * 100).toFixed(1),
    memUsed: (memUsed * 100).toFixed(1),
    memFree: (os.freemem() / 1024 / 1024 / 1024).toFixed(1) + 'GB',
    cpuCores: os.cpus().length
  };
}

// 主循环 - 每10秒检查一次
async function loop() {
  log('📊 Performance Monitor 启动');
  
  setInterval(() => {
    const res = checkResources();
    log(`资源: CPU负载 ${res.cpuLoad}% | 内存 ${res.memUsed}% | 空闲 ${res.memFree}`);
    
    // 内存不足时警告
    if (parseFloat(res.memUsed) > 80) {
      log('⚠️ 内存使用超过80%');
    }
    if (parseFloat(res.cpuLoad) > 80) {
      log('⚠️ CPU负载超过80%');
    }
  }, 10000);
  
  // 保存初始状态
  save();
}

module.exports = { record, getStats, checkResources, MARKETS };
loop();
