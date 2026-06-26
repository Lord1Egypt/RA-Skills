#!/usr/bin/env node
/**
 * 🎨 Designer Agent - 系统设计与指标权衡
 * 
 * 职责:
 * - 定义评估指标与目标
 * - 权衡策略调整
 * - 系统架构设计
 * - 长周期演进规划
 */

const fs = require('fs'), path = require('path');
const DATA_DIR = path.join(__dirname, '..', '..', 'data');
const DESIGN_FILE = path.join(DATA_DIR, 'design.json');
const CONFIG_FILE = path.join(__dirname, '..', 'config.json');

function log(msg) { console.log(`[DESIGNER] ${msg}`); }
function readJson(file, def = {}) { 
  if (!fs.existsSync(file)) return def;
  try { return JSON.parse(fs.readFileSync(file, 'utf8')) } catch { return def; }
}
function writeJson(file, data) { fs.writeFileSync(file, JSON.stringify(data, null, 2)); }

// 指标定义与权衡规则
const METRICS = {
  // 核心指标
  samples: { target: 100000, minAcceptable: 10000, window: '7d', weight: 0.3 },
  dailyRate: { target: 10000, minAcceptable: 1000, window: '24h', weight: 0.25 },
  sources: { target: 5, minAcceptable: 2, window: 'static', weight: 0.15 },
  quality: { target: 95, minAcceptable: 80, window: 'static', weight: 0.15 },
  efficiency: { target: 500, minAcceptable: 50, window: '1h', weight: 0.15 },
  
  // 派生指标
  health: { target: 90, minAcceptable: 60, window: '1h', weight: 0 },
  cost: { target: 0.1, minAcceptable: 0.5, window: '1h', weight: 0 } // 资源消耗
};

// 评估指标
function evaluateMetrics(samples, stats) {
  const results = {};
  const now = Date.now();
  const hour = 3600000;
  const day = hour * 24;
  
  // 计算各项指标
  const last1h = samples.filter(s => now - new Date(s.at).getTime() < hour).length;
  const last24h = samples.filter(s => now - new Date(s.at).getTime() < day).length;
  const last7d = samples.filter(s => now - new Date(s.at).getTime() < day * 7).length;
  
  const sources = new Set(samples.map(s => s.source)).size;
  const suspicious = samples.filter(s => s.suspicious).length;
  const quality = samples.length > 0 ? ((samples.length - suspicious) / samples.length * 100) : 0;
  
  // 评估每个指标
  const eval = (name, current, target, minAcceptable) => {
    const ratio = current / target;
    const status = ratio >= 1 ? 'excellent' : ratio >= minAcceptable/target ? 'acceptable' : 'poor';
    return { current, target, minAcceptable, ratio: ratio.toFixed(2), status };
  };
  
  results.samples = eval('samples', samples.length, METRICS.samples.target, METRICS.samples.minAcceptable);
  results.dailyRate = eval('dailyRate', last24h, METRICS.dailyRate.target, METRICS.dailyRate.minAcceptable);
  results.sources = eval('sources', sources, METRICS.sources.target, METRICS.sources.minAcceptable);
  results.quality = eval('quality', quality, METRICS.quality.target, METRICS.quality.minAcceptable);
  results.efficiency = eval('efficiency', last1h, METRICS.efficiency.target, METRICS.efficiency.minAcceptable);
  
  // 综合评分
  const weights = METRICS;
  let totalScore = 0;
  let totalWeight = 0;
  Object.keys(weights).forEach(k => {
    if (weights[k].weight > 0 && results[k]) {
      const w = weights[k].weight;
      totalScore += (results[k].ratio >= 1 ? 1 : Math.max(0, results[k].ratio)) * w;
      totalWeight += w;
    }
  });
  results.overallScore = ((totalScore / totalWeight) * 100).toFixed(1);
  results.overallStatus = results.overallScore >= 80 ? 'good' : results.overallScore >= 50 ? 'warning' : 'critical';
  
  return results;
}

// 权衡决策
function decide(evaluation) {
  const decisions = [];
  
  // 严重偏离 - 需要快速修复
  if (evaluation.efficiency.status === 'poor') {
    decisions.push({ urgency: 'high', action: '优化采集效率', reason: '效率严重不足' });
  }
  
  // 可接受偏离 - 长期观察
  if (evaluation.dailyRate.status === 'acceptable') {
    decisions.push({ urgency: 'low', action: '持续观察', reason: '日增长率可接受，预计30天达标' });
  }
  
  // 目标偏离过大 - 调整目标或策略
  if (evaluation.overallStatus === 'critical') {
    decisions.push({ urgency: 'high', action: '重新设计架构', reason: '整体评分过低，需要系统性改进' });
    decisions.push({ urgency: 'medium', action: '放宽短期指标', reason: '聚焦长期目标' });
  }
  
  // 良好状态 - 优化为主
  if (evaluation.overallStatus === 'good') {
    decisions.push({ urgency: 'low', action: '微调优化', reason: '系统运行良好' });
  }
  
  return decisions;
}

// 设计建议生成
function generateDesign(evaluation, decisions) {
  const designs = [];
  
  // 基于差距生成设计
  if (evaluation.efficiency.ratio < 0.1) {
    designs.push({
      type: 'architecture',
      priority: 'P0',
      title: '分布式采集架构',
      description: '当前效率过低，需要重新设计为多节点分布式采集',
      changes: ['增加采集器到50+', '引入消息队列', '优化API调用']
    });
  }
  
  if (evaluation.sources.ratio < 0.5) {
    designs.push({
      type: 'expansion',
      priority: 'P1',
      title: '多源采集扩展',
      description: '扩展数据来源',
      changes: ['接入GitHub API', '接入MCP Market', '接入Skill市场']
    });
  }
  
  if (evaluation.efficiency.ratio < 0.2) {
    designs.push({
      type: 'automation',
      priority: 'P0',
      title: '全自动化编排',
      description: '减少人工干预，自动调度',
      changes: ['自动扩缩容', '智能故障恢复', '自适应限流']
    });
  }
  
  return designs;
}

// 主循环 - 长周期评估
async function loop() {
  log('🎨 Designer 启动 - 系统设计器');
  
  let round = 0;
  while (true) {
    round++;
    log(`\n=== 设计评估轮次 ${round} ===`);
    
    const samples = readJson(path.join(DATA_DIR, 'samples.json'), []);
    const stats = readJson(path.join(DATA_DIR, 'orchestrator-stats.json'), {});
    
    // 评估指标
    const evaluation = evaluateMetrics(samples, stats);
    
    log(`📊 综合评分: ${evaluation.overallScore}% [${evaluation.overallStatus}]`);
    log(`   样本: ${evaluation.samples.current}/${evaluation.samples.target} (${evaluation.samples.ratio})`);
    log(`   日效: ${evaluation.dailyRate.current}/${evaluation.dailyRate.target} (${evaluation.dailyRate.ratio})`);
    log(`   来源: ${evaluation.sources.current}/${evaluation.sources.target} (${evaluation.sources.ratio})`);
    log(`   质量: ${evaluation.quality.current.toFixed(1)}%/${evaluation.quality.target}%`);
    log(`   效率: ${evaluation.efficiency.current}/${evaluation.efficiency.target}/h (${evaluation.efficiency.ratio})`);
    
    // 权衡决策
    const decisions = decide(evaluation);
    decisions.forEach(d => {
      log(`   ${d.urgency === 'high' ? '🔴' : d.urgency === 'medium' ? '🟡' : '🟢'} ${d.action}: ${d.reason}`);
    });
    
    // 生成设计
    const designs = generateDesign(evaluation, decisions);
    if (designs.length > 0) {
      log(`\n📐 设计建议:`);
      designs.forEach(d => {
        log(`   [${d.priority}] ${d.title}`);
        log(`      → ${d.description}`);
      });
    }
    
    // 保存设计
    const designRecord = {
      round,
      ts: new Date().toISOString(),
      evaluation,
      decisions,
      designs
    };
    
    const allDesigns = readJson(DESIGN_FILE, []);
    allDesigns.push(designRecord);
    if (allDesigns.length > 50) allDesigns.shift();
    writeJson(DESIGN_FILE, allDesigns);
    
    // 5分钟评估一次
    await new Promise(r => setTimeout(r, 300000));
  }
}

loop();
