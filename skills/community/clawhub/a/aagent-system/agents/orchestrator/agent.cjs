#!/usr/bin/env node
/**
 * 🎯 Orchestrator v2 - 总体协调与健康保障
 * 
 * 核心职责:
 * - 启动所有必要角色
 * - 监控健康状态
 * - 阈值触发研究者
 * - 故障自动恢复
 */

const fs = require('fs'), path = require('path'), { exec } = require('child_process');
const AGENT_DIR = path.join(__dirname, '..');
const DATA_DIR = path.join(__dirname, '..', 'data');
const LOG_FILE = path.join(__dirname, '..', '..', 'data', 'orchestrator.log');

// 角色配置
const ROLES = {
  'ultra-collector': { count: 5, critical: true, restartDelay: 30000 },
  'fast-scanner': { count: 1, critical: true, restartDelay: 60000 },
  'evolver': { count: 1, critical: true, restartDelay: 300000 },
  'designer': { count: 1, critical: false, restartDelay: 300000 },
  'perf-monitor': { count: 1, critical: false, restartDelay: 60000 }
};

// 研究触发阈值
const RESEARCH_THRESHOLD = 1000; // 新增1000样本触发研究

let lastResearchCount = 0;
let lastSampleCount = 0;

function log(msg) {
  const ts = new Date().toISOString().slice(11, 19);
  const line = `[${ts}] ${msg}`;
  console.log(line);
  fs.appendFileSync(LOG_FILE, line + '\n');
}

// 检查进程状态
function checkProcess(name) {
  return new Promise(resolve => {
    exec(`pgrep -f "${name}" | wc -l`, (err, out) => {
      const count = parseInt(out.trim()) || 0;
      resolve(count);
    });
  });
}

// 启动角色
async function startRole(name, index = 0) {
  return new Promise(resolve => {
    const cmd = `cd ${__dirname} && AGENT_NAME=${name} AGENT_INDEX=${index} node agents/${name}/agent.cjs > /dev/null 2>&1 &`;
    exec(cmd);
    log(`🚀 启动 ${name}-${index}`);
    setTimeout(resolve, 2000);
  });
}

// 检查并恢复角色
async function checkAndRecover() {
  log('🔍 健康检查...');
  
  for (const [role, config] of Object.entries(ROLES)) {
    const running = await checkProcess(role);
    
    if (running < config.count) {
      log(`⚠️ ${role} 运行${running}个，需要${config.count}个`);
      
      // 启动缺失的进程
      for (let i = running; i < config.count; i++) {
        await startRole(role, i);
      }
    } else {
      log(`✅ ${role}: ${running}个运行中`);
    }
  }
}

// 检查是否需要触发研究
async function checkResearchTrigger() {
  const samples = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'samples.json'), 'utf8'));
  const currentCount = samples.length;
  const newSamples = currentCount - lastSampleCount;
  
  if (newSamples >= RESEARCH_THRESHOLD && (currentCount - lastResearchCount) >= RESEARCH_THRESHOLD) {
    log(`📊 触发研究: 新增${newSamples}个样本`);
    
    // 启动研究者
    const running = await checkProcess('researcher');
    if (running === 0) {
      await startRole('researcher');
      lastResearchCount = currentCount;
    }
  }
  
  lastSampleCount = currentCount;
}

// 总体状态报告
async function report() {
  const samples = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'samples.json'), 'utf8'));
  const malicious = JSON.parse(fs.readFileSync(path.join(DATA_DIR, 'malicious.json'), 'utf8'));
  
  log('========== 状态报告 ==========');
  log(`📦 样本: ${samples.length}`);
  log(`🚨 恶意: ${malicious.length}`);
  
  for (const [role, config] of Object.entries(ROLES)) {
    const running = await checkProcess(role);
    const status = running >= config.count ? '✅' : '❌';
    log(`${status} ${role}: ${running}/${config.count}`);
  }
  log('================================');
}

// 主循环
async function loop() {
  log('🎯 Orchestrator v2 启动');
  
  // 初始启动所有角色
  await checkAndRecover();
  
  let round = 0;
  while (true) {
    round++;
    
    // 每轮检查健康
    await checkAndRecover();
    
    // 检查研究触发
    await checkResearchTrigger();
    
    // 每5轮报告状态
    if (round % 5 === 0) {
      await report();
    }
    
    // 等待30秒
    await new Promise(r => setTimeout(r, 30000));
  }
}

loop();
