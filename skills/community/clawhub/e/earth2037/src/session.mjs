import WebSocket from 'ws';
import { gunzipSync } from 'node:zlib';
import { format } from 'node:util';
import { GatewayError, checkUrl, requireValue } from './common.mjs';
import { assertGameCommandAllowed } from './command-policy.mjs';

/** A single ordered socket, with explicit connection and no automatic reconnect/replay. */
export class GameSession {
  constructor(config) { this.config = config; this.counter = 0; this.events = []; this.eventCursor = 0; this.pongs = []; this.chunks = new Map(); }
  async connect(ticket, identity) {
    requireValue(ticket?.server_id === identity.server_id && ticket?.role_id === identity.role_id,
      'ticket_binding_mismatch', 'Ticket does not match selected server/role');
    requireValue(ticket.expires_at > Date.now()/1000 + 3 && ticket.protocol_version === 2, 'invalid_ticket', 'Expired ticket or unsupported protocol');
    const url = checkUrl(ticket.ws_url, 'wss:', this.config.allowLocal);
    await this.close(); this.identity = null; this.events = []; this.eventCursor = 0; this.counter = 0;
    const socket = this.socket = new WebSocket(url, { maxPayload: 8 * 1024 * 1024, followRedirects: false, handshakeTimeout: this.config.timeoutMs });
    const hello = new Promise((resolve, reject) => {
      this.hello = { resolve, reject };
      this.helloTimer = setTimeout(() => reject(new GatewayError('hello_timeout', 'No protocol-v2 hello received')), this.config.timeoutMs);
    });
    socket.on('message', bytes => this.receive(bytes));
    socket.on('error', () => { if (this.socket === socket) this.fail('socket_error'); });
    socket.on('close', () => { if (this.socket === socket) this.fail('disconnected'); });
    try {
      const greeting = await hello;
      requireValue(greeting.protocolVersion === 2 || greeting.data?.protocolVersion === 2, 'protocol_mismatch', 'Server did not advertise protocol v2');
      const response = await this.command('login_ticket', [ticket.ticket], true);
      const frame = response.frames.find(f => f.cmd === 'login_ticket' && f.ok === true);
      let data = frame?.data; if (typeof data === 'string') data = JSON.parse(data);
      requireValue(data?.account_id === identity.account_id && data?.server_id === identity.server_id && data?.role_id === identity.role_id,
        'login_binding_mismatch', 'Server login identity did not match Account Center');
      this.identity = { ...identity, local_user_id: data.local_user_id };
      this.heartbeat = setInterval(() => { if (!this.pending && !this.pongs.length) this.ping().catch(() => {}); }, 15000);
      this.heartbeat.unref();
      return { connected: true, identity: this.identity, exclusiveRoleSession: true };
    } catch (e) { await this.close(); throw e; }
    finally { clearTimeout(this.helloTimer); this.hello = null; }
  }
  receive(bytes) {
    let message;
    try { message = this.decode(JSON.parse(bytes.toString())); } catch { this.fail('invalid_game_frame'); this.socket?.terminate(); return; }
    if (!message) return;
    if (message.cmd === 'hello') { this.hello?.resolve(message); return; }
    if (message.cmd === 'ping') { this.socket?.send(JSON.stringify({ cmd: 'pong' })); return; }
    if (message.cmd === 'pong') { const p = this.pongs.shift(); if (p) { clearTimeout(p.timer); p.resolve(message); } return; }
    if (message.cmd === 'forced_logout') {
      this.event(message); this.fail('session_replaced'); this.socket?.close(); return;
    }
    const p = this.pending;
    if (p && message.id === p.id) {
      p.frames.push(message);
      // The server serializes commands per socket. A ping sent after the first
      // correlated response drains all frames from that command before its pong.
      if (!p.barrier) {
        p.barrier = true;
        this.ping().then(() => {
          if (this.pending !== p) return;
          clearTimeout(p.timer); this.pending = null;
          const errors = p.frames.filter(f => f.ok === false || f.cmd === 'err' || f.cmd === 'cmderr');
          const confirmed = p.frames.some(f => f.ok === true);
          p.resolve({ status: errors.length ? 'rejected' : confirmed ? 'confirmed' : 'unknown', ok: !errors.length && confirmed,
            requestId: p.id, command: p.cmd, frames: p.frames });
        }).catch(() => this.fail('response_barrier_failed'));
      }
    } else this.event(message);
  }
  decode(message) {
    if (message.chunked) {
      const { idx, total } = message.chunked;
      if (!Number.isInteger(idx) || !Number.isInteger(total) || total < 1 || total > 256 || idx < 0 || idx >= total || typeof message.data !== 'string') throw new Error('Invalid chunk');
      const id = message.id;
      const key = id == null ? format('push:%s', String(message.cmd)) : format('%s:%s', String(id), String(message.cmd));
      let group = this.chunks.get(key);
      if (!group) {
        if (this.chunks.size >= 32) throw new Error('Too many incomplete payloads');
        group = { parts: new Map(), total, bytes: 0, started: Date.now() }; this.chunks.set(key, group);
      }
      if (group.total !== total || Date.now() - group.started > this.config.timeoutMs) throw new Error('Invalid chunk sequence');
      if (!group.parts.has(idx)) { group.parts.set(idx, message.data); group.bytes += message.data.length; }
      if (group.bytes > 16 * 1024 * 1024) throw new Error('Payload too large');
      if (group.parts.size !== total) return null;
      message = { ...message, data: Array.from({ length: total }, (_, i) => group.parts.get(i)).join('') };
      delete message.chunked; this.chunks.delete(key);
    }
    if (message.gzip) {
      const text = gunzipSync(Buffer.from(message.data, 'base64'), { maxOutputLength: 16 * 1024 * 1024 }).toString('utf8');
      try { message.data = JSON.parse(text); } catch { message.data = text; }
      message.gzip = false;
    }
    return message;
  }
  event(frame) {
    this.events.push({ cursor: ++this.eventCursor, frame });
    if (this.events.length > 256) this.events.shift();
  }
  readEvents(after = 0) { return { events: this.events.filter(e => e.cursor > after), cursor: this.eventCursor,
    truncated: this.events.length > 0 && after < this.events[0].cursor - 1 }; }
  ping() {
    return new Promise((resolve, reject) => {
      const p = { resolve, reject, timer: setTimeout(() => { this.fail('heartbeat_timeout'); this.socket?.terminate(); }, this.config.timeoutMs) };
      this.pongs.push(p);
      if (this.socket?.readyState !== WebSocket.OPEN) { this.fail('disconnected'); return; }
      this.socket.send(JSON.stringify({ cmd: 'ping' }));
    });
  }
  command(cmd, args, ack) {
    // Enforce the same boundary at the final send path, including future aliases.
    assertGameCommandAllowed(cmd);
    requireValue(this.socket?.readyState === WebSocket.OPEN, 'not_connected', 'Connect to a role before sending game commands');
    requireValue(!this.pending, 'command_in_flight', 'Commands must be serialized');
    const id = ++this.counter;
    return new Promise((resolve, reject) => {
      const p = this.pending = { id, cmd, resolve, reject, frames: [], barrier: false,
        timer: setTimeout(() => { this.fail('command_timeout'); this.socket?.terminate(); }, this.config.timeoutMs) };
      this.socket.send(JSON.stringify({ id, cmd, args, ack }), error => { if (error && this.pending === p) this.fail('send_failed'); });
    });
  }
  fail(code) {
    clearTimeout(this.helloTimer); this.hello?.reject(new GatewayError(code, 'Game connection ended before authentication')); this.hello = null;
    clearInterval(this.heartbeat); this.identity = null; this.chunks.clear();
    if (this.pending) {
      const p = this.pending; this.pending = null; clearTimeout(p.timer);
      p.reject(new GatewayError(code, 'Command outcome is unknown; do not repeat a write with a new operationKey.', { status: 'unknown', requestId: p.id, frames: p.frames }));
    }
    for (const p of this.pongs.splice(0)) { clearTimeout(p.timer); p.reject(new GatewayError(code, 'Connection interrupted')); }
  }
  async close() {
    clearInterval(this.heartbeat); this.fail('disconnected');
    const socket = this.socket; this.socket = null;
    if (socket) { socket.removeAllListeners('message'); socket.terminate(); }
  }
}
