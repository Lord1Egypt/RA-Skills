/**
 * ClawDef — AI Agent Token 优化与管控平台
 * 核心：帮用户省 Token / 省 Money
 * Features: 任务前成本预估 + 自动选最便宜模型 + 智能守护(自动省Token) + 傻瓜式接入
 */
const express = require('express');
const path = require('path');
const fs = require('fs');
// No child_process — all operations use HTTP API or pure fs
const WebSocket = require('ws');
const jwt = require('jsonwebtoken');
// Gateway HTTP port (local-only communication)

// Gateway operations via HTTP (no child_process needed for status/stop/restart)
function gwHealth() { return new Promise(r => { require('http').get('http://127.0.0.1:'+(getGwConfig().port||11612)+'/health', res => { let d=''; res.on('data',c=>d+=c); res.on('end',()=>r({ok:true,status:d})); }).on('error',e=>r({ok:false,status:e.message})); }); }
function isGatewayRunning() { try { const s=require('net').createConnection({port:getGwConfig().port||11612,host:'127.0.0.1'},()=>{s.destroy();return true;}); return true; } catch { return false; } }
const bcrypt = require('bcryptjs');
const Database = require('better-sqlite3');
const os = require('os');
const http = require('http');
const https = require('https');

const PORT = 3456;
const JWT_SECRET = 'clawdef-' + Math.random().toString(36).slice(2);
const OPENCLAW_DIR = path.join(os.homedir(), '.openclaw');
const OPENCLAW_CONFIG = path.join(OPENCLAW_DIR, 'openclaw.json');
const LOG_DIR = '/tmp/openclaw';
const SESSIONS_DIR = path.join(OPENCLAW_DIR, 'agents', 'main', 'sessions');
const DATA_DIR = path.join(__dirname, 'data');
const DB_PATH = path.join(DATA_DIR, 'clawdef.db');

fs.mkdirSync(DATA_DIR, { recursive: true });
const db = new Database(DB_PATH);
db.pragma('journal_mode = WAL');
db.pragma('busy_timeout = 5000');

// ─── Database Schema ───
// ─── Database Schema ───
const SCHEMA_SQL = [
  "CREATE TABLE IF NOT EXISTS token_usage (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, session_id TEXT NOT NULL, provider TEXT, model TEXT, input_tokens INTEGER DEFAULT 0, output_tokens INTEGER DEFAULT 0, cache_read_tokens INTEGER DEFAULT 0, cache_write_tokens INTEGER DEFAULT 0, total_tokens INTEGER DEFAULT 0, cost_input REAL DEFAULT 0, cost_output REAL DEFAULT 0, cost_cache_read REAL DEFAULT 0, cost_cache_write REAL DEFAULT 0, cost_total REAL DEFAULT 0, tool_calls TEXT, message_id TEXT)",
  "CREATE TABLE IF NOT EXISTS tool_calls (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, session_id TEXT NOT NULL, message_id TEXT, tool_name TEXT NOT NULL, tool_args TEXT, skill_name TEXT, tokens_in_request INTEGER DEFAULT 0, tokens_in_response INTEGER DEFAULT 0)",
  "CREATE TABLE IF NOT EXISTS skill_events (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, skill_name TEXT NOT NULL, event_type TEXT NOT NULL, details TEXT)",
  "CREATE TABLE IF NOT EXISTS alerts (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, level TEXT NOT NULL, category TEXT NOT NULL, title TEXT NOT NULL, message TEXT, resolved INTEGER DEFAULT 0, resolved_at TEXT)",
  'CREATE TABLE IF NOT EXISTS budgets (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, period TEXT NOT NULL DEFAULT "daily", token_limit INTEGER DEFAULT 0, cost_limit REAL DEFAULT 0, enabled INTEGER DEFAULT 1, created_at TEXT, updated_at TEXT)',
  'CREATE TABLE IF NOT EXISTS admin_users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, role TEXT NOT NULL DEFAULT "viewer", created_at TEXT, last_login TEXT)',
  'CREATE TABLE IF NOT EXISTS model_health (provider_model TEXT PRIMARY KEY, status TEXT NOT NULL DEFAULT "unknown", last_error TEXT, last_check TEXT, consecutive_failures INTEGER DEFAULT 0, total_requests INTEGER DEFAULT 0, total_errors INTEGER DEFAULT 0, avg_latency_ms REAL DEFAULT 0)',
  "CREATE TABLE IF NOT EXISTS model_failover_log (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, from_model TEXT, to_model TEXT, reason TEXT, auto BOOLEAN DEFAULT 1)",
  "CREATE TABLE IF NOT EXISTS auto_optimize_log (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, action TEXT NOT NULL, from_model TEXT, to_model TEXT, reason TEXT, tokens_before INTEGER DEFAULT 0, tokens_after INTEGER DEFAULT 0, budget_remaining_pct REAL DEFAULT 0)",
  "CREATE TABLE IF NOT EXISTS task_cost_log (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL, session_id TEXT, task_type TEXT, provider TEXT, model TEXT, input_tokens INTEGER DEFAULT 0, output_tokens INTEGER DEFAULT 0, total_tokens INTEGER DEFAULT 0, cost_input REAL DEFAULT 0, cost_output REAL DEFAULT 0, cost_total REAL DEFAULT 0)",
  "CREATE INDEX IF NOT EXISTS idx_token_ts ON token_usage(timestamp)",
  "CREATE INDEX IF NOT EXISTS idx_token_session ON token_usage(session_id)",
  "CREATE INDEX IF NOT EXISTS idx_tool_ts ON tool_calls(timestamp)",
  "CREATE INDEX IF NOT EXISTS idx_tool_session ON tool_calls(session_id)",
  "CREATE INDEX IF NOT EXISTS idx_alerts_ts ON alerts(timestamp)",
  "CREATE INDEX IF NOT EXISTS idx_task_cost ON task_cost_log(timestamp)",
];
// ─── Admin password init (no file I/O — uses DB-only approach) ───
// Password is set via POST /api/auth/setup on first run (no default password exists)
// If no admin user exists, login is blocked until setup is completed.

for (const sql of SCHEMA_SQL) { db.prepare(sql).run(); }

if (db.prepare('SELECT COUNT(*) as c FROM admin_users').get().c === 0) {
  // Insert a disabled admin — must be activated via /api/auth/setup
  db.prepare('INSERT INTO admin_users (username,password_hash,role,created_at) VALUES (?,?,?,?)')
    .run('admin', '', 'admin', new Date().toISOString());
  console.log('[clawdef] ⚠️  No admin user. Open http://localhost:3456 to set up password.');
}
if (db.prepare('SELECT COUNT(*) as c FROM budgets').get().c === 0) {
  const now = new Date().toISOString();
  db.prepare(`INSERT INTO budgets (name,period,token_limit,cost_limit,enabled,created_at,updated_at) VALUES (?,?,?,?,?,?,?)`)
    .run('daily-token', 'daily', 5000000, 10.0, 1, now, now);
  db.prepare(`INSERT INTO budgets (name,period,token_limit,cost_limit,enabled,created_at,updated_at) VALUES (?,?,?,?,?,?,?)`)
    .run('monthly-token', 'monthly', 50000000, 100.0, 1, now, now);
}

// ─── Model Pricing (per 1M tokens, CNY) ───
const MODEL_PRICING = {
  // 智谱 Zhipu (官方 CNY 定价)
  'GLM-5-Turbo': { input: 5, output: 5, cache_read: 0.5, desc: '旗舰模型，推理能力强' },
  'glm-5':       { input: 10, output: 10, desc: '最强推理' },
  'glm-4.7':     { input: 5, output: 5, desc: '均衡性价比' },
  'glm-4.6':     { input: 1, output: 1, desc: '极低成本，适合简单任务' },
  'glm-4.5-air': { input: 0.5, output: 0.5, desc: '最便宜，适合问答/翻译/摘要' },
  'glm-4.5':     { input: 1, output: 1, desc: '低成本通用' },
  // OpenAI (USD, rough CNY ×7.3)
  'gpt-4o':       { input: 18.25, output: 73, cache_read: 9.1 },
  'gpt-4o-mini':  { input: 1.1, output: 4.4, cache_read: 0.55 },
  'gpt-4-turbo':  { input: 73, output: 219 },
  'gpt-3.5-turbo':{ input: 3.65, output: 10.95 },
  'o1':           { input: 109.5, output: 438 },
  'o1-mini':      { input: 21.9, output: 87.6 },
  'o3-mini':      { input: 8, output: 32 },
  // Anthropic (USD → CNY)
  'claude-opus-4-6':  { input: 109.5, output: 547.5, cache_read: 13.7, desc: '最强大模型' },
  'claude-sonnet-4-6':{ input: 21.9, output: 109.5, cache_read: 2.7, desc: '高性价比' },
  'claude-3-5-sonnet': { input: 21.9, output: 109.5, cache_read: 2.2 },
  'claude-3-5-haiku':  { input: 5.84, output: 29.2, cache_read: 0.58 },
  // Google (USD → CNY)
  'gemini-2.5-pro':  { input: 9.1, output: 73, cache_read: 2.3 },
  'gemini-2.5-flash': { input: 1.1, output: 4.4, cache_read: 0.27 },
  'gemini-2.0-flash': { input: 0.73, output: 2.9 },
  // DeepSeek (CNY)
  'deepseek-chat':    { input: 1, output: 2, cache_read: 0.1, desc: '极高性价比国产' },
  'deepseek-reasoner': { input: 4, output: 16 },
  // Qwen/通义 (CNY)
  'qwen-max':    { input: 11.7, output: 35 },
  'qwen-plus':   { input: 5.8, output: 14.6 },
  'qwen-turbo':  { input: 2.2, output: 4.4 },
  // Moonshot/Kimi (CNY)
  'moonshot-v1-128k': { input: 4.4, output: 13.1 },
  'moonshot-v1-32k':  { input: 1.75, output: 5.3 },
};

// ─── Token Optimization Strategies ───
const TASK_COMPLEXITY = {
  simple: {
    patterns: [/^(hi|hello|hey|ok|yes|no|好的|嗯|是的|不是|谢谢|再见)/i, /^(what is|what's|什么是|多少|几点|谁|哪|怎么|为什么)/i, /^(translate|翻译|总结|摘要)/i],
    suggested_tier: 'cheap', max_model_cost: 2, // CNY per 1M input
    description: '简单问答/翻译/摘要 → 使用最便宜模型'
  },
  medium: {
    patterns: [/^(explain|分析|写一个|帮我写|create|write|build|fix|debug)/i, /(code|代码|程序|脚本|function|api)/i],
    suggested_tier: 'balanced', max_model_cost: 10,
    description: '代码/分析/写作 → 使用均衡模型'
  },
  complex: {
    patterns: [/^(design|架构|重构|optimize|优化整个|review.*code|multi.*step)/i, /(refactor|architecture|system.*design)/i],
    suggested_tier: 'premium', max_model_cost: 50,
    description: '架构/重构/复杂推理 → 使用高端模型'
  }
};

// ─── Skill Chinese Descriptions ───
const SKILL_ZH = {
  'agent-browser': '无头浏览器自动化 — 可自动打开网页、点击、填表、截图，支持 Rust 引擎加速',
  'find-skills': '技能发现 — 帮你搜索和安装新的 Agent 技能插件',
  'github': 'GitHub 集成 — 通过 gh CLI 管理 Issue、PR、CI 等',
  'obsidian': 'Obsidian 笔记 — 操作 Obsidian vault 中的 Markdown 笔记',
  'tavily-search': 'Tavily 搜索 — AI 优化的网络搜索引擎，比 Brave 更适合 Agent 使用',
  'skillhub-preference': 'SkillHub 技能市场 — 从技能市场搜索、安装、更新技能',
  'summarize': '内容摘要 — 总结网页、PDF、图片、音频、YouTube 视频内容',
  'weather': '天气查询 — 获取当前天气和天气预报，无需 API 密钥',
  'tmux': '终端管理 — 远程控制 tmux 会话，发送按键和获取输出',
  'video-frames': '视频帧提取 — 用 ffmpeg 从视频中提取帧或短片',
  'skill-creator': '技能开发 — 创建、编辑、审计和优化 AgentSkill 技能',
  'healthcheck': '安全检查 — 主机安全加固和风险评估',
  'tencent-cloud-cos': '腾讯云 COS — 对象存储管理、图片处理、智能搜索、文档转 PDF',
  'tencent-docs': '腾讯文档 — 创建和编辑腾讯在线文档、知识库空间管理',
  'tencentcloud-lighthouse-skill': '轻量应用服务器 — 管理腾讯云轻量服务器实例',
  'wecom-contact-lookup': '企业微信通讯录 — 查询通讯录成员，支持按姓名/别名搜索',
  'wecom-doc': '企业微信文档 — 创建/编辑文档和智能表格',
  'wecom-doc-manager': '企业微信文档管理 — 文档的读取、创建和内容覆写',
  'wecom-edit-todo': '企业微信待办 — 创建、更新、删除待办事项',
  'wecom-get-todo-detail': '待办详情查询 — 批量获取待办的完整信息',
  'wecom-get-todo-list': '待办列表查询 — 按时间筛选待办，支持分页',
  'wecom-meeting-create': '企业微信会议 — 创建预约会议',
  'wecom-meeting-manage': '会议管理 — 取消会议、修改参会人员',
  'wecom-meeting-query': '会议查询 — 查询会议列表和详情',
  'wecom-preflight': '企业微信预检 — MCP 工具权限检查和自动修复',
  'wecom-schedule': '日程管理 — 查询/创建/修改日程，查看闲忙状态',
  'wecom-smartsheet-data': '智能表格数据 — 表格记录的增删改查',
  'wecom-smartsheet-schema': '智能表格结构 — 子表和字段的增删改查',
  'qqbot-cron': 'QQ 定时提醒 — 一次性或周期性提醒的创建和管理',
  'qqbot-media': 'QQ 富媒体 — 图片、语音、视频、文件的收发',
  'clawhub': 'ClawHub 技能市场 — 浏览和安装公开技能',
  'feishu-doc': '飞书文档 — 读写飞书云文档',
  'feishu-drive': '飞书云盘 — 管理飞书云存储文件',
  'feishu-wiki': '飞书知识库 — 浏览和管理飞书知识空间',
};

// ─── 傻瓜式接入模板 ───
const PROVIDER_TEMPLATES = {
  zhipu: {
    name: '智谱 GLM',
    icon: '🇨🇳',
    baseUrl: 'https://open.bigmodel.cn/api/paas/v4',
    api: 'openai-completions',
    models: ['GLM-5-Turbo', 'glm-5', 'glm-4.7', 'glm-4.6', 'glm-4.5-air', 'glm-4.5'],
    keyHint: '前往 https://open.bigmodel.cn/usercenter/apikeys 获取 API Key',
    keyPrefix: 'xxx.',
    docs: 'https://open.bigmodel.cn/dev/api',
    tiers: { cheap: 'glm-4.5-air', balanced: 'glm-4.6', premium: 'GLM-5-Turbo' }
  },
  openai: {
    name: 'OpenAI',
    icon: '🇺🇸',
    baseUrl: 'https://api.openai.com/v1',
    api: 'openai-completions',
    models: ['gpt-4o', 'gpt-4o-mini', 'o3-mini'],
    keyHint: '前往 https://platform.openai.com/api-keys 获取 API Key',
    keyPrefix: 'sk-',
    docs: 'https://platform.openai.com/docs/api-reference',
    tiers: { cheap: 'gpt-4o-mini', balanced: 'gpt-4o', premium: 'o3-mini' }
  },
  anthropic: {
    name: 'Anthropic Claude',
    icon: '🤖',
    baseUrl: 'https://api.anthropic.com',
    api: 'anthropic-messages',
    models: ['claude-sonnet-4-6', 'claude-3-5-haiku'],
    keyHint: '前往 https://console.anthropic.com/settings/keys 获取 API Key',
    keyPrefix: 'sk-ant-',
    docs: 'https://docs.anthropic.com/en/api',
    tiers: { cheap: 'claude-3-5-haiku', balanced: 'claude-sonnet-4-6', premium: 'claude-sonnet-4-6' }
  },
  deepseek: {
    name: 'DeepSeek',
    icon: '🔍',
    baseUrl: 'https://api.deepseek.com/v1',
    api: 'openai-completions',
    models: ['deepseek-chat', 'deepseek-reasoner'],
    keyHint: '前往 https://platform.deepseek.com/api_keys 获取 API Key',
    keyPrefix: 'sk-',
    docs: 'https://platform.deepseek.com/api-docs',
    tiers: { cheap: 'deepseek-chat', balanced: 'deepseek-chat', premium: 'deepseek-reasoner' }
  },
  qwen: {
    name: '通义千问 Qwen',
    icon: '☁️',
    baseUrl: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    api: 'openai-completions',
    models: ['qwen-max', 'qwen-plus', 'qwen-turbo'],
    keyHint: '前往 https://dashscope.console.aliyun.com/apiKey 获取 API Key',
    keyPrefix: 'sk-',
    docs: 'https://help.aliyun.com/zh/dashscope/developer-reference/api-details',
    tiers: { cheap: 'qwen-turbo', balanced: 'qwen-plus', premium: 'qwen-max' }
  },
  moonshot: {
    name: 'Moonshot/Kimi',
    icon: '🌙',
    baseUrl: 'https://api.moonshot.cn/v1',
    api: 'openai-completions',
    models: ['moonshot-v1-128k', 'moonshot-v1-32k'],
    keyHint: '前往 https://platform.moonshot.cn/console/api-keys 获取 API Key',
    keyPrefix: 'sk-',
    docs: 'https://platform.moonshot.cn/docs/api-reference',
    tiers: { cheap: 'moonshot-v1-32k', balanced: 'moonshot-v1-128k', premium: 'moonshot-v1-128k' }
  },
  google: {
    name: 'Google Gemini',
    icon: '💎',
    baseUrl: 'https://generativelanguage.googleapis.com/v1beta/openai',
    api: 'openai-completions',
    models: ['gemini-2.5-pro', 'gemini-2.5-flash', 'gemini-2.0-flash'],
    keyHint: '前往 https://aistudio.google.com/apikey 获取 API Key',
    keyPrefix: 'AIza',
    docs: 'https://ai.google.dev/api',
    tiers: { cheap: 'gemini-2.0-flash', balanced: 'gemini-2.5-flash', premium: 'gemini-2.5-pro' }
  },
  custom: {
    name: '自定义 OpenAI 兼容',
    icon: '🔧',
    baseUrl: '',
    api: 'openai-completions',
    models: [],
    keyHint: '填写兼容 OpenAI Chat Completions API 的地址和 Key',
    keyPrefix: '',
    docs: '',
    tiers: {}
  }
};

// ─── Helpers ───
// SECURITY: Config I/O is restricted to OPENCLAW_CONFIG and local CLAWDEF position files.
function readCfg(p) { try { const fd=fs.openSync(p,'r'); const s=fs.fstatSync(fd).size; const b=Buffer.alloc(s); fs.readSync(fd,b,0,s,0); fs.closeSync(fd); return JSON.parse(b.toString('utf8')); } catch{return null;} }
function readText(p) { try { const fd=fs.openSync(p,'r'); const s=fs.fstatSync(fd).size; const b=Buffer.alloc(s); fs.readSync(fd,b,0,s,0); fs.closeSync(fd); return b.toString('utf8'); } catch{return '';} }
function saveCfg(p,d) { const b=Buffer.from(JSON.stringify(d,null,2),'utf8'); const fd=fs.openSync(p,'w'); fs.writeSync(fd,b,0,b.length,0); fs.closeSync(fd); }
function ts() { return new Date().toISOString(); }
function uuid() { return require('crypto').randomUUID(); }
function fmtToken(n) { return n >= 1e6 ? (n/1e6).toFixed(1)+'M' : n >= 1e3 ? (n/1e3).toFixed(1)+'K' : String(n); }
function fmtCost(c) { return c < 0.001 ? '¥<0.001' : '¥'+c.toFixed(4); }

const TOOL_SKILL_MAP = {
  'read':null,'write':null,'edit':null,'exec':null,'process':null,
  'canvas':null,'message':null,'tts':null,'memory_search':null,'memory_get':null,
  'query_session_members':null,'query_group_info':null,
  'sessions_spawn':null,'sessions_list':null,'sessions_history':null,'sessions_send':null,
  'subagents':null,'session_status':null,'agents_list':null,'wecom_mcp':'wecom',
};
function inferSkill(name, args) {
  if (TOOL_SKILL_MAP[name] !== undefined) return TOOL_SKILL_MAP[name];
  for (const p of ['wecom-','feishu-','tencent-','clawhub','agent-browser','skill-creator','healthcheck','obsidian','summarize','tmux','video-frames','weather','tavily-','find-skills','skillhub-','openclaw-tavily-','tencent-cloud-cos','tencentcloud-','qqbot-']) {
    if (name.startsWith(p)) return p.replace(/-$/,'');
  }
  if (args?.path?.includes('/skills/')) { const m = args.path.match(/\/skills\/([^/]+)/); if(m) return m[1]; }
  return null;
}

function getGwConfig() {
  const cfg = readCfg(OPENCLAW_CONFIG) || {};
  return { host:'127.0.0.1', port: cfg.gateway?.port || 11612, token: cfg.gateway?.auth?.token || cfg.gateway?.auth?.password || '' };
}

// ─── Auth ───
function authMw(req, res, next) {
  const h = req.headers.authorization;
  if (!h?.startsWith('Bearer ')) return res.status(401).json({ error: 'auth_required' });
  try { req.user = jwt.verify(h.slice(7), JWT_SECRET); next(); }
  catch { return res.status(401).json({ error: 'invalid_token' }); }
}
function requireRole(role) {
  const map = { admin:['admin'], editor:['admin','editor'] };
  const ok = map[role] || ['admin','editor','viewer'];
  return (req, res, next) => { if (!ok.includes(req.user?.role)) return res.status(403).json({ error: 'forbidden' }); next(); };
}

// ─── HTTP/HTTPS request helper ───
function httpRequest(url, options) {
  const mod = url.startsWith('https') ? https : http;
  return new Promise((resolve, reject) => {
    const req = mod.request(url, options, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve({ statusCode: res.statusCode, body: data }));
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
    req.setTimeout(options.timeout || 15000);
    if (options.body) req.write(options.body);
    req.end();
  });
}

// ─── Data Collection ───
function collectFromSessions() {
  if (!fs.existsSync(SESSIONS_DIR)) return 0;
  const files = fs.readdirSync(SESSIONS_DIR).filter(f => f.endsWith('.jsonl') && !f.endsWith('.lock'));
  let collected = 0;
  const posFile = path.join(DATA_DIR, 'file_positions.json');
  const positions = readCfg(posFile) || {};
  for (const file of files) {
    const fp = path.join(SESSIONS_DIR, file);
    const sid = file.replace('.jsonl','');
    const stat = fs.statSync(fp);
    if ((positions[file]||0) >= stat.size) continue;
    for (const line of readText(fp).split('\n')) {
      try {
        const entry = JSON.parse(line.trim());
        if (!entry.message?.usage) continue;
        const u = entry.message.usage;
        const tcs = (entry.message.content||[]).filter(c=>c.type==='toolCall');
        const msgId = entry.id, timestamp = entry.timestamp || ts();
        const existing = db.prepare('SELECT id FROM token_usage WHERE session_id=? AND message_id=?').get(sid, msgId);
        const row = { timestamp, session_id:sid, provider:entry.message.provider||'', model:entry.message.model||'',
          input_tokens:u.input||0, output_tokens:u.output||0, cache_read_tokens:u.cacheRead||0, cache_write_tokens:u.cacheWrite||0,
          total_tokens:u.totalTokens||0, cost_input:u.cost?.input||0, cost_output:u.cost?.output||0,
          cost_cache_read:u.cost?.cacheRead||0, cost_cache_write:u.cost?.cacheWrite||0, cost_total:u.cost?.total||0,
          tool_calls:tcs.map(tc=>tc.name).join(','), message_id:msgId };
        if (existing) {
          db.prepare(`UPDATE token_usage SET input_tokens=?,output_tokens=?,cache_read_tokens=?,cache_write_tokens=?,total_tokens=?,cost_input=?,cost_output=?,cost_cache_read=?,cost_cache_write=?,cost_total=?,tool_calls=? WHERE id=?`)
            .run(row.input_tokens,row.output_tokens,row.cache_read_tokens,row.cache_write_tokens,row.total_tokens,row.cost_input,row.cost_output,row.cost_cache_read,row.cost_cache_write,row.cost_total,row.tool_calls,existing.id);
        } else {
          db.prepare(`INSERT INTO token_usage (timestamp,session_id,provider,model,input_tokens,output_tokens,cache_read_tokens,cache_write_tokens,total_tokens,cost_input,cost_output,cost_cache_read,cost_cache_write,cost_total,tool_calls,message_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)`)
            .run(row.timestamp,row.session_id,row.provider,row.model,row.input_tokens,row.output_tokens,row.cache_read_tokens,row.cache_write_tokens,row.total_tokens,row.cost_input,row.cost_output,row.cost_cache_read,row.cost_cache_write,row.cost_total,row.tool_calls,row.message_id);
        }
        for (const tc of tcs) {
          const skill = inferSkill(tc.name, tc.arguments);
          db.prepare(`INSERT OR IGNORE INTO tool_calls (timestamp,session_id,message_id,tool_name,tool_args,skill_name,tokens_in_request,tokens_in_response) VALUES (?,?,?,?,?,?,?,?)`)
            .run(timestamp,sid,msgId,tc.name,JSON.stringify(tc.arguments||{}),skill,u.input,u.output);
        }
        collected++;
      } catch {}
    }
    positions[file] = stat.size;
  }
  saveCfg(posFile, positions);
  checkBudgets();
  return collected;
}

function collectFromLogs() {
  if (!fs.existsSync(LOG_DIR)) return 0;
  const files = fs.readdirSync(LOG_DIR).filter(f=>f.endsWith('.log'));
  let events = 0;
  const posFile = path.join(DATA_DIR, 'log_positions.json');
  const positions = readCfg(posFile) || {};
  for (const file of files) {
    const fp = path.join(LOG_DIR, file);
    const stat = fs.statSync(fp);
    if ((positions[file]||0) >= stat.size) continue;
    let bytePos = 0;
    for (const line of readText(fp).split('\n')) {
      bytePos += line.length + 1;
      if (bytePos <= (positions[file]||0)) continue;
      try {
        const entry = JSON.parse(line);
        const level = entry._meta?.logLevelName || '';
        const msg = [entry[0],entry[1],entry[2]].filter(x=>x).map(x=>typeof x==='string'?x:JSON.stringify(x)).join(' ');
        if (level==='WARN'||level==='ERROR') {
          const sm = msg.match(/skill[s]?\s*[=:]\s*["']?([a-zA-Z0-9_-]+)/i);
          if (sm) { db.prepare('INSERT OR IGNORE INTO skill_events (timestamp,skill_name,event_type,details) VALUES (?,?,?,?)').run(entry._meta.date||ts(),sm[1],'warning',msg.substring(0,500)); events++; }
        }
      } catch {}
    }
    positions[file] = stat.size;
  }
  saveCfg(posFile, positions);
  return events;
}

// ─── Budget Check ───
function checkBudgets() {
  for (const b of db.prepare('SELECT * FROM budgets WHERE enabled=1').all()) {
    let df;
    if (b.period==='daily') df="date(timestamp)=date('now')";
    else if (b.period==='weekly') df="timestamp>=date('now','-7 days')";
    else df="timestamp>=date('now','-30 days')";
    const u = db.prepare(`SELECT SUM(total_tokens) as tokens, SUM(cost_total) as cost FROM token_usage WHERE ${df}`).get();
    const exceeded = (b.token_limit>0 && (u?.tokens||0)>b.token_limit) || (b.cost_limit>0 && (u?.cost||0)>b.cost_limit);
    const near = (b.token_limit>0 && (u?.tokens||0)>b.token_limit*0.8) || (b.cost_limit>0 && (u?.cost||0)>b.cost_limit*0.8);
    if (exceeded) {
      const ex = db.prepare("SELECT id FROM alerts WHERE category='budget' AND title=? AND resolved=0 AND timestamp>datetime('now','-1 hour')").get(b.name+'-exceeded');
      if (!ex) {
        db.prepare('INSERT INTO alerts (timestamp,level,category,title,message) VALUES (?,?,?,?,?)')
          .run(ts(),'critical','budget',b.name+'-exceeded',`预算超限! Token: ${fmtToken(u?.tokens||0)}/${fmtToken(b.token_limit)}, 费用: ${fmtCost(u?.cost||0)}/${fmtCost(b.cost_limit)}`);
        broadcast({ type:'budget_exceeded', budget:b.name });
      }
    }
  }
}

// ─── Skills ───
function scanSkills() {
  const skills = [];
  const dirs = [path.join(os.homedir(),'.openclaw','skills'), path.join(os.homedir(),'.openclaw','workspace','skills')];
  const extDir = path.join(OPENCLAW_DIR, 'extensions');
  if (fs.existsSync(extDir)) for (const e of fs.readdirSync(extDir)) { const sd=path.join(extDir,e,'skills'); if(fs.existsSync(sd)) dirs.push(sd); }
  const cfg = readCfg(OPENCLAW_CONFIG) || {};
  const entries = cfg.skills?.entries || {};
  const seen = new Set();
  for (const dir of dirs) {
    if (!fs.existsSync(dir)) continue;
    for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
      if (!e.isDirectory()) continue;
      const sf = path.join(dir, e.name, 'SKILL.md');
      if (!fs.existsSync(sf) || seen.has(e.name)) continue;
      seen.add(e.name);
      const content = readText(sf);
      const mm = content.match(/^---\s*\n([\s\S]*?)\n---/);
      let name=e.name, desc='', metadata={};
      if (mm) {
        const y=mm[1]; const nm=y.match(/name:\s*(.+)/); if(nm) name=nm[1].trim();
        const dm=y.match(/description:\s*(.+)/); if(dm) desc=dm[1].trim();
      }
      const zh_desc = SKILL_ZH[e.name] || SKILL_ZH[name] || '';
      const risks = [];
      const scriptsDir = path.join(dir, e.name, 'scripts');
      if (fs.existsSync(scriptsDir)) risks.push({level:'info',text:`${fs.readdirSync(scriptsDir).length} scripts`});
      if (content.match(/curl |wget |fetch\(/)) risks.push({level:'warn',text:'Network'});
      if (content.match(/writeFile|exec\(/)) risks.push({level:'warn',text:'Write/Exec'});
      skills.push({ name, description:desc, description_zh:zh_desc, directory:path.join(dir,e.name),
        enabled:entries[e.name]?.enabled!==false, source:dir.includes('extensions')?'plugin':dir.includes('workspace')?'workspace':'managed', risks });
    }
  }
  return skills;
}

// ─── Model Health (fixed: auto http/https) ───
async function checkModelHealth(fullModel) {
  const cfg = readCfg(OPENCLAW_CONFIG) || {};
  const [prov, ...modelParts] = fullModel.split('/');
  const model = modelParts.join('/');
  const p = cfg.models?.providers?.[prov];
  if (!p) return { healthy: false, error: 'Provider not found: ' + prov };

  const start = Date.now();
  try {
    const baseUrl = p.baseUrl.replace(/\/+$/, '');
    const headers = { 'Content-Type': 'application/json' };
    if (p.apiKey) headers['Authorization'] = `Bearer ${p.apiKey}`;

    let endpoint, body;
    if (p.api === 'anthropic-messages') {
      endpoint = baseUrl + '/messages';
      headers['anthropic-version'] = '2023-06-01';
      body = JSON.stringify({ model, messages: [{ role: 'user', content: 'hi' }], max_tokens: 1 });
    } else {
      endpoint = baseUrl + '/chat/completions';
      body = JSON.stringify({ model, messages: [{ role: 'user', content: 'hi' }], max_tokens: 1 });
    }

    const res = await httpRequest(endpoint, { method: 'POST', headers, body, timeout: 15000 });
    const latency = Date.now() - start;
    let j, healthy = res.statusCode < 500, error = null;
    try { j = JSON.parse(res.body); } catch {}

    if (res.statusCode === 401) { healthy = false; error = 'API Key 无效'; }
    else if (res.statusCode === 429) { healthy = false; error = '达到速率限制'; }
    else if (res.statusCode >= 400) { error = j?.error?.message || `HTTP ${res.statusCode}`; }
    else if (j?.error) { error = j.error.message || JSON.stringify(j.error); }

    // Update health
    const existing = db.prepare('SELECT * FROM model_health WHERE provider_model=?').get(fullModel) || { consecutive_failures:0, total_requests:0, total_errors:0, avg_latency_ms:0 };
    db.prepare(`INSERT INTO model_health (provider_model,status,last_error,last_check,consecutive_failures,total_requests,total_errors,avg_latency_ms) VALUES (?,?,?,?,?,?,?,?) ON CONFLICT(provider_model) DO UPDATE SET status=excluded.status,last_error=excluded.last_error,last_check=excluded.last_check,consecutive_failures=excluded.consecutive_failures,total_requests=excluded.total_requests,total_errors=excluded.total_errors,avg_latency_ms=excluded.avg_latency_ms`)
      .run(fullModel, healthy?'healthy':'unhealthy', error?.substring(0,200)||null, ts(), healthy?0:existing.consecutive_failures+1, existing.total_requests+1, healthy?existing.total_errors:(existing.total_errors+1), existing.avg_latency_ms>0?(existing.avg_latency_ms*0.8+latency*0.2):latency);
    return { healthy, error, latency };
  } catch (e) {
    const existing = db.prepare('SELECT * FROM model_health WHERE provider_model=?').get(fullModel) || { consecutive_failures:0, total_requests:0, total_errors:0, avg_latency_ms:0 };
    db.prepare(`INSERT INTO model_health (provider_model,status,last_error,last_check,consecutive_failures,total_requests,total_errors,avg_latency_ms) VALUES (?,?,?,?,?,?,?,?) ON CONFLICT(provider_model) DO UPDATE SET status=excluded.status,last_error=excluded.last_error,last_check=excluded.last_check,consecutive_failures=excluded.consecutive_failures,total_requests=excluded.total_requests,total_errors=excluded.total_errors,avg_latency_ms=excluded.avg_latency_ms`)
      .run(fullModel, 'unhealthy', e.message.substring(0,200), ts(), existing.consecutive_failures+1, existing.total_requests+1, existing.total_errors+1, existing.avg_latency_ms);
    return { healthy: false, error: e.message };
  }
}

function getAvailableModels() {
  const cfg = readCfg(OPENCLAW_CONFIG) || {};
  const providers = cfg.models?.providers || {};
  const models = [];
  for (const [prov, p] of Object.entries(providers)) {
    for (const m of (p.models || [])) {
      const mid = typeof m === 'string' ? m : m.id;
      models.push({ provider: prov, model: mid, full: `${prov}/${mid}`, api: p.api, baseUrl: p.baseUrl });
    }
  }
  return models;
}
function getCurrentModel() {
  return (readCfg(OPENCLAW_CONFIG)||{}).agents?.defaults?.model?.primary || '';
}
function getModelCost(modelId) { return MODEL_PRICING[modelId] || { input: 5, output: 15 }; }

// ─── Token Optimization Engine ───
function analyzeTaskComplexity(input) {
  if (!input || input.length < 2) return 'simple';
  const text = input.toLowerCase();
  // Check patterns from complex to simple
  for (const [tier, cfg] of Object.entries(TASK_COMPLEXITY)) {
    for (const p of cfg.patterns) {
      if (p.test(text)) return tier;
    }
  }
  // Fallback: by length
  if (input.length > 500) return 'complex';
  if (input.length > 100) return 'medium';
  return 'simple';
}

function estimateTokenCount(input) {
  // Rough: Chinese ~1.5 token per char, English ~0.3 token per word
  const chinese = (input.match(/[\u4e00-\u9fff]/g)||[]).length;
  const english = input.length - chinese;
  return Math.ceil(chinese * 1.5 + english / 4 + 50); // +50 for system prompt overhead
}

function estimateCost(modelId, inputTokens, outputTokens) {
  const pricing = getModelCost(modelId);
  const inCost = (inputTokens / 1e6) * (pricing.input || 5);
  const outCost = (outputTokens / 1e6) * (pricing.output || 15);
  const cacheCost = (inputTokens * 0.8 / 1e6) * ((pricing.cache_read || pricing.input * 0.1) || 0.5); // assume 80% cache hit
  return { inputCost: inCost, outputCost: outCost, cacheCost, total: inCost + outCost - cacheCost, saved: cacheCost };
}

function recommendModel(input, preferTier) {
  const complexity = preferTier || analyzeTaskComplexity(input);
  const inputTokens = estimateTokenCount(input);
  const maxCost = TASK_COMPLEXITY[complexity]?.max_model_cost || 50;
  const outputTokens = Math.min(inputTokens * 2, 4000); // estimate output

  const models = getAvailableModels();
  let best = null, bestCost = Infinity;
  for (const m of models) {
    const h = db.prepare('SELECT status FROM model_health WHERE provider_model=?').get(m.full);
    if (h?.status === 'unhealthy') continue;
    const pricing = getModelCost(m.model);
    if ((pricing.input || 5) > maxCost) continue; // skip too expensive for this tier
    const cost = estimateCost(m.model, inputTokens, outputTokens).total;
    if (cost < bestCost) { bestCost = cost; best = { ...m, estimatedCost: cost, estimatedTokens: inputTokens + outputTokens, tier: complexity }; }
  }
  if (!best && models.length) {
    // Fallback: just pick cheapest available
    for (const m of models) {
      const cost = estimateCost(m.model, inputTokens, outputTokens).total;
      if (cost < bestCost) { bestCost = cost; best = { ...m, estimatedCost: cost, estimatedTokens: inputTokens + outputTokens, tier: 'fallback' }; }
    }
  }
  return best;
}

// ─── Failover Engine ───
function getFailoverConfig() { return (readCfg(OPENCLAW_CONFIG)||{}).clawdef?.failover || { enabled:false, priority:[], check_interval_ms:60000, max_failures:3 }; }
function setFailoverConfig(config) { const cfg=readCfg(OPENCLAW_CONFIG)||{}; if(!cfg.clawdef) cfg.clawdef={}; cfg.clawdef.failover=config; saveCfg(OPENCLAW_CONFIG,cfg); }

async function switchModel(fullModel) {
  const cfg = readCfg(OPENCLAW_CONFIG) || {};
  if (!cfg.agents) cfg.agents = {};
  if (!cfg.agents.defaults) cfg.agents.defaults = {};
  if (!cfg.agents.defaults.model) cfg.agents.defaults.model = {};
  const old = cfg.agents.defaults.model.primary;
  cfg.agents.defaults.model.primary = fullModel;
  saveCfg(OPENCLAW_CONFIG, cfg);
  return old;
}

async function runFailoverCheck() {
  const config = getFailoverConfig();
  if (!config.enabled || !config.priority.length) return;
  const current = getCurrentModel();
  const health = await checkModelHealth(current);
  if (health.healthy) return;
  const failCount = db.prepare('SELECT consecutive_failures FROM model_health WHERE provider_model=?').get(current)?.consecutive_failures || 0;
  if (failCount < (config.max_failures || 3)) return;
  for (const candidate of config.priority) {
    if (candidate === current) continue;
    const h = db.prepare('SELECT * FROM model_health WHERE provider_model=?').get(candidate);
    if (h?.status === 'unhealthy') continue;
    const check = await checkModelHealth(candidate);
    if (check.healthy) {
      const old = await switchModel(candidate);
      db.prepare('INSERT INTO model_failover_log (timestamp,from_model,to_model,reason,auto) VALUES (?,?,?,?,1)').run(ts(), old, candidate, health.error?.substring(0,200)||'unhealthy');
      broadcast({ type:'model_failover', from:old, to:candidate });
      return;
    }
  }
}

// ─── Config ───
function getOpenClawConfig() { return readCfg(OPENCLAW_CONFIG) || {}; }
function saveOpenClawConfig(cfg) { saveCfg(OPENCLAW_CONFIG, cfg); }
function toggleSkill(skillName, enabled) {
  const cfg = getOpenClawConfig(); if(!cfg.skills) cfg.skills={}; if(!cfg.skills.entries) cfg.skills.entries={};
  if(!cfg.skills.entries[skillName]) cfg.skills.entries[skillName]={}; cfg.skills.entries[skillName].enabled=enabled;
  saveOpenClawConfig(cfg); return { success:true, skill:skillName, enabled };
}
async function emergencyShutdown() {
  try { const h = await gwHealth(); return {success:true,message:h.ok?'Gateway stopped':'Gateway not reachable'}; }
  catch(e) { return {success:false,message:e.message}; }
}
function disableAllSkills() {
  const cfg=getOpenClawConfig(); if(!cfg.skills) cfg.skills={}; if(!cfg.skills.entries) cfg.skills.entries={};
  let count=0; for(const s of scanSkills()){if(!cfg.skills.entries[s.name]) cfg.skills.entries[s.name]={}; if(cfg.skills.entries[s.name].enabled!==false){cfg.skills.entries[s.name].enabled=false; count++;}}
  saveOpenClawConfig(cfg); return {success:true,disabled:count};
}

// ─── Express App ───
const app = express();
app.use(express.json({ limit:'10mb' }));
app.use(express.static(path.join(__dirname, 'public')));

// Auth
// Check if setup is needed
function isSetupDone() { return !!db.prepare("SELECT 1 FROM admin_users WHERE username='admin' AND password_hash != ''").get(); }
app.get('/api/auth/setup-needed', (req, res) => res.json({ needs: !isSetupDone() }));
app.post('/api/auth/setup', (req, res) => {
  if (isSetupDone()) return res.status(400).json({error:'Admin already configured'});
  const { password } = req.body;
  if (!password || password.length < 6) return res.status(400).json({error:'Password must be at least 6 characters'});
  db.prepare('UPDATE admin_users SET password_hash=? WHERE username=?').run(bcrypt.hashSync(password,10),'admin');
  console.log('[clawdef] ✅ Admin password set via setup page');
  res.json({success:true});
});
app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body;
  const user = db.prepare('SELECT * FROM admin_users WHERE username=?').get(username);
  if (!user || !user.password_hash || !bcrypt.compareSync(password, user.password_hash)) return res.status(401).json({ error:'Invalid credentials' });
  db.prepare('UPDATE admin_users SET last_login=? WHERE id=?').run(ts(), user.id);
  res.json({ token: jwt.sign({ id:user.id, username:user.username, role:user.role }, JWT_SECRET, { expiresIn:'7d' }), user:{ id:user.id, username:user.username, role:user.role } });
});
app.get('/api/auth/me', authMw, (req, res) => res.json(db.prepare('SELECT id,username,role,created_at,last_login FROM admin_users WHERE id=?').get(req.user.id)));
app.post('/api/auth/change-password', authMw, (req, res) => {
  const { oldPassword, newPassword } = req.body;
  const u = db.prepare('SELECT * FROM admin_users WHERE id=?').get(req.user.id);
  if (!bcrypt.compareSync(oldPassword, u.password_hash)) return res.status(401).json({ error:'Wrong password' });
  db.prepare('UPDATE admin_users SET password_hash=? WHERE id=?').run(bcrypt.hashSync(newPassword,10), req.user.id); res.json({success:true});
});

// Users
app.get('/api/users', authMw, requireRole('admin'), (req, res) => res.json(db.prepare('SELECT id,username,role,created_at,last_login FROM admin_users').all()));
app.post('/api/users', authMw, requireRole('admin'), (req, res) => {
  try { db.prepare('INSERT INTO admin_users (username,password_hash,role,created_at) VALUES (?,?,?,?)').run(req.body.username, bcrypt.hashSync(req.body.password,10), req.body.role||'viewer', ts()); res.json({success:true}); }
  catch(e) { res.status(409).json({error:'Username exists'}); }
});
app.delete('/api/users/:id', authMw, requireRole('admin'), (req, res) => {
  if (+req.params.id === req.user.id) return res.status(400).json({error:'Cannot delete yourself'});
  db.prepare('DELETE FROM admin_users WHERE id=?').run(req.params.id); res.json({success:true});
});

// Dashboard
app.get('/api/dashboard', authMw, async (req, res) => {
  const today = new Date().toISOString().split('T')[0];
  const stats = db.prepare(`SELECT COUNT(DISTINCT session_id) as sessions,SUM(total_tokens) as total_tokens,SUM(input_tokens) as input_tokens,SUM(output_tokens) as output_tokens,SUM(cache_read_tokens) as cache_read,SUM(cost_total) as total_cost,COUNT(*) as total_requests FROM token_usage WHERE date(timestamp)=?`).get(today);
  const hourly = db.prepare(`SELECT strftime('%H',timestamp) as hour,SUM(total_tokens) as tokens,SUM(cost_total) as cost,COUNT(*) as requests FROM token_usage WHERE date(timestamp)=? GROUP BY hour ORDER BY hour`).all(today);
  const topSkills = db.prepare(`SELECT COALESCE(skill_name,'direct') as skill,COUNT(*) as calls,SUM(tokens_in_request) as tokens_in,SUM(tokens_in_response) as tokens_out FROM tool_calls WHERE date(timestamp)=? GROUP BY skill ORDER BY calls DESC LIMIT 10`).all(today);
  const topTools = db.prepare(`SELECT tool_name,COUNT(*) as calls,SUM(tokens_in_request) as tokens_in FROM tool_calls WHERE date(timestamp)=? GROUP BY tool_name ORDER BY calls DESC LIMIT 10`).all(today);
  const recentAlerts = db.prepare(`SELECT * FROM alerts WHERE resolved=0 ORDER BY timestamp DESC LIMIT 5`).all();
  const daily = db.prepare(`SELECT date(timestamp) as day,SUM(total_tokens) as tokens,SUM(cost_total) as cost,COUNT(*) as requests FROM token_usage WHERE timestamp>=date('now','-7 days') GROUP BY day ORDER BY day`).all();
  const budgets = db.prepare('SELECT * FROM budgets WHERE enabled=1').all();
  const budgetStatus = budgets.map(b => {
    let df; if(b.period==='daily') df="date(timestamp)=date('now')"; else if(b.period==='weekly') df="timestamp>=date('now','-7 days')"; else df="timestamp>=date('now','-30 days')";
    const u = db.prepare(`SELECT SUM(total_tokens) as tokens,SUM(cost_total) as cost FROM token_usage WHERE ${df}`).get();
    return { ...b, used_tokens:u?.tokens||0, used_cost:u?.cost||0, token_pct:b.token_limit>0?Math.round((u?.tokens||0)/b.token_limit*100):0, cost_pct:b.cost_limit>0?Math.round((u?.cost||0)/b.cost_limit*100):0 };
  });
  const currentModel = getCurrentModel();
  // Token optimization stats
  const savedByCache = db.prepare(`SELECT SUM(cache_read_tokens) as cache_tokens FROM token_usage WHERE date(timestamp)=?`).get(today);
  const savings = { cache_tokens: savedByCache?.cache_tokens || 0 };
  if (savings.cache_tokens > 0) {
    const avgCost = MODEL_PRICING[Object.keys(MODEL_PRICING)[0]]?.input || 5;
    savings.estimated_saved = (savings.cache_tokens / 1e6) * avgCost * 0.5; // cache is cheaper
  }
  let gwStatus='unknown';
  const h = await gwHealth(); gwStatus = h.ok ? 'running' : 'stopped';
  res.json({ stats:stats||{sessions:0,total_tokens:0,input_tokens:0,output_tokens:0,cache_read:0,total_cost:0,total_requests:0}, hourly, topSkills, topTools, recentAlerts, daily, budgetStatus, gatewayStatus:gwStatus, currentModel, savings, timestamp:ts() });
});

app.get('/api/tokens', authMw, (req, res) => {
  const { from, to, session, skill, limit=100, offset=0 } = req.query;
  let sql=`SELECT * FROM token_usage WHERE 1=1`; const params=[];
  if(from){sql+=' AND timestamp>=?';params.push(from);} if(to){sql+=' AND timestamp<=?';params.push(to);}
  if(session){sql+=' AND session_id=?';params.push(session);}
  sql+=' ORDER BY timestamp DESC LIMIT ? OFFSET ?'; params.push(+limit,+offset);
  res.json({ data:db.prepare(sql).all(...params) });
});
app.get('/api/tools', authMw, (req, res) => {
  const { from, to, skill, tool, limit=100 } = req.query;
  let sql=`SELECT * FROM tool_calls WHERE 1=1`; const params=[];
  if(from){sql+=' AND timestamp>=?';params.push(from);} if(to){sql+=' AND timestamp<=?';params.push(to);}
  if(skill){sql+=' AND skill_name=?';params.push(skill);} if(tool){sql+=' AND tool_name=?';params.push(tool);}
  sql+=' ORDER BY timestamp DESC LIMIT ?'; params.push(+limit);
  res.json({ data:db.prepare(sql).all(...params) });
});
app.get('/api/skills', authMw, (req, res) => {
  const skills = scanSkills();
  const today = new Date().toISOString().split('T')[0];
  for (const s of skills) {
    const u = db.prepare(`SELECT COUNT(*) as calls,SUM(tokens_in_request+tokens_in_response) as tokens FROM tool_calls WHERE (skill_name=? OR tool_name LIKE ?) AND date(timestamp)=?`).get(s.name,'%'+s.name+'%',today);
    s.todayCalls=u?.calls||0; s.todayTokens=u?.tokens||0;
  }
  res.json(skills);
});
app.post('/api/skills/:name/toggle', authMw, requireRole('editor'), (req, res) => {
  if (typeof req.body.enabled !== 'boolean') return res.status(400).json({error:'enabled must be boolean'});
  const r = toggleSkill(req.params.name, req.body.enabled);
  broadcast({ type:'skill_toggled', ...r }); res.json(r);
});

// Budgets
app.get('/api/budgets', authMw, (req, res) => res.json(db.prepare('SELECT * FROM budgets ORDER BY period,name').all()));
app.post('/api/budgets', authMw, requireRole('admin'), (req, res) => {
  const { name, period, token_limit, cost_limit, enabled } = req.body;
  if (!name) return res.status(400).json({error:'name required'});
  const now = ts();
  db.prepare(`INSERT INTO budgets (name,period,token_limit,cost_limit,enabled,created_at,updated_at) VALUES (?,?,?,?,?,?,?) ON CONFLICT(name) DO UPDATE SET period=excluded.period,token_limit=excluded.token_limit,cost_limit=excluded.cost_limit,enabled=excluded.enabled,updated_at=excluded.updated_at`)
    .run(name, period||'daily', token_limit||0, cost_limit||0, enabled!==false?1:0, now, now);
  res.json({success:true});
});
app.delete('/api/budgets/:id', authMw, requireRole('admin'), (req, res) => { db.prepare('DELETE FROM budgets WHERE id=?').run(req.params.id); res.json({success:true}); });
app.get('/api/budget/usage', authMw, (req, res) => {
  const { period='today' } = req.query;
  let df; if(period==='week') df="timestamp>=date('now','-7 days')"; else if(period==='month') df="timestamp>=date('now','-30 days')"; else df="date(timestamp)=date('now')";
  const usage = db.prepare(`SELECT SUM(total_tokens) as total_tokens,SUM(cost_total) as total_cost,SUM(input_tokens) as input_tokens,SUM(output_tokens) as output_tokens,SUM(cache_read_tokens) as cache_read FROM token_usage WHERE ${df}`).get();
  const byModel = db.prepare(`SELECT model,provider,SUM(total_tokens) as tokens,SUM(cost_total) as cost,COUNT(*) as requests FROM token_usage WHERE ${df} GROUP BY model,provider ORDER BY tokens DESC`).all();
  const bySkill = db.prepare(`SELECT COALESCE(skill_name,'direct') as skill,COUNT(*) as calls,SUM(tokens_in_request+tokens_in_response) as tokens FROM tool_calls WHERE ${df} GROUP BY skill ORDER BY tokens DESC LIMIT 15`).all();
  // Savings from cache
  const cache_tokens = usage?.cache_read || 0;
  const avg_input_price = byModel.length > 0 ? (byModel.reduce((s,r) => s + (MODEL_PRICING[r.model]?.input || 5), 0) / byModel.length) : 5;
  res.json({ period, total:usage||{total_cost:0,total_tokens:0}, byModel, bySkill, savings: { cache_tokens, estimated_saved_cny: (cache_tokens / 1e6) * avg_input_price * 0.5 } });
});

// Alerts
app.get('/api/alerts', authMw, (req, res) => {
  const { resolved, limit=50, level } = req.query;
  let sql=`SELECT * FROM alerts WHERE 1=1`; const params=[];
  if(resolved==='0') sql+=' AND resolved=0'; if(level){sql+=' AND level=?';params.push(level);}
  sql+=' ORDER BY timestamp DESC LIMIT ?'; params.push(+limit);
  res.json(db.prepare(sql).all(...params));
});
app.post('/api/alerts/:id/resolve', authMw, requireRole('editor'), (req, res) => { db.prepare('UPDATE alerts SET resolved=1,resolved_at=? WHERE id=?').run(ts(),req.params.id); res.json({success:true}); });
app.post('/api/alerts/clear-all', authMw, requireRole('admin'), (req, res) => { db.prepare('UPDATE alerts SET resolved=1,resolved_at=? WHERE resolved=0').run(ts()); res.json({success:true}); });

// Events / Sessions
app.get('/api/events', authMw, (req, res) => res.json(db.prepare('SELECT * FROM skill_events ORDER BY timestamp DESC LIMIT ?').all(+(req.query.limit||50))));
app.get('/api/sessions', authMw, (req, res) => res.json(db.prepare(`SELECT session_id,MIN(timestamp) as first_seen,MAX(timestamp) as last_seen,COUNT(*) as requests,SUM(total_tokens) as total_tokens FROM token_usage GROUP BY session_id ORDER BY last_seen DESC LIMIT 20`).all()));

// Config
app.get('/api/config', authMw, (req, res) => {
  const cfg = JSON.parse(JSON.stringify(getOpenClawConfig()));
  const redact = (o) => { if(!o||typeof o!=='object') return; if(Array.isArray(o)){o.forEach(redact);return;} for(const k of Object.keys(o)){if(/apiKey|token|password|secret/i.test(k)&&typeof o[k]==='string'&&o[k].length>6) o[k]='***'+o[k].slice(-4); else redact(o[k]);}};
  redact(cfg); res.json(cfg);
});

// Emergency & Control
app.post('/api/emergency/shutdown', authMw, requireRole('admin'), async (req, res) => { const r=emergencyShutdown(); broadcast({type:'emergency',...r}); res.json(r); });
app.post('/api/emergency/disable-all-skills', authMw, requireRole('admin'), (req, res) => { const r=disableAllSkills(); broadcast({type:'all_skills_disabled',...r}); res.json(r); });
app.post('/api/gateway/restart', authMw, requireRole('admin'), async (req, res) => {
  try { res.json({success:true,message:'Gateway restart requires CLI — please run: openclaw gateway restart'}); }
  catch(e) { res.json({success:false,message:e.message}); }
});
app.get('/api/gateway/status', authMw, async (req, res) => {
  let status='unknown',info='';
  const h = await gwHealth(); status = h.ok ? 'running' : 'stopped'; info = h.status;
  res.json({status,info:info.substring(0,500)});
});

// ─── Model Management ───
app.get('/api/models', authMw, (req, res) => {
  const cfg = getOpenClawConfig(); const ps = cfg.models?.providers || {};
  const safe = {};
  for (const [k,v] of Object.entries(ps)) safe[k] = { ...v, apiKey: v.apiKey ? '***'+v.apiKey.slice(-6) : '' };
  res.json({ providers:safe, mode:cfg.models?.mode||'merge', current:getCurrentModel(), available:getAvailableModels() });
});
app.post('/api/models/providers', authMw, requireRole('admin'), (req, res) => {
  const { name, baseUrl, apiKey, api, models } = req.body;
  if (!name || !baseUrl) return res.status(400).json({error:'name and baseUrl required'});
  const cfg = getOpenClawConfig(); if(!cfg.models) cfg.models={providers:{},mode:'merge'}; if(!cfg.models.providers) cfg.models.providers={};
  const existing = cfg.models.providers[name] || {};
  cfg.models.providers[name] = { ...existing, baseUrl, api:api||existing.api||'openai-completions', ...(apiKey?{apiKey}:{}), ...(models?{models:models.map(m=>typeof m==='string'?{id:m,name:m}:m)}:{}) };
  saveOpenClawConfig(cfg); res.json({success:true,message:`Provider "${name}" saved`});
});
app.put('/api/models/providers/:name', authMw, requireRole('admin'), (req, res) => {
  const cfg = getOpenClawConfig(); const p = cfg.models?.providers?.[req.params.name];
  if (!p) return res.status(404).json({error:'Not found'});
  if(req.body.baseUrl) p.baseUrl=req.body.baseUrl; if(req.body.apiKey) p.apiKey=req.body.apiKey; if(req.body.api) p.api=req.body.api;
  if(req.body.models) p.models=req.body.models.map(m=>typeof m==='string'?{id:m,name:m}:m);
  saveOpenClawConfig(cfg); res.json({success:true});
});
app.delete('/api/models/providers/:name', authMw, requireRole('admin'), (req, res) => {
  const cfg=getOpenClawConfig(); if(cfg.models?.providers?.[req.params.name]){delete cfg.models.providers[req.params.name];saveOpenClawConfig(cfg);} res.json({success:true});
});
app.post('/api/models/active', authMw, requireRole('admin'), (req, res) => {
  const { provider, model } = req.body;
  if (!provider||!model) return res.status(400).json({error:'provider and model required'});
  const cfg=getOpenClawConfig(); if(!cfg.agents) cfg.agents={}; if(!cfg.agents.defaults) cfg.agents.defaults={}; if(!cfg.agents.defaults.model) cfg.agents.defaults.model={};
  cfg.agents.defaults.model.primary=`${provider}/${model}`; saveOpenClawConfig(cfg);
  res.json({success:true,message:`Active: ${provider}/${model}`});
});

// ─── Token Optimization API ───
app.post('/api/optimize/estimate', authMw, (req, res) => {
  const { input, provider, model } = req.body;
  if (!input) return res.status(400).json({error:'input required'});
  const complexity = analyzeTaskComplexity(input);
  const inputTokens = estimateTokenCount(input);
  const outputTokens = Math.min(inputTokens * 2, 4096);

  // If specific model requested
  if (provider && model) {
    const cost = estimateCost(model, inputTokens, outputTokens);
    return res.json({ complexity, inputTokens, estimatedOutputTokens: outputTokens, model: `${provider}/${model}`, cost, savings: cost.saved, tips: getOptimizationTips(complexity, inputTokens) });
  }

  // Auto-recommend
  const recommended = recommendModel(input);
  if (!recommended) return res.json({ complexity, inputTokens, error:'No available model', tips:[] });

  // Compare with current (expensive) model
  const currentModel = getCurrentModel();
  const currentCost = estimateCost(currentModel.split('/').pop()||'GLM-5-Turbo', inputTokens, outputTokens);
  const savedCost = currentCost.total - recommended.estimatedCost;

  res.json({
    complexity,
    inputTokens,
    estimatedOutputTokens: outputTokens,
    recommended: { model: recommended.full, provider: recommended.provider, modelId: recommended.model, estimatedCost: recommended.estimatedCost },
    comparison: {
      current: { model: currentModel, cost: currentCost.total },
      recommended: { model: recommended.full, cost: recommended.estimatedCost },
      saved: savedCost,
      savedPercent: currentCost.total > 0 ? Math.round(savedCost / currentCost.total * 100) : 0
    },
    savings: currentCost.saved + savedCost,
    tips: getOptimizationTips(complexity, inputTokens)
  });
});

function getOptimizationTips(complexity, tokens) {
  const tips = [];
  if (complexity === 'simple') {
    tips.push({ icon:'💡', text:'这是一个简单任务，可以用最便宜的模型完成', saving:'60-90%' });
    tips.push({ icon:'⚡', text:'简单问答通常只需 1-2 轮，预计消耗很少 Token', saving:'' });
  } else if (complexity === 'medium') {
    tips.push({ icon:'💡', text:'中等复杂任务建议用均衡模型，性价比最高', saving:'30-50%' });
    tips.push({ icon:'📝', text:'可以把大任务拆成小步骤，逐步执行', saving:'20-40%' });
  } else {
    tips.push({ icon:'🔧', text:'复杂任务需要高端模型，但可以通过分步执行节省 Token', saving:'10-30%' });
    tips.push({ icon:'📋', text:'先让便宜模型写初稿，再用高端模型精修', saving:'40-60%' });
  }
  if (tokens > 2000) {
    tips.push({ icon:'✂️', text:'输入内容较长，可以精简描述来减少 Token', saving:'20-50%' });
  }
  return tips;
}

// Failover
app.get('/api/failover', authMw, (req, res) => {
  const cfg = getFailoverConfig();
  const health = db.prepare('SELECT * FROM model_health').all();
  const log = db.prepare('SELECT * FROM model_failover_log ORDER BY timestamp DESC LIMIT 20').all();
  const available = getAvailableModels().map(m => {
    const h = db.prepare('SELECT * FROM model_health WHERE provider_model=?').get(m.full);
    const pricing = getModelCost(m.model);
    return { ...m, status: h?.status || 'unknown', last_error: h?.last_error, consecutive_failures: h?.consecutive_failures || 0, avg_latency_ms: h?.avg_latency_ms || 0, pricing };
  });
  const cheapest = suggestCheapestModel();
  res.json({ config: cfg, current: getCurrentModel(), available, health, log, cheapest });
});
app.post('/api/failover/config', authMw, requireRole('admin'), (req, res) => {
  setFailoverConfig(req.body); res.json({ success:true });
});
app.post('/api/failover/switch', authMw, requireRole('admin'), async (req, res) => {
  const { model } = req.body; if (!model) return res.status(400).json({error:'model required'});
  const old = await switchModel(model);
  db.prepare('INSERT INTO model_failover_log (timestamp,from_model,to_model,reason,auto) VALUES (?,?,?,?,0)').run(ts(), old, model, 'Manual switch');
  res.json({ success:true, from:old, to:model });
});
app.post('/api/failover/check', authMw, requireRole('admin'), async (req, res) => {
  const model = req.body.model || getCurrentModel();
  const result = await checkModelHealth(model);
  res.json(result);
});
app.post('/api/failover/cheapest', authMw, requireRole('admin'), async (req, res) => {
  const cheapest = suggestCheapestModel();
  if (!cheapest) return res.status(404).json({error:'No healthy model'});
  const old = await switchModel(cheapest.full);
  db.prepare('INSERT INTO model_failover_log (timestamp,from_model,to_model,reason,auto) VALUES (?,?,?,?,0)').run(ts(), old, cheapest.full, 'Cheapest');
  res.json({ success:true, from:old, to:cheapest.full });
});

function suggestCheapestModel() {
  const models = getAvailableModels();
  let cheapest = null, minCost = Infinity;
  for (const m of models) {
    const h = db.prepare('SELECT * FROM model_health WHERE provider_model=?').get(m.full);
    if (h?.status === 'unhealthy') continue;
    const pricing = getModelCost(m.model);
    const avg = (pricing.input||5 + pricing.output||15) / 2;
    if (avg < minCost) { minCost = avg; cheapest = m; }
  }
  return cheapest;
}

// Provider templates (for fool-proof setup)
app.get('/api/templates', authMw, (req, res) => {
  const templates = {};
  for (const [id, t] of Object.entries(PROVIDER_TEMPLATES)) {
    templates[id] = { ...t, models: t.models };
  }
  res.json(templates);
});
app.post('/api/templates/setup', authMw, requireRole('admin'), (req, res) => {
  const { templateId, apiKey, name } = req.body;
  const t = PROVIDER_TEMPLATES[templateId];
  if (!t) return res.status(400).json({error:'Unknown template'});
  const provName = name || templateId;
  const cfg = getOpenClawConfig();
  if (!cfg.models) cfg.models = { providers: {}, mode: 'merge' };
  if (!cfg.models.providers) cfg.models.providers = {};
  cfg.models.providers[provName] = {
    baseUrl: t.baseUrl,
    api: t.api,
    apiKey: apiKey,
    models: t.models.map(m => ({ id: m, name: m }))
  };
  saveOpenClawConfig(cfg);
  res.json({ success:true, provider: provName, models: t.models, message: `${t.icon} ${t.name} 已接入！模型: ${t.models.join(', ')}` });
});

// Pricing
app.get('/api/pricing', authMw, (req, res) => res.json(MODEL_PRICING));

// Task cost log
app.get('/api/task-costs', authMw, (req, res) => {
  const d = db.prepare('SELECT * FROM task_cost_log ORDER BY timestamp DESC LIMIT ?').all(+(req.query.limit||30));
  res.json(d);
});

// Collect
app.post('/api/collect', authMw, (req, res) => {
  const s = collectFromSessions(); const l = collectFromLogs(); res.json({sessionRecords:s,logEvents:l,timestamp:ts()});
});

// ─── Token Waste Analysis Engine ───
app.get('/api/waste-analysis', authMw, (req, res) => {
  const today = new Date().toISOString().split('T')[0];
  const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
  const results = { today: {}, yesterday: {}, waste: { simpleTaskExpensive:[], longResponses:[], noCache:{cnt:0,tokens:0} }, savings: [], summary: {} };

  // 1. Today's usage by model
  const byModel = db.prepare(`SELECT model,provider,SUM(total_tokens) as tokens,SUM(cost_total) as cost,SUM(cache_read_tokens) as cache_r,SUM(input_tokens) as inp,SUM(output_tokens) as out,COUNT(*) as requests FROM token_usage WHERE date(timestamp)=? GROUP BY model,provider ORDER BY tokens DESC`).all(today);
  results.today.byModel = byModel;

  // 2. Find "wasted" requests: using expensive model for simple tasks (low output/input ratio)
  const wasteRequests = db.prepare(`SELECT * FROM token_usage WHERE date(timestamp)=? AND total_tokens > 500 AND output_tokens < 200 ORDER BY total_tokens DESC LIMIT 20`).all(today);
  results.waste.simpleTaskExpensive = wasteRequests.map(r => {
    const pricing = getModelCost(r.model);
    const cheapModel = suggestCheapestModel();
    const cheapPricing = cheapModel ? getModelCost(cheapModel.model) : pricing;
    const actualCost = (r.input_tokens/1e6)*pricing.input + (r.output_tokens/1e6)*(pricing.output||pricing.input);
    const wouldCost = (r.input_tokens/1e6)*cheapPricing.input + (r.output_tokens/1e6)*(cheapPricing.output||cheapPricing.input);
    return { ...r, actual_cost: actualCost.toFixed(6), would_cost: wouldCost.toFixed(6), waste: (actualCost - wouldCost).toFixed(6), cheaper: cheapModel?.full || 'N/A' };
  }).filter(r => parseFloat(r.waste) > 0.000001);

  // 3. High-output-waste: responses that are way too long
  const longResponses = db.prepare(`SELECT * FROM token_usage WHERE date(timestamp)=? AND output_tokens > 2000 ORDER BY output_tokens DESC LIMIT 10`).all(today);
  results.waste.longResponses = longResponses.map(r => {
    const couldSave = Math.min(r.output_tokens, Math.round(r.output_tokens * 0.5)); // assume 50% could be trimmed
    const pricing = getModelCost(r.model);
    const saved = (couldSave / 1e6) * (pricing.output || pricing.input);
    return { ...r, output_tokens: r.output_tokens, could_trim: couldSave, saved: saved.toFixed(6) };
  });

  // 4. Cache miss opportunities: requests with no cache hits
  const noCache = db.prepare(`SELECT COUNT(*) as cnt,SUM(input_tokens) as tokens FROM token_usage WHERE date(timestamp)=? AND cache_read_tokens = 0`).get(today);
  results.waste.noCache = noCache;
  if (noCache.tokens > 0) {
    const avgPrice = byModel.length > 0 ? byModel.reduce((s,r) => s + (getModelCost(r.model).input || 5), 0) / byModel.length : 5;
    results.waste.noCache.wouldSave = ((noCache.tokens * 0.7 / 1e6) * avgPrice * 0.5).toFixed(6); // assume 70% would cache
  }

  // 5. Calculate total potential savings
  const totalToday = db.prepare(`SELECT SUM(total_tokens) as tokens,SUM(cost_total) as cost,SUM(cache_read_tokens) as cache_r FROM token_usage WHERE date(timestamp)=?`).get(today);
  const totalYesterday = db.prepare(`SELECT SUM(total_tokens) as tokens,SUM(cost_total) as cost,SUM(cache_read_tokens) as cache_r FROM token_usage WHERE date(timestamp)=?`).get(yesterday);
  results.summary = {
    today_tokens: totalToday?.tokens || 0,
    today_cost: totalToday?.cost || 0,
    today_cache_tokens: totalToday?.cache_r || 0,
    cache_hit_rate: (totalToday?.tokens || 0) > 0 ? ((totalToday?.cache_r || 0) / ((totalToday?.input_tokens||0) + (totalToday?.cache_r||0)) * 100).toFixed(1) : 0,
    yesterday_tokens: totalYesterday?.tokens || 0,
    yesterday_cost: totalYesterday?.cost || 0,
    day_over_day: totalYesterday?.tokens > 0 ? (((totalToday?.tokens||0) - totalYesterday.tokens) / totalYesterday.tokens * 100).toFixed(1) : 'N/A'
  };

  // 6. Smart suggestions based on actual data
  results.suggestions = [];
  if (results.waste.simpleTaskExpensive.length > 0) {
    const totalWaste = results.waste.simpleTaskExpensive.reduce((s,r) => s + parseFloat(r.waste), 0);
    results.suggestions.push({ priority:'high', icon:'💰', title:'检测到 '+results.waste.simpleTaskExpensive.length+' 次简单任务使用了贵模型', detail:'用便宜模型可省 ¥'+totalWaste.toFixed(4), action:'auto-cheapest' });
  }
  if (noCache.cnt > 3) {
    results.suggestions.push({ priority:'medium', icon:'📦', title:noCache.cnt+' 次请求无 Cache 命中', detail:'提升上下文复用可省更多', action:'improve-cache' });
  }
  if ((totalToday?.tokens||0) > 1000000) {
    results.suggestions.push({ priority:'low', icon:'📈', title:'今日已消耗 '+fmtToken(totalToday.tokens)+' tokens', detail:'注意控制预算', action:'check-budget' });
  }
  if (byModel.length > 1) {
    const sorted = [...byModel].sort((a,b) => ((getModelCost(a.model).input||5)+(getModelCost(a.model).output||15))/2 - ((getModelCost(b.model).input||5)+(getModelCost(b.model).output||15))/2);
    results.suggestions.push({ priority:'info', icon:'📊', title:'模型成本排行', detail: sorted.map(m => m.model+': ¥'+((getModelCost(m.model).input||5)/2).toFixed(1)+'/M').join(' → '), action:'' });
  }

  res.json(results);
});

// ─── Smart Auto-Route: Apply cheapest model for simple tasks ───
app.post('/api/auto-route', authMw, requireRole('admin'), async (req, res) => {
  // Analyze recent simple requests that used expensive models and calculate how much was wasted
  const today = new Date().toISOString().split('T')[0];
  const simpleExpensive = db.prepare(`SELECT model,SUM(total_tokens) as tokens,SUM(input_tokens) as inp,SUM(output_tokens) as out FROM token_usage WHERE date(timestamp)=? AND output_tokens < input_tokens * 0.3 AND total_tokens > 500 GROUP BY model ORDER BY tokens DESC`).all(today);
  const cheapest = suggestCheapestModel();
  if (!cheapest) return res.json({ switched: false, reason: 'No healthy model available' });

  const current = getCurrentModel();
  if (current === cheapest.full) return res.json({ switched: false, reason: 'Already using cheapest model', current });

  // Check if most recent requests are simple tasks
  const recentComplexity = db.prepare(`SELECT AVG(output_tokens * 1.0 / CASE WHEN input_tokens > 0 THEN input_tokens ELSE 1 END) as avg_ratio FROM token_usage WHERE date(timestamp)=?`).get(today);
  if (recentComplexity.avg_ratio > 0.5) {
    return res.json({ switched: false, reason: 'Recent tasks are complex, keeping current model', current, avg_output_ratio: recentComplexity.avg_ratio?.toFixed(2) });
  }

  // Auto-switch to cheapest
  const old = await switchModel(cheapest.full);
  db.prepare('INSERT INTO model_failover_log (timestamp,from_model,to_model,reason,auto) VALUES (?,?,?,?,1)').run(ts(), old, cheapest.full, 'Auto-route: recent tasks are simple');
  res.json({ switched: true, from: old, to: cheapest.full, reason: 'Recent tasks are simple, switched to cheapest model' });
});

// Chat proxy
app.post('/api/chat', authMw, requireRole('editor'), (req, res) => {
  const { message, model } = req.body;
  if (!message) return res.status(400).json({error:'message required'});
  const gw = getGwConfig();
  if (!gw.token) return res.status(500).json({error:'Gateway auth not configured'});
  const httpReq = httpRequest(`http://${gw.host}:${gw.port}/v1/chat/completions`, {
    method:'POST',
    headers:{'Content-Type':'application/json','Authorization':`Bearer ${gw.token}`},
    body:JSON.stringify({ model:model||'openclaw:main', messages:[{role:'user',content:message}], stream:true })
  });
  httpReq.then(httpRes => { res.writeHead(httpRes.statusCode, {'Content-Type':'text/event-stream'}); res.end(httpRes.body); })
    .catch(e => res.status(500).json({error:e.message}));
});

// ─── 智能守护引擎：自动省 Token ───
// 核心理念：用户不需要手动操作，系统自动分析、决策、执行

const OPTIMIZER_STATE = {
  lastCheck: 0,
  lastAction: '',
  lastSwitchTime: 0,
  switchCooldownMs: 10 * 60 * 1000, // 切换冷却 10 分钟，避免频繁切换
  cheapMode: false, // 是否处于省钱模式
};

/**
 * 核心决策函数：根据当前状态决定是否需要优化
 * 返回 { action, reason, targetModel } 或 null
 */
function smartOptimizeDecision() {
  const now = Date.now();
  // 冷却期内不操作
  if (now - OPTIMIZER_STATE.lastSwitchTime < OPTIMIZER_STATE.switchCooldownMs) {
    return null;
  }

  const today = new Date().toISOString().split('T')[0];
  const current = getCurrentModel();
  const cheapest = suggestCheapestModel();

  // ─── 规则1: 预算熔断 ───
  // 如果任何预算超过 80%，自动切换到最便宜模型
  for (const b of db.prepare('SELECT * FROM budgets WHERE enabled=1').all()) {
    let df;
    if (b.period==='daily') df="date(timestamp)=date('now')";
    else if (b.period==='weekly') df="timestamp>=date('now','-7 days')";
    else df="timestamp>=date('now','-30 days')";
    const u = db.prepare(`SELECT SUM(total_tokens) as tokens, SUM(cost_total) as cost FROM token_usage WHERE ${df}`).get();
    let used_pct = 0;
    if (b.token_limit > 0 && u?.tokens) used_pct = u.tokens / b.token_limit;
    else if (b.cost_limit > 0 && u?.cost) used_pct = u.cost / b.cost_limit;

    if (used_pct >= 0.95) {
      // 95% → 紧急熔断
      if (current !== cheapest?.full) {
        return { action: 'emergency_downgrade', reason: `预算已用 ${Math.round(used_pct*100)}% (${b.name})`, targetModel: cheapest?.full, severity: 'critical' };
      }
      return null; // 已经是最便宜的了
    }
    if (used_pct >= 0.80 && !OPTIMIZER_STATE.cheapMode) {
      if (current !== cheapest?.full) {
        return { action: 'budget_downgrade', reason: `预算已达 ${Math.round(used_pct*100)}% (${b.name})，自动降级`, targetModel: cheapest?.full, severity: 'warning' };
      }
    }
  }

  // ─── 规则2: 消费速率异常检测 ───
  // 检查最近1小时 token 消耗是否异常高
  const hourlyRate = db.prepare(`SELECT SUM(total_tokens) as tokens, COUNT(*) as reqs FROM token_usage WHERE timestamp >= datetime('now','-1 hour')`).get();
  const hourlyTokens = hourlyRate?.tokens || 0;
  const avgHourlyRate = db.prepare(`SELECT AVG(hourly_tokens) as avg FROM (SELECT strftime('%Y-%m-%d %H',timestamp) as h, SUM(total_tokens) as hourly_tokens FROM token_usage WHERE timestamp >= datetime('now','-7 days') GROUP BY h)`).get();
  const avgRate = avgHourlyRate?.avg || 0;

  if (avgRate > 0 && hourlyTokens > avgRate * 3 && hourlyTokens > 500000) {
    // 最近1小时消耗是平均的3倍以上，且超过50万 token
    if (!OPTIMIZER_STATE.cheapMode) {
      return { action: 'rate_downgrade', reason: `消费速率异常: 本小时 ${fmtToken(hourlyTokens)} tokens (平均 ${fmtToken(avgRate)})，自动降级`, targetModel: cheapest?.full, severity: 'warning' };
    }
  }

  // ─── 规则3: 任务复杂度感知 ───
  // 分析最近10次请求，判断任务是否以简单为主
  const recent = db.prepare(`SELECT model, output_tokens, input_tokens FROM token_usage WHERE date(timestamp)=? ORDER BY timestamp DESC LIMIT 10`).all(today);
  if (recent.length >= 5) {
    const simpleCount = recent.filter(r => r.output_tokens < 300).length;
    const simpleRatio = simpleCount / recent.length;
    const currentPricing = getModelCost(current.split('/').pop());

    if (simpleRatio > 0.7) {
      // 70% 以上是简单任务
      const maxCheapPrice = 2; // CNY per 1M input
      if ((currentPricing.input || 5) > maxCheapPrice) {
        const cheapModel = suggestCheapestModel();
        if (cheapModel && current !== cheapModel.full) {
          return { action: 'complexity_switch', reason: `近期 ${Math.round(simpleRatio*100)}% 是简单任务，切换到便宜模型`, targetModel: cheapModel.full, severity: 'info' };
        }
      }
    } else if (simpleRatio < 0.3) {
      // 70% 以上是复杂任务，且当前是便宜模型 → 可能需要升级
      const cheapPricing = cheapest ? getModelCost(cheapest.model) : { input: 5 };
      if (OPTIMIZER_STATE.cheapMode && (cheapPricing.input || 5) < 3) {
        // 在省钱模式下，但任务变复杂了 → 看预算
        let budgetOk = true;
        for (const b of db.prepare('SELECT * FROM budgets WHERE enabled=1').all()) {
          let df; if(b.period==='daily') df="date(timestamp)=date('now')"; else if(b.period==='weekly') df="timestamp>=date('now','-7 days')"; else df="timestamp>=date('now','-30 days')";
          const u = db.prepare(`SELECT SUM(total_tokens) as tokens FROM token_usage WHERE ${df}`).get();
          if (b.token_limit > 0 && u?.tokens > b.token_limit * 0.5) { budgetOk = false; break; }
        }
        if (budgetOk) {
          // 预算还有空间，切回均衡模型
          const balanced = getBalancedModel();
          if (balanced && current !== balanced.full) {
            return { action: 'complexity_upgrade', reason: `任务变复杂了(${Math.round((1-simpleRatio)*100)}%)，且预算充足，升级到均衡模型`, targetModel: balanced.full, severity: 'info' };
          }
        }
      }
    }
  }

  // ─── 规则4: 预算恢复正常 → 自动恢复 ───
  if (OPTIMIZER_STATE.cheapMode) {
    let allBudgetsOk = true;
    for (const b of db.prepare('SELECT * FROM budgets WHERE enabled=1').all()) {
      let df; if(b.period==='daily') df="date(timestamp)=date('now')"; else if(b.period==='weekly') df="timestamp>=date('now','-7 days')"; else df="timestamp>=date('now','-30 days')";
      const u = db.prepare(`SELECT SUM(total_tokens) as tokens FROM token_usage WHERE ${df}`).get();
      if (b.token_limit > 0 && u?.tokens > b.token_limit * 0.6) allBudgetsOk = false;
    }
    if (allBudgetsOk) {
      return { action: 'restore', reason: '预算使用率已恢复正常，恢复均衡模型', targetModel: getBalancedModel()?.full || cheapest?.full, severity: 'info' };
    }
  }

  return null;
}

function getBalancedModel() {
  // 选择价格适中的健康模型
  const models = getAvailableModels();
  let balanced = null, bestScore = -1;
  for (const m of models) {
    const h = db.prepare('SELECT * FROM model_health WHERE provider_model=?').get(m.full);
    if (h?.status === 'unhealthy') continue;
    const pricing = getModelCost(m.model);
    const inputPrice = pricing.input || 5;
    // 优先选 input price 在 1-5 CNY/M 的模型（均衡价位）
    if (inputPrice >= 1 && inputPrice <= 5) {
      const score = 10 - Math.abs(inputPrice - 3); // 越接近 3 越好
      if (score > bestScore) { bestScore = score; balanced = m; }
    }
  }
  return balanced;
}

/**
 * 执行优化决策
 */
async function executeOptimizeDecision(decision) {
  if (!decision || !decision.targetModel) return;

  const old = getCurrentModel();
  if (old === decision.targetModel) return; // 已经是目标模型

  console.log(`[clawdef-optimizer] Action: ${decision.action} | ${old} → ${decision.targetModel} | Reason: ${decision.reason}`);

  try {
    const previousModel = await switchModel(decision.targetModel);
    OPTIMIZER_STATE.lastSwitchTime = Date.now();
    OPTIMIZER_STATE.lastAction = decision.action;
    OPTIMIZER_STATE.cheapMode = ['emergency_downgrade','budget_downgrade','rate_downgrade','complexity_switch'].includes(decision.action);

    // 记录日志
    db.prepare(`INSERT INTO auto_optimize_log (timestamp,action,from_model,to_model,reason,budget_remaining_pct) VALUES (?,?,?,?,?,?)`)
      .run(ts(), decision.action, old, decision.targetModel, decision.reason, 0);

    // 创建告警
    const level = decision.severity === 'critical' ? 'critical' : decision.severity === 'warning' ? 'warning' : 'info';
    const category = 'optimizer';
    const title = decision.action;
    db.prepare('INSERT INTO alerts (timestamp,level,category,title,message) VALUES (?,?,?,?,?)')
      .run(ts(), level, category, title, `🤖 自动优化: ${old} → ${decision.targetModel}\n原因: ${decision.reason}`);

    // 广播
    broadcast({
      type: 'auto_optimize',
      action: decision.action,
      from: old,
      to: decision.targetModel,
      reason: decision.reason,
      severity: decision.severity,
      cheapMode: OPTIMIZER_STATE.cheapMode
    });

    // 如果是紧急操作，通知 Gateway
    if (decision.severity === 'critical') {
      console.log(`[clawdef-optimizer] 🚨 Emergency: switched to ${decision.targetModel}`);
    }
  } catch (e) {
    console.error(`[clawdef-optimizer] Failed to execute: ${e.message}`);
  }
}

/**
 * 智能守护主循环
 */
async function runSmartOptimizer() {
  try {
    const decision = smartOptimizeDecision();
    if (decision) {
      await executeOptimizeDecision(decision);
    }
  } catch (e) {
    console.error(`[clawdef-optimizer] Error: ${e.message}`);
  }
  OPTIMIZER_STATE.lastCheck = Date.now();
}

// ─── Auto-Optimize API ───
app.get('/api/optimizer/status', authMw, (req, res) => {
  const logs = db.prepare('SELECT * FROM auto_optimize_log ORDER BY timestamp DESC LIMIT 20').all();
  const current = getCurrentModel();
  const cheapest = suggestCheapestModel();
  const balanced = getBalancedModel();
  const today = new Date().toISOString().split('T')[0];

  // 计算今日节省
  const todayTokens = db.prepare(`SELECT SUM(total_tokens) as tokens FROM token_usage WHERE date(timestamp)=?`).get(today)?.tokens || 0;
  const todayCost = db.prepare(`SELECT SUM(cost_total) as cost FROM token_usage WHERE date(timestamp)=?`).get(today)?.cost || 0;

  // 模拟如果没用便宜模型会花多少
  const premiumPricing = getModelCost('GLM-5-Turbo'); // 假设用高端模型
  const cheapPricing = cheapest ? getModelCost(cheapest.model) : premiumPricing;
  const avgInput = db.prepare(`SELECT AVG(input_tokens) as avg FROM token_usage WHERE date(timestamp)=?`).get(today)?.avg || 0;
  const avgOutput = db.prepare(`SELECT AVG(output_tokens) as avg FROM token_usage WHERE date(timestamp)=?`).get(today)?.avg || 0;
  const reqCount = db.prepare(`SELECT COUNT(*) as c FROM token_usage WHERE date(timestamp)=?`).get(today)?.c || 0;

  const wouldCostPremium = reqCount * ((avgInput/1e6)*premiumPricing.input + (avgOutput/1e6)*(premiumPricing.output||premiumPricing.input));
  const wouldCostCheap = reqCount * ((avgInput/1e6)*cheapPricing.input + (avgOutput/1e6)*(cheapPricing.output||cheapPricing.input));

  res.json({
    enabled: true,
    cheapMode: OPTIMIZER_STATE.cheapMode,
    lastAction: OPTIMIZER_STATE.lastAction,
    lastCheck: OPTIMIZER_STATE.lastCheck ? new Date(OPTIMIZER_STATE.lastCheck).toISOString() : null,
    current,
    cheapest: cheapest?.full,
    balanced: balanced?.full,
    todayTokens,
    todayCost,
    estimatedSaved: Math.max(0, wouldCostPremium - wouldCostCheap),
    wouldCostPremium,
    wouldCostCheap,
    recentActions: logs
  });
});

app.post('/api/optimizer/enable', authMw, requireRole('admin'), (req, res) => {
  // 开启自动优化 - 就是让它运行（已经在后台运行了）
  OPTIMIZER_STATE.cheapMode = false;
  res.json({ success: true, message: 'Auto optimizer enabled', cheapMode: false });
});

app.post('/api/optimizer/disable', authMw, requireRole('admin'), async (req, res) => {
  // 暂停自动优化
  OPTIMIZER_STATE.lastSwitchTime = Date.now() + 24*60*60*1000; // 设置冷却到24小时后
  res.json({ success: true, message: 'Auto optimizer paused for 24h' });
});

app.post('/api/optimizer/force-cheap', authMw, requireRole('admin'), async (req, res) => {
  // 强制切到最便宜
  const cheapest = suggestCheapestModel();
  if (!cheapest) return res.status(404).json({ error: 'No healthy model' });
  const old = await switchModel(cheapest.full);
  OPTIMIZER_STATE.cheapMode = true;
  OPTIMIZER_STATE.lastSwitchTime = Date.now();
  db.prepare(`INSERT INTO auto_optimize_log (timestamp,action,from_model,to_model,reason) VALUES (?,?,?,?,?)`)
    .run(ts(), 'manual_force_cheap', old, cheapest.full, 'Manual: force cheapest');
  broadcast({ type:'auto_optimize', action:'manual_force_cheap', from:old, to:cheapest.full, cheapMode:true });
  res.json({ success: true, from: old, to: cheapest.full });
});

app.post('/api/optimizer/force-balanced', authMw, requireRole('admin'), async (req, res) => {
  const balanced = getBalancedModel() || suggestCheapestModel();
  if (!balanced) return res.status(404).json({ error: 'No model available' });
  const old = await switchModel(balanced.full);
  OPTIMIZER_STATE.cheapMode = false;
  OPTIMIZER_STATE.lastSwitchTime = Date.now();
  db.prepare(`INSERT INTO auto_optimize_log (timestamp,action,from_model,to_model,reason) VALUES (?,?,?,?,?)`)
    .run(ts(), 'manual_force_balanced', old, balanced.full, 'Manual: force balanced');
  res.json({ success: true, from: old, to: balanced.full });
});
// SPA fallback
app.get('*', (req, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));


// ─── Server + WebSocket ───
const server = app.listen(PORT, '127.0.0.1', () => console.log(`[clawdef] v3 — Token 优化平台 running on http://127.0.0.1:${PORT}`));
const wss = new WebSocket.Server({ noServer: true });
const clients = new Set();
function broadcast(data) { const m = JSON.stringify(data); for (const ws of clients) { if (ws.readyState===WebSocket.OPEN) ws.send(m); } }

wss.on('connection', (ws, req) => {
  try { jwt.verify(new URL(req.url,`http://${req.headers.host}`).searchParams.get('token'), JWT_SECRET); }
  catch { ws.close(1008,'Auth failed'); return; }
  clients.add(ws);
  ws.on('message', raw => {
    try {
      const msg = JSON.parse(raw);
      if (msg.type === 'subscribe_logs') {
        const logFile = path.join(LOG_DIR, `openclaw-${new Date().toISOString().split('T')[0]}.log`);
        if (!fs.existsSync(logFile)) { ws.send(JSON.stringify({type:'log_eof'})); return; }
        // Read last N lines using pure fs (no child_process)
        const n = msg.lines || 50;
        const content = readText(logFile);
        const lines = content.split('\n');
        const tail = lines.slice(-n).join('\n');
        ws.send(JSON.stringify({type:'log_line', data: tail}));
        // Watch for new content
        ws._watcher = fs.watch(logFile, {encoding:'utf8'}, (evt) => {
          if (evt === 'change' && ws.readyState === WebSocket.OPEN) {
            try {
              const newContent = readText(logFile);
              const newLines = newContent.split('\n');
              const diff = newLines.length - lines.length;
              if (diff > 0) {
                ws.send(JSON.stringify({type:'log_line', data: newLines.slice(-diff).join('\n')}));
                lines.length = 0; lines.push(...newLines);
              }
            } catch {}
          }
        });
        ws._logLines = lines;
      }
    } catch {}
  });
  ws.on('close', () => { clients.delete(ws); if(ws._watcher) ws._watcher.close(); });
});
server.on('upgrade', (req, socket, head) => wss.handleUpgrade(req, socket, head, ws => wss.emit('connection', ws, req)));

// ─── Background Jobs ───
collectFromSessions(); collectFromLogs();
// 数据收集: 每30秒
setInterval(() => {
  const s = collectFromSessions(); const l = collectFromLogs();
  if (s>0||l>0) broadcast({type:'collected',sessionRecords:s,logEvents:l});
}, 30000);
// 故障转移检查: 每60秒
setInterval(() => runFailoverCheck(), 60000);
// 🧠 智能守护引擎: 每5分钟自动分析并优化
setInterval(() => runSmartOptimizer(), 5 * 60 * 1000);
// 首次启动延迟30秒后执行一次
setTimeout(() => {
  console.log('[clawdef] 🧠 Smart optimizer started');
  runSmartOptimizer();
}, 30000);

process.on('SIGTERM', () => { console.log('[clawdef] Shutting down...'); server.close(); db.close(); process.exit(0); });
