'use strict';

const fs = require('fs');
const path = require('path');
const os = require('os');
const { resolveModel, MODEL_PRICING } = require('./analyzer');

// ── ANSI codes ───────────────────────────────────────────
const R   = '\x1b[0m';
const B   = '\x1b[1m';
const D   = '\x1b[90m';
const RED = '\x1b[31m';
const GRN = '\x1b[32m';
const YEL = '\x1b[33m';
const CYN = '\x1b[36m';
const WHT = '\x1b[37m';
const BG_DARK = '\x1b[48;5;233m';
const CLEAR = '\x1b[2J\x1b[H';
const HIDE_CURSOR = '\x1b[?25l';
const SHOW_CURSOR = '\x1b[?25h';

// ── Helpers ──────────────────────────────────────────────
function modelLabel(modelStr) {
  const key = resolveModel(modelStr);
  return key ? (MODEL_PRICING[key]?.label || key) : (modelStr || 'unknown');
}

function fmtCost(n) {
  if (n >= 1)    return `$${n.toFixed(2)}`;
  if (n >= 0.01) return `$${n.toFixed(4)}`;
  return `$${n.toFixed(6)}`;
}

function fmtTokens(n) {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000)     return `${(n / 1_000).toFixed(1)}K`;
  return String(n);
}

function timestamp() {
  return new Date().toLocaleTimeString();
}

function relTime(ms) {
  const s = Math.floor(ms / 1000);
  if (s < 60)  return `${s}s ago`;
  if (s < 3600) return `${Math.floor(s / 60)}m ago`;
  return `${Math.floor(s / 3600)}h ago`;
}

// ── Parse a single .jsonl line for usage ─────────────────
function parseUsageLine(line) {
  try {
    const entry = JSON.parse(line);
    if (entry.type !== 'message') return null;
    const u = entry.usage || entry.message?.usage;
    if (!u) return null;
    const model = entry.model || entry.message?.model;
    const ts = entry.timestamp || entry.message?.timestamp;
    const cost = u.cost
      ? (typeof u.cost === 'object' ? u.cost.total || 0 : u.cost)
      : 0;
    return {
      model,
      input: u.input || 0,
      output: u.output || 0,
      cacheRead: u.cacheRead || 0,
      cacheWrite: u.cacheWrite || 0,
      totalTokens: u.totalTokens || 0,
      cost,
      timestamp: ts ? new Date(ts).getTime() : Date.now(),
    };
  } catch {
    return null;
  }
}

// ── Live Dashboard ───────────────────────────────────────
function startLiveDashboard(opts = {}) {
  const openclawHome = opts.openclawHome || process.env.OPENCLAW_HOME || path.join(os.homedir(), '.openclaw');
  const refreshMs = opts.refreshMs || 2000;

  // State
  const sessions = new Map(); // sessionId -> { name, model, cost, tokens, messages, lastSeen, cacheRead, cacheWrite }
  const feed = [];           // last N events for the activity feed
  const MAX_FEED = 12;
  let todayCost = 0;
  let todayMessages = 0;
  let todayTokens = 0;
  let todayCacheRead = 0;
  let todayCacheWrite = 0;
  let peakCostPerMsg = 0;
  let startTime = Date.now();
  let lastEventTime = null;

  // File watchers & byte offsets
  const watchers = new Map();  // filePath -> fs.FSWatcher
  const offsets = new Map();   // filePath -> byte offset (for tailing)
  const fileToSession = new Map(); // filePath -> { id, name }

  // ── Discover sessions.json for friendly names ──────────
  function getSessionNames() {
    const names = new Map(); // sessionId -> friendly key name
    const agentsDir = path.join(openclawHome, 'agents');
    try {
      for (const agent of fs.readdirSync(agentsDir)) {
        const sjPath = path.join(agentsDir, agent, 'sessions', 'sessions.json');
        if (!fs.existsSync(sjPath)) continue;
        const sj = JSON.parse(fs.readFileSync(sjPath, 'utf8'));
        for (const [key, val] of Object.entries(sj)) {
          if (val.sessionId) {
            // Use shortest meaningful name
            const short = key
              .replace('agent:main:', '')
              .replace(/:[a-f0-9-]{36}/g, '')
              .replace(/:run$/, '');
            if (!names.has(val.sessionId) || short.length < names.get(val.sessionId).length) {
              names.set(val.sessionId, short);
            }
          }
        }
      }
    } catch { /* ok */ }
    return names;
  }

  // ── Discover & watch .jsonl files ──────────────────────
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
          if (watchers.has(filePath)) continue; // already watching

          const sessionId = file.replace('.jsonl', '');
          const friendlyName = sessionNames.get(sessionId) || sessionId.slice(0, 8);
          fileToSession.set(filePath, { id: sessionId, name: friendlyName });

          // Initial parse — only count today's messages
          initialParse(filePath, sessionId, friendlyName);

          // Watch for changes
          try {
            const watcher = fs.watch(filePath, () => {
              tailFile(filePath);
            });
            watchers.set(filePath, watcher);
          } catch { /* can't watch */ }
        }
      }
    } catch { /* agents dir missing */ }
  }

  // ── Initial parse: read existing today's data ──────────
  function initialParse(filePath, sessionId, friendlyName) {
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const stat = fs.statSync(filePath);
      offsets.set(filePath, stat.size); // start tailing from end

      const todayStart = new Date();
      todayStart.setHours(0, 0, 0, 0);
      const todayMs = todayStart.getTime();

      let sessionCost = 0, sessionTokens = 0, sessionMessages = 0;
      let sessionCacheRead = 0, sessionCacheWrite = 0;
      let sessionModel = null, sessionLastSeen = null;

      for (const line of content.split('\n')) {
        if (!line.trim()) continue;
        const usage = parseUsageLine(line);
        if (!usage) continue;

        if (!sessionModel) sessionModel = usage.model;
        sessionLastSeen = usage.timestamp;

        // Only count today for the live totals
        if (usage.timestamp >= todayMs) {
          sessionCost += usage.cost;
          sessionTokens += usage.totalTokens;
          sessionMessages++;
          sessionCacheRead += usage.cacheRead;
          sessionCacheWrite += usage.cacheWrite;
          todayCost += usage.cost;
          todayMessages++;
          todayTokens += usage.totalTokens;
          todayCacheRead += usage.cacheRead;
          todayCacheWrite += usage.cacheWrite;
          if (usage.cost > peakCostPerMsg) peakCostPerMsg = usage.cost;
        }
      }

      if (sessionMessages > 0 || sessionModel) {
        sessions.set(sessionId, {
          name: friendlyName,
          model: sessionModel,
          cost: sessionCost,
          tokens: sessionTokens,
          messages: sessionMessages,
          lastSeen: sessionLastSeen,
          cacheRead: sessionCacheRead,
          cacheWrite: sessionCacheWrite,
        });
      }
    } catch { /* can't read */ }
  }

  // ── Tail new data from file ────────────────────────────
  function tailFile(filePath) {
    try {
      const stat = fs.statSync(filePath);
      const prevOffset = offsets.get(filePath) || 0;
      if (stat.size <= prevOffset) return;

      const fd = fs.openSync(filePath, 'r');
      const buf = Buffer.alloc(stat.size - prevOffset);
      fs.readSync(fd, buf, 0, buf.length, prevOffset);
      fs.closeSync(fd);
      offsets.set(filePath, stat.size);

      const newContent = buf.toString('utf8');
      const session = fileToSession.get(filePath);
      if (!session) return;

      for (const line of newContent.split('\n')) {
        if (!line.trim()) continue;
        const usage = parseUsageLine(line);
        if (!usage) continue;

        // Update session totals
        const existing = sessions.get(session.id) || {
          name: session.name, model: null, cost: 0, tokens: 0,
          messages: 0, lastSeen: null, cacheRead: 0, cacheWrite: 0,
        };
        existing.model = usage.model || existing.model;
        existing.cost += usage.cost;
        existing.tokens += usage.totalTokens;
        existing.messages++;
        existing.lastSeen = usage.timestamp;
        existing.cacheRead += usage.cacheRead;
        existing.cacheWrite += usage.cacheWrite;
        sessions.set(session.id, existing);

        // Update today totals
        todayCost += usage.cost;
        todayMessages++;
        todayTokens += usage.totalTokens;
        todayCacheRead += usage.cacheRead;
        todayCacheWrite += usage.cacheWrite;
        if (usage.cost > peakCostPerMsg) peakCostPerMsg = usage.cost;
        lastEventTime = Date.now();

        // Add to activity feed
        feed.unshift({
          time: new Date(usage.timestamp).toLocaleTimeString(),
          session: session.name,
          model: modelLabel(usage.model),
          cost: usage.cost,
          tokens: usage.totalTokens,
          cacheWrite: usage.cacheWrite,
        });
        if (feed.length > MAX_FEED) feed.length = MAX_FEED;
      }

      render();
    } catch { /* file read error */ }
  }

  // ── Render the dashboard ───────────────────────────────
  function render() {
    const cols = process.stdout.columns || 80;
    const rows = process.stdout.rows || 24;
    const line = D + '─'.repeat(Math.min(cols - 2, 80)) + R;
    const uptime = Math.floor((Date.now() - startTime) / 1000);
    const uptimeStr = uptime < 60 ? `${uptime}s` : `${Math.floor(uptime / 60)}m ${uptime % 60}s`;

    let out = CLEAR;

    // Header
    out += `${CYN}${B}  CLAWCULATOR LIVE${R}  ${D}·${R} ${D}watching ${watchers.size} transcript${watchers.size !== 1 ? 's' : ''}${R}  ${D}·${R} ${D}uptime ${uptimeStr}${R}  ${D}·${R} ${D}${timestamp()}${R}\n`;
    out += `${line}\n`;

    // Big numbers row
    const costColor = todayCost > 10 ? RED : todayCost > 1 ? YEL : GRN;
    out += `\n`;
    out += `  ${D}TODAY'S SPEND${R}      ${D}MESSAGES${R}        ${D}AVG $/MSG${R}       ${D}PEAK $/MSG${R}\n`;
    out += `  ${B}${costColor}${fmtCost(todayCost)}${R}`;
    out += `${' '.repeat(Math.max(1, 18 - fmtCost(todayCost).length))}`;
    out += `${B}${WHT}${todayMessages}${R}`;
    out += `${' '.repeat(Math.max(1, 16 - String(todayMessages).length))}`;
    const avgCost = todayMessages > 0 ? todayCost / todayMessages : 0;
    out += `${B}${WHT}${fmtCost(avgCost)}${R}`;
    out += `${' '.repeat(Math.max(1, 16 - fmtCost(avgCost).length))}`;
    out += `${B}${RED}${fmtCost(peakCostPerMsg)}${R}\n`;
    out += `\n`;

    // Token breakdown bar
    const totalTok = todayTokens + todayCacheRead + todayCacheWrite;
    if (totalTok > 0) {
      out += `  ${D}TOKENS${R}  ${WHT}${fmtTokens(todayTokens)} i/o${R}  ${D}·${R}  ${GRN}${fmtTokens(todayCacheRead)} cache read${R}  ${D}·${R}  ${YEL}${fmtTokens(todayCacheWrite)} cache write${R}\n`;
      out += `\n`;
    }

    out += `${line}\n`;

    // Active sessions
    out += `  ${CYN}${B}ACTIVE SESSIONS${R}\n`;
    const sortedSessions = [...sessions.entries()]
      .filter(([, s]) => s.messages > 0)
      .sort((a, b) => b[1].cost - a[1].cost);

    if (sortedSessions.length === 0) {
      out += `  ${D}No API calls yet today. Waiting...${R}\n`;
    } else {
      out += `  ${D}${'Name'.padEnd(20)} ${'Model'.padEnd(22)} ${'Msgs'.padEnd(6)} ${'Cost'.padEnd(12)} Last Active${R}\n`;
      for (const [, s] of sortedSessions.slice(0, 8)) {
        const name = s.name.length > 18 ? s.name.slice(0, 16) + '…' : s.name;
        const model = modelLabel(s.model);
        const modelDisp = model.length > 20 ? model.slice(0, 18) + '…' : model;
        const age = s.lastSeen ? relTime(Date.now() - s.lastSeen) : '—';
        const costStr = fmtCost(s.cost);
        const costClr = s.cost > 5 ? RED : s.cost > 0.5 ? YEL : GRN;
        out += `  ${WHT}${name.padEnd(20)}${R} ${D}${modelDisp.padEnd(22)}${R} ${WHT}${String(s.messages).padEnd(6)}${R} ${costClr}${costStr.padEnd(12)}${R} ${D}${age}${R}\n`;
      }
    }
    out += `\n${line}\n`;

    // Live activity feed
    out += `  ${CYN}${B}LIVE FEED${R}${lastEventTime ? `  ${D}last event: ${relTime(Date.now() - lastEventTime)}${R}` : ''}\n`;
    if (feed.length === 0) {
      out += `  ${D}Waiting for API calls...${R}\n`;
    } else {
      for (const ev of feed.slice(0, 8)) {
        const costClr = ev.cost > 0.5 ? RED : ev.cost > 0.05 ? YEL : GRN;
        const cacheTag = ev.cacheWrite > 10000 ? ` ${D}(${fmtTokens(ev.cacheWrite)} cache write)${R}` : '';
        out += `  ${D}${ev.time}${R} ${WHT}${ev.session.padEnd(14)}${R} ${D}${ev.model.slice(0, 18).padEnd(18)}${R} ${costClr}${fmtCost(ev.cost).padEnd(10)}${R} ${D}${fmtTokens(ev.tokens)} tok${R}${cacheTag}\n`;
      }
    }
    out += `\n${line}\n`;

    // Footer
    out += `  ${D}Press ${WHT}q${D} to quit · ${WHT}r${D} to refresh · Ctrl+C to exit${R}\n`;

    process.stdout.write(out);
  }

  // ── Keyboard input ─────────────────────────────────────
  if (process.stdin.isTTY) {
    process.stdin.setRawMode(true);
    process.stdin.resume();
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (key) => {
      if (key === 'q' || key === '\u0003') { // q or Ctrl+C
        cleanup();
        process.exit(0);
      }
      if (key === 'r') {
        // Force re-discover and re-render
        discoverFiles();
        render();
      }
    });
  }

  // ── Cleanup ────────────────────────────────────────────
  function cleanup() {
    process.stdout.write(SHOW_CURSOR);
    for (const [, watcher] of watchers) {
      try { watcher.close(); } catch {}
    }
    watchers.clear();
    console.log(`\n${CYN}Clawculator Live${R} stopped. Today's total: ${B}${fmtCost(todayCost)}${R} across ${todayMessages} messages.\n`);
  }

  process.on('SIGINT', () => { cleanup(); process.exit(0); });
  process.on('SIGTERM', () => { cleanup(); process.exit(0); });

  // ── Start ──────────────────────────────────────────────
  process.stdout.write(HIDE_CURSOR);
  discoverFiles();
  render();

  // Periodic refresh + file discovery (catch new sessions)
  const refreshInterval = setInterval(() => {
    render();
  }, refreshMs);

  // Re-discover new files every 30s
  const discoverInterval = setInterval(() => {
    discoverFiles();
  }, 30000);

  return { cleanup, render };
}

module.exports = { startLiveDashboard };
