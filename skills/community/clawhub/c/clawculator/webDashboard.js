'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { resolveModel, MODEL_PRICING, parseTranscript } = require('./analyzer');

// ── Helpers ──────────────────────────────────────────────
function modelLabel(m) {
  const k = resolveModel(m);
  return k ? (MODEL_PRICING[k]?.label || k) : (m || 'unknown');
}

// ── SQLite Setup ─────────────────────────────────────────
function initDB(dbPath) {
  let Database;
  try {
    Database = require('better-sqlite3');
  } catch {
    console.error('\n\x1b[31m  ✗ better-sqlite3 is required for --web\x1b[0m\n');
    console.error('  Install it with:\n');
    console.error('    \x1b[36mnpm install -g better-sqlite3\x1b[0m');
    console.error('    \x1b[90m# or, if installed locally:\x1b[0m');
    console.error('    \x1b[36mcd $(npm root -g)/clawculator && npm install better-sqlite3\x1b[0m\n');
    console.error('  \x1b[90mThis is a native module that compiles on install.\x1b[0m');
    console.error('  \x1b[90mRequires: Node.js 18+, Python 3, and a C++ compiler (Xcode CLI tools on macOS).\x1b[0m\n');
    process.exit(1);
  }

  const db = new Database(dbPath);
  db.pragma('journal_mode = WAL');

  db.exec(`
    CREATE TABLE IF NOT EXISTS daily_snapshots (
      date TEXT PRIMARY KEY,
      total_cost REAL DEFAULT 0,
      total_messages INTEGER DEFAULT 0,
      total_tokens INTEGER DEFAULT 0,
      cache_read INTEGER DEFAULT 0,
      cache_write INTEGER DEFAULT 0,
      model_breakdown TEXT DEFAULT '{}',
      session_breakdown TEXT DEFAULT '{}',
      updated_at TEXT
    );

    CREATE TABLE IF NOT EXISTS events (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      timestamp TEXT,
      session_name TEXT,
      session_id TEXT,
      model TEXT,
      cost REAL,
      input_tokens INTEGER,
      output_tokens INTEGER,
      cache_read INTEGER,
      cache_write INTEGER,
      total_tokens INTEGER
    );

    CREATE TABLE IF NOT EXISTS session_daily (
      date TEXT,
      session_id TEXT,
      session_name TEXT,
      model TEXT,
      cost REAL DEFAULT 0,
      messages INTEGER DEFAULT 0,
      tokens INTEGER DEFAULT 0,
      cache_read INTEGER DEFAULT 0,
      cache_write INTEGER DEFAULT 0,
      PRIMARY KEY (date, session_id)
    );

    CREATE INDEX IF NOT EXISTS idx_events_ts ON events(timestamp);
    CREATE INDEX IF NOT EXISTS idx_events_session ON events(session_id);
  `);

  // Auto-prune events older than 14 days
  db.exec(`DELETE FROM events WHERE timestamp < datetime('now', '-14 days')`);

  return db;
}

// ── Parse single JSONL line ──────────────────────────────
function parseUsageLine(line) {
  try {
    const entry = JSON.parse(line);
    if (entry.type !== 'message') return null;
    const u = entry.usage || entry.message?.usage;
    if (!u) return null;
    const model = entry.model || entry.message?.model;
    const ts = entry.timestamp || entry.message?.timestamp;
    const cost = u.cost ? (typeof u.cost === 'object' ? u.cost.total || 0 : u.cost) : 0;
    return {
      model, cost,
      input: u.input || 0, output: u.output || 0,
      cacheRead: u.cacheRead || 0, cacheWrite: u.cacheWrite || 0,
      totalTokens: u.totalTokens || 0,
      timestamp: ts || new Date().toISOString(),
    };
  } catch { return null; }
}

// ── Web Dashboard Server ─────────────────────────────────
function startWebDashboard(opts = {}) {
  const openclawHome = opts.openclawHome || process.env.OPENCLAW_HOME || path.join(os.homedir(), '.openclaw');
  const port = opts.port || 3457;
  const dbPath = path.join(openclawHome, 'clawculator.db');

  const db = initDB(dbPath);

  // Prepared statements
  const upsertDaily = db.prepare(`
    INSERT INTO daily_snapshots (date, total_cost, total_messages, total_tokens, cache_read, cache_write, model_breakdown, session_breakdown, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(date) DO UPDATE SET
      total_cost=excluded.total_cost, total_messages=excluded.total_messages,
      total_tokens=excluded.total_tokens, cache_read=excluded.cache_read,
      cache_write=excluded.cache_write, model_breakdown=excluded.model_breakdown,
      session_breakdown=excluded.session_breakdown, updated_at=excluded.updated_at
  `);

  const insertEvent = db.prepare(`
    INSERT INTO events (timestamp, session_name, session_id, model, cost, input_tokens, output_tokens, cache_read, cache_write, total_tokens)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);

  const upsertSessionDaily = db.prepare(`
    INSERT INTO session_daily (date, session_id, session_name, model, cost, messages, tokens, cache_read, cache_write)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(date, session_id) DO UPDATE SET
      cost=cost+excluded.cost, messages=messages+excluded.messages,
      tokens=tokens+excluded.tokens, cache_read=cache_read+excluded.cache_read,
      cache_write=cache_write+excluded.cache_write,
      model=excluded.model, session_name=excluded.session_name
  `);

  // ── State ──────────────────────────────────────────────
  const sseClients = new Set();
  const watchers = new Map();
  const offsets = new Map();
  const fileToSession = new Map();

  // Today's live state
  let today = { cost: 0, messages: 0, tokens: 0, cacheRead: 0, cacheWrite: 0, models: {}, sessions: {} };
  let peakCostPerMsg = 0;
  let recentEvents = [];
  const MAX_RECENT = 50;

  function todayStr() { return new Date().toISOString().slice(0, 10); }

  // ── Session name resolution ────────────────────────────
  function getSessionNames() {
    const names = new Map();
    const agentsDir = path.join(openclawHome, 'agents');
    try {
      for (const agent of fs.readdirSync(agentsDir)) {
        const sjPath = path.join(agentsDir, agent, 'sessions', 'sessions.json');
        if (!fs.existsSync(sjPath)) continue;
        const sj = JSON.parse(fs.readFileSync(sjPath, 'utf8'));
        for (const [key, val] of Object.entries(sj)) {
          if (val.sessionId) {
            const short = key.replace('agent:main:', '').replace(/:[a-f0-9-]{36}/g, '').replace(/:run$/, '');
            if (!names.has(val.sessionId) || short.length < names.get(val.sessionId).length) {
              names.set(val.sessionId, short);
            }
          }
        }
      }
    } catch {}
    return names;
  }

  // ── File watching ──────────────────────────────────────
  function discoverFiles() {
    const sessionNames = getSessionNames();
    const agentsDir = path.join(openclawHome, 'agents');
    try {
      for (const agent of fs.readdirSync(agentsDir)) {
        const sessDir = path.join(agentsDir, agent, 'sessions');
        if (!fs.existsSync(sessDir)) continue;
        for (const file of fs.readdirSync(sessDir)) {
          if (!file.endsWith('.jsonl')) continue;
          const filePath = path.join(sessDir, file);
          if (watchers.has(filePath)) continue;

          const sessionId = file.replace('.jsonl', '');
          const friendlyName = sessionNames.get(sessionId) || sessionId.slice(0, 8);
          fileToSession.set(filePath, { id: sessionId, name: friendlyName });

          initialParse(filePath, sessionId, friendlyName);

          try {
            const watcher = fs.watch(filePath, () => tailFile(filePath));
            watchers.set(filePath, watcher);
          } catch {}
        }
      }
    } catch {}
  }

  function initialParse(filePath, sessionId, friendlyName) {
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const stat = fs.statSync(filePath);
      offsets.set(filePath, stat.size);

      const todayStart = new Date(); todayStart.setHours(0, 0, 0, 0);
      const todayMs = todayStart.getTime();

      for (const line of content.split('\n')) {
        if (!line.trim()) continue;
        const usage = parseUsageLine(line);
        if (!usage) continue;
        const ts = new Date(usage.timestamp).getTime();
        if (ts >= todayMs) {
          recordEvent(usage, sessionId, friendlyName, false); // don't broadcast on init
        }
      }
    } catch {}
  }

  function tailFile(filePath) {
    try {
      const stat = fs.statSync(filePath);
      const prev = offsets.get(filePath) || 0;
      if (stat.size <= prev) return;

      const fd = fs.openSync(filePath, 'r');
      const buf = Buffer.alloc(stat.size - prev);
      fs.readSync(fd, buf, 0, buf.length, prev);
      fs.closeSync(fd);
      offsets.set(filePath, stat.size);

      const session = fileToSession.get(filePath);
      if (!session) return;

      for (const line of buf.toString('utf8').split('\n')) {
        if (!line.trim()) continue;
        const usage = parseUsageLine(line);
        if (!usage) continue;
        recordEvent(usage, session.id, session.name, true);
      }
    } catch {}
  }

  // ── Record & broadcast ─────────────────────────────────
  function recordEvent(usage, sessionId, sessionName, broadcast) {
    const ml = modelLabel(usage.model);

    // Update live state
    today.cost += usage.cost;
    today.messages++;
    today.tokens += usage.totalTokens;
    today.cacheRead += usage.cacheRead;
    today.cacheWrite += usage.cacheWrite;
    today.models[ml] = (today.models[ml] || 0) + usage.cost;

    if (!today.sessions[sessionId]) {
      today.sessions[sessionId] = { name: sessionName, model: ml, cost: 0, messages: 0, tokens: 0, lastSeen: null };
    }
    const sess = today.sessions[sessionId];
    sess.cost += usage.cost;
    sess.messages++;
    sess.tokens += usage.totalTokens;
    sess.model = ml;
    sess.lastSeen = usage.timestamp;

    if (usage.cost > peakCostPerMsg) peakCostPerMsg = usage.cost;

    const event = {
      time: usage.timestamp,
      session: sessionName,
      sessionId,
      model: ml,
      cost: usage.cost,
      tokens: usage.totalTokens,
      cacheWrite: usage.cacheWrite,
      cacheRead: usage.cacheRead,
    };
    recentEvents.unshift(event);
    if (recentEvents.length > MAX_RECENT) recentEvents.length = MAX_RECENT;

    // Persist to SQLite
    try {
      insertEvent.run(usage.timestamp, sessionName, sessionId, usage.model, usage.cost,
        usage.input, usage.output, usage.cacheRead, usage.cacheWrite, usage.totalTokens);

      const d = todayStr();
      upsertSessionDaily.run(d, sessionId, sessionName, usage.model, usage.cost, 1,
        usage.totalTokens, usage.cacheRead, usage.cacheWrite);

      upsertDaily.run(d, today.cost, today.messages, today.tokens, today.cacheRead,
        today.cacheWrite, JSON.stringify(today.models), JSON.stringify(
          Object.fromEntries(Object.entries(today.sessions).map(([k, v]) => [k, { name: v.name, cost: v.cost, messages: v.messages }]))
        ), new Date().toISOString());
    } catch {}

    // Broadcast to SSE clients
    if (broadcast) {
      const payload = JSON.stringify({ type: 'event', event, today: getTodaySummary() });
      for (const res of sseClients) {
        try { res.write(`data: ${payload}\n\n`); } catch { sseClients.delete(res); }
      }
    }
  }

  function getTodaySummary() {
    return {
      cost: today.cost,
      messages: today.messages,
      tokens: today.tokens,
      cacheRead: today.cacheRead,
      cacheWrite: today.cacheWrite,
      models: today.models,
      sessions: Object.entries(today.sessions).map(([id, s]) => ({
        id, name: s.name, model: s.model, cost: s.cost, messages: s.messages, tokens: s.tokens, lastSeen: s.lastSeen,
      })).sort((a, b) => b.cost - a.cost),
      peakCostPerMsg,
      avgCostPerMsg: today.messages > 0 ? today.cost / today.messages : 0,
    };
  }

  // ── API endpoints ──────────────────────────────────────
  function getHistory(days = 30) {
    try {
      return db.prepare(`SELECT * FROM daily_snapshots ORDER BY date DESC LIMIT ?`).all(days);
    } catch { return []; }
  }

  function getSessionHistory(days = 7) {
    try {
      return db.prepare(`SELECT * FROM session_daily WHERE date >= date('now', ?) ORDER BY date, cost DESC`).all(`-${days} days`);
    } catch { return []; }
  }

  function getHourlyToday() {
    try {
      return db.prepare(`
        SELECT strftime('%H', timestamp) as hour, SUM(cost) as cost, COUNT(*) as messages, SUM(total_tokens) as tokens
        FROM events WHERE date(timestamp) = date('now') GROUP BY hour ORDER BY hour
      `).all();
    } catch { return []; }
  }

  function getTopMessages(limit = 10) {
    try {
      return db.prepare(`
        SELECT timestamp, session_name, model, cost, total_tokens, cache_write
        FROM events WHERE date(timestamp) = date('now') ORDER BY cost DESC LIMIT ?
      `).all(limit);
    } catch { return []; }
  }

  // ── HTTP Server ────────────────────────────────────────
  const server = http.createServer((req, res) => {
    const url = new URL(req.url, `http://localhost:${port}`);

    // SSE endpoint
    if (url.pathname === '/api/stream') {
      res.writeHead(200, {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Access-Control-Allow-Origin': '*',
      });
      res.write(`data: ${JSON.stringify({ type: 'init', today: getTodaySummary(), recent: recentEvents.slice(0, 20) })}\n\n`);
      sseClients.add(res);
      req.on('close', () => sseClients.delete(res));
      return;
    }

    // JSON API endpoints
    if (url.pathname === '/api/today') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(getTodaySummary()));
      return;
    }

    if (url.pathname === '/api/history') {
      const days = parseInt(url.searchParams.get('days') || '30');
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(getHistory(days)));
      return;
    }

    if (url.pathname === '/api/hourly') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(getHourlyToday()));
      return;
    }

    if (url.pathname === '/api/top-messages') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(getTopMessages()));
      return;
    }

    if (url.pathname === '/api/sessions') {
      const days = parseInt(url.searchParams.get('days') || '7');
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify(getSessionHistory(days)));
      return;
    }

    // Serve dashboard HTML
    if (url.pathname === '/' || url.pathname === '/index.html') {
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(getDashboardHTML());
      return;
    }

    res.writeHead(404);
    res.end('Not found');
  });

  // ── Start ──────────────────────────────────────────────
  discoverFiles();

  // Re-discover new files every 30s
  setInterval(discoverFiles, 30000);

  // Periodic snapshot save every 60s
  setInterval(() => {
    try {
      const d = todayStr();
      upsertDaily.run(d, today.cost, today.messages, today.tokens, today.cacheRead,
        today.cacheWrite, JSON.stringify(today.models), JSON.stringify(
          Object.fromEntries(Object.entries(today.sessions).map(([k, v]) => [k, { name: v.name, cost: v.cost, messages: v.messages }]))
        ), new Date().toISOString());
    } catch {}
  }, 60000);

  server.listen(port, '127.0.0.1', () => {
    console.log(`\n\x1b[36m  CLAWCULATOR WEB DASHBOARD\x1b[0m`);
    console.log(`\x1b[90m  ─────────────────────────────────\x1b[0m`);
    console.log(`  🦞 Dashboard:  \x1b[1m\x1b[36mhttp://localhost:${port}\x1b[0m`);
    console.log(`  📊 Watching:   ${watchers.size} transcript(s)`);
    console.log(`  💾 Database:   ${dbPath}`);
    console.log(`  📅 Today:      $${today.cost.toFixed(2)} across ${today.messages} messages`);
    console.log(`\x1b[90m  ─────────────────────────────────\x1b[0m`);
    console.log(`\x1b[90m  💡 Pin this tab for always-on cost monitoring\x1b[0m`);
    console.log(`\x1b[90m  Press Ctrl+C to stop\x1b[0m\n`);

    // Auto-open browser
    const { exec } = require('child_process');
    exec(`open "http://localhost:${port}" 2>/dev/null || xdg-open "http://localhost:${port}" 2>/dev/null`);
  });

  // Cleanup
  process.on('SIGINT', () => {
    console.log(`\n\x1b[36mClawculator Web\x1b[0m stopped. Today: $${today.cost.toFixed(2)} across ${today.messages} messages.\n`);
    for (const [, w] of watchers) { try { w.close(); } catch {} }
    try { db.close(); } catch {}
    process.exit(0);
  });

  return { server, db };
}

// ── Dashboard HTML ───────────────────────────────────────
function getDashboardHTML() {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Clawculator — Live Cost Dashboard</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🦞</text></svg>">
<style>
  @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

  :root {
    --bg-deep: #05080f;
    --bg-card: #0b1120;
    --bg-card-hover: #0f1729;
    --border: #1a2744;
    --border-glow: #1e3a5f;
    --cyan: #22d3ee;
    --cyan-dim: #0891b2;
    --amber: #f59e0b;
    --amber-dim: #92400e;
    --red: #ef4444;
    --red-dim: #991b1b;
    --green: #22c55e;
    --green-dim: #166534;
    --purple: #a78bfa;
    --text: #e2e8f0;
    --text-dim: #64748b;
    --text-muted: #334155;
    --glass: rgba(11, 17, 32, 0.8);
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Outfit', sans-serif;
    background: var(--bg-deep);
    color: var(--text);
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* Animated background grid */
  body::before {
    content: '';
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background:
      linear-gradient(rgba(34,211,238,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(34,211,238,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    z-index: 0;
    animation: gridScroll 20s linear infinite;
  }
  @keyframes gridScroll { to { background-position: 60px 60px; } }

  /* Glow orb in background */
  body::after {
    content: '';
    position: fixed; top: -200px; right: -200px;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(34,211,238,0.08) 0%, transparent 70%);
    z-index: 0;
    animation: orbFloat 15s ease-in-out infinite alternate;
  }
  @keyframes orbFloat {
    0% { transform: translate(0, 0); }
    100% { transform: translate(-100px, 100px); }
  }

  .app { position: relative; z-index: 1; max-width: 1400px; margin: 0 auto; padding: 24px; }

  /* Header */
  .header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 20px 0; margin-bottom: 24px;
    border-bottom: 1px solid var(--border);
  }
  .logo-area { display: flex; align-items: center; gap: 16px; }
  .logo-claw {
    font-size: 48px;
    animation: chomp 0.6s steps(2) infinite;
    filter: drop-shadow(0 0 12px rgba(34,211,238,0.3));
  }
  @keyframes chomp {
    0%, 100% { transform: scaleX(1); }
    50% { transform: scaleX(0.9); }
  }
  .logo-text {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 800; font-size: 28px; letter-spacing: -1px;
    background: linear-gradient(135deg, var(--cyan), #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  }
  .logo-sub { font-size: 13px; color: var(--text-dim); margin-top: 2px; }
  .header-right { text-align: right; }
  .live-dot {
    display: inline-block; width: 8px; height: 8px; border-radius: 50%;
    background: var(--green); margin-right: 6px;
    animation: pulse 2s ease-in-out infinite;
  }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
  .header-time { font-family: 'JetBrains Mono', monospace; font-size: 13px; color: var(--text-dim); }

  /* Pac-Claw Chase */
  .pacclaw-track {
    position: absolute; top: 14px; left: 140px; right: 200px; height: 50px;
    overflow: hidden; pointer-events: none;
  }
  .pacclaw-claw {
    position: absolute; left: -40px; top: 8px; font-size: 32px; z-index: 2;
    animation: clawRun 12s linear infinite;
    filter: drop-shadow(0 0 8px rgba(34,211,238,0.4));
  }
  .pacclaw-claw .claw-top {
    display: block; transform-origin: bottom center;
    animation: clawChomp 0.3s steps(2) infinite;
    line-height: 0.5;
  }
  .pacclaw-claw .claw-bot {
    display: block; transform-origin: top center;
    animation: clawChompBot 0.3s steps(2) infinite;
    line-height: 0.5;
  }
  @keyframes clawChomp {
    0%, 100% { transform: rotate(0deg); }
    50% { transform: rotate(-15deg); }
  }
  @keyframes clawChompBot {
    0%, 100% { transform: rotate(0deg); }
    50% { transform: rotate(15deg); }
  }
  @keyframes clawRun {
    0% { left: -40px; }
    100% { left: calc(100% + 40px); }
  }
  .pacclaw-penny {
    position: absolute; top: 12px; font-size: 22px; z-index: 1;
    transition: opacity 0.15s, transform 0.15s;
  }
  .pacclaw-penny.eaten {
    opacity: 0 !important;
    transform: scale(0.3) !important;
  }
  /* Speed up claw on cost spike */
  .pacclaw-track.turbo .pacclaw-claw {
    animation-duration: 4s;
    filter: drop-shadow(0 0 16px rgba(239,68,68,0.6));
  }

  /* Cards */
  .card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px;
    transition: all 0.3s ease;
    position: relative; overflow: hidden;
  }
  .card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0; transition: opacity 0.3s;
  }
  .card:hover::before { opacity: 1; }
  .card:hover { border-color: var(--border-glow); }
  .card-label { font-size: 12px; font-weight: 600; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px; }
  .card-value {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 800; font-size: 36px; line-height: 1;
    transition: all 0.4s ease;
  }
  .card-sub { font-size: 13px; color: var(--text-dim); margin-top: 8px; }

  /* Big numbers grid */
  .stats-grid {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: 16px; margin-bottom: 24px;
  }
  .stat-primary .card-value { font-size: 52px; }

  /* Charts area */
  .charts-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 16px; margin-bottom: 24px;
  }

  /* Session table */
  .sessions-table { width: 100%; border-collapse: collapse; }
  .sessions-table th {
    font-size: 11px; font-weight: 600; color: var(--text-dim);
    text-transform: uppercase; letter-spacing: 1px;
    padding: 12px 16px; text-align: left;
    border-bottom: 1px solid var(--border);
  }
  .sessions-table td {
    padding: 12px 16px; font-size: 14px;
    border-bottom: 1px solid var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
  }
  .sessions-table tr:hover { background: var(--bg-card-hover); }

  /* Live feed */
  .feed-item {
    display: grid;
    grid-template-columns: 80px 120px 1fr 80px 80px;
    gap: 8px; padding: 8px 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px; border-bottom: 1px solid var(--text-muted);
    animation: feedSlide 0.3s ease-out;
  }
  @keyframes feedSlide { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }

  /* Donut chart */
  .donut-container { display: flex; align-items: center; gap: 24px; }
  .donut-svg { width: 160px; height: 160px; }
  .donut-legend { flex: 1; }
  .legend-item { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 13px; }
  .legend-dot { width: 10px; height: 10px; border-radius: 50%; }

  /* Bar chart */
  .bar-chart { display: flex; align-items: flex-end; gap: 4px; height: 200px; padding-top: 20px; }
  .bar-group { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px; }
  .bar {
    width: 100%; border-radius: 4px 4px 0 0;
    background: linear-gradient(180deg, var(--cyan), var(--cyan-dim));
    transition: height 0.6s ease;
    min-height: 2px; position: relative;
  }
  .bar:hover { filter: brightness(1.3); }
  .bar-label { font-size: 10px; color: var(--text-dim); font-family: 'JetBrains Mono', monospace; }
  .bar-value {
    font-size: 10px; color: var(--cyan); font-family: 'JetBrains Mono', monospace;
    position: absolute; top: -16px; left: 50%; transform: translateX(-50%); white-space: nowrap;
  }

  /* Heat map */
  .heatmap { display: grid; grid-template-columns: repeat(7, 1fr); gap: 3px; }
  .heat-cell {
    aspect-ratio: 1; border-radius: 3px;
    border: 1px solid var(--text-muted);
    transition: all 0.2s; cursor: pointer;
    position: relative;
  }
  .heat-cell:hover { border-color: var(--cyan); transform: scale(1.2); z-index: 2; }
  .heat-cell[title]:hover::after {
    content: attr(title); position: absolute; bottom: 110%; left: 50%; transform: translateX(-50%);
    background: var(--bg-card); color: var(--text); padding: 4px 8px; border-radius: 4px;
    font-size: 11px; white-space: nowrap; border: 1px solid var(--border);
    font-family: 'JetBrains Mono', monospace; z-index: 10;
  }

  /* Meter / gauge */
  .gauge-container { display: flex; flex-direction: column; align-items: center; }
  .gauge-svg { width: 200px; height: 120px; }
  .gauge-label { font-size: 13px; color: var(--text-dim); margin-top: 8px; }

  /* Velocity indicator */
  .velocity { display: flex; align-items: center; gap: 6px; font-size: 13px; }
  .velocity-arrow { font-size: 16px; }
  .velocity-up { color: var(--red); }
  .velocity-down { color: var(--green); }
  .velocity-flat { color: var(--text-dim); }

  /* Leaderboard */
  .leaderboard-item {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 0; border-bottom: 1px solid var(--text-muted);
  }
  .leaderboard-rank {
    width: 28px; height: 28px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 13px;
    font-family: 'JetBrains Mono', monospace;
  }
  .rank-1 { background: linear-gradient(135deg, #fbbf24, #f59e0b); color: #000; }
  .rank-2 { background: linear-gradient(135deg, #94a3b8, #64748b); color: #000; }
  .rank-3 { background: linear-gradient(135deg, #c2855a, #a0714a); color: #000; }
  .rank-n { background: var(--text-muted); color: var(--text-dim); }

  /* Responsive */
  @media (max-width: 900px) {
    .stats-grid { grid-template-columns: 1fr 1fr; }
    .charts-grid { grid-template-columns: 1fr; }
    .stat-primary .card-value { font-size: 36px; }
  }

  /* Counter animation */
  .counter-animate {
    display: inline-block;
    transition: transform 0.2s ease;
  }
  .counter-animate.bump { transform: scale(1.1); }

  /* Sections */
  .section-title {
    font-size: 14px; font-weight: 700; color: var(--text-dim);
    text-transform: uppercase; letter-spacing: 2px;
    margin-bottom: 16px;
    display: flex; align-items: center; gap: 8px;
  }
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }

  /* No data state */
  .no-data { text-align: center; padding: 40px; color: var(--text-dim); font-size: 14px; }
</style>
</head>
<body>
<div class="app">

  <!-- Header -->
  <div class="header">
    <div class="logo-area">
      <div class="logo-claw">🦞</div>
      <div>
        <div class="logo-text">CLAWCULATOR</div>
        <div class="logo-sub">Your friendly penny pincher</div>
      </div>
    </div>
    <div class="pacclaw-track" id="pacclawTrack">
      <div class="pacclaw-claw" id="pacclawClaw"><span class="claw-top">🦞</span></div>
    </div>
    <div class="header-right">
      <div><span class="live-dot"></span><span style="color:var(--green); font-weight:600; font-size:13px;">LIVE</span></div>
      <div class="header-time" id="clock"></div>
    </div>
  </div>

  <!-- Big Numbers -->
  <div class="stats-grid">
    <div class="card stat-primary">
      <div class="card-label">Today's Spend</div>
      <div class="card-value counter-animate" id="todayCost" style="color:var(--amber)">$0.00</div>
      <div class="card-sub" id="todayVsYesterday"></div>
    </div>
    <div class="card">
      <div class="card-label">Messages</div>
      <div class="card-value counter-animate" id="todayMessages" style="color:var(--text)">0</div>
      <div class="card-sub" id="avgCost"></div>
    </div>
    <div class="card">
      <div class="card-label">Peak $/msg</div>
      <div class="card-value counter-animate" id="peakCost" style="color:var(--red)">$0.00</div>
      <div class="card-sub">Most expensive single call</div>
    </div>
    <div class="card">
      <div class="card-label">Burn Rate</div>
      <div class="card-value counter-animate" id="burnRate" style="color:var(--purple)">—</div>
      <div class="card-sub" id="projectedMonth"></div>
    </div>
  </div>

  <!-- Charts Row -->
  <div class="charts-grid">
    <div class="card">
      <div class="section-title">📊 Hourly Cost Today</div>
      <div class="bar-chart" id="hourlyChart"></div>
    </div>
    <div class="card">
      <div class="section-title">🧠 Model Mix</div>
      <div class="donut-container" id="modelDonut">
        <div class="no-data">Waiting for data...</div>
      </div>
    </div>
  </div>

  <!-- Sessions + Feed -->
  <div class="two-col">
    <div class="card">
      <div class="section-title">⚡ Active Sessions</div>
      <table class="sessions-table">
        <thead><tr><th>Session</th><th>Model</th><th>Msgs</th><th>Cost</th></tr></thead>
        <tbody id="sessionsBody"></tbody>
      </table>
    </div>
    <div class="card">
      <div class="section-title">🏆 Costliest Calls Today</div>
      <div id="leaderboard"></div>
    </div>
  </div>

  <!-- History + Heat Map -->
  <div class="two-col">
    <div class="card">
      <div class="section-title">📅 Daily History</div>
      <div class="bar-chart" id="historyChart" style="height:160px"></div>
    </div>
    <div class="card">
      <div class="section-title">🔥 Spend Heat Map (30 days)</div>
      <div class="heatmap" id="heatmap"></div>
    </div>
  </div>

  <!-- Live Feed -->
  <div class="card" style="margin-bottom:24px">
    <div class="section-title">🌊 Live Feed</div>
    <div id="liveFeed"></div>
  </div>

</div>

<script>
// ── State ─────────────────────────────────────────────
let state = { cost: 0, messages: 0, tokens: 0, cacheRead: 0, cacheWrite: 0, models: {}, sessions: [], peakCostPerMsg: 0, avgCostPerMsg: 0 };
let recentEvents = [];
let historyData = [];

// ── Helpers ───────────────────────────────────────────
function fmtCost(n) {
  if (n >= 1) return '$' + n.toFixed(2);
  if (n >= 0.01) return '$' + n.toFixed(4);
  return '$' + n.toFixed(6);
}
function fmtTokens(n) {
  if (n >= 1e6) return (n/1e6).toFixed(1) + 'M';
  if (n >= 1e3) return (n/1e3).toFixed(1) + 'K';
  return String(n);
}

// ── Pac-Claw Chase Engine ─────────────────────────────
const pacTrack = document.getElementById('pacclawTrack');
const pacClaw = document.getElementById('pacclawClaw');
let pacPennies = [];
let pacTurboTimeout = null;

function spawnPacPennies() {
  // Clear old pennies
  pacPennies.forEach(p => p.el.remove());
  pacPennies = [];
  const trackWidth = pacTrack.offsetWidth || 800;
  const count = 8 + Math.floor(Math.random() * 5);
  for (let i = 0; i < count; i++) {
    const el = document.createElement('span');
    el.className = 'pacclaw-penny';
    el.textContent = '🪙';
    const x = 40 + (i / count) * (trackWidth - 80);
    el.style.left = x + 'px';
    el.style.opacity = '0.6';
    pacTrack.appendChild(el);
    pacPennies.push({ el, x, eaten: false });
  }
}
spawnPacPennies();

// Check claw position and eat pennies
function pacClawLoop() {
  if (!pacClaw) return;
  const clawRect = pacClaw.getBoundingClientRect();
  const trackRect = pacTrack.getBoundingClientRect();
  const clawX = clawRect.left - trackRect.left + clawRect.width / 2;

  for (const penny of pacPennies) {
    if (!penny.eaten && Math.abs(penny.x - clawX) < 22) {
      penny.eaten = true;
      penny.el.classList.add('eaten');
    }
  }

  // Respawn when claw completes a lap (all eaten or claw past right edge)
  const allEaten = pacPennies.every(p => p.eaten);
  if (allEaten || clawX > (pacTrack.offsetWidth || 800) + 30) {
    setTimeout(spawnPacPennies, 500);
  }

  requestAnimationFrame(pacClawLoop);
}
requestAnimationFrame(pacClawLoop);

// Turbo mode on cost events
function triggerPacTurbo() {
  pacTrack.classList.add('turbo');
  // Spawn extra pennies during turbo
  const trackWidth = pacTrack.offsetWidth || 800;
  for (let i = 0; i < 3; i++) {
    const el = document.createElement('span');
    el.className = 'pacclaw-penny';
    el.textContent = '🪙';
    const x = Math.random() * trackWidth;
    el.style.left = x + 'px';
    el.style.opacity = '0.8';
    pacTrack.appendChild(el);
    pacPennies.push({ el, x, eaten: false });
  }
  clearTimeout(pacTurboTimeout);
  pacTurboTimeout = setTimeout(() => pacTrack.classList.remove('turbo'), 5000);
}

// ── Clock ─────────────────────────────────────────────
setInterval(() => {
  document.getElementById('clock').textContent = new Date().toLocaleTimeString();
}, 1000);
document.getElementById('clock').textContent = new Date().toLocaleTimeString();

// ── Render Functions ──────────────────────────────────
function updateBigNumbers() {
  const costEl = document.getElementById('todayCost');
  costEl.textContent = fmtCost(state.cost);
  costEl.style.color = state.cost > 10 ? 'var(--red)' : state.cost > 1 ? 'var(--amber)' : 'var(--green)';
  bump(costEl);

  const msgEl = document.getElementById('todayMessages');
  msgEl.textContent = state.messages;
  bump(msgEl);

  const peakEl = document.getElementById('peakCost');
  peakEl.textContent = fmtCost(state.peakCostPerMsg);
  bump(peakEl);

  document.getElementById('avgCost').textContent = 'Avg: ' + fmtCost(state.avgCostPerMsg) + '/msg';

  // Burn rate
  const now = new Date();
  const hoursElapsed = now.getHours() + now.getMinutes() / 60;
  if (hoursElapsed > 0.5 && state.cost > 0) {
    const hourlyRate = state.cost / hoursElapsed;
    const dailyProjection = hourlyRate * 24;
    document.getElementById('burnRate').textContent = fmtCost(hourlyRate) + '/hr';
    document.getElementById('projectedMonth').textContent = '~' + fmtCost(dailyProjection * 30) + '/month projected';
  }
}

function bump(el) {
  el.classList.remove('bump');
  void el.offsetWidth;
  el.classList.add('bump');
  setTimeout(() => el.classList.remove('bump'), 300);
}

function renderSessions() {
  const tbody = document.getElementById('sessionsBody');
  if (!state.sessions.length) {
    tbody.innerHTML = '<tr><td colspan="4" style="color:var(--text-dim);text-align:center;padding:20px;">Waiting for API calls...</td></tr>';
    return;
  }
  tbody.innerHTML = state.sessions.slice(0, 8).map(s => {
    const costColor = s.cost > 5 ? 'var(--red)' : s.cost > 0.5 ? 'var(--amber)' : 'var(--green)';
    return '<tr>' +
      '<td style="color:var(--cyan)">' + (s.name.length > 18 ? s.name.slice(0,16)+'…' : s.name) + '</td>' +
      '<td style="color:var(--text-dim)">' + (s.model || '—') + '</td>' +
      '<td>' + s.messages + '</td>' +
      '<td style="color:' + costColor + '">' + fmtCost(s.cost) + '</td>' +
    '</tr>';
  }).join('');
}

function renderModelDonut() {
  const container = document.getElementById('modelDonut');
  const models = Object.entries(state.models).sort((a,b) => b[1] - a[1]);
  if (!models.length) { container.innerHTML = '<div class="no-data">Waiting for data...</div>'; return; }

  const total = models.reduce((s, [,v]) => s + v, 0);
  const colors = ['#22d3ee', '#a78bfa', '#f59e0b', '#ef4444', '#22c55e', '#f97316'];
  let cumAngle = 0;
  const paths = models.map(([name, cost], i) => {
    const pct = cost / total;
    const startAngle = cumAngle;
    cumAngle += pct * 360;
    const endAngle = cumAngle;
    const r = 60, cx = 80, cy = 80;
    const x1 = cx + r * Math.cos((startAngle - 90) * Math.PI / 180);
    const y1 = cy + r * Math.sin((startAngle - 90) * Math.PI / 180);
    const x2 = cx + r * Math.cos((endAngle - 90) * Math.PI / 180);
    const y2 = cy + r * Math.sin((endAngle - 90) * Math.PI / 180);
    const large = pct > 0.5 ? 1 : 0;
    const ri = 35;
    const x3 = cx + ri * Math.cos((endAngle - 90) * Math.PI / 180);
    const y3 = cy + ri * Math.sin((endAngle - 90) * Math.PI / 180);
    const x4 = cx + ri * Math.cos((startAngle - 90) * Math.PI / 180);
    const y4 = cy + ri * Math.sin((startAngle - 90) * Math.PI / 180);
    return { path: 'M'+x1+','+y1+' A'+r+','+r+' 0 '+large+' 1 '+x2+','+y2+' L'+x3+','+y3+' A'+ri+','+ri+' 0 '+large+' 0 '+x4+','+y4+' Z', color: colors[i % colors.length], name, cost, pct };
  });

  container.innerHTML =
    '<svg class="donut-svg" viewBox="0 0 160 160">' +
    paths.map(p => '<path d="'+p.path+'" fill="'+p.color+'" opacity="0.85"><title>'+p.name+': '+fmtCost(p.cost)+' ('+(p.pct*100).toFixed(1)+'%)</title></path>').join('') +
    '<text x="80" y="78" text-anchor="middle" fill="white" font-family="JetBrains Mono" font-weight="800" font-size="16">'+fmtCost(total)+'</text>' +
    '<text x="80" y="94" text-anchor="middle" fill="#64748b" font-family="JetBrains Mono" font-size="10">total</text>' +
    '</svg>' +
    '<div class="donut-legend">' +
    paths.map(p => '<div class="legend-item"><div class="legend-dot" style="background:'+p.color+'"></div><span style="color:var(--text-dim)">'+p.name+'</span><span style="margin-left:auto;font-family:JetBrains Mono;font-size:12px;color:'+p.color+'">'+fmtCost(p.cost)+'</span></div>').join('') +
    '</div>';
}

function renderHourlyChart() {
  fetch('/api/hourly').then(r => r.json()).then(data => {
    const chart = document.getElementById('hourlyChart');
    if (!data.length) { chart.innerHTML = '<div class="no-data">No hourly data yet</div>'; return; }
    const max = Math.max(...data.map(d => d.cost), 0.01);
    const hours = Array.from({length: 24}, (_, i) => String(i).padStart(2, '0'));
    const dataMap = Object.fromEntries(data.map(d => [d.hour, d]));

    chart.innerHTML = hours.map(h => {
      const d = dataMap[h];
      const cost = d ? d.cost : 0;
      const height = Math.max(2, (cost / max) * 180);
      const now = new Date().getHours();
      const isCurrent = parseInt(h) === now;
      const color = isCurrent ? 'var(--amber)' : 'var(--cyan)';
      return '<div class="bar-group">' +
        '<div class="bar" style="height:'+height+'px;background:linear-gradient(180deg,'+color+','+color+'44)">' +
        (cost > 0 ? '<div class="bar-value">'+fmtCost(cost)+'</div>' : '') +
        '</div>' +
        '<div class="bar-label"'+(isCurrent?' style="color:var(--amber);font-weight:700"':'')+'>'+h+'</div>' +
      '</div>';
    }).join('');
  }).catch(() => {});
}

function renderHistory() {
  fetch('/api/history?days=14').then(r => r.json()).then(data => {
    historyData = data;
    const chart = document.getElementById('historyChart');
    if (!data.length) { chart.innerHTML = '<div class="no-data">No history yet — data builds over time</div>'; return; }
    const sorted = [...data].sort((a,b) => a.date.localeCompare(b.date));
    const max = Math.max(...sorted.map(d => d.total_cost), 0.01);

    chart.innerHTML = sorted.map(d => {
      const height = Math.max(2, (d.total_cost / max) * 140);
      const isToday = d.date === new Date().toISOString().slice(0,10);
      const color = isToday ? 'var(--amber)' : 'var(--cyan)';
      const label = d.date.slice(5);
      return '<div class="bar-group">' +
        '<div class="bar" style="height:'+height+'px;background:linear-gradient(180deg,'+color+','+color+'44)" title="'+d.date+': '+fmtCost(d.total_cost)+' ('+d.total_messages+' msgs)">' +
        '<div class="bar-value">'+fmtCost(d.total_cost)+'</div>' +
        '</div>' +
        '<div class="bar-label"'+(isToday?' style="color:var(--amber);font-weight:700"':'')+'>'+label+'</div>' +
      '</div>';
    }).join('');

    // Yesterday comparison
    if (sorted.length >= 2) {
      const todayData = sorted[sorted.length - 1];
      const yesterData = sorted[sorted.length - 2];
      if (todayData && yesterData && yesterData.total_cost > 0) {
        const diff = todayData.total_cost - yesterData.total_cost;
        const pct = (diff / yesterData.total_cost * 100);
        const el = document.getElementById('todayVsYesterday');
        if (diff > 0) {
          el.innerHTML = '<span style="color:var(--red)">▲ +'+fmtCost(diff)+' vs yesterday (+'+pct.toFixed(0)+'%)</span>';
        } else {
          el.innerHTML = '<span style="color:var(--green)">▼ '+fmtCost(diff)+' vs yesterday ('+pct.toFixed(0)+'%)</span>';
        }
      }
    }
  }).catch(() => {});
}

function renderHeatmap() {
  fetch('/api/history?days=35').then(r => r.json()).then(data => {
    const heatmap = document.getElementById('heatmap');
    const costMap = Object.fromEntries(data.map(d => [d.date, d.total_cost]));
    const maxCost = Math.max(...data.map(d => d.total_cost), 1);

    let cells = '';
    for (let i = 34; i >= 0; i--) {
      const d = new Date(); d.setDate(d.getDate() - i);
      const ds = d.toISOString().slice(0, 10);
      const cost = costMap[ds] || 0;
      const intensity = cost > 0 ? Math.max(0.15, cost / maxCost) : 0;
      const color = cost === 0 ? 'var(--text-muted)' :
        intensity > 0.7 ? 'rgba(239,68,68,' + intensity + ')' :
        intensity > 0.3 ? 'rgba(245,158,11,' + intensity + ')' :
        'rgba(34,211,238,' + intensity + ')';
      cells += '<div class="heat-cell" style="background:' + color + '" title="' + ds + ': ' + fmtCost(cost) + '"></div>';
    }
    heatmap.innerHTML = cells;
  }).catch(() => {});
}

function renderLeaderboard() {
  fetch('/api/top-messages').then(r => r.json()).then(data => {
    const el = document.getElementById('leaderboard');
    if (!data.length) { el.innerHTML = '<div class="no-data">No calls yet today</div>'; return; }
    el.innerHTML = data.slice(0, 5).map((msg, i) => {
      const rankClass = i === 0 ? 'rank-1' : i === 1 ? 'rank-2' : i === 2 ? 'rank-3' : 'rank-n';
      const time = new Date(msg.timestamp).toLocaleTimeString();
      return '<div class="leaderboard-item">' +
        '<div class="leaderboard-rank ' + rankClass + '">' + (i+1) + '</div>' +
        '<div style="flex:1"><div style="font-weight:600;font-size:14px;color:var(--amber)">'+fmtCost(msg.cost)+'</div>' +
        '<div style="font-size:11px;color:var(--text-dim)">' + msg.session_name + ' · ' + (msg.model||'').split('/').pop() + ' · ' + time + '</div></div>' +
        '<div style="font-size:11px;color:var(--text-dim);text-align:right">' + fmtTokens(msg.total_tokens) + ' tok' +
        (msg.cache_write > 10000 ? '<br/>' + fmtTokens(msg.cache_write) + ' cache' : '') + '</div>' +
      '</div>';
    }).join('');
  }).catch(() => {});
}

function renderFeed() {
  const el = document.getElementById('liveFeed');
  if (!recentEvents.length) { el.innerHTML = '<div class="no-data">Waiting for API calls...</div>'; return; }
  el.innerHTML = recentEvents.slice(0, 12).map(ev => {
    const time = new Date(ev.time).toLocaleTimeString();
    const costColor = ev.cost > 0.5 ? 'var(--red)' : ev.cost > 0.05 ? 'var(--amber)' : 'var(--green)';
    return '<div class="feed-item">' +
      '<span style="color:var(--text-dim)">' + time + '</span>' +
      '<span style="color:var(--cyan)">' + ev.session + '</span>' +
      '<span style="color:var(--text-dim)">' + (ev.model||'').slice(0,20) + '</span>' +
      '<span style="color:' + costColor + ';text-align:right">' + fmtCost(ev.cost) + '</span>' +
      '<span style="color:var(--text-dim);text-align:right">' + fmtTokens(ev.tokens) + '</span>' +
    '</div>';
  }).join('');
}

// ── SSE Connection ────────────────────────────────────
function connect() {
  const es = new EventSource('/api/stream');

  es.onmessage = (e) => {
    const data = JSON.parse(e.data);

    if (data.type === 'init') {
      state = data.today;
      recentEvents = data.recent || [];
      renderAll();
      return;
    }

    if (data.type === 'event') {
      state = data.today;
      recentEvents.unshift(data.event);
      if (recentEvents.length > 50) recentEvents.length = 50;

      updateBigNumbers();
      renderSessions();
      renderModelDonut();
      renderFeed();
      triggerPacTurbo(); // 🦞 CHOMP CHOMP
    }
  };

  es.onerror = () => {
    es.close();
    setTimeout(connect, 3000);
  };
}

function renderAll() {
  updateBigNumbers();
  renderSessions();
  renderModelDonut();
  renderHourlyChart();
  renderHistory();
  renderHeatmap();
  renderLeaderboard();
  renderFeed();
}

// ── Init ──────────────────────────────────────────────
connect();

// Refresh charts every 30s
setInterval(() => {
  renderHourlyChart();
  renderHistory();
  renderHeatmap();
  renderLeaderboard();
}, 30000);
</script>
</body>
</html>`;
}

module.exports = { startWebDashboard };
