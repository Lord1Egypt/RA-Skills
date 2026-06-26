/**
 * WebSocket 通信 Worker — 负责 WebSocket 连接 + PCM 音频上行
 * 参考 NuwaAI demo 的 human-socket-worker.js
 */
const sockets = { main: null };
const pcmQueues = { main: [] };
const MAX_PCM_QUEUED = 5;
const MAX_WS_BUFFERED = 384 * 1024;
let flushTimer = null;

function tryFlushPcm(conn) {
  const ws = sockets[conn];
  const q = pcmQueues[conn];
  if (!ws || ws.readyState !== WebSocket.OPEN) { q.length = 0; return; }
  while (q.length > 0 && ws.bufferedAmount < MAX_WS_BUFFERED) {
    ws.send(q.shift());
  }
}

function ensureFlushTimer() {
  if (flushTimer != null) return;
  flushTimer = setInterval(() => tryFlushPcm('main'), 100);
}

self.onmessage = function (e) {
  const d = e.data;
  if (!d || !d.cmd) return;

  switch (d.cmd) {
    case 'connect': {
      const prev = sockets.main;
      if (prev) { try { prev.close(); } catch (_) {} }
      pcmQueues.main.length = 0;
      const ws = new WebSocket(d.url);
      sockets.main = ws;
      ws.binaryType = 'arraybuffer';
      ws.onopen = () => self.postMessage({ evt: 'open' });
      ws.onmessage = (ev) => {
        if (typeof ev.data === 'string') self.postMessage({ evt: 'message', data: ev.data });
      };
      ws.onclose = () => { sockets.main = null; pcmQueues.main.length = 0; self.postMessage({ evt: 'close' }); };
      ws.onerror = () => self.postMessage({ evt: 'error' });
      break;
    }
    case 'close': {
      const ws = sockets.main;
      if (ws) { try { ws.close(); } catch (_) {} sockets.main = null; }
      pcmQueues.main.length = 0;
      break;
    }
    case 'sendJson': {
      const ws = sockets.main;
      if (ws && ws.readyState === WebSocket.OPEN) ws.send(d.text);
      break;
    }
    case 'sendPcm': {
      ensureFlushTimer();
      while (pcmQueues.main.length >= MAX_PCM_QUEUED) pcmQueues.main.shift();
      pcmQueues.main.push(d.buffer);
      tryFlushPcm('main');
      break;
    }
    case 'clearPcm':
      pcmQueues.main.length = 0;
      break;
  }
};
