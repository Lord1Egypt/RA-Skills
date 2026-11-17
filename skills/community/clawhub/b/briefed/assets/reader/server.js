const express = require('express');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = Number(process.env.BRIEFED_PORT) || 3001;
// Loopback only by default. Two ways to read on another device, both need BRIEFED_TOKEN:
//  - Recommended: keep the loopback bind and put an HTTPS proxy in front
//    (e.g. `tailscale serve`), listing its hostname in BRIEFED_ALLOWED_HOSTS.
//  - Bind BRIEFED_HOST to a Tailscale IP (encrypted by WireGuard), or to any
//    other address with BRIEFED_ALLOW_PLAIN_HTTP=1 (token sent unencrypted).
const HOST = process.env.BRIEFED_HOST || '127.0.0.1';
const TOKEN = process.env.BRIEFED_TOKEN || '';
const ALLOWED_HOSTS = (process.env.BRIEFED_ALLOWED_HOSTS || '')
  .split(',').map(h => h.trim().toLowerCase()).filter(Boolean);
const ALLOW_PLAIN_HTTP = process.env.BRIEFED_ALLOW_PLAIN_HTTP === '1';
const LOOPBACK_HOSTS = ['127.0.0.1', 'localhost', '::1'];
const IS_LOOPBACK = LOOPBACK_HOSTS.includes(HOST);
const AUTH_COOKIE = 'briefed_token';

function fail(message) {
  console.error(message);
  process.exit(1);
}

if ((!IS_LOOPBACK || ALLOWED_HOSTS.length) && TOKEN.length < 16) {
  fail(
    'Remote access requires authentication.\n' +
    'Set BRIEFED_TOKEN to a random secret of at least 16 characters, e.g.:\n' +
    '  export BRIEFED_TOKEN=$(openssl rand -hex 24)'
  );
}

if (!IS_LOOPBACK && !isTailscaleAddress(HOST) && !ALLOW_PLAIN_HTTP) {
  fail(
    `Refusing to serve plain HTTP on ${HOST}: the token and your email would be sent unencrypted.\n` +
    'Recommended: keep the default 127.0.0.1 bind and use `tailscale serve` for HTTPS (see SKILL.md).\n' +
    'Or bind to your Tailscale IP, or set BRIEFED_ALLOW_PLAIN_HTTP=1 to accept the risk on a trusted network.'
  );
}

// Behind a local HTTPS proxy (tailscale serve), trust its X-Forwarded-Proto
// so req.secure is true and the auth cookie is marked Secure.
app.set('trust proxy', 'loopback');

// Paths
const STORIES_FILE = path.join(__dirname, '..', 'newsletter-today.json');
const INTERESTS_FILE = path.join(__dirname, '..', 'newsletter-interests.json');
const READING_LIST_FILE = path.join(__dirname, '..', 'reading-list.md');
const NOTES_FILE = path.join(__dirname, '..', 'newsletter-notes.json');

// Security headers. The email viewer is a srcdoc iframe, which inherits this
// policy; it adds its own stricter policy that blocks remote images by default.
app.use((req, res, next) => {
  res.set({
    'Content-Security-Policy': [
      "default-src 'self'",
      "script-src 'self'",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https: http:",
      "frame-src 'self'",
      "frame-ancestors 'none'",
      "base-uri 'none'",
      "form-action 'none'",
    ].join('; '),
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'no-referrer',
  });
  next();
});

// Reject requests whose Host header isn't this server (blocks DNS rebinding).
app.use((req, res, next) => {
  if (!IS_LOOPBACK) return next(); // token auth covers remote mode
  const host = (req.hostname || '').replace(/^\[|\]$/g, '').toLowerCase();
  if (LOOPBACK_HOSTS.includes(host) || ALLOWED_HOSTS.includes(host)) return next();
  res.status(403).send('Forbidden');
});

// A proxied request on a loopback bind must still authenticate, even if the
// proxy rewrites Host to 127.0.0.1.
app.use((req, res, next) => {
  const proxied = req.get('x-forwarded-for') || req.get('x-forwarded-host') || req.get('forwarded');
  if (IS_LOOPBACK && proxied && !TOKEN) {
    return res.status(403).send('Proxied access requires BRIEFED_TOKEN.');
  }
  next();
});

// Token auth (required in remote mode, optional locally). Visit /?token=...
// once; an HttpOnly cookie is set and the token is stripped from the URL.
app.use((req, res, next) => {
  if (!TOKEN) return next();

  if (typeof req.query.token === 'string') {
    if (!tokenMatches(req.query.token)) return res.status(401).send('Invalid token');
    res.cookie(AUTH_COOKIE, TOKEN, {
      httpOnly: true,
      sameSite: 'lax',
      secure: req.secure,
      maxAge: 1000 * 60 * 60 * 24 * 90,
    });
    return res.redirect(req.path);
  }

  const header = req.get('authorization') || '';
  const bearer = header.startsWith('Bearer ') ? header.slice(7) : '';
  if (tokenMatches(readCookie(req, AUTH_COOKIE)) || tokenMatches(bearer)) return next();

  res.status(401).send('Unauthorized — open the reader link that includes ?token=');
});

app.use(express.json({ limit: '64kb' }));
app.use(express.static(path.join(__dirname, 'public')));

// GET / — serve SPA
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// GET /api/today — return today's stories
app.get('/api/today', (req, res) => {
  try {
    if (!fs.existsSync(STORIES_FILE)) {
      return res.status(404).json({ error: 'No stories file found. Run the newsletter digest first.' });
    }
    const data = JSON.parse(fs.readFileSync(STORIES_FILE, 'utf8'));
    // Strip bodies from list response — fetched on demand via /api/story/:id
    const light = { ...data, stories: data.stories.map(s => ({ ...s, hasBody: !!(s.body), body: undefined })) };
    res.json(light);
  } catch (err) {
    console.error('Error reading stories:', err);
    res.status(500).json({ error: 'Failed to read stories file.' });
  }
});

// GET /api/story/:id — fetch single story body on demand
app.get('/api/story/:id', (req, res) => {
  try {
    if (!fs.existsSync(STORIES_FILE)) {
      return res.status(404).json({ error: 'No stories file.' });
    }
    const data = JSON.parse(fs.readFileSync(STORIES_FILE, 'utf8'));
    const story = data.stories.find(s => s.id === req.params.id);
    if (!story) return res.status(404).json({ error: 'Story not found.' });
    res.json({ id: story.id, body: story.body || '' });
  } catch (err) {
    res.status(500).json({ error: 'Failed to read story.' });
  }
});

// POST /api/vote — record up/down vote
app.post('/api/vote', (req, res) => {
  const { storyId, vote } = req.body || {};
  if (!storyId || !['up', 'down', 'open'].includes(vote)) {
    return res.status(400).json({ error: 'storyId and vote ("up", "down", or "open") required.' });
  }

  try {
    const interests = readInterests();

    if (vote === 'open') {
      // Soft signal — cap at 1 per story per session to avoid noise
      const alreadyOpened = interests.signals.some(
        s => s.storyId === storyId && s.vote === 'open'
      );
      if (alreadyOpened) return res.json({ ok: true, storyId, vote, skipped: true });
    } else {
      // Hard vote — replace any previous up/down for this story
      interests.signals = interests.signals.filter(
        s => !(s.storyId === storyId && ['up', 'down'].includes(s.vote))
      );
    }

    interests.signals.push({ storyId, vote, ts: new Date().toISOString() });
    writeInterests(interests);
    res.json({ ok: true, storyId, vote });
  } catch (err) {
    console.error('Error writing vote:', err);
    res.status(500).json({ error: 'Failed to record vote.' });
  }
});

// POST /api/save — save to reading list
app.post('/api/save', (req, res) => {
  const { storyId, note } = req.body || {};
  if (!storyId) {
    return res.status(400).json({ error: 'storyId required.' });
  }

  try {
    // Find story details
    let story = null;
    if (fs.existsSync(STORIES_FILE)) {
      const data = JSON.parse(fs.readFileSync(STORIES_FILE, 'utf8'));
      story = data.stories.find(s => s.id === storyId);
    }

    // Append to reading-list.md
    const ts = new Date().toISOString();
    const date = ts.slice(0, 10);
    const safeHeadline = escapeMarkdown(story ? story.headline : storyId);
    const safeSource = escapeMarkdown(story ? story.source : 'Unknown');
    const safeId = escapeMarkdown(storyId);
    const safeNote = note ? escapeMarkdown(note) : '';
    const safeGmailUrl = sanitizeUrl(story?.gmailUrl);

    let entry = `\n## ${safeHeadline}\n`;
    entry += `- **Date saved:** ${date}\n`;
    entry += `- **Source:** ${safeSource}\n`;
    if (safeGmailUrl) entry += `- **Link:** [Open in Gmail](${safeGmailUrl})\n`;
    if (safeNote) entry += `- **Note:** ${safeNote}\n`;
    entry += `- **ID:** ${safeId}\n`;

    fs.appendFileSync(READING_LIST_FILE, entry, { mode: 0o600 });

    // Also add a save signal to interests
    const interests = readInterests();
    interests.signals = interests.signals.filter(s => !(s.storyId === storyId && s.vote === 'save'));
    interests.signals.push({ storyId, vote: 'save', ts, note: note || null });
    writeInterests(interests);

    res.json({ ok: true, storyId });
  } catch (err) {
    console.error('Error saving story:', err);
    res.status(500).json({ error: 'Failed to save story.' });
  }
});

// GET /api/notes — return all saved notes
app.get('/api/notes', (req, res) => {
  try {
    const notes = readNotes();
    res.json(notes);
  } catch (err) {
    res.status(500).json({ error: 'Failed to read notes.' });
  }
});

// POST /api/note — save or update a note for a story
app.post('/api/note', (req, res) => {
  const { storyId, note } = req.body || {};
  if (!storyId) return res.status(400).json({ error: 'storyId required.' });

  try {
    const notes = readNotes();
    if (note && note.trim()) {
      notes[storyId] = { note: note.trim(), ts: new Date().toISOString() };
    } else {
      delete notes[storyId]; // empty note = delete
    }
    writeNotes(notes);
    res.json({ ok: true, storyId });
  } catch (err) {
    console.error('Error saving note:', err);
    res.status(500).json({ error: 'Failed to save note.' });
  }
});

// Helpers
// Tailscale assigns 100.64.0.0/10 and fd7a:115c:a1e0::/48; that traffic is WireGuard-encrypted.
function isTailscaleAddress(host) {
  const v4 = host.match(/^100\.(\d+)\.\d+\.\d+$/);
  if (v4) return Number(v4[1]) >= 64 && Number(v4[1]) <= 127;
  return /^fd7a:115c:a1e0:/i.test(host);
}

function tokenMatches(candidate) {
  if (!TOKEN || typeof candidate !== 'string') return false;
  const a = crypto.createHash('sha256').update(candidate).digest();
  const b = crypto.createHash('sha256').update(TOKEN).digest();
  return crypto.timingSafeEqual(a, b);
}

function readCookie(req, name) {
  const header = req.get('cookie') || '';
  for (const part of header.split(';')) {
    const [k, ...v] = part.trim().split('=');
    if (k === name) {
      try { return decodeURIComponent(v.join('=')); } catch { return ''; }
    }
  }
  return '';
}

// Email-derived data is private: write owner-only (0600).
function writePrivate(file, contents) {
  fs.writeFileSync(file, contents, { mode: 0o600 });
  fs.chmodSync(file, 0o600);
}

function readNotes() {
  if (!fs.existsSync(NOTES_FILE)) return {};
  return JSON.parse(fs.readFileSync(NOTES_FILE, 'utf8'));
}

function writeNotes(data) {
  writePrivate(NOTES_FILE, JSON.stringify(data, null, 2));
}

function readInterests() {
  if (!fs.existsSync(INTERESTS_FILE)) {
    return { version: 1, topics: {}, signals: [], sources: {} };
  }
  return JSON.parse(fs.readFileSync(INTERESTS_FILE, 'utf8'));
}

function writeInterests(data) {
  writePrivate(INTERESTS_FILE, JSON.stringify(data, null, 2));
}

function escapeMarkdown(input) {
  return String(input || '')
    .replace(/\\/g, '\\\\')
    .replace(/([`*_{}[\]()#+\-.!|>])/g, '\\$1')
    .replace(/[\r\n]+/g, ' ')
    .trim();
}

function sanitizeUrl(url) {
  if (!url) return null;
  try {
    const u = new URL(String(url));
    if (u.protocol !== 'https:' && u.protocol !== 'http:') return null;
    return u.toString();
  } catch {
    return null;
  }
}

// Start server
app.listen(PORT, HOST, () => {
  const shownHost = HOST.includes(':') ? `[${HOST}]` : HOST;
  console.log(`📰 Briefed reader running at http://${shownHost}:${PORT}`);
  if (TOKEN) console.log('   Auth: token required (open the reader once with ?token=<BRIEFED_TOKEN>)');
  if (ALLOWED_HOSTS.length) console.log(`   Proxy hosts: ${ALLOWED_HOSTS.join(', ')}`);
  if (!IS_LOOPBACK && ALLOW_PLAIN_HTTP && !isTailscaleAddress(HOST)) {
    console.warn('   ⚠️  Plain HTTP on a network address: the token and email content are not encrypted.');
  }
  console.log(`   Stories: ${STORIES_FILE}`);
  console.log(`   Interests: ${INTERESTS_FILE}`);
});
