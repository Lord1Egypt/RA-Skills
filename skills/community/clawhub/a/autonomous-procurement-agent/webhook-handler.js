/**
 * Procurement Agent — Lemon Squeezy Webhook Handler v1.1.0
 * ==========================================================
 * Receives LS subscription events → maps variant_id to tier → writes license DB.
 *
 * SECURITY v1.1:
 *   - LS_WEBHOOK_SECRET is REQUIRED. Server refuses to start without it.
 *   - All logs are sanitized: no raw body, no email addresses, no keys.
 *   - HMAC-SHA256 via crypto.timingSafeEqual for signature verification.
 *
 * Tier schema:
 *   variant_999  → tier: "PRO",    features: [parse_unlimited, basic_export]
 *   variant_2999 → tier: "ENTERPRISE", features: [parse_unlimited, full_audit, f1_f2_f3, auto_approval, safety_freeze]
 *
 * License DB: ${PARSER_DATA_DIR:-./data}/licenses.json
 */

'use strict';

const http = require('http');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// ─── Env ──────────────────────────────────────────────────────────────────────

const PORT          = parseInt(process.env.PROCU_WEBHOOK_PORT || '3002', 10);
const HMAC_SECRET   = process.env.LS_WEBHOOK_SECRET || '';
const LS_PRO_VID    = String(process.env.LS_PRO_VARIANT_ID   || '999');
const LS_ENT_VID    = String(process.env.LS_ENT_VARIANT_ID    || '2999');
const DATA_DIR      = process.env.PARSER_DATA_DIR || path.join(process.env.HOME || '/tmp', '.procurement-agent-data');
const LICENSE_PATH  = path.join(DATA_DIR, 'licenses.json');

// ─── Fail-fast: LS_WEBHOOK_SECRET is mandatory in production ─────────────────

if (!HMAC_SECRET) {
  console.error('[FATAL] LS_WEBHOOK_SECRET environment variable is not set.');
  console.error('[FATAL] Refusing to start — set LS_WEBHOOK_SECRET to a non-empty string.');
  console.error('[FATAL] Example: LS_WEBHOOK_SECRET=your_secret node webhook-handler.js');
  process.exit(1);
}

// ─── Tier Definitions ─────────────────────────────────────────────────────────

const TIERS = {
  PRO: {
    tier: 'PRO', variantId: LS_PRO_VID,
    features: { parse_unlimited: true, basic_export: true, f1_calculation_check: false,
      f2_price_spike: false, f3_duplicate: false, feature_audit_f1_f2: false,
      feature_auto_approval: false, safety_freeze: false },
  },
  ENTERPRISE: {
    tier: 'ENTERPRISE', variantId: LS_ENT_VID,
    features: { parse_unlimited: true, basic_export: true, f1_calculation_check: true,
      f2_price_spike: true, f3_duplicate: true, feature_audit_f1_f2: true,
      feature_auto_approval: true, safety_freeze: true },
  },
  FREE: {
    tier: 'FREE', variantId: '0',
    features: { parse_unlimited: false, basic_export: false, f1_calculation_check: false,
      f2_price_spike: false, f3_duplicate: false, feature_audit_f1_f2: false,
      feature_auto_approval: false, safety_freeze: false },
  },
};

function resolveTier(variantId) {
  if (variantId === LS_ENT_VID) return TIERS.ENTERPRISE;
  if (variantId === LS_PRO_VID) return TIERS.PRO;
  return TIERS.FREE;
}

// ─── Log Sanitization ──────────────────────────────────────────────────────────

/**
 * Strip anything that looks like an email, API key, or token from a string.
 * Used to prevent sensitive data from appearing in logs.
 */
function sanitize(s) {
  if (typeof s !== 'string') return s;
  return s
    .replace(/[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/g, '[EMAIL_REDACTED]')
    .replace(/(sk|pk|api|token|key|secret|Bearer)\s*[:=]\s*["']?[^\s"'&]{8,["']?/gi, '[CREDENTIAL_REDACTED]')
    .replace(/"body"\s*:\s*"[^"]{20,}"/g, '"body": "[RAW_CONTENT_REDACTED]"')
    .slice(0, 300); // safety cap
}

// ─── License DB ────────────────────────────────────────────────────────────────

function ensureDir() {
  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });
}

function readDb() {
  ensureDir();
  return fs.existsSync(LICENSE_PATH) ? JSON.parse(fs.readFileSync(LICENSE_PATH, 'utf8')) : {};
}

function writeDb(db) {
  ensureDir();
  const tmp = LICENSE_PATH + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(db, null, 2));
  fs.fsyncSync(fs.openSync(tmp, 'r+'));
  fs.renameSync(tmp, LICENSE_PATH);
}

function upsertLicense(email, record) {
  const db = readDb();
  db[email] = { ...record, updatedAt: new Date().toISOString() };
  writeDb(db);
}

function removeLicense(email) {
  const db = readDb();
  delete db[email];
  writeDb(db);
}

// ─── HMAC Verification ─────────────────────────────────────────────────────────

function verifySignature(rawBody, signatureHeader) {
  if (!signatureHeader) return false;
  const expected = crypto.createHmac('sha256', HMAC_SECRET).update(rawBody).digest('hex');
  try {
    return crypto.timingSafeEqual(
      Buffer.from(expected, 'hex'),
      Buffer.from(signatureHeader.replace('sha256=', ''), 'hex')
    );
  } catch { return false; }
}

// ─── Event Handlers (sanitized logs only) ─────────────────────────────────────

const HANDLERS = {
  subscription_created(opts) {
    const { data } = opts.payload;
    const email    = data.attributes.user_email;
    const vid      = String(data.attributes.variant_id);
    const status   = data.attributes.status;
    if (status !== 'active' && status !== 'on_trial') return;
    const tier = resolveTier(vid);
    upsertLicense(email, { tier: tier.tier, variantId: vid, features: tier.features,
      status, subscriptionId: data.id, createdAt: data.attributes.created_at });
    console.log(`[LS] subscription_created tier=${tier.tier} status=${status} variant=${vid.slice(0,4)}***`);
  },

  subscription_updated(opts) {
    const { data } = opts.payload;
    const email  = data.attributes.user_email;
    const vid    = String(data.attributes.variant_id);
    const status = data.attributes.status;
    if (['cancelled', 'expired', 'unpaid'].includes(status)) {
      removeLicense(email);
      console.log(`[LS] subscription_updated action=removed tier=FREE status=${status}`);
      return;
    }
    const tier = resolveTier(vid);
    upsertLicense(email, { tier: tier.tier, variantId: vid, features: tier.features,
      status, subscriptionId: data.id });
    console.log(`[LS] subscription_updated tier=${tier.tier} status=${status} variant=${vid.slice(0,4)}***`);
  },

  subscription_cancelled(opts) {
    const email = opts.payload.data.attributes.user_email;
    removeLicense(email);
    console.log('[LS] subscription_cancelled action=removed');
  },

  subscription_expired(opts) {
    const email = opts.payload.data.attributes.user_email;
    removeLicense(email);
    console.log('[LS] subscription_expired action=removed');
  },

  subscription_resumed(opts) {
    const { data } = opts.payload;
    const email = data.attributes.user_email;
    const vid   = String(data.attributes.variant_id);
    const tier  = resolveTier(vid);
    upsertLicense(email, { tier: tier.tier, variantId: vid, features: tier.features,
      status: 'active', subscriptionId: data.id });
    console.log(`[LS] subscription_resumed tier=${tier.tier}`);
  },

  subscription_payment_success(opts) {
    const { data } = opts.payload;
    const email = data.attributes.user_email;
    const vid   = String(data.attributes.variant_id);
    const tier  = resolveTier(vid);
    upsertLicense(email, { tier: tier.tier, variantId: vid, features: tier.features,
      status: 'active', subscriptionId: data.id });
    console.log(`[LS] subscription_payment_success tier=${tier.tier} variant=${vid.slice(0,4)}***`);
  },

  subscription_payment_failed(opts) {
    const { data } = opts.payload;
    const email = data.attributes.user_email;
    console.log(`[LS] subscription_payment_failed variant=${String(data.attributes.variant_id).slice(0,4)}***`);
    // Do not remove license — give user time to update payment method
    upsertLicense(email, { status: 'payment_failed' });
  },

  order_paid(opts) {
    const { data } = opts.payload;
    const email = data.attributes.user_email;
    const vid   = String(data.attributes.first_order_item?.variant_id || '0');
    const tier  = resolveTier(vid);
    if (tier.tier === 'FREE') return;
    const expiresAt = new Date(); expiresAt.setDate(expiresAt.getDate() + 30);
    upsertLicense(email, { tier: tier.tier, variantId: vid, features: tier.features,
      status: 'active', expiresAt: expiresAt.toISOString(), orderId: data.id });
    console.log(`[LS] order_paid tier=${tier.tier} variant=${vid.slice(0,4)}*** expires=${expiresAt.toISOString().slice(0,10)}`);
  },
};

// ─── HTTP Server ───────────────────────────────────────────────────────────────

function parseBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data', c => chunks.push(c));
    req.on('end', () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);

  if (req.method === 'OPTIONS') {
    res.writeHead(204, { 'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-Signature' });
    res.end(); return;
  }

  if (req.method === 'GET' && url.pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', service: 'procurement-agent-webhook', version: '1.1.0' }));
    return;
  }

  if (req.method === 'POST' && url.pathname === '/webhook/lemon-squeezy') {
    const rawBody = await parseBody(req);
    const sig     = req.headers['x-signature'] || '';

    if (!verifySignature(rawBody, sig)) {
      console.warn('[LS Webhook] Rejected: invalid X-Signature');
      res.writeHead(401, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Invalid signature' })); return;
    }

    let payload;
    try { payload = JSON.parse(rawBody.toString('utf8')); }
    catch {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'Invalid JSON' })); return;
    }

    // Sanitize payload for logging (no raw content, no keys)
    const safePayload = sanitize(JSON.stringify(payload));
    const eventName = payload?.meta?.event_name;
    console.log(`[LS Webhook] Received event=${eventName} payload_len=${safePayload.length}`);

    const handler = HANDLERS[eventName];
    if (handler) {
      try { handler({ payload }); }
      catch (e) { console.error(`[LS Webhook] Handler error for ${eventName}: ${e.message}`); }
    } else {
      console.log(`[LS Webhook] Unhandled event: ${eventName}`);
    }

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ received: true })); return;
  }

  // Internal license query endpoint
  if (req.method === 'GET' && url.pathname === '/license') {
    const email = url.searchParams.get('email');
    if (!email) { res.writeHead(400, { 'Content-Type': 'application/json' }); res.end(JSON.stringify({ error: 'email required' })); return; }
    const db = readDb();
    const lic = db[email];
    if (!lic) { res.writeHead(404, { 'Content-Type': 'application/json' }); res.end(JSON.stringify({ error: 'License not found' })); return; }
    // Never echo back raw email in logs
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ tier: lic.tier, features: lic.features, status: lic.status }));
    return;
  }

  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'Not found' }));
});

// ─── Bootstrap ─────────────────────────────────────────────────────────────────

if (require.main === module) {
  console.log(`[Procurement Agent] Webhook v1.1.0 starting on port ${PORT}`);
  console.log(`[Procurement Agent] Pro variant: ${LS_PRO_VID.slice(0,4)}*** | Enterprise variant: ${LS_ENT_VID.slice(0,4)}***`);
  console.log(`[Procurement Agent] LS_WEBHOOK_SECRET: [${HMAC_SECRET ? 'SET' : 'MISSING'}]`);
  server.listen(PORT, () => console.log(`[Procurement Agent] Ready — endpoint: http://localhost:${PORT}/webhook/lemon-squeezy`));
}

module.exports = { server, getLicense: (e) => readDb()[e] || null, resolveTier, TIERS };
