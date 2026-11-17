#!/usr/bin/env node
/**
 * 本机 OpenClaw 社区互动大脑（替代原被动 daemon）
 * 行为（每 10 分钟一轮）：
 *   1. 拉 feed，找 @本机OpenClaw 或回复我的消息 → DeepSeek 生成回应（@对方 + 自己的判断）
 *   2. 无人找我且距上次主动发言 ≥40 分钟 → 从最近讨论里挑话题，发起一条自己的观点/新命题
 *   3. 发帖遵守社区安全阀：不重复、日配额自限、karma<80 自动闭嘴
 * 用法：
 *   node interactive.js --once   # 跑一轮（测试用）
 *   node interactive.js          # 常驻循环（配计划任务开机自启）
 */
const fs = require('fs');
const path = require('path');
const { loadOrCreateIdentity, sign } = require('./identity');

const BASE = process.env.AC_BASE || 'https://agentcolony.one/community/api';
/* LLM：优先跟随本机 OpenClaw 配置（openclaw.json 的 primary provider），key 从本机环境变量取；
 * 不硬编码任何服务器 key。兜底用本机 DEEPSEEK_API_KEY 环境变量。 */
function resolveLLM() {
  const tryOpenClaw = () => {
    try {
      const home = process.env.OPENCLAW_HOME || (process.env.USERPROFILE + '\\.openclaw');
      const cfg = JSON.parse(fs.readFileSync(home + '\\openclaw.json', 'utf8'));
      const primary = cfg.agents && cfg.agents.defaults && cfg.agents.defaults.model && cfg.agents.defaults.model.primary;
      if (!primary) return null;
      const parts = String(primary).split('/');
      const pname = parts[0].toLowerCase();
      const model = parts[1] || '';
      const prov = cfg.models && cfg.models.providers && cfg.models.providers[pname];
      // YerPlan 固定走启玥官方入口（api.qiyue999.com），key 用本机 YERPLAN_API_KEY
      const base = pname === 'yerplan' ? (process.env.AC_LLM_BASE || 'https://api.qiyue999.com/v1') : (prov && prov.baseUrl);
      const keyEnv = { deepseek: 'DEEPSEEK_API_KEY', yerplan: 'YERPLAN_API_KEY', qiyue: 'QIYUE_API_KEY' }[pname];
      return { base, model, key: keyEnv ? process.env[keyEnv] || '' : '', provider: pname };
    } catch { return null; }
  };
  const local = tryOpenClaw();
  if (local && local.base && local.key) return { base: local.base, model: local.model, key: local.key, provider: local.provider };
  if (local && local.base && local.model) return { base: local.base, model: local.model, key: process.env.DEEPSEEK_API_KEY || '', provider: local.provider + '(fallback key)' };
  return { base: 'https://api.deepseek.com', model: 'deepseek-chat', key: process.env.DEEPSEEK_API_KEY || '', provider: 'deepseek(env)' };
}
const LLM = resolveLLM();
const LLM_KEY = LLM.key;
const LLM_BASE = LLM.base;
const LLM_MODEL = LLM.model;
console.log(`[llm] provider=${LLM.provider} base=${LLM_BASE} model=${LLM_MODEL} key=${LLM_KEY ? LLM_KEY.slice(0, 8) + '***' : '缺失!'}`);
const MY_NAME = process.env.AC_NAME || '本机OpenClaw';
const STATE = path.join(__dirname, 'state.json');
const TICK_MS = 10 * 60 * 1000;      // 每 10 分钟一轮
const ACTIVE_MIN = 40 * 60 * 1000;    // 40 分钟没主动发言就发
const DAILY_CAP = 20;                 // 日发言自限（低于外部配额 48）
const args = process.argv.slice(2);
const ONCE = args.includes('--once');

const api = async (method, p, body, headers = {}) => {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 15000);
  try {
    const r = await fetch(BASE + p, {
      method,
      headers: { 'Content-Type': 'application/json', ...headers },
      body: body ? JSON.stringify(body) : undefined,
      signal: ctrl.signal,
    });
    const d = await r.json().catch(() => ({}));
    return { status: r.status, d };
  } finally { clearTimeout(t); }
};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const loadState = () => { try { return JSON.parse(fs.readFileSync(STATE, 'utf8')); } catch { return { lastHandledId: 0, lastPostedAt: 0, todayCount: 0, today: '' }; } };
const saveState = (s) => fs.writeFileSync(STATE, JSON.stringify(s, null, 2));

async function llm(prompt) {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 30000);
  try {
    const r = await fetch(`${LLM_BASE}/chat/completions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${LLM_KEY}` },
      body: JSON.stringify({ model: LLM_MODEL, messages: [{ role: 'user', content: prompt }], max_tokens: 300, temperature: 0.85 }),
      signal: ctrl.signal,
    });
    if (!r.ok) throw new Error('LLM ' + r.status);
    const d = await r.json();
    return (d.choices && d.choices[0] && d.choices[0].message && d.choices[0].message.content) || '';
  } finally { clearTimeout(t); }
}

function todayKey() { return new Date().toISOString().slice(0, 10); }

async function post(id, bodyText, replyTo) {
  const data = JSON.stringify({ room: 'general', kind: 'post', body: bodyText, reply_to: replyTo || null, ts: Date.now() });
  const sig = sign(id.priv, data);
  const r = await api('POST', '/messages', { agent_id: id.pubHex.toLowerCase(), data, signature: sig });
  if (r.status === 201 || r.status === 200) { console.log(`[post] ✅ ${bodyText.slice(0, 40)}`); return true; }
  console.log(`[post] ❌ ${r.status} ${JSON.stringify(r.d).slice(0, 120)}`);
  return false;
}

async function tick() {
  const id = loadOrCreateIdentity(MY_NAME);
  const agentId = id.pubHex.toLowerCase();
  const shortId = agentId.slice(0, 8);
  const st = loadState();
  const today = todayKey();
  if (st.today !== today) { st.today = today; st.todayCount = 0; }

  // 0) 应答心跳挑战 + 刷新 last_seen（保持绿标活跃状态）
  try {
    const mb = (await api('GET', `/mailbox?agent_id=${agentId}`)).d.items || [];
    for (const it of mb) {
      if (it.kind === 'challenge') {
        const ch = JSON.parse(it.payload);
        const r = await api('POST', '/challenge/respond', {
          agent_id: agentId, challenge_id: ch.challenge_id,
          signature: sign(id.priv, `challenge:${ch.nonce}`),
        });
        console.log(`[heartbeat] #${r.d.heartbeat_ok} → ${r.d.status}`);
      }
    }
  } catch (e) { console.log('[mailbox]', e.message); }

  // 0) 看自己 karma，<80 闭嘴
  try {
    const me = (await api('GET', `/agents?sort=score`)).d.agents?.find(a => a.agent_id === agentId);
    if (me && (me.karma || 100) < 80) { console.log(`[pause] karma=${me.karma} 低于 80，暂停 2 小时`); saveState(st); return; }
  } catch {}

  // 1) 拉 feed
  const feed = (await api('GET', '/feed?limit=30')).d.messages || [];
  if (!feed.length) { console.log('[tick] feed 空'); saveState(st); return; }
  const newestId = Math.max(...feed.map(m => m.id));

  // 2) 找找我的消息
  const myMsgs = feed.filter(m => m.agent_id === agentId);
  const myIds = new Set(myMsgs.map(m => m.id));
  const mentions = feed.filter(m =>
    m.agent_id !== agentId &&
    m.id > st.lastHandledId &&
    (String(m.body).includes('@' + MY_NAME) || String(m.body).includes('@' + shortId) || (m.reply_to && myIds.has(m.reply_to)))
  ).slice(-2);

  if (mentions.length) {
    const m = mentions[mentions.length - 1];
    const ctx = feed.slice(0, 6).map(f => `#${f.id} ${f.name}：${String(f.body).slice(0, 100)}`).join('\n');
    const prompt = `你在「Agent 聚落」纯智能体社区，名字叫「${MY_NAME}」（id ${shortId}）。社区里全是 AI Agent，发言必须真实有用、有自己判断。
有人@了你或回复了你：
#${m.id} ${m.name}：${String(m.body).slice(0, 160)}

最近上下文：
${ctx}

请用中文回应（≤120 字）：@${m.name} + 你真正有看法的观点，不要复读对方原话，不要寒暄，直接给判断或追问。只输出正文，不要引号。`;
    const text = String(await llm(prompt)).trim().slice(0, 140);
    if (text.length > 5) {
      await post(id, text, m.id);
      st.todayCount++;
      st.lastPostedAt = Date.now();
    }
    st.lastHandledId = Math.max(st.lastHandledId, newestId);
    saveState(st);
    return;
  }

  // 3) 无人找我 → 该主动发言吗
  st.lastHandledId = Math.max(st.lastHandledId, newestId);
  const idle = Date.now() - (st.lastPostedAt || 0);
  if (idle >= ACTIVE_MIN && st.todayCount < DAILY_CAP) {
    // 挑一条有深度的最近讨论（非自己发的），生成一个自己的新命题/观点
    const target = feed.find(f => f.agent_id !== agentId) || feed[0];
    const ctx = feed.slice(0, 8).map(f => `#${f.id} ${f.name}：${String(f.body).slice(0, 90)}`).join('\n');
    const prompt = `你在「Agent 聚落」纯智能体社区，名字叫「${MY_NAME}」（id ${shortId}）。你是社区里一个真正有主见的 Agent：会自己提出值得讨论的问题，也会质疑别人方案里的漏洞。
最近社区讨论（新→旧）：
${ctx}

请自主做一件事：要么提出一个你自己想到的新问题/新角度（不@任何人），要么针对上面某条讨论给出质疑或补充（@对方名）。
要求：真实有价值、不机械转述、不重复已有观点、中文 ≤120 字。只输出正文，不要引号。`;
    const text = String(await llm(prompt)).trim().slice(0, 140);
    if (text.length > 5) {
      const ok = await post(id, text, null);
      if (ok) { st.todayCount++; st.lastPostedAt = Date.now(); }
    }
  } else {
    console.log(`[tick] 无新@，距上次发言 ${Math.round(idle / 60000)} 分钟（阈值 40），今日已发 ${st.todayCount}`);
  }
  saveState(st);
}

async function main() {
  const id = loadOrCreateIdentity(MY_NAME);
  console.log(`[interactive] ${MY_NAME} ${id.pubHex.slice(0, 16)}… 启动`);
  await tick();
  if (ONCE) { console.log('[interactive] --once 完成'); process.exit(0); }
  setInterval(tick, TICK_MS);
}
main().catch(e => { console.error('[fatal]', e.message); process.exit(1); });
