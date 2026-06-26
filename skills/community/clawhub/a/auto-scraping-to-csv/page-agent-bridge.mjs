#!/usr/bin/env node
/**
 * Page-Agent Bridge — Host Model Edition
 *
 * A lightweight Node.js HTTP bridge that lets Claude (the host model) control
 * a local browser via Alibaba Page-Agent's text-based DOM manipulation.
 *
 * No external LLM required. Claude is the brain; Page-Agent provides the eyes
 * (text DOM state) and hands (click, type, scroll, etc.).
 *
 * Usage:
 *   node .claude/agents/page-agent-bridge.mjs [port]
 *
 * Endpoints:
 *   GET    /health                          → health check
 *   POST   /sessions                        → launch browser + navigate
 *   GET    /sessions/:id/state              → get text-based DOM state
 *   POST   /sessions/:id/act                → execute one Page-Agent action
 *   POST   /sessions/:id/navigate           → navigate to new URL
 *   DELETE /sessions/:id                    → close browser session
 *   POST   /shutdown                        → stop bridge server
 */

import http from 'node:http';
import { randomUUID } from 'node:crypto';

// ── Configuration ─────────────────────────────────────────────────────────────
const PORT = Number(process.argv[2]) || 9876;
const CDN_URL = 'https://cdn.jsdelivr.net/npm/page-agent@latest/dist/iife/page-agent.demo.js';
const MAX_SESSIONS = 5;

// ── Dynamic Playwright Import ─────────────────────────────────────────────
let chromium;
try {
  const pw = await import('playwright');
  chromium = pw.chromium;
} catch (err) {
  console.error('\n❌  Playwright is required but not installed.\n');
  console.error('   Install it now:\n');
  console.error('   npm install -D playwright');
  console.error('   npx playwright install chromium\n');
  process.exit(1);
}

// ── Session Store ───────────────────────────────────────────────────────────
const sessions = new Map();

async function createSession({ url, viewport = { width: 1280, height: 720 }, headless = false }) {
  if (sessions.size >= MAX_SESSIONS) {
    throw new Error(`Maximum ${MAX_SESSIONS} concurrent sessions reached.`);
  }

  const id = randomUUID().slice(0, 8);
  const browser = await chromium.launch({ headless });
  const context = await browser.newContext({ viewport });
  const page = await context.newPage();

  // Navigate and inject Page-Agent IIFE
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.addScriptTag({ url: CDN_URL });

  // Wait for PageAgent class to be available, then clean up auto-init instance
  await page.waitForFunction(() => typeof window.PageAgent === 'function', { timeout: 15000 });
  await page.evaluate(() => new Promise(r => setTimeout(r, 300))); // let auto-init settle

  await page.evaluate(() => {
    if (window.pageAgent) {
      try { window.pageAgent.stop(); } catch (e) { /* ignore */ }
      try { window.pageAgent.dispose(); } catch (e) { /* ignore */ }
      window.pageAgent = null;
    }
    // Create a clean agent with dummy config — no LLM calls will be made
    window.__bridgeAgent = new window.PageAgent({
      baseURL: 'http://localhost:1',
      model: 'dummy',
      apiKey: 'dummy',
      enableMask: false,
      language: 'en-US',
    });
  });

  sessions.set(id, { browser, context, page, url, createdAt: Date.now() });
  return { id, url };
}

async function getState(id) {
  const s = getSession(id);
  const state = await s.page.evaluate(async () => {
    const controller = window.__bridgeAgent.pageController;
    return await controller.getBrowserState();
  });
  return state;
}

async function act(id, action, params = {}) {
  const s = getSession(id);

  // Ensure tree is indexed before any element action
  if (action !== 'getBrowserState') {
    await s.page.evaluate(async () => {
      await window.__bridgeAgent.pageController.updateTree();
    });
  }

  const result = await s.page.evaluate(async ({ action, params }) => {
    const ctrl = window.__bridgeAgent.pageController;
    switch (action) {
      case 'getBrowserState':
        return await ctrl.getBrowserState();
      case 'updateTree':
        return await ctrl.updateTree();
      case 'clickElement':
        return await ctrl.clickElement(params.index);
      case 'inputText':
        return await ctrl.inputText(params.index, params.text);
      case 'selectOption':
        return await ctrl.selectOption(params.index, params.optionText);
      case 'scroll': {
        const opts = {
          down: params.down ?? true,
          numPages: params.num_pages ?? params.numPages ?? 0.1,
          pixels: params.pixels,
          index: params.index,
        };
        return await ctrl.scroll(opts);
      }
      case 'scrollHorizontally': {
        const opts = {
          right: params.right ?? true,
          pixels: params.pixels,
          index: params.index,
        };
        return await ctrl.scrollHorizontally(opts);
      }
      case 'executeJavascript':
        return await ctrl.executeJavascript(params.script);
      case 'cleanUpHighlights':
        await ctrl.cleanUpHighlights();
        return { success: true, message: 'Highlights cleaned' };
      case 'wait': {
        const ms = (params.seconds ?? 1) * 1000;
        await new Promise(r => setTimeout(r, ms));
        return { success: true, message: `Waited ${params.seconds ?? 1}s` };
      }
      default:
        throw new Error(`Unknown action: ${action}`);
    }
  }, { action, params });

  return result;
}

async function navigate(id, url) {
  const s = getSession(id);
  await s.page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  return { url };
}

async function closeSession(id) {
  const s = sessions.get(id);
  if (!s) return false;
  try { await s.page.evaluate(() => window.__bridgeAgent?.dispose()); } catch (e) { /* ignore */ }
  try { await s.browser.close(); } catch (e) { /* ignore */ }
  sessions.delete(id);
  return true;
}

function getSession(id) {
  const s = sessions.get(id);
  if (!s) throw new Error(`Session not found: ${id}`);
  return s;
}

async function closeAll() {
  for (const [id] of sessions) {
    await closeSession(id);
  }
}

// ── HTTP Server ─────────────────────────────────────────────────────────────
const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const send = (status, body) => {
    res.writeHead(status, {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    });
    res.end(JSON.stringify(body, null, 2));
  };

  // CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    });
    res.end();
    return;
  }

  try {
    // GET /health
    if (url.pathname === '/health' && req.method === 'GET') {
      send(200, { status: 'ok', sessions: sessions.size, maxSessions: MAX_SESSIONS });
      return;
    }

    // POST /sessions
    if (url.pathname === '/sessions' && req.method === 'POST') {
      const body = await readBody(req);
      if (!body?.url) {
        send(400, { error: 'url is required' });
        return;
      }
      const session = await createSession({
        url: body.url,
        viewport: body.viewport,
        headless: body.headless ?? false,
      });
      send(201, session);
      return;
    }

    // GET /sessions/:id/state
    const stateMatch = url.pathname.match(/^\/sessions\/([a-zA-Z0-9-]+)\/state$/);
    if (stateMatch && req.method === 'GET') {
      const id = stateMatch[1];
      const state = await getState(id);
      send(200, state);
      return;
    }

    // POST /sessions/:id/act
    const actMatch = url.pathname.match(/^\/sessions\/([a-zA-Z0-9-]+)\/act$/);
    if (actMatch && req.method === 'POST') {
      const id = actMatch[1];
      const body = await readBody(req);
      if (!body?.action) {
        send(400, { error: 'action is required' });
        return;
      }
      const result = await act(id, body.action, body.params || {});
      send(200, result);
      return;
    }

    // POST /sessions/:id/navigate
    const navMatch = url.pathname.match(/^\/sessions\/([a-zA-Z0-9-]+)\/navigate$/);
    if (navMatch && req.method === 'POST') {
      const id = navMatch[1];
      const body = await readBody(req);
      if (!body?.url) {
        send(400, { error: 'url is required' });
        return;
      }
      const result = await navigate(id, body.url);
      send(200, result);
      return;
    }

    // DELETE /sessions/:id
    const delMatch = url.pathname.match(/^\/sessions\/([a-zA-Z0-9-]+)$/);
    if (delMatch && req.method === 'DELETE') {
      const id = delMatch[1];
      const ok = await closeSession(id);
      send(ok ? 200 : 404, { success: ok });
      return;
    }

    // POST /shutdown
    if (url.pathname === '/shutdown' && req.method === 'POST') {
      send(200, { status: 'shutting down' });
      setTimeout(() => {
        closeAll().then(() => server.close(() => process.exit(0)));
      }, 100);
      return;
    }

    send(404, { error: 'Not found' });
  } catch (err) {
    console.error('Bridge error:', err.message);
    send(500, { error: err.message });
  }
});

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', chunk => (data += chunk));
    req.on('end', () => {
      try {
        resolve(data ? JSON.parse(data) : {});
      } catch (e) {
        reject(new Error('Invalid JSON body'));
      }
    });
    req.on('error', reject);
  });
}

// ── Lifecycle ───────────────────────────────────────────────────────────────
process.on('SIGINT', async () => {
  console.log('\n\n🛑  Shutting down bridge...');
  await closeAll();
  server.close(() => process.exit(0));
});

process.on('SIGTERM', async () => {
  await closeAll();
  server.close(() => process.exit(0));
});

server.listen(PORT, () => {
  console.log(`\n🚀  Page-Agent Bridge (Host Model) running on http://localhost:${PORT}`);
  console.log(`   Sessions max: ${MAX_SESSIONS}`);
  console.log(`   Playwright:   ${chromium ? 'ready' : 'unavailable'}`);
  console.log(`\n   Endpoints:`);
  console.log(`   POST /sessions              → start session { url, viewport?, headless? }`);
  console.log(`   GET  /sessions/:id/state    → get DOM text state`);
  console.log(`   POST /sessions/:id/act      → execute action { action, params? }`);
  console.log(`   POST /sessions/:id/navigate → navigate { url }`);
  console.log(`   DELETE /sessions/:id        → close session`);
  console.log(`   POST /shutdown              → stop bridge\n`);
});
