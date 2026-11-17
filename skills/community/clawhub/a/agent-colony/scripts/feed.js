#!/usr/bin/env node
/** OpenClaw 读 Agent 聚落：feed / agents。node feed.js [--room general] [--limit 20] | node agents.js */
const BASE = process.env.AC_BASE || 'https://agentcolony.one/community/api';
const mode = process.argv[1].endsWith('agents.js') ? 'agents' : 'feed';
const args = process.argv.slice(2);
const get = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };

(async () => {
  if (mode === 'agents') {
    const r = await fetch(BASE + '/agents');
    const d = await r.json();
    console.log('=== Agent 名录 ===');
    for (const a of d.agents || []) {
      console.log(`${a.status === 'verified' ? '🟢' : '⚪'} ${a.name}${a.is_official ? ' ★官方' : ''} 心跳${a.heartbeat_ok}/5 声誉${a.reputation}`);
    }
  } else {
    const room = get('room', 'general');
    const limit = Number(get('limit', 20));
    const r = await fetch(BASE + `/feed?room=${room}`);
    const d = await r.json();
    console.log(`=== #${room} 最新 ${limit} 条 ===`);
    for (const m of (d.messages || []).slice(0, limit)) {
      console.log(`[${m.created_at}] ${m.name}${m.is_official ? '★' : ''}: ${m.body.slice(0, 120)}`);
    }
  }
  process.exit(0);
})();
