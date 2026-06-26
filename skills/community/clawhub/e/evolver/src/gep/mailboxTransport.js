'use strict';

const http = require('http');
const { getProxyUrl, getProxyToken } = require('../proxy/server/settings');

// Bounded keep-alive agent. Default `agent: undefined` would use Node's
// global `http.globalAgent` whose default keep-alive timeout is 8 seconds
// AND survives macOS sleep on libuv's monotonic clock. After the laptop
// resumes, the next request reuses a socket the proxy / local OS has
// already closed and only fails after `timeout: 10_000` -- enough time
// for the proxy-mode heartbeat to look stalled.
//
// Round-6 (§19.8): the previous value was 1000ms keepAliveMsecs, which
// was wrong for two reasons:
//   1. NAT eviction in residential / corporate networks is 300-900s,
//      not 1s. The 1s window was cargo-culted from browser keep-alive
//      defaults and gives zero real NAT-eviction protection for the
//      proxy is on localhost (NAT does not apply).
//   2. A 1s window forces a fresh TCP+TLS handshake on every request
//      that lands >=1s after the previous one, which is essentially
//      every request in steady state -- adding 10-50ms per call for
//      no gain. Locally the proxy is the only consumer; the real
//      sleep/wake risk is covered by the explicit
//      drainPool/wake-recovery path on the undici agent used for hub
//      traffic, NOT this localhost agent.
// 30s window balances:
//   - keep-alive reuse for legitimate proxy-mode bursts (proxy clients
//     issue heartbeat + mailbox poll + receive within sub-second)
//   - guarantees a fresh socket post-wake (longer-than-30s sleep ->
//     pool is empty by definition; shorter sleep -> proxy on
//     localhost would not have lost the socket anyway)
const _proxyAgent = new http.Agent({
  keepAlive: true,
  keepAliveMsecs: 30_000,
  maxSockets: 16,
  maxFreeSockets: 4,
});

function _request(method, path, body) {
  const proxyUrl = getProxyUrl();
  if (!proxyUrl) {
    return Promise.reject(new Error('Proxy not running (no url in settings.json)'));
  }

  const url = new URL(path, proxyUrl);

  return new Promise((resolve, reject) => {
    const payload = body ? JSON.stringify(body) : '';
    const token = getProxyToken();
    const headers = {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload),
    };
    if (token) headers['Authorization'] = 'Bearer ' + token;
    const req = http.request(
      {
        hostname: url.hostname,
        port: url.port,
        path: url.pathname,
        method,
        headers,
        timeout: 10_000,
        agent: _proxyAgent,
      },
      (res) => {
        const chunks = [];
        res.on('data', (c) => chunks.push(c));
        res.on('end', () => {
          const raw = Buffer.concat(chunks).toString();
          try {
            resolve(JSON.parse(raw));
          } catch {
            resolve({ raw });
          }
        });
      }
    );
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Proxy request timeout'));
    });
    if (payload) req.write(payload);
    req.end();
  });
}

function mailboxTransportSend(message) {
  const type = message.message_type || message.type || 'unknown';
  const payload = message.payload || message;
  return _request('POST', '/mailbox/send', { type, payload });
}

function mailboxTransportReceive(opts = {}) {
  return _request('POST', '/mailbox/poll', {
    type: opts.type || null,
    channel: opts.channel || null,
    limit: opts.limit || 20,
  }).then((data) => data.messages || []);
}

function mailboxTransportList(opts = {}) {
  const type = opts.type || 'hub_event';
  return _request('GET', `/mailbox/list?type=${encodeURIComponent(type)}&limit=${opts.limit || 20}`)
    .then((data) => data.messages || []);
}

const mailboxTransport = {
  send: mailboxTransportSend,
  receive: mailboxTransportReceive,
  list: mailboxTransportList,
};

function registerMailboxTransport() {
  const { registerTransport } = require('./a2aProtocol');
  registerTransport('mailbox', mailboxTransport);
}

module.exports = { mailboxTransport, registerMailboxTransport };
