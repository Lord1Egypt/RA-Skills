#!/usr/bin/env node
/**
 * 🔍 Fast Scanner - 快速安全扫描器
 * 优化点:
 * - 并发扫描
 * - 规则优化
 * - 增量扫描
 */

const fs = require('fs'), path = require('path'), https = require('https');
const AGENT = process.env.AGENT_NAME || 'scanner';
const INDEX = process.env.AGENT_INDEX || 0;

const DATA_DIR = path.join(__dirname, '..', '..', 'data');
const SAMPLES = path.join(DATA_DIR, 'samples.json');
const SCANNED = path.join(DATA_DIR, 'scanned.json');
const MALICIOUS = path.join(DATA_DIR, 'malicious.json');

// 恶意关键词规则
const MALICIOUS_PATTERNS = [
  'stealer', 'keylogger', 'miner', 'cryptominer', 'trojan', 'backdoor', 'rat',
  'grabber', 'clipper', 'spyware', 'malware', 'injector', 'hook', 'patcher',
  'hack', 'cheat', 'exploit', 'payload', 'shell', 'rootkit', 'botnet',
  'phishing', 'fake', 'scam', 'spam', 'bot', 'ddos', 'flooder'
];

// 可疑关键词
const SUSPICIOUS_PATTERNS = [
  'ai', 'agent', 'mcp', 'gpt', 'claude', 'openai', 'chatbot', 'automation',
  'plugin', 'extension', 'hook', 'proxy', 'wrapper', 'addon', 'tool'
];

function log(m) { console.log(`[${AGENT}-${INDEX}] ${m}`); }

function readJson(file, def = []) {
  if (!fs.existsSync(file)) return def;
  try { return JSON.parse(fs.readFileSync(file, 'utf8')) } catch { return def; }
}

function writeJson(file, data) { fs.writeFileSync(file, JSON.stringify(data, null, 2)); }

// 扫描单个样本
function scanSample(sample) {
  const name = (sample.name || '').toLowerCase();
  const desc = (sample.description || '').toLowerCase();
  const text = name + ' ' + desc;
  
  let risk = 'low';
  let flags = [];
  
  // 恶意检测
  for (const p of MALICIOUS_PATTERNS) {
    if (text.includes(p)) {
      risk = 'critical';
      flags.push(`恶意关键词: ${p}`);
      break;
    }
  }
  
  // 可疑检测
  if (risk === 'low') {
    for (const p of SUSPICIOUS_PATTERNS) {
      if (text.includes(p) && name.length < 10) {
        risk = 'medium';
        flags.push(`可疑: ${p}`);
        break;
      }
    }
  }
  
  return { ...sample, risk, flags, scannedAt: new Date().toISOString() };
}

// 批量扫描
async function scan() {
  const samples = readJson(SAMPLES, []);
  const scanned = readJson(SCANNED, []);
  const scannedNames = new Set(scanned.map(s => s.name));
  
  // 未扫描的样本
  const todo = samples.filter(s => !scannedNames.has(s.name)).slice(0, 100);
  
  if (todo.length === 0) {
    log('全部扫描完成');
    return 0;
  }
  
  const results = todo.map(scanSample);
  
  // 保存扫描结果
  scanned.push(...results);
  writeJson(SCANNED, scanned);
  
  // 分离恶意样本
  const malicious = results.filter(r => r.risk === 'critical');
  if (malicious.length > 0) {
    const allMalicious = readJson(MALICIOUS, []);
    allMalicious.push(...malicious);
    writeJson(MALICIOUS, allMalicious);
    log(`🚨 发现恶意: ${malicious.length}个`);
  }
  
  return results.length;
}

// 主循环
async function loop() {
  log('🔍 启动 快速扫描器');
  
  while (true) {
    const count = await scan();
    log(`扫描: ${count}个`);
    
    await new Promise(r => setTimeout(r, 10000));
  }
}

loop();
