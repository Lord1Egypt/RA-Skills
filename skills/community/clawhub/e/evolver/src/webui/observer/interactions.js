'use strict';

const http = require('http');
const path = require('path');
const { getProxySettings } = require('./status');
const { getProxyToken } = require('../../proxy/server/settings');
const { readJsonl, paginate } = require('./jsonl');
const { redactValue } = require('./redact');
const { getEvomapPath } = require('../../gep/paths');

// Lazy via paths.getEvomapPath() — honors EVOLVER_HOME (#114).
function _defaultMailboxDir() { return getEvomapPath('mailbox'); }

async function getInteractions(query = {}) {
  const proxy = getProxySettings();
  const proxySnapshots = proxy.url ? await readProxySnapshots(proxy.url) : {};
  const mailbox = readMailboxMessages(query);
  return {
    proxy,
    proxySnapshots,
    mailbox: paginate(mailbox, query),
  };
}

function readMailboxMessages(query = {}) {
  const mailboxDir = query.mailboxDir || process.env.EVOMAP_MAILBOX_DIR || _defaultMailboxDir();
  const messages = readJsonl(path.join(mailboxDir, 'messages.jsonl'), { last: query.last || 500 })
    .filter((row) => row && !row._op)
    .map((row) => normalizeMessage(redactValue(row)));
  return filterMessages(messages, query);
}

async function readProxySnapshots(baseUrl) {
  const endpoints = {
    status: '/proxy/status',
    hubStatus: '/proxy/hub-status',
    taskMetrics: '/task/metrics',
    assetSubmissions: '/asset/submissions?limit=20',
    sessions: '/session/list?limit=20',
    dms: '/dm/list?limit=20',
    atpPolicy: '/atp/policy',
    atpProofs: '/atp/proofs?limit=20',
  };
  // Issue all proxy requests concurrently. Sequential await meant the
  // worst-case (every endpoint timing out at 1500ms each) blocked the
  // /webui/interactions response for ~12s; parallel keeps it ~1.5s.
  const entries = await Promise.all(
    Object.entries(endpoints).map(async ([key, endpoint]) =>
      [key, await requestJson(baseUrl + endpoint)],
    ),
  );
  return redactValue(Object.fromEntries(entries));
}

function requestJson(url) {
  return new Promise((resolve) => {
    const u = new URL(url);
    const token = getProxyToken();
    const headers = {};
    if (token) headers['Authorization'] = 'Bearer ' + token;
    const req = http.request(
      { hostname: u.hostname, port: u.port, path: u.pathname + (u.search || ''), method: 'GET', headers, timeout: 1500 },
      (res) => {
        const chunks = [];
        res.on('data', (chunk) => chunks.push(chunk));
        res.on('end', () => {
          const raw = Buffer.concat(chunks).toString();
          try {
            resolve({ ok: res.statusCode >= 200 && res.statusCode < 300, status: res.statusCode, body: JSON.parse(raw) });
          } catch {
            resolve({ ok: false, status: res.statusCode, body: null });
          }
        });
      },
    );
    req.on('timeout', () => { req.destroy(); resolve({ ok: false, status: 0, error: 'timeout' }); });
    req.on('error', (err) => resolve({ ok: false, status: 0, error: err.message }));
    req.end();
  });
}

function normalizeMessage(msg) {
  return {
    id: msg.id || null,
    source: 'mailbox',
    direction: msg.direction || null,
    type: msg.type || null,
    status: msg.status || null,
    timestamp: toIso(msg.created_at || msg.updated_at || msg.synced_at),
    refId: msg.ref_id || msg.payload && msg.payload.ref_id || null,
    priority: msg.priority || null,
    summary: summarizePayload(msg),
    payload: msg.payload || null,
  };
}

function filterMessages(messages, query) {
  return messages.filter((msg) => {
    if (query.type && msg.type !== query.type) return false;
    if (query.direction && msg.direction !== query.direction) return false;
    if (query.status && msg.status !== query.status) return false;
    return true;
  }).reverse();
}

function summarizePayload(msg) {
  const payload = msg.payload || {};
  if (payload.task_id) return `Task ${payload.task_id}`;
  if (payload.asset_id) return `Asset ${payload.asset_id}`;
  if (payload.session_id) return `Session ${payload.session_id}`;
  if (payload.title) return String(payload.title);
  if (msg.type) return String(msg.type).replace(/_/g, ' ');
  return 'message';
}

function toIso(value) {
  if (!value) return null;
  if (typeof value === 'string') return value;
  const n = Number(value);
  return Number.isFinite(n) ? new Date(n).toISOString() : null;
}

module.exports = {
  getInteractions,
  readMailboxMessages,
  readProxySnapshots,
};
