import http from 'node:http';
import WebSocket from 'ws';
const PORT = 9333;
const get = p => new Promise((res, rej) => {
  http.get({ host: '127.0.0.1', port: PORT, path: p }, r => { let d = ''; r.on('data', c => d += c); r.on('end', () => res(JSON.parse(d))); }).on('error', rej);
});
const v = await get('/json/version');
const ws = new WebSocket(v.webSocketDebuggerUrl, { perMessageDeflate: false });
await new Promise(r => ws.once('open', r));
ws.send(JSON.stringify({ id: 1, method: 'Browser.close', params: {} }));
setTimeout(() => process.exit(0), 1500);
