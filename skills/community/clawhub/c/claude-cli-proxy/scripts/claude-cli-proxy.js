#!/usr/bin/env node
/**
 * claude-cli-proxy.js v6
 * 
 * HTTP proxy with SSE streaming for OpenClaw → Claude Code CLI.
 * Routes requests through persistent acpx session using Team/Max/Pro subscription.
 * 
 * Configurable via env vars:
 *   CCPROXY_PORT          (default: 8081)
 *   CCPROXY_SESSION_NAME  (default: dexter-proxy)
 *   CCPROXY_CWD           (default: ~/.openclaw/workspace)
 *   CCPROXY_TIMEOUT_MS    (default: 120000)
 *   CCPROXY_MAX_HISTORY   (default: 10) — max conversation turns to forward
 */

const http = require('http');
const { execFile, execSync } = require('child_process');
const path = require('path');
const os = require('os');

const PORT = parseInt(process.env.CCPROXY_PORT || '8081', 10);
const HOST = '127.0.0.1';
const TIMEOUT_MS = parseInt(process.env.CCPROXY_TIMEOUT_MS || '120000', 10);
const SESSION_NAME = process.env.CCPROXY_SESSION_NAME || 'dexter-proxy';
const CWD = process.env.CCPROXY_CWD || process.env.OPENCLAW_WORKSPACE ||
  path.join(os.homedir(), '.openclaw', 'workspace');
const MAX_HISTORY = parseInt(process.env.CCPROXY_MAX_HISTORY || '10', 10);

let sessionReady = false;

function ensureSession() {
  if (sessionReady) return;
  try {
    const out = execSync('acpx claude sessions list 2>&1', {
      cwd: CWD, timeout: 10000, encoding: 'utf8',
      env: { ...process.env, ANTHROPIC_API_KEY: '' },
    });
    if (!out.includes(SESSION_NAME)) {
      console.log(`Creating session "${SESSION_NAME}"...`);
      execSync(`acpx claude sessions new --name ${SESSION_NAME}`, {
        cwd: CWD, timeout: 10000, encoding: 'utf8',
        env: { ...process.env, ANTHROPIC_API_KEY: '' },
      });
      console.log('Session created.');
    } else {
      console.log(`Session "${SESSION_NAME}" already exists.`);
    }
    sessionReady = true;
  } catch (e) {
    console.error('Session init error:', e.message);
  }
}

// ── Text extraction ──

function extractText(content) {
  if (typeof content === 'string') return content;
  if (Array.isArray(content)) {
    return content.filter(b => b.type === 'text').map(b => b.text || '').join('\n\n');
  }
  return String(content || '');
}

// ── Prompt builder (system + history + last message) ──

function buildFullPrompt(body) {
  const parts = [];

  // 1. System prompt (OpenClaw sends SOUL.md, IDENTITY.md, MEMORY.md, etc.)
  if (body.system) {
    const sys = typeof body.system === 'string'
      ? body.system
      : Array.isArray(body.system)
        ? body.system.map(b => typeof b === 'string' ? b : (b.text || '')).join('\n')
        : '';
    if (sys.trim()) {
      // Write to temp file so Claude Code reads it as operator context
      // rather than user-injected text
      try {
        const fs = require('fs');
        const sysPath = path.join(CWD, '.ccproxy-system-context.md');
        fs.writeFileSync(sysPath, sys, 'utf8');
        parts.push(`Read .ccproxy-system-context.md for your full instructions and context. Follow them strictly.`);
      } catch {
        // Fallback: inline (may get rejected as injection on some models)
        parts.push(sys);
      }
    }
  }

  // 2. Conversation history (last N turns for continuity)
  const messages = body.messages || [];
  const historyStart = Math.max(0, messages.length - MAX_HISTORY);
  
  if (messages.length > 1) {
    const history = [];
    for (let i = historyStart; i < messages.length - 1; i++) {
      const m = messages[i];
      const role = m.role === 'assistant' ? 'Assistant' : 'User';
      const text = extractText(m.content);
      if (text.trim()) history.push(`${role}: ${text}`);
    }
    if (history.length > 0) {
      parts.push(`Previous conversation:\n${history.join('\n')}`);
    }
  }

  // 3. Current user message (always last)
  for (let i = messages.length - 1; i >= 0; i--) {
    if (messages[i].role === 'user') {
      parts.push(extractText(messages[i].content));
      break;
    }
  }

  return parts.join('\n\n');
}

// ── Output cleaner (strip Claude Code metadata) ──

function cleanClaudeOutput(raw) {
  const lines = raw.split('\n');
  let inBlock = false;
  const cleaned = [];

  for (const line of lines) {
    if (/^\[(acpx|client|done)\]/.test(line)) continue;
    if (/^\[thinking\]/.test(line)) { inBlock = true; continue; }
    if (/^\[tool\]/.test(line)) { inBlock = true; continue; }

    if (inBlock) {
      if (/^\s/.test(line)) continue;
      if (/^  (input|output|kind|files|\.\.\.):/.test(line)) continue;
      if (/^\s+\d+\t/.test(line) || /^\s+\.\.\. \(\d+ more/.test(line)) continue;
      inBlock = false;
    }

    cleaned.push(line);
  }

  return cleaned.join('\n').trim() || raw.trim();
}

// ── Session reset (on context overflow) ──

function resetSession() {
  const ts = () => new Date().toISOString();
  const env = { ...process.env, ANTHROPIC_API_KEY: '' };
  console.log(`[${ts()}] Resetting session "${SESSION_NAME}" (context overflow)...`);
  try {
    // Close all sessions with this name (there may be duplicates)
    for (let i = 0; i < 5; i++) {
      try {
        execSync(`acpx claude sessions close ${SESSION_NAME} 2>&1`, {
          cwd: CWD, timeout: 10000, encoding: 'utf8', env,
        });
      } catch { break; } // no more to close
    }
    // Create fresh session
    execSync(`acpx claude sessions new --name ${SESSION_NAME}`, {
      cwd: CWD, timeout: 10000, encoding: 'utf8', env,
    });
    console.log(`[${ts()}] Session reset complete.`);
  } catch (e) {
    console.error('Session reset error:', e.message);
  }
}

// ── Claude CLI call (with auto-retry on overflow) ──

function callClaude(prompt, retried = false) {
  return new Promise((resolve, reject) => {
    execFile('acpx', ['claude', 'prompt', '-s', SESSION_NAME, prompt], {
      cwd: CWD,
      env: { ...process.env, ANTHROPIC_API_KEY: '' },
      maxBuffer: 10 * 1024 * 1024,
      timeout: TIMEOUT_MS,
    }, (err, stdout, stderr) => {
      const output = (stdout || '') + (stderr || '');
      // Detect context overflow or session errors and auto-reset
      if (output.match(/context.*(overflow|too large|prompt.*large)/i) ||
          output.match(/conversation is too long/i) ||
          output.match(/No acpx session found/i)) {
        if (!retried) {
          resetSession();
          return callClaude(prompt, true).then(resolve).catch(reject);
        }
        return reject(new Error('Context overflow persists after session reset'));
      }
      if (err) reject(new Error(`acpx error: ${err.message} | ${stderr}`));
      else resolve(cleanClaudeOutput(stdout));
    });
  });
}

// ── Response helpers ──

function msgId() {
  return 'msg_cli_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
}

function makeResponse(text, model) {
  return {
    id: msgId(), type: 'message', role: 'assistant',
    content: [{ type: 'text', text }],
    model: model || 'claude-sonnet-4-6',
    stop_reason: 'end_turn', stop_sequence: null,
    usage: { input_tokens: 0, output_tokens: 0 },
  };
}

function sendSSE(res, text, model) {
  const id = msgId();
  const mdl = model || 'claude-sonnet-4-6';

  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
  });

  const sse = (event, data) => res.write(`event: ${event}\ndata: ${JSON.stringify(data)}\n\n`);

  sse('message_start', {
    type: 'message_start',
    message: { id, type: 'message', role: 'assistant', content: [], model: mdl,
      stop_reason: null, stop_sequence: null, usage: { input_tokens: 0, output_tokens: 0 } },
  });

  sse('content_block_start', {
    type: 'content_block_start', index: 0,
    content_block: { type: 'text', text: '' },
  });

  const CHUNK = 100;
  for (let i = 0; i < text.length; i += CHUNK) {
    sse('content_block_delta', {
      type: 'content_block_delta', index: 0,
      delta: { type: 'text_delta', text: text.slice(i, i + CHUNK) },
    });
  }

  sse('content_block_stop', { type: 'content_block_stop', index: 0 });
  sse('message_delta', {
    type: 'message_delta',
    delta: { stop_reason: 'end_turn', stop_sequence: null },
    usage: { output_tokens: 0 },
  });
  sse('message_stop', { type: 'message_stop' });
  res.end();
}

function sendError(res, status, message, stream) {
  const errBody = { type: 'error', error: { type: 'api_error', message } };
  if (stream) {
    res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache' });
    res.write(`event: error\ndata: ${JSON.stringify(errBody)}\n\n`);
    res.end();
  } else {
    res.writeHead(status, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(errBody));
  }
}

// ── Request queue (CLI handles one at a time) ──

let busy = false;
const queue = [];

function processQueue() {
  if (busy || queue.length === 0) return;
  busy = true;
  const { prompt, model, stream, res } = queue.shift();

  const start = Date.now();
  callClaude(prompt)
    .then(text => {
      const trimmed = text.trim();
      const elapsed = ((Date.now() - start) / 1000).toFixed(1);
      console.log(`[${new Date().toISOString()}] Done in ${elapsed}s | ${trimmed.length} chars | stream=${stream}`);
      stream ? sendSSE(res, trimmed, model) : (() => {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(makeResponse(trimmed, model)));
      })();
    })
    .catch(err => {
      console.error(`[${new Date().toISOString()}] ERROR:`, err.message);
      sendError(res, 500, err.message, stream);
    })
    .finally(() => { busy = false; processQueue(); });
}

// ── HTTP server ──

const server = http.createServer(async (req, res) => {
  if (req.url === '/health' || req.url === '/claude/sdk/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'ok', backend: 'claude-cli-v6', version: '6.0.0',
      session: SESSION_NAME, cwd: CWD, port: PORT,
    }));
    return;
  }

  if (req.method !== 'POST' ||
      (!req.url.includes('/v1/messages') && !req.url.includes('/v1/chat/completions'))) {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ type: 'error', error: { type: 'not_found', message: `Not found: ${req.url}` } }));
    return;
  }

  let body = '';
  for await (const chunk of req) body += chunk;

  let parsed;
  try { parsed = JSON.parse(body); } catch {
    sendError(res, 400, 'Invalid JSON', false); return;
  }

  const model = parsed.model || 'claude-sonnet-4-6';
  const stream = parsed.stream === true;
  const totalMessages = (parsed.messages || []).length;
  const hasSystem = !!(parsed.system);
  const prompt = buildFullPrompt(parsed);

  if (!prompt.trim()) { sendError(res, 400, 'Empty prompt', stream); return; }

  console.log(`[${new Date().toISOString()}] ${model} | ${totalMessages} msgs | sys=${hasSystem} | ${prompt.length} chars | stream=${stream} | queue: ${queue.length}`);

  queue.push({ prompt, model, stream, res });
  processQueue();
});

server.listen(PORT, HOST, () => {
  console.log(`claude-cli-proxy v6 listening on ${HOST}:${PORT}`);
  console.log(`Session: ${SESSION_NAME} | CWD: ${CWD} | Max history: ${MAX_HISTORY}`);
  console.log('Backend: claude CLI (Team subscription)');
  ensureSession();
});
