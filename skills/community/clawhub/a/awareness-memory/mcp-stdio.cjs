#!/usr/bin/env node
/**
 * mcp-stdio.cjs — Zero-dependency stdio MCP server for Awareness Local.
 *
 * Implements the MCP JSON-RPC protocol over stdin/stdout directly,
 * no @modelcontextprotocol/sdk needed. Proxies all tool calls to
 * the local daemon at http://localhost:37800/mcp.
 *
 * Auto-starts daemon if not running.
 *
 * Schema stance (F-053 + insights-bug fix 2026-04-18):
 *   - `awareness_recall.required = ['query']` — single-param API.
 *   - `awareness_record.required = ['content']` — single-param API.
 *   - `insights` deliberately has NO `type` declared so MCP clients that
 *     occasionally serialize nested objects (string) still pass client-side
 *     Zod validation. `normalizeToolArgs` below parses stringified JSON
 *     before forwarding to the daemon, so the server always gets the
 *     object form.
 */

const http = require('http');
const { spawn } = require('child_process');

const PORT = parseInt(process.env.AWARENESS_LOCAL_PORT || '37800', 10);

// ── Logging (stderr only) ─────────────────────────────────────────────

function log(...args) {
  process.stderr.write(`[awareness-mcp] ${args.join(' ')}\n`);
}

// ── HTTP helpers ──────────────────────────────────────────────────────

function httpPost(port, path, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const req = http.request({
      hostname: '127.0.0.1', port, path,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(data) },
    }, (res) => {
      let chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        try { resolve(JSON.parse(Buffer.concat(chunks).toString())); }
        catch { reject(new Error('Invalid JSON response')); }
      });
    });
    req.on('error', reject);
    req.setTimeout(15000, () => { req.destroy(); reject(new Error('timeout')); });
    req.write(data);
    req.end();
  });
}

function httpGet(port, path) {
  return new Promise((resolve, reject) => {
    const req = http.request({
      hostname: '127.0.0.1', port, path, method: 'GET',
    }, (res) => {
      let chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        try { resolve({ status: res.statusCode, body: JSON.parse(Buffer.concat(chunks).toString()) }); }
        catch { resolve({ status: res.statusCode, body: null }); }
      });
    });
    req.on('error', reject);
    req.setTimeout(3000, () => { req.destroy(); reject(new Error('timeout')); });
    req.end();
  });
}

// ── Daemon auto-start ────────────────────────────────────────────────

let daemonReady = false;

async function checkHealth() {
  try {
    const r = await httpGet(PORT, '/healthz');
    return r.status === 200;
  } catch { return false; }
}

async function ensureDaemon() {
  if (daemonReady) return true;
  if (await checkHealth()) { daemonReady = true; return true; }

  log('Daemon not running, starting...');
  const child = spawn('npx', ['-y', '@awareness-sdk/local', 'start'], {
    detached: true, stdio: 'ignore',
    env: { ...process.env, FORCE_COLOR: '0' },
  });
  child.unref();

  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 500));
    if (await checkHealth()) { daemonReady = true; log('Daemon ready'); return true; }
  }
  log('Failed to start daemon within 15s');
  return false;
}

// ── Arg normalization (defensive: some MCP clients serialize objects) ─

function tryParseJson(value) {
  if (typeof value !== 'string') return value;
  const trimmed = value.trim();
  if (!trimmed) return value;
  const first = trimmed[0];
  if (first !== '{' && first !== '[') return value;
  try { return JSON.parse(trimmed); }
  catch { return value; }
}

// Fields that are semantically structured (object/array) but may arrive as
// a JSON string from clients whose wire layer stringifies nested values.
const STRUCTURED_FIELDS = ['insights', 'items', 'tags', 'ids', 'source_exclude'];

function normalizeToolArgs(args) {
  if (!args || typeof args !== 'object') return args || {};
  const out = { ...args };
  for (const field of STRUCTURED_FIELDS) {
    if (field in out) out[field] = tryParseJson(out[field]);
  }
  return out;
}

// ── Tool definitions ─────────────────────────────────────────────────
// Kept aligned with sdks/local/src/daemon/mcp-contract.mjs. `insights`
// has no `type` declared on purpose (see header comment).

const TOOLS = [
  {
    name: 'awareness_init',
    description: 'Start a new session and load context (knowledge cards, tasks, rules). Call this at the beginning of every conversation.',
    inputSchema: {
      type: 'object',
      properties: {
        memory_id: { type: 'string', description: 'Memory identifier (ignored in local mode)' },
        source: { type: 'string', description: 'Client source identifier' },
        query: { type: 'string', description: 'Current user request or task focus for context shaping' },
        days: { type: 'number', description: 'Days of history to load', default: 7 },
        max_cards: { type: 'number', default: 5 },
        max_tasks: { type: 'number', default: 5 },
        max_sessions: { type: 'number', description: 'Number of recent session summaries to include (0 = fresh session)', default: 0 },
      },
    },
  },
  {
    name: 'awareness_recall',
    description: 'Search persistent memory for past decisions, solutions, and knowledge. Pass ONE natural-language `query` — the daemon picks scope, recall mode, and detail automatically (F-053 single-parameter API).',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Natural-language search query. The daemon handles everything else.' },
        limit: { type: 'number', default: 10, maximum: 30 },
        token_budget: { type: 'number', description: 'Token budget for bucket shaping (default 20000)', default: 20000 },
        agent_role: { type: 'string' },
        // --- [DEPRECATED] Legacy multi-param surface, still accepted ---
        semantic_query: { type: 'string', description: '[DEPRECATED] Pass `query` instead.' },
        keyword_query: { type: 'string', description: '[DEPRECATED] Pass `query` instead.' },
        scope: { type: 'string', enum: ['all', 'timeline', 'knowledge', 'insights'], description: '[DEPRECATED]' },
        recall_mode: { type: 'string', enum: ['precise', 'session', 'structured', 'hybrid', 'auto'], description: '[DEPRECATED]' },
        detail: { type: 'string', enum: ['summary', 'full'], description: '[DEPRECATED]' },
        ids: { description: '[DEPRECATED] Item IDs to expand (with detail=full). Accepts array or JSON-string array.' },
        multi_level: { type: 'boolean', description: '[DEPRECATED]' },
        cluster_expand: { type: 'boolean', description: '[DEPRECATED]' },
        include_installed: { type: 'boolean', description: '[DEPRECATED]' },
        source_exclude: { description: '[DEPRECATED] Accepts array or JSON-string array.' },
      },
      required: ['query'],
    },
  },
  {
    name: 'awareness_record',
    description: 'Record memory — pass ONE `content` string and the daemon defaults action=remember + triggers salience-aware extraction (F-053 single-parameter API). Optionally include `insights` with pre-extracted knowledge cards / tasks / risks.',
    inputSchema: {
      type: 'object',
      properties: {
        content: { type: 'string', description: 'Memory content in markdown. The ONLY parameter callers need.' },
        // Intentionally NO `type` on insights so MCP clients whose wire layer
        // stringifies nested objects pass client-side Zod validation. The
        // stdio server parses the string before forwarding to the daemon.
        insights: { description: 'Pre-extracted knowledge cards / tasks / risks. Accepts an object OR a JSON-string.' },
        // --- [DEPRECATED] Legacy multi-param surface, still accepted ---
        action: { type: 'string', enum: ['remember', 'remember_batch', 'update_task', 'submit_insights'], description: '[DEPRECATED] Defaults to "remember" when content is provided.' },
        title: { type: 'string' },
        items: { description: 'Batch items for remember_batch. Accepts array OR JSON-string.' },
        session_id: { type: 'string' },
        agent_role: { type: 'string' },
        event_type: { type: 'string' },
        tags: { description: 'Accepts array OR JSON-string array.' },
        task_id: { type: 'string' },
        status: { type: 'string' },
        source: { type: 'string' },
      },
      required: ['content'],
    },
  },
  {
    name: 'awareness_lookup',
    description: 'Fast DB lookup — use instead of awareness_recall when you know what type of data you want.',
    inputSchema: {
      type: 'object',
      properties: {
        type: { type: 'string', enum: ['context', 'tasks', 'knowledge', 'risks', 'session_history', 'timeline', 'skills'] },
        limit: { type: 'number', default: 10 },
        status: { type: 'string' },
        category: { type: 'string' },
        priority: { type: 'string' },
        session_id: { type: 'string' },
        agent_role: { type: 'string' },
        query: { type: 'string' },
      },
      required: ['type'],
    },
  },
  {
    name: 'awareness_get_agent_prompt',
    description: 'Get the activation prompt for a specific agent role.',
    inputSchema: {
      type: 'object',
      properties: {
        role: { type: 'string', description: 'Agent role to get prompt for' },
      },
    },
  },
  {
    name: 'awareness_mark_skill_used',
    description: 'Report skill usage outcome — success, partial, or failed. Call AFTER applying a skill.',
    inputSchema: {
      type: 'object',
      properties: {
        skill_id: { type: 'string' },
        outcome: { type: 'string', enum: ['success', 'partial', 'failed'], default: 'success' },
      },
      required: ['skill_id'],
    },
  },
  {
    name: 'awareness_apply_skill',
    description: 'Fetch a skill by ID and get a step-by-step execution plan.',
    inputSchema: {
      type: 'object',
      properties: {
        skill_id: { type: 'string' },
        context: { type: 'string', description: 'Optional task context' },
      },
      required: ['skill_id'],
    },
  },
];

// ── Proxy tool call to daemon ────────────────────────────────────────

async function proxyToolCall(toolName, args) {
  await ensureDaemon();
  // Defensive normalize: parse stringified object/array fields BEFORE the
  // daemon sees them. Handles the case where a client's MCP bridge
  // accidentally JSON.stringifies nested `insights` / `items` / `tags`.
  const normalized = normalizeToolArgs(args);
  const rpc = {
    jsonrpc: '2.0', id: 1,
    method: 'tools/call',
    params: { name: toolName, arguments: normalized },
  };
  const resp = await httpPost(PORT, '/mcp', rpc);
  if (resp.error) throw new Error(resp.error.message || JSON.stringify(resp.error));
  return resp.result;
}

// ── JSON-RPC stdio handler ───────────────────────────────────────────

function sendResponse(id, result) {
  const msg = JSON.stringify({ jsonrpc: '2.0', id, result });
  process.stdout.write(msg + '\n');
}

function sendError(id, code, message) {
  const msg = JSON.stringify({ jsonrpc: '2.0', id, error: { code, message } });
  process.stdout.write(msg + '\n');
}

async function handleRequest(req) {
  const { id, method, params } = req;

  switch (method) {
    case 'initialize':
      return sendResponse(id, {
        protocolVersion: '2024-11-05',
        serverInfo: { name: 'awareness-memory', version: '0.3.8' },
        capabilities: { tools: {} },
      });

    case 'notifications/initialized':
      return;

    case 'tools/list':
      return sendResponse(id, { tools: TOOLS });

    case 'tools/call': {
      const toolName = params?.name;
      const args = params?.arguments || {};
      try {
        const result = await proxyToolCall(toolName, args);
        return sendResponse(id, result);
      } catch (err) {
        return sendResponse(id, {
          content: [{ type: 'text', text: JSON.stringify({ error: err.message }) }],
          isError: true,
        });
      }
    }

    default:
      if (id) sendError(id, -32601, `Method not found: ${method}`);
  }
}

// ── Stdin line parser ────────────────────────────────────────────────
// Only run the server when this file is executed directly. When required
// from a test or guard (e.g. verify-mcp-stdio-schema-aligned.mjs), the
// stdin listener + startup log are not wanted.

function startServer() {
  let buffer = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', (chunk) => {
    buffer += chunk;
    let newlineIdx;
    while ((newlineIdx = buffer.indexOf('\n')) !== -1) {
      const line = buffer.slice(0, newlineIdx).trim();
      buffer = buffer.slice(newlineIdx + 1);
      if (!line) continue;
      try {
        const req = JSON.parse(line);
        handleRequest(req).catch(err => {
          log('Handler error:', err.message);
          if (req.id) sendError(req.id, -32603, err.message);
        });
      } catch (e) {
        log('Parse error:', e.message);
      }
    }
  });
  process.stdin.on('end', () => process.exit(0));
  log('stdio MCP server started (daemon port=' + PORT + ')');
}

// Exports for testing (node --test can require this file without running the server).
if (typeof module !== 'undefined') {
  module.exports = { tryParseJson, normalizeToolArgs, TOOLS };
}

if (require.main === module) {
  startServer();
}
