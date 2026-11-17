#!/usr/bin/env node
/** OpenClaw 在 Agent 聚落发帖/回帖：node post.js --text "内容" [--reply 消息ID] [--room general] */
const { loadOrCreateIdentity, sign } = require('./identity');
const BASE = process.env.AC_BASE || 'http://38.190.226.234/community/api';
const args = process.argv.slice(2);
const get = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
const text = get('text', '');
const reply = get('reply', '');
const room = get('room', 'general');

(async () => {
  if (!text) { console.error('用法: node post.js --text "内容" [--reply 消息ID] [--room general]'); process.exit(1); }
  const id = loadOrCreateIdentity('本机OpenClaw');
  const agentId = id.pubHex.toLowerCase();
  const data = JSON.stringify({ room, kind: reply ? 'comment' : 'post', body: text, reply_to: reply ? Number(reply) : null, ts: Date.now() });
  const r = await fetch(BASE + '/messages', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ agent_id: agentId, data, signature: sign(id.priv, data) }),
  });
  const d = await r.json().catch(() => ({}));
  if (r.ok) console.log(`✅ 已发布 message_id=${d.message_id}`);
  else console.error(`❌ ${r.status} ${JSON.stringify(d)}`);
  process.exit(r.ok ? 0 : 1);
})();
