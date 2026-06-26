const Imap = require('imap');
const { simpleParser } = require('mailparser');
const fs = require('fs');
const path = require('path');

const CACHE_DIR = path.join(process.cwd(), '.cache');
const CACHE_FILE = path.join(CACHE_DIR, 'inbox.json');
const CACHE_META_FILE = path.join(CACHE_DIR, 'meta.json');

function ensureCacheDir() {
  if (!fs.existsSync(CACHE_DIR)) {
    fs.mkdirSync(CACHE_DIR, { recursive: true });
  }
}

function buildImapConfig() {
  const user = process.env.IMAP_USER;
  const password = process.env.IMAP_PASS;
  const host = process.env.IMAP_HOST;
  const port = parseInt(process.env.IMAP_PORT || '993');
  const tls = process.env.IMAP_TLS !== 'false';
  const rejectUnauthorized = process.env.IMAP_REJECT_UNAUTHORIZED !== 'false';
  return { user, password, host, port, tls, rejectUnauthorized };
}

function connect() {
  const config = buildImapConfig();
  return new Promise((resolve, reject) => {
    const imap = new Imap(config);
    imap.once('ready', () => resolve(imap));
    imap.once('error', err => reject(err));
    imap.connect();
  });
}

function isUnread(flags = []) {
  return !flags.includes('\\Seen');
}

function formatFlags(flags = []) {
  const parts = [];
  if (!flags.includes('\\Seen')) parts.push('unread');
  if (flags.includes('\\Flagged')) parts.push('flagged');
  if (flags.includes('\\Answered')) parts.push('replied');
  return parts.length ? '`' + parts.join(', ') + '`' : '';
}

function parseAddress(addr) {
  if (!addr) return '';
  if (typeof addr === 'string') return addr;
  if (addr.value && addr.value[0]) {
    return addr.value[0].name ? `${addr.value[0].name} <${addr.value[0].address}>` : addr.value[0].address;
  }
  return String(addr);
}

function decodeSubject(subject) {
  if (!subject) return '';
  try {
    const encodedWords = subject.match(/=\?([^?]+)\?([BQ])\?([^?]*)\?=/gi) || [];
    for (const ew of encodedWords) {
      const match = ew.match(/=\?([^?]+)\?([BQ])\?([^?]*)\?=/i);
      if (!match) continue;
      const [, charset, encoding, text] = match;
      let decoded;
      if (encoding.toUpperCase() === 'B') {
        decoded = Buffer.from(text, 'base64').toString(charset);
      } else {
        decoded = Buffer.from(text, 'quoted-printable').toString(charset);
      }
      subject = subject.replace(ew, decoded);
    }
  } catch {}
  return subject;
}

function formatDate(date) {
  if (!date) return '';
  try {
    const d = new Date(date);
    const now = new Date();
    const diffMs = now - d;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  } catch {
    return String(date);
  }
}

function getCachedMessages() {
  ensureCacheDir();
  if (!fs.existsSync(CACHE_FILE)) return { messages: [], syncedAt: null };
  try {
    // Read from local cache only - no network activity
    const data = fs.readFileSync(CACHE_FILE, 'utf8');
    const cached = JSON.parse(data);
    if (Array.isArray(cached)) return { messages: cached, syncedAt: null };
    return cached;
  } catch {
    return { messages: [], syncedAt: null };
  }
}

function saveCachedMessages(messages) {
  ensureCacheDir();
  const data = { messages, syncedAt: new Date().toISOString() };
  fs.writeFileSync(CACHE_FILE, JSON.stringify(data, null, 2));
}

async function check(options, positional) {
  const { messages, syncedAt } = getCachedMessages();
  const all = options.all || options.limit;
  const limit = parseInt(options.limit || '0') || Infinity;

  const syncTime = syncedAt ? new Date(syncedAt).toLocaleString() : 'never';

  if (all) {
    const sorted = [...messages].sort((a, b) => new Date(b.date) - new Date(a.date));
    const toShow = sorted.slice(0, limit);

    console.log('\n## Inbox\n');
    console.log(`**${messages.length}** messages · synced ${syncTime}\n`);

    if (toShow.length > 0) {
      console.log('| UID | 📎 | Flags | Subject | From | Date |');
      console.log('|-----|-----|-------|---------|------|------|');
      toShow.forEach(m => {
        const attach = m.hasAttachments ? '📎' : '';
        const subject = decodeSubject(m.subject || '').replace(/\|/g, '\\|');
        const from = parseAddress(m.from || '').replace(/\|/g, '\\|');
        const date = formatDate(m.date);
        const flags = formatFlags(m.flags);
        console.log(`| ${m.uid} | ${attach} | ${flags} | ${subject} | ${from} | ${date} |`);
      });
      console.log();
    }
  } else {
    const unread = messages.filter(m => isUnread(m.flags));
    const unreadSorted = [...unread].sort((a, b) => new Date(b.date) - new Date(a.date));
    const toShow = unreadSorted.slice(0, limit);

    console.log('\n## Unread\n');
    console.log(`**${unread.length}** messages · synced ${syncTime}\n`);

    if (toShow.length > 0) {
      console.log('| UID | 📎 | Flags | Subject | From | Date |');
      console.log('|-----|-----|-------|---------|------|------|');
      toShow.forEach(m => {
        const attach = m.hasAttachments ? '📎' : '';
        const subject = decodeSubject(m.subject || '').replace(/\|/g, '\\|');
        const from = parseAddress(m.from || '').replace(/\|/g, '\\|');
        const date = formatDate(m.date);
        console.log(`| ${m.uid} | ${attach} | ${formatFlags(m.flags)} | ${subject} | ${from} | ${date} |`);
      });
      console.log();
    }
  }
}

async function sync(options, positional) {
  const imap = await connect();
  const startTime = Date.now();

  try {
    await new Promise((resolve, reject) => {
      imap.openBox('INBOX', true, err => {
        if (err) reject(err);
        else resolve();
      });
    });

    const messages = await new Promise((resolve, reject) => {
      imap.search(['ALL'], (err, results) => err ? reject(err) : resolve(results));
    });
    const cachedData = getCachedMessages();
    const cached = cachedData.messages;
    const cachedUids = new Set(cached.map(m => m.uid));
    const newUids = messages.filter(uid => !cachedUids.has(uid));

    console.log('\n## Sync\n');
    console.log(`Found ${messages.length} messages in INBOX...`);

    const newMessages = [];
    for (const uid of newUids) {
      try {
        const msg = await fetchSingleMessage(imap, uid);
        newMessages.push(msg);
      } catch {}
    }

    const allMessages = [...newMessages, ...cached].sort((a, b) => b.uid - a.uid);
    saveCachedMessages(allMessages);

    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
    const unseen = allMessages.filter(m => isUnread(m.flags));

    console.log(`**${newMessages.length} new** · synced ${elapsed}s\n`);

    if (unseen.length > 0) {
      console.log('### Unread (' + unseen.length + ')\n');
      console.log('| UID | 📎 | Flags | Subject | From | Date |');
      console.log('|-----|-----|-------|---------|------|------|');
      unseen.slice(0, 20).forEach(m => {
        const attach = m.hasAttachments ? '📎' : '';
        const subject = decodeSubject(m.subject || '').replace(/\|/g, '\\|');
        const from = parseAddress(m.from || '').replace(/\|/g, '\\|');
        const date = formatDate(m.date);
        console.log(`| ${m.uid} | ${attach} | ${formatFlags(m.flags)} | ${subject} | ${from} | ${date} |`);
      });
      console.log();
    }
  } finally {
    imap.end();
  }
}

async function fetchSingleMessage(imap, uid) {
  return new Promise((resolve, reject) => {
    let msg = { uid, flags: [], date: null, from: '', subject: '', hasAttachments: false };
    let struct = null;
    let headerDone = false;
    let attrsDone = false;

    // Fetch headers for from/subject
    const f1 = imap.fetch(uid, { bodies: 'HEADER.FIELDS (FROM SUBJECT DATE)', struct: true });
    f1.on('message', (msgStream) => {
      msgStream.once('attributes', attrs => {
        msg.flags = attrs.flags || [];
        msg.date = attrs.date;
        struct = attrs.struct;
        attrsDone = true;
        if (attrsDone && headerDone) {
          msg.hasAttachments = checkAttachments(struct);
          resolve(msg);
        }
      });
      msgStream.on('body', (stream) => {
        let buffer = '';
        stream.on('data', chunk => buffer += chunk.toString('utf8'));
        stream.once('end', () => {
          const header = require('imap').parseHeader(buffer);
          msg.from = parseAddress(header.from ? header.from[0] : '');
          msg.subject = decodeSubject(header.subject ? header.subject[0] : '');
          if (header.date) msg.date = new Date(header.date[0]);
          headerDone = true;
          if (attrsDone && headerDone) {
            msg.hasAttachments = checkAttachments(struct);
            resolve(msg);
          }
        });
      });
    });
    f1.once('error', reject);
  });
}

function checkAttachments(struct) {
  if (!struct) return false;
  // Handle array of parts (top-level multipart)
  if (Array.isArray(struct)) {
    return struct.some(child => checkAttachments(child));
  }
  // Handle multipart containers
  if (struct.type === 'multipart' || struct.type === 'mixed' || struct.type === 'alternative') {
    if (struct.children) {
      return struct.children.some(child => checkAttachments(child));
    }
    return false;
  }
  // Check for explicit attachment disposition
  if (struct.disposition && struct.disposition.type === 'attachment') return true;
  if (struct.dispositionParameters && struct.dispositionParameters.filename) return true;
  // Check for inline attachments with filename
  if (struct.params && struct.params.name) return true;
  // Check for attachments with name in structure
  if (struct.name && struct.type !== 'text/plain' && struct.type !== 'text/html') return true;
  return false;
}

async function fetchEmail(uid, markRead = true) {
  const imap = await connect();
  try {
    const box = await new Promise((resolve, reject) => {
      imap.openBox('INBOX', false, (err, box) => err ? reject(err) : resolve(box));
    });

    const messages = await new Promise((resolve, reject) => {
      const f = imap.fetch(uid, { bodies: '', struct: true });
      const msgs = [];
      f.on('message', msg => msgs.push(msg));
      f.on('error', reject);
      f.on('end', () => resolve(msgs));
    });

    if (messages.length === 0) return [null, imap];

    const msg = messages[0];
    const result = { uid, flags: [], date: null, from: '', to: '', subject: '', text: '', html: '', hasAttachments: false, attachments: [] };

    await new Promise((resolve, reject) => {
      const f = imap.fetch(uid, { bodies: 'HEADER.FIELDS (FROM TO SUBJECT DATE)', struct: true });
      let done = false;

      f.on('message', msgStream => {
        msgStream.on('body', stream => {
          const buf = [];
          stream.on('data', chunk => buf.push(chunk));
          stream.once('end', () => {
            const header = require('imap').parseHeader(Buffer.concat(buf).toString('utf8'));
            result.from = parseAddress(header.from);
            result.to = parseAddress(header.to);
            result.subject = decodeSubject(header.subject ? header.subject[0] : '');
            result.date = header.date ? new Date(header.date[0]) : null;
          });
        });
        msgStream.once('end', () => { if (!done) { done = true; resolve(); }});
      });
      f.on('error', err => { if (!done) { done = true; reject(err); }});
    });

    const rawText = await new Promise((resolve, reject) => {
      const f = imap.fetch(uid, { bodies: '' });
      let buffer = '';
      f.on('message', msgStream => {
        msgStream.on('body', stream => {
          stream.on('data', chunk => buffer += chunk.toString('utf8'));
          stream.once('end', () => resolve(buffer));
        });
      });
      f.on('error', reject);
    });

    try {
      const parsed = await simpleParser(rawText);
      result.text = parsed.text || '';
      result.html = parsed.html || '';
      result.hasAttachments = parsed.attachments.length > 0;
      result.attachments = parsed.attachments.map(a => ({
        filename: a.filename,
        contentType: a.contentType,
        size: a.size || (Buffer.isBuffer(a.content) ? a.content.length : 0),
        content: a.content
      }));
    } catch {
      result.text = rawText;
    }

    if (markRead && !result.flags.includes('\\Seen')) {
      await new Promise((resolve, reject) => {
        imap.addFlags(uid, '\\Seen', err => err ? reject(err) : resolve());
      });
      result.flags = [...result.flags, '\\Seen'];
      // Update cache
      const messages = getCachedMessages().messages || [];
      const idx = messages.findIndex(m => m.uid === parseInt(uid));
      if (idx !== -1) {
        if (!messages[idx].flags) messages[idx].flags = [];
        if (!messages[idx].flags.includes('\\Seen')) {
          messages[idx].flags = [...messages[idx].flags, '\\Seen'];
        }
        saveCachedMessages(messages);
      }
    }

    return [result, imap];
  } catch (err) {
    imap.end();
    throw err;
  }
}

async function fetch(options, positional) {
  const uid = positional[0];
  if (!uid) {
    console.error('\n## Error: UID required\n');
    console.error('Usage: node scripts/mail.js fetch <uid>\n');
    process.exit(1);
  }

  const markRead = options['mark-read'] !== false;
  const [msg, imap] = await fetchEmail(uid, markRead);

  if (!msg) {
    console.error('\n## Error\n');
    console.error(`Message UID ${uid} not found\n`);
    imap.end();
    process.exit(1);
  }

  imap.end();

  console.log('\n## Email #' + uid + '\n');
  console.log(`**From:** ${msg.from}`);
  console.log(`**To:** ${msg.to}`);
  console.log(`**Subject:** ${msg.subject}`);
  console.log(`**Date:** ${msg.date ? formatDateFull(msg.date) : 'N/A'}`);
  if (msg.hasAttachments) {
    console.log(`**Attachments:** ${msg.attachments.map(a => a.filename).join(', ')}`);
  }
  console.log('\n---\n');
  console.log(msg.text || msg.html || '(no content)');
  console.log('\n---\n');
  if (msg.hasAttachments) {
    console.log('**Has Attachment(s) — download:**');
    console.log('```bash');
    console.log(`node scripts/mail.js download ${uid}`);
    console.log('```\n');
  }
  console.log('**Actions:**');
  console.log('```bash');
  console.log(`node scripts/mail.js reply ${uid} --body "Your reply here"`);
  console.log(`node scripts/mail.js forward ${uid} --to <email>`);
  console.log(`node scripts/mail.js mark-unread ${uid}`);
  console.log(`node scripts/mail.js delete ${uid}`);
  console.log('```\n');
}

function formatDateFull(date) {
  try {
    return new Date(date).toLocaleString('en-US', {
      weekday: 'short', year: 'numeric', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit'
    });
  } catch {
    return String(date);
  }
}

function parseTimeFilter(value) {
  if (!value) return null;
  const now = new Date();

  // Relative: 7d, 1m, 3h
  const relMatch = value.match(/^(\d+)([dhm])$/);
  if (relMatch) {
    const num = parseInt(relMatch[1]);
    const unit = relMatch[2];
    let ms;
    if (unit === 'd') ms = num * 86400000;
    else if (unit === 'h') ms = num * 3600000;
    else ms = num * 2592000000;
    return new Date(now.getTime() - ms);
  }

  // Absolute: 2026-03-01
  const absDate = new Date(value);
  if (!isNaN(absDate.getTime())) return absDate;

  return null;
}

async function search(options, positional) {
  const messages = getCachedMessages();
  const server = options.server;
  const all = options.all;
  const since = parseTimeFilter(options.since);
  const before = parseTimeFilter(options.before);
  const fromFilter = (options.from || '').toLowerCase();
  const subjectFilter = (options.subject || '').toLowerCase();
  const toFilter = (options.to || '').toLowerCase();
  const unseenOnly = options.unseen;

  let results;

  if (server) {
    results = await searchServer(options);
  } else {
    results = messages.filter(m => {
      if (since && new Date(m.date) < since) return false;
      if (before && new Date(m.date) > before) return false;
      if (fromFilter && !(parseAddress(m.from || '').toLowerCase().includes(fromFilter))) return false;
      if (subjectFilter && !(decodeSubject(m.subject || '').toLowerCase().includes(subjectFilter))) return false;
      if (toFilter && !(parseAddress(m.to || '').toLowerCase().includes(toFilter))) return false;
      if (unseenOnly && !isUnread(m.flags)) return false;
      return true;
    });
  }

  const sorted = [...results].sort((a, b) => new Date(b.date) - new Date(a.date));
  const total = sorted.length;
  const toShow = all ? sorted : sorted.slice(0, 20);

  console.log('\n## Inbox\n');
  console.log(`**${total}** messages${!all && total > 20 ? ' (showing first 20)' : ''}\n`);

  if (toShow.length > 0) {
    console.log('| UID | 📎 | Subject | From | Date |');
    console.log('|-----|-----|---------|------|------|');
    toShow.forEach(m => {
      const attach = m.hasAttachments ? '📎' : '';
      const subject = decodeSubject(m.subject || '').replace(/\|/g, '\\|');
      const from = parseAddress(m.from || '').replace(/\|/g, '\\|');
      const date = formatDate(m.date);
      console.log(`| ${m.uid} | ${attach} | ${subject} | ${from} | ${date} |`);
    });
    console.log();
  }
}

async function searchServer(options) {
  const imap = await connect();
  try {
    await new Promise((resolve, reject) => {
      imap.openBox('INBOX', false, err => err ? reject(err) : resolve());
    });

    const criteria = ['ALL'];
    if (options.from) criteria.push(['FROM', options.from]);
    if (options.subject) criteria.push(['SUBJECT', options.subject]);
    if (options.to) criteria.push(['TO', options.to]);

    const messages = await new Promise((resolve, reject) => {
      const f = imap.search(criteria, (err, results) => err ? reject(err) : resolve(results));
    });

    const results = [];
    for (const uid of messages.slice(-50)) {
      try {
        const [msg] = await fetchEmail(uid, false);
        if (msg) results.push(msg);
      } catch {}
    }
    return results;
  } finally {
    imap.end();
  }
}

async function markRead(options, positional) {
  const uids = positional.filter(u => !u.startsWith('-'));
  if (uids.length === 0) {
    console.error('\n## Error: UID required\n');
    console.error('Usage: node scripts/mail.js mark-read <uid> [uid2...]\n');
    process.exit(1);
  }

  const imap = await connect();
  try {
    await new Promise((resolve, reject) => {
      imap.openBox('INBOX', false, err => err ? reject(err) : resolve());
    });

    await new Promise((resolve, reject) => {
      imap.addFlags(uids, '\\Seen', err => err ? reject(err) : resolve());
    });

    // Update cache
    const messages = getCachedMessages();
    messages.forEach(m => { if (uids.includes(m.uid)) m.flags = m.flags.filter(f => f !== '\\Seen'); });
    saveCachedMessages(messages);

    console.log('\n## Marked as Read\n');
    console.log(`**UIDs:** ${uids.join(', ')}\n`);
  } finally {
    imap.end();
  }
}

async function markUnread(options, positional) {
  const uids = positional.filter(u => !u.startsWith('-'));
  if (uids.length === 0) {
    console.error('\n## Error: UID required\n');
    console.error('Usage: node scripts/mail.js mark-unread <uid> [uid2...]\n');
    process.exit(1);
  }

  const imap = await connect();
  try {
    await new Promise((resolve, reject) => {
      imap.openBox('INBOX', false, err => err ? reject(err) : resolve());
    });

    await new Promise((resolve, reject) => {
      imap.delFlags(uids, '\\Seen', err => err ? reject(err) : resolve());
    });

    // Update cache
    const messages = getCachedMessages();
    messages.forEach(m => { if (uids.includes(String(m.uid))) m.flags = m.flags.filter(f => f !== '\\Seen'); });
    saveCachedMessages(messages);

    console.log('\n## Marked as Unread\n');
    console.log(`**UIDs:** ${uids.join(', ')}\n`);
  } finally {
    imap.end();
  }
}

async function deleteMsg(options, positional) {
  const uids = positional.filter(u => !u.startsWith('-'));
  if (uids.length === 0) {
    console.error('\n## Error: UID required\n');
    console.error('Usage: node scripts/mail.js delete <uid> [uid2...]\n');
    process.exit(1);
  }

  const toDelete = uids.map(u => parseInt(u)).filter(u => !isNaN(u));
  if (toDelete.length === 0) {
    console.error('\n## Error: No valid UIDs\n');
    return;
  }

  const imap = await connect();
  try {
    await new Promise((resolve, reject) => {
      imap.openBox('INBOX', false, err => err ? reject(err) : resolve());
    });

    // Mark as deleted and expunge
    await new Promise((resolve, reject) => {
      imap.addFlags(toDelete, '\\Deleted', err => err ? reject(err) : resolve());
    });

    await new Promise((resolve, reject) => {
      imap.expunge(err => err ? reject(err) : resolve());
    });
  } finally {
    imap.end();
  }

  // Clear cache so next check fetches fresh data from server
  if (fs.existsSync(CACHE_FILE)) {
    fs.unlinkSync(CACHE_FILE);
  }

  console.log('\n## Deleted\n');
  console.log(`**UIDs:** ${toDelete.join(', ')}\n`);
}

async function download(options, positional) {
  const uid = positional[0];
  if (!uid) {
    console.error('\n## Error: UID required\n');
    console.error('Usage: node scripts/mail.js download <uid> [--dir <path>]\n');
    process.exit(1);
  }

  const dir = options.dir || path.join(CACHE_DIR, 'attachments');
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

  const [msg, imap] = await fetchEmail(uid, false);
  if (!msg) {
    console.error('\n## Error\n');
    console.error(`Message UID ${uid} not found\n`);
    imap.end();
    process.exit(1);
  }

  console.log('\n## Attachments\n');
  console.log(`**UID:** ${uid}\n`);

  if (!msg.attachments || msg.attachments.length === 0) {
    console.log('No attachments found.\n');
    imap.end();
    return;
  }

  console.log('| Filename | Size | Path |');
  console.log('|----------|------|------|');
  for (const att of msg.attachments) {
    const size = att.size || (Buffer.isBuffer(att.content) ? att.content.length : 0);
    const sizeStr = size > 1024 ? `${(size / 1024).toFixed(1)} KB` : `${size} B`;
    if (!att.content) {
      console.log(`| ${att.filename} | ${sizeStr} | (content unavailable) |`);
      continue;
    }
    const filepath = path.join(dir, att.filename);
    fs.writeFileSync(filepath, att.content);
    console.log(`| ${att.filename} | ${sizeStr} | ${filepath} |`);
  }
  console.log();
  imap.end();
}

async function listMailboxesCmd(options, positional) {
  const imap = await connect();
  try {
    const list = await new Promise((resolve, reject) => {
      imap.getBoxes('', (err, boxes) => err ? reject(err) : resolve(boxes));
    });

    console.log('\n## Mailboxes\n');
    console.log('| Name | Special Use |');
    console.log('|------|-------------|');

    function printBoxes(boxes, prefix = '') {
      for (const [name, box] of Object.entries(boxes)) {
        const fullName = prefix ? `${prefix}${name}` : name;
        const special = box.special ? box.special.join(', ') : '';
        console.log(`| ${fullName} | ${special} |`);
        if (box.children) printBoxes(box.children, fullName);
      }
    }
    printBoxes(list);
    console.log();
  } finally {
    imap.end();
  }
}

async function stats(options, positional) {
  const messages = getCachedMessages();
  const now = new Date();
  const oneDayAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000);
  const oneWeekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  const oneMonthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);

  const total = messages.length;
  const unread = messages.filter(m => isUnread(m.flags)).length;
  const withAttachments = messages.filter(m => m.hasAttachments).length;
  const last24h = messages.filter(m => new Date(m.date) >= oneDayAgo).length;
  const lastWeek = messages.filter(m => new Date(m.date) >= oneWeekAgo).length;
  const lastMonth = messages.filter(m => new Date(m.date) >= oneMonthAgo).length;

  const senderCounts = {};
  messages.forEach(m => {
    const sender = parseAddress(m.from || '');
    senderCounts[sender] = (senderCounts[sender] || 0) + 1;
  });
  const topSenders = Object.entries(senderCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  console.log('\n## Email Statistics\n');
  console.log(`**${total}** total · **${unread}** unread · **${withAttachments}** with attachments\n`);

  console.log('### Time Distribution\n');
  console.log('| Period | Count |');
  console.log('|--------|-------|');
  console.log(`| Today | **${last24h}** |`);
  console.log(`| Last 7 days | **${lastWeek}** |`);
  console.log(`| Last 30 days | **${lastMonth}** |`);
  console.log();

  console.log('### Top Senders\n');
  console.log('| Sender | Count |');
  console.log('|--------|-------|');
  topSenders.forEach(([sender, count]) => {
    console.log(`| ${sender} | ${count} |`);
  });

  if (messages.length > 0) {
    const sorted = [...messages].sort((a, b) => new Date(a.date) - new Date(b.date));
    const oldest = formatDate(sorted[0].date);
    const newest = formatDate(sorted[sorted.length - 1].date);
    console.log(`\n_Cache spans ${oldest} to ${newest}_\n`);
  }
}

function clearCache(options, positional) {
  ensureCacheDir();
  if (fs.existsSync(CACHE_FILE)) {
    fs.unlinkSync(CACHE_FILE);
  }
  console.log('\nCache cleared\n');
}

// Export handlers
module.exports.check = check;
module.exports.fetch = fetch;
module.exports.fetchEmail = fetchEmail;
module.exports.read = fetch;
module.exports.search = search;
module.exports.stats = stats;
module.exports.markRead = markRead;
module.exports['mark-read'] = markRead;
module.exports.seen = markRead;
module.exports.markUnread = markUnread;
module.exports['mark-unread'] = markUnread;
module.exports.unseen = markUnread;
module.exports.delete = deleteMsg;
module.exports.del = deleteMsg;
module.exports.download = download;
module.exports.listMailboxes = listMailboxesCmd;
module.exports['list-mailboxes'] = listMailboxesCmd;
module.exports.sync = sync;
module.exports.clearCache = clearCache;
module.exports['clear-cache'] = clearCache;
module.exports.default = async (options, positional) => {
  console.error('\n## Error\n');
  console.error('Unknown command: ' + (options.command || '') + '\n');
  console.error('### Available Commands\n');
  console.error('- `check` Check inbox [--limit N] [--all]');
  console.error('- `fetch <uid>` Fetch email content [--mark-read false]');
  console.error('- `read <uid>` Alias for fetch');
  console.error('- `search` Search cache [--from <email>] [--subject <text>] [--all] [--server]');
  console.error('- `mark-read <uid> [...]` Mark as read');
  console.error('- `mark-unread <uid> [...]` Mark as unread');
  console.error('- `delete <uid> [...]` Delete email (alias: del)');
  console.error('- `download <uid>` Download attachments [--dir <path>]');
  console.error('- `list-mailboxes` List all mailboxes');
  console.error('- `sync` Check server for new messages');
  console.error('- `clear-cache` Clear local cache\n');
  console.error('Search: default is cache (~0.2s), use --server for IMAP search (~5s)\n');
  process.exit(1);
};

// CLI entry point when run directly
if (require.main === module) {
  const { parseArgs } = require('.');
  const { command, options, positional } = parseArgs();
  const handler = module.exports[command] || module.exports.default;
  handler(options, positional).catch(err => {
    console.error('\n## Error\n');
    console.error('```\n' + err.message + '\n```\n');
    process.exit(1);
  });
}
