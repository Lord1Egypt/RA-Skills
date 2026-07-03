/**
 * Express route handler for receiving inbound emails via Resend webhook.
 * 
 * Mount with: app.use('/api/inbound-email', inboundEmailRoutes);
 * 
 * Endpoints:
 *   POST /api/inbound-email       — Receive webhook from Resend
 *   GET  /api/inbound-email       — List unread emails
 *   GET  /api/inbound-email/:id   — Read specific email (marks as read)
 *   POST /api/inbound-email/:id/ack — Mark as processed
 * 
 * Required secrets:
 *   RESEND_WEBHOOK_SECRET — From Resend webhook creation
 * 
 * Environment:
 *   INBOX_DIR — Path to inbox storage (default: <workspace>/mail/inbox)
 */
const express = require('express');
const router = express.Router();
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');

// Resolve inbox directory (override with INBOX_DIR env var)
const INBOX_DIR = process.env.INBOX_DIR || path.join(__dirname, '..', '..', '..', 'mail', 'inbox');

// Ensure inbox exists
if (!fs.existsSync(INBOX_DIR)) {
  fs.mkdirSync(INBOX_DIR, { recursive: true });
}

/**
 * Verify Resend webhook signature
 * Resend signs with: HMAC-SHA256(timestamp.body, secret)
 * Header format: "t=<timestamp>,<hash>"
 */
function verifySignature(rawBody, signature, secret) {
  try {
    const parts = signature.split(',').map(s => s.trim());
    const timestamp = parts.find(p => p.startsWith('t='));
    const hash = parts.find(p => !p.startsWith('t='));
    if (!timestamp || !hash) return false;
    const signedPayload = `${timestamp.slice(2)}.${rawBody}`;
    const expected = crypto.createHmac('sha256', secret)
      .update(signedPayload).digest('hex');
    return crypto.timingSafeEqual(Buffer.from(hash), Buffer.from(expected));
  } catch {
    return false;
  }
}

// POST / — Receive inbound email from Resend webhook
router.post('/', express.raw({ type: 'application/json' }), async (req, res) => {
  try {
    // Verify webhook signature
    const signature = req.headers['x-resend-signature'] || req.headers['resend-signature'];
    const secret = process.env.RESEND_WEBHOOK_SECRET;

    if (secret && signature) {
      if (!verifySignature(req.body.toString(), signature, secret)) {
        console.warn('[INBOUND EMAIL] Invalid signature');
        return res.status(401).json({ error: 'Invalid signature' });
      }
    } else if (secret) {
      console.warn('[INBOUND EMAIL] No signature header, rejecting');
      return res.status(401).json({ error: 'Missing signature' });
    }

    const body = JSON.parse(req.body.toString());
    const { from, to, subject, html, text, headers } = body;
    const timestamp = new Date().toISOString();
    const id = `email_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    const email = {
      id,
      timestamp,
      from,
      to,
      subject: subject || '(no subject)',
      text: text || '',
      html: html || '',
      headers: headers || {},
      read: false,
      processed: false,
    };

    // Save to inbox
    fs.writeFileSync(path.join(INBOX_DIR, `${id}.json`), JSON.stringify(email, null, 2));

    // Append to mail log
    const logPath = path.join(INBOX_DIR, '..', 'mail.log');
    fs.appendFileSync(logPath, `${timestamp} | ${from} | ${to} | ${subject || '(no subject)'}\n`);

    console.log(`[INBOUND EMAIL] ${timestamp} FROM: ${from} SUBJECT: ${subject || '(no subject)'}`);
    res.status(200).json({ ok: true, id });
  } catch (err) {
    console.error('[INBOUND EMAIL] Error:', err.message);
    res.status(500).json({ error: 'Failed to process email' });
  }
});

// GET / — List unread (unprocessed) emails, newest first
router.get('/', async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 50;
    const files = fs.readdirSync(INBOX_DIR)
      .filter(f => f.endsWith('.json') && !f.includes('.processed') && f !== '.lastcheck')
      .sort().reverse().slice(0, limit);

    const emails = files.map(f => {
      try { return JSON.parse(fs.readFileSync(path.join(INBOX_DIR, f), 'utf8')); }
      catch { return null; }
    }).filter(Boolean);

    res.json({ emails, count: emails.length });
  } catch (err) {
    res.status(500).json({ error: 'Failed to read inbox' });
  }
});

// GET /:id — Read specific email (marks as read)
router.get('/:id', async (req, res) => {
  try {
    const filePath = path.join(INBOX_DIR, `${req.params.id}.json`);
    if (!fs.existsSync(filePath)) return res.status(404).json({ error: 'Email not found' });
    const email = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    email.read = true;
    fs.writeFileSync(filePath, JSON.stringify(email, null, 2));
    res.json(email);
  } catch (err) {
    res.status(500).json({ error: 'Failed to read email' });
  }
});

// POST /:id/ack — Mark email as processed
router.post('/:id/ack', async (req, res) => {
  try {
    const filePath = path.join(INBOX_DIR, `${req.params.id}.json`);
    if (!fs.existsSync(filePath)) return res.status(404).json({ error: 'Email not found' });
    const email = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    email.processed = true;
    fs.writeFileSync(filePath, JSON.stringify(email, null, 2));
    // Rename to .processed to hide from listing
    fs.renameSync(filePath, `${filePath}.processed`);
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ error: 'Failed to ack email' });
  }
});

module.exports = router;
