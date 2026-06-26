import express from 'express';
import cors from 'cors';
import { readFileSync, existsSync, watch } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { networkInterfaces } from 'os';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Resolve character.json the same way _paths.mjs does:
// workspace/claw-rpg/character.json  (survives skill reinstalls)
function findWorkspace() {
  const candidates = [
    join(process.env.USERPROFILE || '', '.openclaw', 'workspace'),
    join(process.env.HOME        || '', '.openclaw', 'workspace'),
  ];
  for (const p of candidates) if (existsSync(p)) return p;
  return candidates[0];
}
const WORKSPACE      = process.env.OPENCLAW_WORKSPACE || findWorkspace();
const CHARACTER_FILE = join(WORKSPACE, 'claw-rpg', 'character.json');
const app = express();

app.use(cors());
app.use(express.json());

// ── SSE 客戶端管理 ───────────────────────────────────────────
const clients = new Set();

function readChar() {
  if (!existsSync(CHARACTER_FILE)) return null;
  try { return JSON.parse(readFileSync(CHARACTER_FILE, 'utf8')); }
  catch { return null; }
}

function broadcast(data) {
  const msg = `data: ${JSON.stringify(data)}\n\n`;
  for (const res of clients) {
    try { res.write(msg); }
    catch { clients.delete(res); }
  }
}

// 監聽 character.json 變化，debounce 200ms 避免重複觸發
let debounceTimer = null;
if (existsSync(CHARACTER_FILE)) {
  watch(CHARACTER_FILE, () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const char = readChar();
      if (char) broadcast(char);
    }, 200);
  });
}

// ── API ──────────────────────────────────────────────────────
app.get('/api/character', (_req, res) => {
  const char = readChar();
  if (!char) return res.status(404).json({ error: 'No character found. Run: node scripts/init.mjs' });
  res.json(char);
});

// SSE 端點：客戶端訂閱實時更新
app.get('/api/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.flushHeaders();

  // 立即推送當前數據
  const char = readChar();
  if (char) res.write(`data: ${JSON.stringify(char)}\n\n`);

  // 加入廣播列表
  clients.add(res);

  // 心跳（每 25s 防止連接超時）
  const heartbeat = setInterval(() => {
    try { res.write(': ping\n\n'); }
    catch { clearInterval(heartbeat); clients.delete(res); }
  }, 25000);

  req.on('close', () => {
    clearInterval(heartbeat);
    clients.delete(res);
  });
});

app.get('/api/arena', (_req, res) => {
  const file = join(ROOT, 'arena-history.json');
  res.json(existsSync(file) ? JSON.parse(readFileSync(file, 'utf8')) : []);
});

app.use(express.static(join(__dirname, 'dist')));
app.get('/{*path}', (_req, res) => {
  const idx = join(__dirname, 'dist', 'index.html');
  if (existsSync(idx)) return res.sendFile(idx);
  res.send('<pre>Run: npm run build\nThen: npm start</pre>');
});

// Detect LAN IP dynamically at startup
function getLanIp() {
  try {
    for (const iface of Object.values(networkInterfaces())) {
      for (const addr of iface) {
        if (addr.family === 'IPv4' && !addr.internal) return addr.address;
      }
    }
  } catch {}
  return 'localhost';
}

const PORT = process.env.PORT || 3500;
app.listen(PORT, '0.0.0.0', () => {
  const lanIp = getLanIp();
  console.log(`\n🦞 Claw RPG Dashboard → http://localhost:${PORT}`);
  console.log(`   LAN access       → http://${lanIp}:${PORT}`);
  console.log(`   Character file   → ${CHARACTER_FILE}\n`);
});
