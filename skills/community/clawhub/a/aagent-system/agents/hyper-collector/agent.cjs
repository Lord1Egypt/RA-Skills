#!/usr/bin/env node
/**
 * ⚡ Hyper Collector - 极速采集器
 * 优化点:
 * - 并发请求
 * - 批量关键词
 * - 高效API调用
 */

const fs = require('fs'), path = require('path'), https = require('https');
const AGENT = process.env.AGENT_NAME || 'hyper-collector';
const INDEX = process.env.AGENT_INDEX || 0;
const TARGET = 100000;

const DATA_DIR = path.join(__dirname, '..', '..', 'data');
const SAMPLES = path.join(DATA_DIR, 'samples.json');
const BATCH_SIZE = 50; // 每次批量采集数

// 高频关键词池
const KEYWORDS = [
  // AI/LLM
  'gpt', 'claude', 'openai', 'langchain', 'llm', 'chatgpt', 'ai', 'agent', 'autogen', 'crewai',
  // 开发工具
  'cursor', 'windsurf', 'vscode', 'vscode-extension', 'plugin', 'ide', 'editor',
  // 框架
  'react', 'vue', 'angular', 'node', 'python', 'typescript', 'javascript',
  // DevOps
  'docker', 'kubernetes', 'k8s', 'terraform', 'ansible', 'ci', 'cd',
  // 通信
  'telegram', 'discord', 'slack', 'whatsapp', 'feishu', 'lark', 'wechat',
  // MCP/技能
  'mcp', 'mcp-server', 'mcp-client', 'skill', 'openplugin',
  // Web3
  'crypto', 'web3', 'ethereum', 'solana', 'bitcoin', 'wallet', 'nft',
  // 安全
  'security', 'audit', 'pentest', 'exploit', 'vulnerability', 'cve', 'scan'
];

function log(m) { console.log(`[${AGENT}-${INDEX}] ${m}`); }

function readJson(file, def = []) {
  if (!fs.existsSync(file)) return def;
  try { return JSON.parse(fs.readFileSync(file, 'utf8')) } catch { return def; }
}

function saveBatch(items) {
  let s = readJson(SAMPLES);
  let c = 0;
  for (const pkg of items) {
    const key = `npm:${pkg.name}`;
    if (!s.find(x => `npm:${x.name}` === key)) {
      s.push({ ...pkg, source: 'npm-registry', at: new Date().toISOString() });
      c++;
    }
  }
  fs.writeFileSync(SAMPLES, JSON.stringify(s, null, 2));
  return c;
}

// 并发请求
function fetchNpm(keyword) {
  return new Promise((resolve, reject) => {
    const url = `https://registry.npmjs.com/-/v1/search?text=${encodeURIComponent(keyword)}&size=30`;
    https.get(url, { timeout: 8000 }, res => {
      if (res.statusCode !== 200) return resolve([]);
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          const items = (json.objects || []).map(o => ({
            name: o.package.name,
            version: o.package.version,
            description: o.package.description,
            publisher: o.package.publisher?.name
          }));
          resolve(items);
        } catch { resolve([]); }
      });
    }).on('error', () => resolve([])).on('timeout', () => resolve([]));
  });
}

async function collect() {
  // 随机选5个关键词并发
  const batch = [];
  for (let i = 0; i < 5; i++) {
    const kw = KEYWORDS[Math.floor(Math.random() * KEYWORDS.length)];
    batch.push(fetchNpm(kw));
  }
  
  const results = await Promise.all(batch);
  const flat = results.flat();
  const saved = saveBatch(flat);
  
  return saved;
}

async function loop() {
  log(`⚡ 启动 批量采集模式`);
  let round = 0;
  
  while (true) {
    round++;
    const saved = await collect();
    
    const s = readJson(SAMPLES).length;
    log(`轮${round}: +${saved} 总:${s}/${TARGET}`);
    
    // 随机延迟 2-5秒
    await new Promise(r => setTimeout(r, 2000 + Math.random() * 3000));
  }
}

loop();
