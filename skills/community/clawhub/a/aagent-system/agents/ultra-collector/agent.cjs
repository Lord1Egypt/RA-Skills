#!/usr/bin/env node
/**
 * 🚀 Ultra Collector v2 - 带性能统计
 * 优化: 减少进程、添加统计、适配不同市场
 */

const fs = require('fs'), path = require('path'), https = require('https'), http = require('http');
const AGENT = process.env.AGENT_NAME || 'ultra';
const INDEX = process.env.AGENT_INDEX || 0;

const DATA = path.join(__dirname, '..', '..', 'data');
const SAMPLES = path.join(DATA, 'samples.json');
const PERF_FILE = path.join(DATA, 'perf-stats.json');

// 市场配置与极限
const MARKETS = {
  'npm': { 
    name: 'npm', 
    baseUrl: 'registry.npmjs.com', 
    timeout: 5000,
    rateLimit: 100, // 每分钟
    recommended: 3 // 推荐并发数
  },
  'cnpm': { 
    name: 'cnpm', 
    baseUrl: 'registry.npmmirror.com', 
    timeout: 5000,
    rateLimit: 150,
    recommended: 4
  }
};

// 高频关键词
const KEYWORDS = [
  'gpt', 'claude', 'openai', 'langchain', 'llm', 'ai', 'agent', 'chatgpt',
  'cursor', 'windsurf', 'vscode', 'plugin', 'ide', 'extension',
  'react', 'vue', 'angular', 'node', 'python', 'typescript',
  'docker', 'kubernetes', 'k8s', 'terraform',
  'telegram', 'discord', 'slack', 'feishu', 'lark',
  'mcp', 'mcp-server', 'skill',
  'crypto', 'web3', 'ethereum', 'wallet',
  'security', 'audit', 'pentest', 'cve'
];

function log(m) { console.log(`[${AGENT}-${INDEX}] ${m}`); }

function readJson(f, def = []) {
  if (!fs.existsSync(f)) return def;
  try { return JSON.parse(fs.readFileSync(f, 'utf8')) } catch { return def; }
}

function save(items) {
  if (!items.length) return 0;
  let s = readJson(SAMPLES);
  let c = 0;
  for (const pkg of items) {
    const key = `npm:${pkg.name}`;
    if (!s.find(x => `npm:${x.name}` === key)) {
      s.push({ ...pkg, source: pkg._source || 'npm', at: new Date().toISOString() });
      c++;
    }
  }
  fs.writeFileSync(SAMPLES, JSON.stringify(s, null, 2));
  return c;
}

function savePerf(market, success, timeMs, isTimeout) {
  let perf = readJson(PERF_FILE, { markets: {} });
  if (!perf.markets[market]) {
    perf.markets[market] = { requests: 0, success: 0, failed: 0, timeouts: 0, totalTime: 0, avgTime: 0 };
  }
  const m = perf.markets[market];
  m.requests++;
  m.totalTime += timeMs;
  m.avgTime = m.totalTime / m.requests;
  if (success) m.success++;
  else {
    m.failed++;
    if (isTimeout) m.timeouts++;
  }
  fs.writeFileSync(PERF_FILE, JSON.stringify(perf, null, 2));
}

function fetch(url, source) {
  const startTime = Date.now();
  return new Promise(resolve => {
    const proto = url.startsWith('https') ? https : http;
    const req = proto.get(url, { timeout: 5000 }, res => {
      const timeMs = Date.now() - startTime;
      if (res.statusCode !== 200) { 
        savePerf(source, false, timeMs, false);
        resolve([]); 
        return; 
      }
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          const items = (json.objects || []).map(o => ({
            name: o.package?.name,
            version: o.package?.version,
            description: o.package?.description,
            publisher: o.package?.publisher?.name,
            _source: source
          })).filter(x => x.name);
          savePerf(source, true, timeMs, false);
          resolve(items);
        } catch { 
          savePerf(source, false, timeMs, false);
          resolve([]); 
        }
      });
    });
    req.on('error', () => {
      savePerf(source, false, Date.now() - startTime, false);
      resolve([]);
    });
    req.on('timeout', () => { 
      req.destroy(); 
      savePerf(source, false, 5000, true);
      resolve([]); 
    });
  });
}

async function collect() {
  // 80% cnpm, 20% npm (根据性能指标)
  const market = Math.random() < 0.8 ? 'cnpm' : 'npm';
  const cfg = MARKETS[market];
  
  const kw = KEYWORDS[Math.floor(Math.random() * KEYWORDS.length)];
  const url = `https://${cfg.baseUrl}/-/v1/search?text=${encodeURIComponent(kw)}&size=30`;
  
  const items = await fetch(url, market);
  const saved = save(items);
  
  return saved;
}

async function loop() {
  log('🚀 Ultra v2 启动');
  
  while (true) {
    const saved = await collect();
    const total = readJson(SAMPLES).length;
    log(`+${saved} 总:${total}`);
    
    // 延迟 2-3秒 (平衡速度与资源)
    await new Promise(r => setTimeout(r, 2000 + Math.random() * 1000));
  }
}

loop();
