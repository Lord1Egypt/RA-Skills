#!/usr/bin/env node
/**
 * Agent Dashboard API Server
 * 轻量级 HTTP 服务，提供 Agent 状态数据
 * 端口：8889
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8889;
const DATA_FILE = path.join(__dirname, 'agent-data.json');
const QUOTA_FILE = path.join(__dirname, 'quota-data.json');
const { learnFromManual } = require('./quota-tracker');
const CACHE_DURATION = 180000; // 3 分钟

let cachedData = null;
let lastFetch = 0;

function getData() {
  const now = Date.now();
  
  // 使用缓存（3 分钟内不重复读取文件）
  if (cachedData && (now - lastFetch) < CACHE_DURATION) {
    return cachedData;
  }

  try {
    const content = fs.readFileSync(DATA_FILE, 'utf8');
    cachedData = JSON.parse(content);
    lastFetch = now;
    console.log(`✅ 数据已加载：${cachedData.length} 个 Agent`);
  } catch (e) {
    console.error('读取数据文件失败:', e.message);
    return cachedData || [];
  }
  
  return cachedData;
}

const server = http.createServer((req, res) => {
  console.log(`${new Date().toISOString()} ${req.method} ${req.url}`);

  // CORS 头（允许前端访问）
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // 处理带查询参数的 URL（如 /api/quota?t=123）
  const urlPath = req.url.split('?')[0];
  
  if (urlPath === '/api/agents' && req.method === 'GET') {
    const data = getData();
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data));
  } else if (urlPath === '/api/quota' && req.method === 'GET') {
    try {
      const q = JSON.parse(fs.readFileSync(QUOTA_FILE, 'utf8'));
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(q));
    } catch {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'no data' }));
    }
  } else if (urlPath === '/api/quota' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const input = JSON.parse(body);
        const q = JSON.parse(fs.readFileSync(QUOTA_FILE, 'utf8'));
        if (typeof input.manualTotal === 'number') {
          q.manualTotal = input.manualTotal;
          q.manualUpdatedAt = Date.now();
          // 记录手动输入历史，方便后续精确追踪每日增量
          if (!q.manualHistory) q.manualHistory = [];
          const todayStr = new Date().toISOString().slice(0, 10);
          const existing = q.manualHistory.findIndex(h => h.date === todayStr);
          if (existing >= 0) {
            q.manualHistory[existing].total = input.manualTotal;
            q.manualHistory[existing].ts = Date.now();
          } else {
            q.manualHistory.push({ date: todayStr, total: input.manualTotal, ts: Date.now() });
          }
          // 计算天数：按日期差（不含起始日）
          const cycleDays = 31;
          const start = new Date(q.config.billingCycleStart || '2026-04-11');
          const now = new Date();
          // 只比较日期，不比较时间
          const startDate = new Date(start.getFullYear(), start.getMonth(), start.getDate());
          const todayDate = new Date(now.getFullYear(), now.getMonth(), now.getDate());
          const daysPassed = Math.round((todayDate - startDate) / 86400000); // 4/11→4/14 = 3天
          const daysRemaining = Math.max(0, cycleDays - daysPassed);
          const manualDailyAvg = Math.round(input.manualTotal / daysPassed);
          const manualProjected = input.manualTotal + (manualDailyAvg * daysRemaining);
          const manualSafeLimit = daysRemaining > 0 ? Math.round((18000 - input.manualTotal) / daysRemaining) : 0;
          q.manualStats = {
            usedTotal: input.manualTotal,
            dailyAvg: manualDailyAvg,
            projectedTotal: manualProjected,
            projectedPct: Math.round((manualProjected / 18000) * 100),
            safeDailyLimit: manualSafeLimit,
            daysPassed,
            daysRemaining,
          };
          // 触发学习：用实际值校准预测模型
          learnFromManual(q);
          // 立即更新 stats，让预测值与实际值同步
          const { updateQuota } = require('./quota-tracker');
          updateQuota();
          // 重新分配每日数据，让每日用量趋势图反映实际值
          if (q.manualHistory && q.manualHistory.length > 0) {
            const sorted = [...q.manualHistory].sort((a, b) => a.date.localeCompare(b.date));
            const start = new Date(q.config.billingCycleStart || '2026-04-11');
            const todayStr = new Date().toISOString().slice(0, 10);
            
            const newDaily = {};
            
            // 用实际历史记录的增量分配每日数据
            for (let i = 0; i < sorted.length; i++) {
              const curr = sorted[i];
              const prev = i > 0 ? sorted[i - 1] : null;
              
              if (!prev) {
                // 第一次记录：从周期开始日到第一次记录日，平均分摊
                const firstDate = new Date(curr.date);
                const daysFromStart = Math.round((firstDate - new Date(start.toISOString().slice(0, 10))) / 86400000) + 1;
                const dailyAvg = Math.round(curr.total / daysFromStart);
                
                for (let j = 0; j < daysFromStart; j++) {
                  const d = new Date(start.getTime() + j * 86400000);
                  const dateKey = d.toISOString().slice(0, 10);
                  newDaily[dateKey] = dailyAvg;
                }
                // 修正舍入误差
                const sum = Object.values(newDaily).reduce((a, b) => a + b, 0);
                const diff = curr.total - sum;
                if (diff !== 0 && newDaily[curr.date] != null) {
                  newDaily[curr.date] += diff;
                }
              } else {
                // 后续记录：按实际增量分配
                const prevDate = new Date(prev.date);
                const currDate = new Date(curr.date);
                const daysBetween = Math.round((currDate - prevDate) / 86400000);
                const delta = curr.total - prev.total;
                const dailyAvg = daysBetween > 0 ? Math.round(delta / daysBetween) : delta;
                
                for (let j = 1; j <= daysBetween; j++) {
                  const d = new Date(prevDate.getTime() + j * 86400000);
                  const dateKey = d.toISOString().slice(0, 10);
                  newDaily[dateKey] = dailyAvg;
                }
                // 修正舍入误差
                const daysKeys = Object.keys(newDaily).filter(k => k > prev.date && k <= curr.date);
                if (daysKeys.length > 0) {
                  const sum = daysKeys.reduce((a, k) => a + newDaily[k], 0);
                  const diff = delta - sum;
                  if (diff !== 0) {
                    newDaily[curr.date] = (newDaily[curr.date] || 0) + diff;
                  }
                }
              }
            }
            
            q.usage.daily = newDaily;
            q.usage.total = sorted[sorted.length - 1].total;
          }
        }
        fs.writeFileSync(QUOTA_FILE, JSON.stringify(q, null, 2));
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true }));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
    });
  } else if (urlPath === '/api/health' && req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', cached: !!cachedData, lastFetch }));
  } else if (urlPath === '/api/cron' && req.method === 'GET') {
    // 读取 Cron 任务列表
    try {
      const cronFile = path.join(__dirname, 'cron-cache.json');
      const data = fs.existsSync(cronFile) ? JSON.parse(fs.readFileSync(cronFile, 'utf8')) : { jobs: [], lastUpdated: 0 };
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(data));
    } catch {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ jobs: [], lastUpdated: 0 }));
    }
  } else if (urlPath === '/api/cron-update' && req.method === 'POST') {
    // 保存 Cron 修改请求
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const input = JSON.parse(body);
        const pendingFile = path.join(__dirname, 'cron-pending.json');
        fs.writeFileSync(pendingFile, JSON.stringify({
          changes: input.changes,
          requestedAt: Date.now(),
          status: 'pending'
        }, null, 2));
        console.log('📝 Cron 修改请求已保存:', Object.keys(input.changes).length, '项');
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true }));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: e.message }));
      }
    });
  } else {
    res.writeHead(404);
    res.end('Not Found');
  }
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`🚀 Agent Dashboard API running on http://localhost:${PORT}`);
  console.log(`📊 Endpoints:`);
  console.log(`   GET /api/agents  - Agent 状态数据`);
  console.log(`   GET /api/health  - 健康检查`);
  console.log(`💾 Cache duration: ${CACHE_DURATION / 1000}秒`);
  
  // 首次获取数据
  getData();
});
