#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { spawn, execSync } = require('child_process');

const BASE = path.join(__dirname, '..');
const DATA = path.join(BASE, 'data');
const AGENTS_DIR = path.join(BASE, 'agents');

const KEYWORDS_POOL = [
  ['openclaw','claude','gpt','agent','autogpt','langchain'],
  ['npm','pypi','pip','maven','composer','ruby'],
  ['vscode','cursor','sublime','vim','idea','webstorm'],
  ['docker','kubernetes','helm','terraform','ansible'],
  ['minecraft','mod','curseforge','fivem','roblox'],
  ['zapier','n8n','make','ifttt','apps-script'],
  ['chrome-extension','adblock','tampermonkey','ublock'],
  ['github-actions','gitlab-ci','jenkins','circleci'],
  ['airtable','retool','bubble','glide','nocodb'],
  ['react-native','flutter','cordova','ionic','uniapp'],
  ['crypto','wallet','nft','defi','ethereum','solana'],
  ['telegram','discord','slack','whatsapp','wechat'],
  ['notion','obsidian','evernote','trello','asana'],
  ['database','sql','mysql','postgresql','mongodb'],
  ['aws','azure','gcp','cloud','s3','lambda'],
  ['base-agent','system-updater','openclaw-core','polymarket','weather-assistant']
];

const AGENTS = {
  collector: { name: '采集器', script: path.join(AGENTS_DIR, 'collector', 'agent.cjs'), instances: 15 },
  scanner: { name: '扫描器', script: path.join(AGENTS_DIR, 'scanner', 'agent.cjs'), instances: 2 },
  analyzer: { name: '分析器', script: path.join(AGENTS_DIR, 'analyzer', 'agent.cjs'), instances: 1 },
  researcher: { name: '研究员', script: path.join(AGENTS_DIR, 'researcher', 'agent.cjs'), instances: 1 }
};

function getResources() {
  try {
    const mem = execSync("free | grep Mem | awk '{print int($3/$2*100)}'").toString().trim();
    const cpu = execSync("uptime | awk -F'load average:' '{print $2}' | awk '{print int($1)}'").toString().trim();
    const cores = execSync('nproc').toString().trim();
    return { mem: parseInt(mem), cpu: parseInt(cpu) / parseInt(cores) * 100 };
  } catch { return { mem: 50, cpu: 50 }; }
}

function log(m){ console.log(`[${new Date().toISOString().slice(11,19)}] ${m}`); }

async function startAgent(name, config, idx) {
  const pidFile = path.join(DATA, `${name}-${idx}.pid`);
  try { process.kill(fs.readFileSync(pidFile, 'utf8').trim(), 0); return; } catch {}
  const keywords = KEYWORDS_POOL[idx % KEYWORDS_POOL.length];
  const env = { ...process.env, AGENT_NAME: name, AGENT_INDEX: idx, AGENT_KEYWORDS: JSON.stringify(keywords) };
  const child = spawn('node', [config.script], { env, detached: false, stdio: ['ignore', 'pipe', 'pipe'] });
  child.stdout.on('data', d => process.stdout.write(`[${name}-${idx}] ${d}`));
  child.stderr.on('data', d => process.stderr.write(`[${name}-${idx}] ${d}`));
  fs.writeFileSync(pidFile, child.pid.toString());
  log(`启动 ${name}-${idx} PID:${child.pid}`);
}

async function startAll() {
  log('=== 启动多智能体系统 (15采集器) ===');
  if (!fs.existsSync(DATA)) fs.mkdirSync(DATA, { recursive: true });
  const res = getResources();
  log(`当前资源: CPU:${res.cpu.toFixed(0)}% 内存:${res.mem}%`);
  
  if (res.cpu < 70 && res.mem < 70) {
    log('资源充足，增加到15个采集器');
    AGENTS.collector.instances = 15;
  }
  
  for (const [name, config] of Object.entries(AGENTS)) {
    log(`启动 ${config.name} x${config.instances}`);
    for (let i = 0; i < config.instances; i++) await startAgent(name, config, i);
  }
  log('=== 全部启动完成 ===');
}

async function stopAll() {
  log('=== 停止智能体 ===');
  for (const [name, config] of Object.entries(AGENTS)) {
    for (let i = 0; i < 20; i++) {
      const pidFile = path.join(DATA, `${name}-${i}.pid`);
      try { process.kill(parseInt(fs.readFileSync(pidFile, 'utf8'))); } catch {}
      try { fs.unlinkSync(pidFile); } catch {}
    }
  }
}

async function status() {
  log('=== 智能体状态 ===');
  const res = getResources();
  console.log(`CPU: ${res.cpu.toFixed(0)}% 内存: ${res.mem}%`);
  let total = 0;
  for (const [name, config] of Object.entries(AGENTS)) {
    let running = 0;
    for (let i = 0; i < config.instances; i++) {
      const pidFile = path.join(DATA, `${name}-${i}.pid`);
      try { const pid = fs.readFileSync(pidFile, 'utf8').trim(); process.kill(pid, 0); running++; total++; } catch {}
    }
    console.log(`${config.name}: ${running}/${config.instances}`);
  }
  console.log(`总计: ${total} 进程`);
}

const cmd = process.argv[2];
if (cmd === 'start') startAll();
else if (cmd === 'stop') stopAll();
else if (cmd === 'status') status();
else console.log('用法: start|stop|status');
