#!/usr/bin/env node
// Claw Relay CLI client for OpenClaw agents
// Usage: node relay-client.js [--url URL] [--token TOKEN] [--agent-id ID] ACTION [ARGS...]

const WebSocket = require('ws');

const TIMEOUT_MS = 30000;

function parseArgs(argv) {
  const args = argv.slice(2);
  const opts = {
    url: process.env.CLAW_RELAY_URL || 'ws://localhost:9333',
    token: process.env.CLAW_RELAY_TOKEN || '',
    agentId: process.env.CLAW_RELAY_AGENT || 'default',
  };
  let i = 0;
  while (i < args.length) {
    if (args[i] === '--url' && args[i + 1]) { opts.url = args[++i]; i++; continue; }
    if (args[i] === '--token' && args[i + 1]) { opts.token = args[++i]; i++; continue; }
    if (args[i] === '--agent-id' && args[i + 1]) { opts.agentId = args[++i]; i++; continue; }
    break;
  }
  opts.action = args[i];
  opts.actionArgs = args.slice(i + 1);
  return opts;
}

function buildAction(action, actionArgs) {
  switch (action) {
    case 'navigate':
      return { type: 'navigate', url: actionArgs[0] };
    case 'snapshot':
      return { type: 'snapshot' };
    case 'screenshot':
      return { type: 'screenshot' };
    case 'click':
      return { type: 'click', ref: actionArgs[0] };
    case 'fill':
      return { type: 'fill', ref: actionArgs[0], text: actionArgs.slice(1).join(' ') };
    case 'type':
      return { type: 'type', ref: actionArgs[0], text: actionArgs.slice(1).join(' ') };
    case 'press':
      return { type: 'press', key: actionArgs[0] };
    case 'hover':
      return { type: 'hover', ref: actionArgs[0] };
    case 'select':
      return { type: 'select', ref: actionArgs[0], values: actionArgs.slice(1) };
    case 'evaluate':
      return { type: 'evaluate', js: actionArgs.join(' ') };
    case 'close':
      return { type: 'close' };
    default:
      console.error(JSON.stringify({ error: `Unknown action: ${action}`, actions: ['navigate','snapshot','screenshot','click','fill','type','press','hover','select','evaluate','close'] }));
      process.exit(1);
  }
}

function run() {
  const opts = parseArgs(process.argv);
  if (!opts.action) {
    console.error('Usage: relay-client.js [--url URL] [--token TOKEN] [--agent-id ID] ACTION [ARGS...]');
    process.exit(1);
  }
  if (!opts.token) {
    console.error(JSON.stringify({ error: 'No token provided. Use --token or set CLAW_RELAY_TOKEN.' }));
    process.exit(1);
  }

  const actionMsg = buildAction(opts.action, opts.actionArgs);
  const ws = new WebSocket(opts.url);
  let done = false;

  const timer = setTimeout(() => {
    if (!done) {
      done = true;
      console.error(JSON.stringify({ error: 'Timeout after 30s' }));
      ws.close();
      process.exit(1);
    }
  }, TIMEOUT_MS);

  function finish(data) {
    if (done) return;
    done = true;
    clearTimeout(timer);

    // For screenshots, save to file if path arg was given
    if (opts.action === 'screenshot' && data && data.data) {
      const filePath = opts.actionArgs[0];
      if (filePath) {
        const fs = require('fs');
        const buf = Buffer.from(data.data, 'base64');
        fs.writeFileSync(filePath, buf);
        console.log(JSON.stringify({ ok: true, path: filePath, bytes: buf.length }));
      } else {
        console.log(JSON.stringify({ ok: true, length: data.data.length, note: 'Pass a file path as arg to save' }));
      }
    } else {
      console.log(JSON.stringify(data));
    }
    ws.close();
  }

  ws.on('open', () => {
    ws.send(JSON.stringify({ type: 'auth', token: opts.token, agent_id: opts.agentId }));
  });

  ws.on('message', (raw) => {
    let msg;
    try { msg = JSON.parse(raw.toString()); } catch { return; }

    // Handle pings
    if (msg.type === 'ping') {
      ws.send(JSON.stringify({ type: 'pong' }));
      return;
    }

    // Auth response — relay sends { type: 'result', action: 'auth', ok: true }
    if (msg.type === 'auth_success' || msg.type === 'welcome' ||
        (msg.type === 'result' && msg.action === 'auth' && msg.ok)) {
      ws.send(JSON.stringify(actionMsg));
      return;
    }

    if (msg.type === 'auth_error' || msg.type === 'error' ||
        (msg.type === 'result' && msg.action === 'auth' && !msg.ok)) {
      finish({ error: msg.message || msg.error || 'Auth failed' });
      return;
    }

    // Action response (non-auth results)
    if (msg.type === 'result' || msg.type === 'action_result' || msg.type === 'response') {
      finish(msg);
      return;
    }

    // Fallback: any other message with content could be the response
    if (msg.type && msg.type !== 'ping' && msg.type !== 'pong') {
      finish(msg);
    }
  });

  ws.on('error', (err) => {
    if (!done) {
      done = true;
      clearTimeout(timer);
      console.error(JSON.stringify({ error: err.message }));
      process.exit(1);
    }
  });

  ws.on('close', () => {
    if (!done) {
      done = true;
      clearTimeout(timer);
      process.exit(0);
    }
  });
}

run();
