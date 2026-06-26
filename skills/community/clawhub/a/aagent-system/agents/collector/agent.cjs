#!/usr/bin/env node
const fs = require('fs'), path = require('path'), {exec} = require('child_process'), https = require('https'), http = require('http');
const AGENT = process.env.AGENT_NAME || 'collector';
const INDEX = process.env.AGENT_INDEX || 0;
const TARGET = 1000000;

const DATA = path.join(__dirname, '..', '..', 'data');
const SAMPLES = path.join(DATA, 'samples.json');
const STATS = { success: 0, fail: 0, total: 0 };

// 高质量核心关键词 (去除无效变体)
const CORE_KEYWORDS = [
  // AI/LLM
  'openclaw', 'claude', 'gpt', 'llm', 'langchain', 'openai', 'anthropic', 'gemini',
  'chatbot', 'ai-agent', 'autogen', 'crewai', 'phi-data',
  // IDE/Editor
  'cursor', 'windsurf', 'vscode', 'sublime', 'vim', 'emacs',
  // DevOps
  'docker', 'kubernetes', 'k8s', 'terraform', 'ansible',
  // Crypto
  'crypto', 'wallet', 'ethereum', 'solana', 'bitcoin', 'web3',
  // 通信
  'telegram', 'discord', 'slack', 'whatsapp', 'feishu', 'lark',
  // 效率
  'notion', 'obsidian', 'zapier', 'n8n', 'automation',
  // MCP/技能
  'mcp', 'mcp-server', 'mcp-client', 'skill', 'plugin', 'extension',
  // 安全 (攻防)
  'security', 'audit', 'pentest', 'exploit', 'vulnerability', 'cve',
  // 恶意样本关键词
  'stealer', 'keylogger', 'miner', 'cryptominer', 'trojan', 'backdoor', 'rat'
];

// 仅保留有效的变体
const VARIANTS = CORE_KEYWORDS.flatMap(kw => [
  kw, kw + '-js', kw + '-py', kw + '-ts', 
  kw + '-core', kw + '-cli', kw + '-sdk',
  '@' + kw, kw + '-ai', 'ai-' + kw
]);

const ALL_KEYWORDS = [...new Set([...CORE_KEYWORDS, ...VARIANTS])];

function log(m){ console.log(`[${AGENT}-${INDEX}] ${m}`); }

// HTTP 请求封装
function fetch(url, timeout = 10000) {
  return new Promise((resolve, reject) => {
    const proto = url.startsWith('https') ? https : http;
    const req = proto.get(url, { timeout }, res => {
      if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode}`));
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });
  });
}

function save(p){
  let s = [];
  if(fs.existsSync(SAMPLES)) try { s = JSON.parse(fs.readFileSync(SAMPLES, 'utf8')) } catch {}
  const key = `${p.source}:${p.name}`;
  if(s.find(x => `${x.source}:${x.name}` === key)) return false;
  s.push({ ...p, agent: AGENT, index: INDEX, at: new Date().toISOString() });
  fs.writeFileSync(SAMPLES, JSON.stringify(s, null, 2));
  return true;
}

function wait(ms) { return new Promise(r => setTimeout(r, ms)); }

// 使用 npm registry API
async function collectNpm(kw) {
  try {
    // 使用 registry.npmjs.com 搜索
    const url = `https://registry.npmjs.com/-/v1/search?text=${encodeURIComponent(kw)}&size=30&from=0`;
    const html = await fetch(url, 15000);
    const data = JSON.parse(html);
    
    if (data.objects && data.objects.length > 0) {
      let c = 0;
      for (const pkg of data.objects.slice(0, 30)) {
        const item = pkg.package;
        if (save({
          name: item.name,
          version: item.version,
          description: item.description,
          publisher: item.publisher?.name,
          source: 'npm-registry',
          keyword: kw,
          domain: 'npmjs.com'
        })) c++;
      }
      STATS.success += c;
      log(`+${c} ${kw}`);
      return c;
    }
  } catch (e) {
    STATS.fail++;
    log(`err ${kw}: ${e.message}`);
  }
  return 0;
}

// 备用: 使用 npm search
async function collectNpmSearch(kw) {
  try {
    const { exec } = require('child_process');
    return new Promise((resolve) => {
      exec(`npm search "${kw}" --json 2>/dev/null`, { timeout: 15000 }, (ex, out) => {
        if (ex) { resolve(0); return; }
        try {
          const p = JSON.parse(out);
          if (Array.isArray(p) && p.length) {
            let c = 0;
            for (const x of p.slice(0, 30)) {
              if (save({ name: x.name, version: x.version, source: 'npm', keyword: kw })) c++;
            }
            STATS.success += c;
            log(`+${c} ${kw} [search]`);
            resolve(c);
          } else {
            resolve(0);
          }
        } catch { resolve(0); }
      });
    });
  } catch { return 0; }
}

async function collect() {
  const kw = ALL_KEYWORDS[Math.floor(Math.random() * ALL_KEYWORDS.length)];
  STATS.total++;
  
  // 先尝试 npm registry API
  let count = await collectNpm(kw);
  
  // 如果没结果，备用 npm search
  if (count === 0) {
    await wait(1000); // 避免太快
    count = await collectNpmSearch(kw);
  }
  
  // 统计每100次
  if (STATS.total % 100 === 0) {
    const rate = STATS.success / STATS.total * 100;
    log(`统计: 成功率 ${rate.toFixed(1)}% (${STATS.success}/${STATS.total})`);
  }
}

async function loop() {
  log(`启动 优化版 目标:${TARGET} 关键词:${ALL_KEYWORDS.length}`);
  let round = 0;
  
  while (true) {
    round++;
    await collect();
    
    // 随机延迟 5-12 秒
    await wait(5000 + Math.random() * 7000);
    
    const s = fs.existsSync(SAMPLES) ? JSON.parse(fs.readFileSync(SAMPLES, 'utf8')).length : 0;
    log(`进度:${s}/${TARGET} 轮:${round}`);
  }
}

loop();
