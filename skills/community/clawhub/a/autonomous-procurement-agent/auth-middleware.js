/**
 * Procurement Agent — License Auth Middleware v1.0
 * ===============================================
 * Intercepts calls to Enterprise-gated features and verifies license tier.
 *
 * Enterprise-only features:
 *   feature_audit_f1_f2    — F1 calculation verification + F2 price spike detection
 *   feature_auto_approval  — auto-approval below limit + approval flow
 *   safety_freeze          — circuit breaker + emergency alert
 *   f3_duplicate           — duplicate quote detection across 7-day window
 *
 * Auth flow:
 *   1. Check in-process cache (licenseCache Map, TTL 60s)
 *   2. If cache miss → GET ${PROCU_WEBHOOK_URL}/license?email=<email>
 *   3. If webhook unreachable → check PROCU_ALLOWED_TIER env var (dev fallback)
 *
 * @requires webhook-handler.js to be running at PROCU_WEBHOOK_URL
 */

'use strict';

const https = require('https');
const http = require('http');

// ─── Config ───────────────────────────────────────────────────────────────────

const PROCU_WEBHOOK_URL   = process.env.PROCU_WEBHOOK_URL   || 'http://localhost:3002';
const PROCU_ALLOWED_TIER  = process.env.PROCU_ALLOWED_TIER  || 'FREE';
const LICENSE_CACHE_TTL_MS = 60 * 1000; // 60-second license cache

// ─── In-Process License Cache ─────────────────────────────────────────────────

const licenseCache = new Map();

function getCachedLicense(email) {
  const entry = licenseCache.get(email);
  if (!entry) return null;
  if (Date.now() - entry.ts > LICENSE_CACHE_TTL_MS) {
    licenseCache.delete(email);
    return null;
  }
  return entry.license;
}

function setCachedLicense(email, license) {
  licenseCache.set(email, { license, ts: Date.now() });
}

// ─── HTTP GET Helper ──────────────────────────────────────────────────────────

function httpGet(urlStr) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlStr);
    const transport = url.protocol === 'https:' ? https : http;
    const req = transport.get(url, { timeout: 5000 }, (res) => {
      if (res.statusCode !== 200) {
        reject(new Error(`Webhook returned ${res.statusCode}`));
        return;
      }
      const chunks = [];
      res.on('data', c => chunks.push(c));
      res.on('end', () => {
        try { resolve(JSON.parse(Buffer.concat(chunks).toString())); }
        catch (e) { reject(new Error('Invalid JSON from webhook')); }
      });
    });
    req.on('error', e => reject(e));
    req.on('timeout', () => { req.destroy(); reject(new Error('Webhook timeout')); });
  });
}

// ─── License Lookup ────────────────────────────────────────────────────────────

async function getUserLicense(email) {
  if (!email) return { tier: 'FREE', features: {} };

  // 1. Cache hit
  const cached = getCachedLicense(email);
  if (cached) return cached;

  // 2. Webhook lookup
  try {
    const license = await httpGet(`${PROCU_WEBHOOK_URL}/license?email=${encodeURIComponent(email)}`);
    setCachedLicense(email, license);
    return license;
  } catch (err) {
    // 3. Webhook unreachable → dev/fallback mode using env var
    console.warn(`[Auth] Webhook unreachable (${err.message}) — using PROCU_ALLOWED_TIER=${PROCU_ALLOWED_TIER}`);
    return { tier: PROCU_ALLOWED_TIER, features: getFeaturesForTier(PROCU_ALLOWED_TIER) };
  }
}

// ─── Feature Map ───────────────────────────────────────────────────────────────

function getFeaturesForTier(tier) {
  const maps = {
    PRO: {
      parse_unlimited: true,
      basic_export: true,
      f1_calculation_check: false,
      f2_price_spike: false,
      f3_duplicate: false,
      feature_audit_f1_f2: false,
      feature_auto_approval: false,
      safety_freeze: false,
    },
    ENTERPRISE: {
      parse_unlimited: true,
      basic_export: true,
      f1_calculation_check: true,
      f2_price_spike: true,
      f3_duplicate: true,
      feature_audit_f1_f2: true,
      feature_auto_approval: true,
      safety_freeze: true,
    },
    FREE: {
      parse_unlimited: false,
      basic_export: false,
      f1_calculation_check: false,
      f2_price_spike: false,
      f3_duplicate: false,
      feature_audit_f1_f2: false,
      feature_auto_approval: false,
      safety_freeze: false,
    },
  };
  return maps[tier] || maps.FREE;
}

// ─── Core Auth Function ───────────────────────────────────────────────────────

/**
 * authorize(email, feature) — throws if user lacks the required feature
 *
 * Usage:
 *   await authorize('user@example.com', 'feature_audit_f1_f2');
 *   // → passes: user is ENTERPRISE
 *   // → throws: user is PRO or FREE
 *
 * @param {string|null} email
 * @param {string} feature  — feature flag key from TIER_DEFINITIONS
 * @returns {Promise<{tier, features}>} — resolved license record on success
 * @throws {Error} — if feature not allowed
 */
async function authorize(email, feature) {
  const license = await getUserLicense(email || '');
  const allowed = license.features && license.features[feature];
  if (!allowed) {
    const msg =
      feature === 'feature_audit_f1_f2' ||
      feature === 'feature_auto_approval' ||
      feature === 'safety_freeze'
        ? `Error: This feature requires an Enterprise License. [${feature}]`
        : `Error: Feature [${feature}] not available on your current plan (${license.tier || 'FREE'}).`;
    const err = new Error(msg);
    err.code = 'LICENSE_DENIED';
    err.requiredFeature = feature;
    err.userTier = license.tier || 'FREE';
    err.upgradeUrl = `${PROCU_WEBHOOK_URL.replace('/webhook/lemon-squeezy', '')}/upgrade`;
    throw err;
  }
  return license;
}

// ─── Sync Auth Wrapper (for use in sync contexts) ─────────────────────────────

/**
 * authorizeSync(email, feature) — same as authorize() but for sync contexts.
 * Uses cache + env fallback only (no async webhook call).
 *
 * Use this only when you need to guard a code path without await.
 * Prefer authorize() in async functions.
 */
function authorizeSync(email, feature) {
  if (!email) {
    const err = new Error(`Error: This feature requires an Enterprise License. [${feature}]`);
    err.code = 'LICENSE_DENIED';
    err.requiredFeature = feature;
    err.userTier = 'FREE';
    throw err;
  }

  const cached = getCachedLicense(email);
  if (cached) {
    const allowed = cached.features && cached.features[feature];
    if (!allowed) {
      const err = new Error(`Error: This feature requires an Enterprise License. [${feature}]`);
      err.code = 'LICENSE_DENIED';
      err.requiredFeature = feature;
      err.userTier = cached.tier || 'FREE';
      throw err;
    }
    return cached;
  }

  // Cache miss in sync context — use env fallback (do NOT block)
  // Caller should use authorize() for production async contexts
  const tier = PROCU_ALLOWED_TIER;
  const features = getFeaturesForTier(tier);
  const allowed = features[feature];
  if (!allowed) {
    const err = new Error(`Error: This feature requires an Enterprise License. [${feature}]`);
    err.code = 'LICENSE_DENIED';
    err.requiredFeature = feature;
    err.userTier = tier;
    throw err;
  }
  return { tier, features };
}

// ─── Middleware Factory (for use in HTTP contexts) ────────────────────────────

/**
 * requireFeature(featureKey) → Express-style middleware
 *
 * Looks for `email` in req.query.email or req.headers.authorization (Bearer token).
 * Attaches license record to req.license on success.
 *
 * Usage in webhook or HTTP handler:
 *   const auth = requireFeature('feature_audit_f1_f2');
 *   app.use('/audit', auth, auditHandler);
 */
function requireFeature(feature) {
  return async (req, res, next) => {
    try {
      // Extract email: from query param, or from Bearer token (base64-encoded email)
      let email = req.query && req.query.email;
      const auth = req.headers && req.headers.authorization;
      if (!email && auth && auth.startsWith('Bearer ')) {
        try { email = Buffer.from(auth.slice(7), 'base64').toString(); } catch (_) {}
      }
      const license = await authorize(email, feature);
      req.license = license;
      next();
    } catch (err) {
      if (err.code === 'LICENSE_DENIED') {
        res.setHeader('Content-Type', 'application/json');
        res.status(403).end(JSON.stringify({
          error: err.message,
          required: err.requiredFeature,
          current_tier: err.userTier,
          upgrade: 'Visit your Lemon Squeezy dashboard to upgrade to Enterprise.'
        }));
      } else {
        next(err);
      }
    }
  };
}

// ─── Cache Invalidation ───────────────────────────────────────────────────────

function revokeLicense(email) {
  licenseCache.delete(email);
}

module.exports = {
  authorize,
  authorizeSync,
  requireFeature,
  getUserLicense,
  revokeLicense,
  getFeaturesForTier,
};
