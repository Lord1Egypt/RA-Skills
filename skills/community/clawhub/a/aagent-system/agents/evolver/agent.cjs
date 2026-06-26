#!/usr/bin/env node
/**
 * 🔄 Evolver Agent - 自我演进优化系统
 * 
 * 核心能力:
 * - 自我评估当前方案
 * - 发现差距与问题
 * - 自动调整优化
 * - 闭环演进
 */

const fs = require('fs'), path = require('path');
const DATA_DIR = path.join(__dirname, '..', '..', 'data');
const EVOLUTION_FILE = path.join(DATA_DIR, 'evolution.json');
const CONFIG_FILE = path.join(__dirname, '..', 'config.json');

const TARGETS = {
  samples: 100000,
  daily: 10000,
  sources: 5,
  quality: 95
};

// 默认配置
let config = {
  collectors: 10,
  interval: 8000,
  keywords: [],
  sources: ['npm-registry'],
  strategies: {
    useRegistryApi: true,
    useSearch: true,
    typosquatting: false
  }
};

// 加载配置
function loadConfig() {
  if (fs.existsSync(CONFIG_FILE)) {
    try { config = { ...config, ...JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8')) }; } catch {}
  }
  return config;
}

function saveConfig() {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
}

function log(msg) {
  console.log(`[EVOLVER] ${msg}`);
}

function readJson(file, def = []) {
  if (!fs.existsSync(file)) return def;
  try { return JSON.parse(fs.readFileSync(file, 'utf8')) } catch { return def; }
}

// 关键指标收集
function collectMetrics() {
  const samples = readJson(path.join(DATA_DIR, 'samples.json'), []);
  const stats = readJson(path.join(DATA_DIR, 'orchestrator-stats.json'), {});
  
  const now = Date.now();
  const hour = 3600000;
  const day = hour * 24;
  
  // 增长指标
  const last1h = samples.filter(s => now - new Date(s.at).getTime() < hour).length;
  const last6h = samples.filter(s => now - new Date(s.at).getTime() < hour * 6).length;
  const last24h = samples.filter(s => now - new Date(s.at).getTime() < day).length;
  
  // 来源分析
  const sources = {};
  samples.forEach(s => { sources[s.source] = (sources[s.source] || 0) + 1; });
  
  // 关键词分析
  const keywords = {};
  samples.forEach(s => { if (s.keyword) keywords[s.keyword] = (keywords[s.keyword] || 0) + 1; });
  const topKeywords = Object.entries(keywords).sort((a, b) => b[1] - a[1]).slice(0, 10);
  
  // 效率计算
  const efficiency = last24h / 24; // 每小时
  const daysToGoal = (TARGETS.samples - samples.length) / last24h;
  
  return {
    total: samples.length,
    last1h,
    last6h,
    last24h,
    efficiency: efficiency.toFixed(1),
    daysToGoal: daysToGoal > 0 ? daysToGoal.toFixed(0) : 0,
    sources: Object.keys(sources).length,
    sourceDist: sources,
    topKeywords,
    progress: (samples.length / TARGETS.samples * 100).toFixed(2)
  };
}

// 差距分析
function analyzeGap(metrics) {
  const gaps = [];
  
  // 目标差距
  if (metrics.daysToGoal > 30) {
    gaps.push({ type: 'speed', severity: 'critical', current: metrics.last24h, target: TARGETS.daily, gap: TARGETS.daily - metrics.last24h });
  }
  
  // 来源差距
  if (metrics.sources < TARGETS.sources) {
    gaps.push({ type: 'source', severity: 'high', current: metrics.sources, target: TARGETS.sources, gap: TARGETS.sources - metrics.sources });
  }
  
  // 效率差距
  if (parseFloat(metrics.efficiency) < 100) {
    gaps.push({ type: 'efficiency', severity: 'medium', current: metrics.efficiency, target: 400, gap: 400 - metrics.efficiency });
  }
  
  return gaps;
}

// 优化策略生成
function generateStrategy(gaps, metrics) {
  const strategies = [];
  
  gaps.forEach(gap => {
    switch (gap.type) {
      case 'speed':
        if (gap.current < 100) {
          strategies.push({ action: '增加采集器', param: { collectors: config.collectors + 5 }, reason: '速度严重不足' });
          strategies.push({ action: '缩短间隔', param: { interval: Math.max(3000, config.interval - 2000) }, reason: '提高采集频率' });
        }
        break;
      case 'source':
        strategies.push({ action: '添加数据源', param: { sources: [...config.sources, 'github', 'mcp-market'] }, reason: '扩展来源' });
        break;
      case 'efficiency':
        strategies.push({ action: '优化关键词', param: { keywords: getBetterKeywords(metrics) }, reason: '提高命中率' });
        break;
    }
  });
  
  return strategies;
}

// 获取更好的关键词
function getBetterKeywords(metrics) {
  // 分析哪些关键词有效
  const effective = metrics.topKeywords.filter(([k, v]) => v > 5).map(([k]) => k);
  return effective.length > 0 ? effective : config.keywords;
}

// 执行优化
async function applyStrategy(strategy) {
  log(`🔧 执行优化: ${strategy.action}`);
  
  switch (strategy.action) {
    case '增加采集器':
      config.collectors = strategy.param.collectors;
      // 启动新采集器
      for (let i = 0; i < 5; i++) {
        const { exec } = require('child_process');
        exec(`cd ${DATA_DIR}/../../ && AGENT_NAME=collector AGENT_INDEX=${Date.now()+i} node agents/collector/agent.cjs > /dev/null 2>&1 &`);
      }
      break;
      
    case '缩短间隔':
      config.interval = strategy.param.interval;
      break;
      
    case '添加数据源':
      config.sources = strategy.param.sources;
      break;
      
    case '优化关键词':
      config.keywords = strategy.param.keywords;
      break;
  }
  
  saveConfig();
  return strategy;
}

// 演进记录
function recordEvolution(metrics, gaps, strategies, applied) {
  const evolution = readJson(EVOLUTION_FILE, []);
  evolution.push({
    ts: new Date().toISOString(),
    metrics: { total: metrics.total, last24h: metrics.last24h, efficiency: metrics.efficiency },
    gaps: gaps.map(g => g.type),
    strategies: strategies.map(s => s.action),
    applied: applied.map(a => a.action),
    config: { ...config }
  });
  
  // 只保留最近20条
  if (evolution.length > 20) evolution.shift();
  
  fs.writeFileSync(EVOLUTION_FILE, JSON.stringify(evolution, null, 2));
  return evolution;
}

// 主循环
async function loop() {
  log('🔄 Evolver 启动 - 自我演进系统');
  
  loadConfig();
  
  let round = 0;
  while (true) {
    round++;
    log(`\n=== 演进轮次 ${round} ===`);
    
    // 1. 收集指标
    const metrics = collectMetrics();
    log(`📊 指标: 总数=${metrics.total} 24h=${metrics.last24h} 效率=${metrics.efficiency}/h 来源=${metrics.sources}`);
    
    // 2. 差距分析
    const gaps = analyzeGap(metrics);
    if (gaps.length > 0) {
      log(`⚠️ 差距: ${gaps.map(g => `${g.type}(${g.current}/${g.target})`).join(', ')}`);
    }
    
    // 3. 生成策略
    const strategies = generateStrategy(gaps, metrics);
    if (strategies.length > 0) {
      log(`💡 策略: ${strategies.map(s => s.action).join(' | ')}`);
      
      // 4. 执行策略
      const applied = [];
      for (const strategy of strategies.slice(0, 2)) { // 每次最多应用2个
        try {
          await applyStrategy(strategy);
          applied.push(strategy);
        } catch (e) {
          log(`❌ 执行失败: ${e.message}`);
        }
      }
      
      // 5. 记录演进
      recordEvolution(metrics, gaps, strategies, applied);
    } else {
      log('✅ 无需优化，当前状态良好');
    }
    
    // 6. 评估效果
    await new Promise(r => setTimeout(r, 60000)); // 1分钟评估一次
  }
}

loop();
