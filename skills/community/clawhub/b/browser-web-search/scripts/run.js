#!/usr/bin/env node

/**
 * browser-web-search-skill launcher
 *
 * This launcher does NOT spawn external processes. It loads the pinned
 * 'browser-web-search' npm package as an ES module via dynamic import and
 * invokes its entry by injecting a validated, allow-listed argv. There is
 * no shell, no subprocess, and no exec sink in this file.
 *
 * Security posture (mapping to applied codeguard-0-* rules):
 *
 * 1. Input validation & injection defense (codeguard-0-input-validation-injection):
 *    - Subcommands and adapter names allow-listed via Sets / strict regex
 *    - All forwarded args length-bounded and stripped of NUL/control chars
 *    - Only well-known long flags forwarded; '--' delimiter prevents option injection
 *    - argv is injected into the imported module; never rendered into a shell string
 *
 * 2. Authorization & access control (codeguard-0-authorization-access-control):
 *    Four sequential gates, evaluated in order; first deny wins. Public
 *    adapters bypass Gates 2-4. See enforceSensitivityPolicy() for the
 *    canonical doc string.
 *      Gate 1 (BWS_PUBLIC_ONLY=1)            — hard isolation, overrides all
 *      Gate 2 (BWS_ENABLE_SENSITIVE_TIER=1)  — sealed by default since v0.4.4
 *      Gate 3 (BWS_ALLOW_SENSITIVE=1 or --i-understand-sensitive)
 *                                            — per-session / per-call opt-in
 *      Gate 4 (platform consent ledger)      — v0.4.10; per (site, pkgVersion,
 *                                              entrySha512) one-time consent,
 *                                              invalidated on any drift
 *
 *    The sealed-tier and consent-ledger gates respond to ClawScan's May 2026
 *    findings ("Identity and Privilege Abuse" + the residual third-party-
 *    dependency concern). Unknown adapters default to 'sensitive' so future
 *    upstream bws additions cannot silently bypass the gates.
 *
 * 3. Privacy & data protection (codeguard-0-privacy-data-protection):
 *    - BWS_PUBLIC_ONLY=1 hard-isolates the launcher to public adapters only
 *      and overrides any tier/session/per-call opt-in.
 *    - Sensitive calls emit a structured 'transparency block' on stderr
 *      (v0.4.10) that names the third-party package + audited SHA-512 +
 *      gate path; this prevents a wrapping AI agent from silently invoking
 *      sensitive functionality.
 *    - Optional --dry-run runs all gates without invoking the package.
 *    - No request payloads / response bodies are ever logged.
 *
 * 4. Logging (codeguard-0-logging):
 *    - Append-only JSON-lines audit log at ~/.bws/audit.log
 *    - Records: timestamp, adapter, site, primaryDomain (when known),
 *      classification, decision, reason, sha256(args) prefix, pkgVersion
 *      (for sensitive allow records), dryRun
 *    - Never logs raw args, secrets, cookies, or response data
 *
 * 5. Supply chain (codeguard-0-supply-chain-security):
 *    - Pinned to REQUIRED_VERSION; module-not-found yields actionable install command
 *    - Skill itself does NOT auto-install or auto-update the npm package
 *    - Dynamic import target is a string literal package name; resolution paths
 *      are restricted to platform-standard global node_modules locations
 *    - Before dynamic import, the resolved entry is gated by:
 *        * package.json name + version match against REQUIRED_VERSION
 *        * file size match against ENTRY_EXPECTED_SIZE
 *        * SHA-512 (timing-safe) match against ENTRY_SHA512_BASE64
 *      Mismatch denies-by-default and writes an audit record. There is
 *      intentionally NO env override for the integrity gate; bumping the
 *      pinned package requires re-auditing and updating these constants.
 *      The verified { pkgVersion, entrySha512 } returned from the gate seeds
 *      Gate 4's consent ledger, so consent is bound to the bytes actually
 *      loaded (not to a caller-claimed identity).
 *    - Symbolic links anywhere in the resolved entry path are rejected.
 *    - process.cwd() / launcher-local node_modules are OFF by default and
 *      only enabled via BWS_ALLOW_LOCAL_INSTALL=1 (development opt-in).
 *
 * Version coupling:
 *    SKILL_VERSION (launcher + docs) and REQUIRED_VERSION (audited pinned
 *    npm package) evolve INDEPENDENTLY. Bumping REQUIRED_VERSION requires
 *    re-auditing upstream and updating ENTRY_EXPECTED_SIZE + ENTRY_SHA512_BASE64
 *    in lockstep; this invalidates all prior Gate 4 consents by design.
 */

'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

// Skill version (this launcher + SKILL.md + config.json) vs REQUIRED_VERSION
// (the audited pinned npm package). They evolve INDEPENDENTLY:
//   - SKILL_VERSION bumps when the launcher's policy / docs change.
//   - REQUIRED_VERSION bumps only after re-auditing the upstream package
//     AND updating ENTRY_EXPECTED_SIZE + ENTRY_SHA512_BASE64 in lockstep.
const SKILL_VERSION = '0.4.10';
const REQUIRED_VERSION = '0.4.3';
const PINNED_PACKAGE = 'browser-web-search';

// Pinned integrity for the package's executed entry file (dist/index.js).
// Computed from the official npm tarball:
//   npm pack browser-web-search@0.4.3
//   tar -xzf browser-web-search-0.4.3.tgz
//   shasum -a 512 package/dist/index.js
// Tarball SRI (npm registry, dist.integrity):
//   sha512-BppWwwWoAQ5VYFdLj0jiQo8n8PCNTYGeJoscRcwYBVB90SNcWVNR1jMbEvBK1FmdNzyYHB+XqrexveNUgDiB0g==
// Bump this CONSTANT in lockstep with REQUIRED_VERSION; mismatched values
// will refuse to load the on-disk module (deny-by-default).
const ENTRY_SHA512_BASE64 =
  'qoGLsUMOPgzIpdxtGMv08Gjy84bkh0AF90mKG9qvagq9O2ngcKcLg+GAy3Z8bljkvdfKcrQSp55xPO9mVCuv3Q==';
const ENTRY_REL_PATH = path.join('dist', 'index.js');
const ENTRY_EXPECTED_SIZE = 22871;

// ---------- CLI surface allow-lists ----------

const SUBCOMMANDS = new Set(['list', 'search', 'info', 'run', 'help']);
const ADAPTER_NAME_RE = /^[a-zA-Z0-9_-]{1,64}\/[a-zA-Z0-9_-]{1,64}$/;
const IDENT_RE = /^[\p{L}\p{N}_\-./ ]{1,200}$/u;

// Launcher-only flags are stripped from argv before forwarding to the pinned
// package. Each flag corresponds to a gate / transparency mechanism in this
// launcher; the package itself never sees them and so cannot bypass them.
const LAUNCHER_ONLY_FLAGS = new Set([
  '--i-understand-sensitive',
  // v0.4.10 — residual mitigations layered ON TOP of the v0.4.4 sealed tier.
  // See SECURITY.md "Residual mitigations" for the rationale (ClawScan
  // May 2026 verdict: "core functionality inherently relies on a third-party
  // dependency to handle sensitive session data").
  '--dry-run',
  '--accept-platform-consent',
]);

const ALLOWED_FLAGS = new Set([
  '--json',
  '--jq',
  '--count',
  '--sort',
  '--id',
  '--limit',
  '--page',
  ...LAUNCHER_ONLY_FLAGS,
]);

const MAX_ARG_LEN = 1024;
const CONTROL_CHAR_RE = /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/;

// ---------- Sensitivity classification ----------
//
// Source of truth: SKILL.md adapter table. Keep these lists in sync when
// SKILL.md is updated. Misclassification only weakens the deny-by-default
// posture; it never increases the privileges granted to bws.

// Sites whose every adapter command operates inside an authenticated session
// (private feeds, DMs, account-restricted content).
const ALWAYS_SENSITIVE_SITES = new Set([
  'weixin',
  'xiaohongshu',
  'weibo',
  'xueqiu',
  'jike',
  'douban',
  'qidian',
  'ctrip',
  'x',
  'linkedin',
]);

// Command suffixes that always touch account/private surfaces, regardless of
// site (e.g. zhihu/me, bilibili/feed, youtube/history).
const SENSITIVE_SUFFIX_RE = /\/(me|feed|history|comments|user_posts|article)$/;

// Sites for which the publicly listed commands are safe to call without
// authenticated state. Adapters of these sites that ALSO match
// SENSITIVE_SUFFIX_RE are still treated as sensitive (e.g. zhihu/me).
const PUBLIC_SITES = new Set([
  // 国内公共
  'thepaper', 'qqnews', 'netease', 'sina', '36kr', 'huxiu',
  'wallstreetcn', 'eastmoney', 'juejin', 'csdn', 'cnblogs',
  'v2ex', 'baidu', 'hupu', 'youdao', 'smzdm', 'infoq',
  // 国际公共
  'google', 'bing', 'duckduckgo', 'github', 'hn', 'reddit',
  'bbc', 'reuters', 'verge', 'ars', 'engadget', 'stackoverflow',
  'devto', 'npm', 'pypi', 'arxiv', 'imdb', 'genius', 'wikipedia',
  'openlibrary', 'yahoo-finance', 'gsmarena', 'producthunt',
  // Variable sites: their /search /hot /trending /popular /top* commands
  // are public. Sensitive commands of these sites still trigger gating
  // through SENSITIVE_SUFFIX_RE.
  'toutiao', 'zhihu', 'bilibili', 'boss', 'youtube',
]);

function classifyAdapter(adapter) {
  if (SENSITIVE_SUFFIX_RE.test(adapter)) return 'sensitive';
  const site = adapter.split('/', 1)[0];
  if (ALWAYS_SENSITIVE_SITES.has(site)) return 'sensitive';
  if (PUBLIC_SITES.has(site)) return 'public';
  return 'sensitive';
}

// Static, well-known site → primary domain map. Used ONLY to enrich the
// audit log so post-hoc forensics can answer "which domains were touched
// by sensitive calls in the last N days". Missing entries are NOT an error;
// the adapter site is always logged regardless.
const SITE_PRIMARY_DOMAIN = Object.freeze({
  // ALWAYS_SENSITIVE_SITES — high-value forensics targets
  weixin: 'mp.weixin.qq.com',
  xiaohongshu: 'www.xiaohongshu.com',
  weibo: 'weibo.com',
  xueqiu: 'xueqiu.com',
  jike: 'web.okjike.com',
  douban: 'www.douban.com',
  qidian: 'www.qidian.com',
  ctrip: 'www.ctrip.com',
  x: 'x.com',
  linkedin: 'www.linkedin.com',
  // Variable-tier sites whose sensitive suffixes can hit account data
  zhihu: 'www.zhihu.com',
  bilibili: 'www.bilibili.com',
  toutiao: 'www.toutiao.com',
  boss: 'www.zhipin.com',
  youtube: 'www.youtube.com',
});

function siteOf(adapter) {
  return adapter.split('/', 1)[0] || null;
}

function primaryDomainOf(adapter) {
  const s = siteOf(adapter);
  if (!s) return null;
  return SITE_PRIMARY_DOMAIN[s] || null;
}

// ---------- Audit log ----------

const AUDIT_DIR = path.join(os.homedir(), '.bws');
const AUDIT_LOG = path.join(AUDIT_DIR, 'audit.log');
const MAX_AUDIT_LOG_BYTES = 1024 * 1024; // 1 MiB; rotate above this

// v0.4.10 — Platform consent ledger (Gate 4). One-time-per-(site,pkg,hash)
// consent record. Any change to pkgVersion or entrySha512 invalidates prior
// consent and forces re-consent. Bypass requires BWS_SKIP_PLATFORM_CONSENT=1.
const CONSENT_LEDGER = path.join(AUDIT_DIR, 'consents.json');
const MAX_CONSENT_LEDGER_BYTES = 256 * 1024;

function hashArgs(args) {
  if (!args.length) return null;
  const h = crypto.createHash('sha256');
  for (const a of args) {
    h.update(a, 'utf8');
    h.update('\u0000');
  }
  return h.digest('hex').slice(0, 16);
}

function audit(record) {
  try {
    fs.mkdirSync(AUDIT_DIR, { recursive: true, mode: 0o700 });
    if (fs.existsSync(AUDIT_LOG)) {
      const stat = fs.statSync(AUDIT_LOG);
      if (stat.size > MAX_AUDIT_LOG_BYTES) {
        try { fs.renameSync(AUDIT_LOG, `${AUDIT_LOG}.1`); } catch (_) { /* best effort */ }
      }
    }
    const line = JSON.stringify({
      ts: new Date().toISOString(),
      pid: process.pid,
      ...record,
    }) + '\n';
    fs.appendFileSync(AUDIT_LOG, line, { mode: 0o600 });
  } catch (err) {
    process.stderr.write(`[bws] audit log write failed: ${err.message}\n`);
  }
}

// ---------- Platform consent ledger (Gate 4, v0.4.10) ----------

/**
 * Safely load and parse the consent ledger.
 *
 * Hardening (codeguard-0-input-validation-injection / supply-chain):
 *   - size-cap before reading (prevents pathological reads of a tampered file)
 *   - JSON.parse (no eval), rejects non-object root
 *   - reject any non-symlink condition: refuse to read through a symlink at
 *     the ledger path itself (an attacker may try to redirect to /etc/...)
 *   - per-site value is shape-checked and ignored if malformed; this keeps
 *     gate decisions safe even with a partially corrupted ledger
 *
 * Returns a plain object keyed by site. Never throws; on any error returns {}.
 */
function loadConsentLedger() {
  try {
    fs.mkdirSync(AUDIT_DIR, { recursive: true, mode: 0o700 });
    let st;
    try {
      st = fs.lstatSync(CONSENT_LEDGER);
    } catch (_) {
      return Object.create(null);
    }
    if (st.isSymbolicLink()) {
      process.stderr.write(
        `[bws] WARNING: consent ledger at ${CONSENT_LEDGER} is a symlink; ` +
        `ignoring it. Remove the symlink and re-consent.\n`,
      );
      return Object.create(null);
    }
    if (!st.isFile()) return Object.create(null);
    if (st.size > MAX_CONSENT_LEDGER_BYTES) {
      process.stderr.write(
        `[bws] WARNING: consent ledger larger than ${MAX_CONSENT_LEDGER_BYTES} bytes; ` +
        `refusing to parse. Move it aside and re-consent.\n`,
      );
      return Object.create(null);
    }
    const raw = fs.readFileSync(CONSENT_LEDGER, 'utf8');
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
      return Object.create(null);
    }
    return parsed;
  } catch (_) {
    return Object.create(null);
  }
}

/**
 * Write the consent ledger back atomically. On any error, log and continue
 * (the call has already been authorized by the in-memory ledger; persistence
 * failure should not block the user, but is recorded for forensics).
 */
function saveConsentLedger(ledger) {
  try {
    fs.mkdirSync(AUDIT_DIR, { recursive: true, mode: 0o700 });
    const tmp = `${CONSENT_LEDGER}.tmp`;
    fs.writeFileSync(tmp, JSON.stringify(ledger, null, 2) + '\n', { mode: 0o600 });
    fs.renameSync(tmp, CONSENT_LEDGER);
  } catch (err) {
    process.stderr.write(`[bws] consent ledger write failed: ${err.message}\n`);
  }
}

/**
 * Decide whether (site, pkgVersion, entrySha512) is already consented to.
 * Returns { consented: boolean, reason: string, record?: {...} }.
 */
function checkConsent(ledger, site, pkgVersion, entrySha512) {
  const rec = ledger && Object.prototype.hasOwnProperty.call(ledger, site)
    ? ledger[site] : null;
  if (!rec || typeof rec !== 'object') {
    return { consented: false, reason: 'no-record' };
  }
  if (rec.pkgVersion !== pkgVersion) {
    return { consented: false, reason: 'pkg-version-changed', record: rec };
  }
  if (rec.entrySha512 !== entrySha512) {
    return { consented: false, reason: 'pkg-integrity-changed', record: rec };
  }
  return { consented: true, reason: 'matching-record', record: rec };
}

function recordConsent(ledger, site, primaryDomain, pkgVersion, entrySha512) {
  const now = new Date().toISOString();
  const existing = (ledger && ledger[site]) || {};
  ledger[site] = {
    primaryDomain: primaryDomain || existing.primaryDomain || null,
    firstConsent: existing.firstConsent || now,
    lastConsent: now,
    pkgVersion,
    entrySha512,
  };
  saveConsentLedger(ledger);
}

// ---------- Transparency block (v0.4.10) ----------

/**
 * Emit a structured transparency line to stderr BEFORE the package is
 * imported. Always emitted for sensitive calls (regardless of any
 * opt-in / consent state); optional for public calls via BWS_TRANSPARENCY=1.
 *
 * Purpose: make it impossible for a wrapping AI agent or downstream script
 * to silently invoke a sensitive call. The block names the third-party
 * package, its audited integrity hash, the gate path taken, and the audit /
 * consent paths so a human reviewer can replay the decision.
 *
 * No request payloads, no response bodies, no args (only the SHA-256 prefix
 * already computed by hashArgs()).
 */
function emitTransparencyBlock(record) {
  const line = '[bws] transparency:' + JSON.stringify(record);
  process.stderr.write(line + '\n');
}

// ---------- Validation helpers ----------

function fail(message) {
  console.error(JSON.stringify({ success: false, error: message }));
  process.exit(1);
}

function assertSafeArg(value, label) {
  if (typeof value !== 'string' || value.length === 0) {
    fail(`Invalid ${label}: empty or non-string`);
  }
  if (value.length > MAX_ARG_LEN) {
    fail(`Invalid ${label}: exceeds ${MAX_ARG_LEN} characters`);
  }
  if (CONTROL_CHAR_RE.test(value)) {
    fail(`Invalid ${label}: contains control characters`);
  }
}

function assertAllowedFlag(token) {
  const head = token.split('=', 1)[0];
  if (!ALLOWED_FLAGS.has(head)) {
    fail(`Disallowed flag: ${head}`);
  }
}

function validateForwardArgs(args) {
  for (const arg of args) {
    assertSafeArg(arg, 'argument');
    if (arg.startsWith('-')) {
      assertAllowedFlag(arg);
    }
  }
}

function stripLauncherOnlyFlags(args) {
  return args.filter((a) => {
    const head = a.split('=', 1)[0];
    return !LAUNCHER_ONLY_FLAGS.has(head);
  });
}

// ---------- Sensitivity gating ----------

/**
 * Sensitivity gate. Four-tier model since v0.4.10 (was three since v0.4.4,
 * was single-tier opt-in before that).
 *
 * Order of precedence (first match wins; all decisions write an audit record):
 *
 *   Gate 1 — BWS_PUBLIC_ONLY=1
 *     Hard isolation. Sensitive adapters are unconditionally denied.
 *     Cannot be overridden by tier or per-call opt-in. (Unchanged.)
 *
 *   Gate 2 — Sensitive tier (sealed by default in v0.4.4+)
 *     Sensitive adapters are denied unless BWS_ENABLE_SENSITIVE_TIER=1.
 *
 *   Gate 3 — Per-session / per-call opt-in (existing)
 *     Once the tier is enabled, the caller still needs ONE of:
 *       - BWS_ALLOW_SENSITIVE=1
 *       - --i-understand-sensitive flag
 *
 *   Gate 4 — Platform consent ledger (NEW in v0.4.10)
 *     For each (site, pkgVersion, entrySha512) triple, the caller must have
 *     a stored consent record at ~/.bws/consents.json. First-time access
 *     requires --accept-platform-consent on the call; the launcher writes
 *     the record. Any change to pkgVersion or entrySha512 invalidates prior
 *     consent and forces re-consent (directly addresses the "future upgrades
 *     go silently through" residual risk).
 *     Bypass: BWS_SKIP_PLATFORM_CONSENT=1 (with loud stderr warning).
 *
 * Public adapters are unaffected by Gates 2/3/4 and the consent ledger.
 *
 * Inputs:
 *   adapter         — validated adapter name (site/action)
 *   rawArgs         — raw CLI args (used to detect launcher-only flags)
 *   options         — { pkgVersion, entrySha512, dryRun }
 *                     pkgVersion / entrySha512 are sourced from the verified
 *                     manifest+entry (only computed AFTER integrity gate
 *                     passes), so the consent ledger cannot be primed with
 *                     a fabricated identity.
 */
/**
 * Pre-integrity gates (1, 2, 3). These do NOT need disk access and run
 * BEFORE the launcher resolves / verifies the pinned package. That order
 * is important: a caller invoking `weixin/search` without
 * BWS_ENABLE_SENSITIVE_TIER=1 must receive the gate-2 message, not a
 * confusing "package not found" message from the resolver.
 *
 * Returns { gateReason } describing why the call is allowed so far; on any
 * deny path the function calls fail() and never returns.
 */
function enforcePreIntegrityGates(adapter, rawArgs, options) {
  const { dryRun = false } = options || {};
  const classification = classifyAdapter(adapter);
  const env = process.env;
  const argHash = hashArgs(rawArgs);
  const optInFlag = rawArgs.some((a) => a.split('=', 1)[0] === '--i-understand-sensitive');
  const optInEnv = env.BWS_ALLOW_SENSITIVE === '1';
  const publicOnly = env.BWS_PUBLIC_ONLY === '1';
  const tierEnabled = env.BWS_ENABLE_SENSITIVE_TIER === '1';
  const site = siteOf(adapter);

  const baseRecord = {
    adapter,
    site,
    primaryDomain: primaryDomainOf(adapter),
    argHash,
    classification,
    dryRun: dryRun || undefined,
  };

  // Gate 1: BWS_PUBLIC_ONLY=1 — hardest isolation, overrides everything.
  if (classification === 'sensitive' && publicOnly) {
    audit({ ...baseRecord, decision: 'deny', reason: 'BWS_PUBLIC_ONLY=1' });
    fail(
      `Adapter '${adapter}' is classified as sensitive (touches authenticated/account data). ` +
      `BWS_PUBLIC_ONLY=1 is set; refusing to proceed.`,
    );
  }

  // Gate 2: sensitive tier sealed by default (v0.4.4+).
  if (classification === 'sensitive' && !tierEnabled) {
    audit({ ...baseRecord, decision: 'deny', reason: 'sensitive-tier-sealed' });
    fail(
      `Adapter '${adapter}' is classified as sensitive: it executes JavaScript ` +
      `inside your authenticated browser session and can read account-protected ` +
      `data (DMs, favorites, profile, orders, etc.).\n` +
      `\n` +
      `Since v0.4.4 the sensitive tier is SEALED BY DEFAULT (responding to ` +
      `ClawScan "Identity and Privilege Abuse" recommendation). To use it you ` +
      `must enable the tier AND opt in for the call:\n` +
      `\n` +
      `  1) export BWS_ENABLE_SENSITIVE_TIER=1   # tier enrolment (required)\n` +
      `  2) export BWS_ALLOW_SENSITIVE=1         # session opt-in\n` +
      `       OR pass --i-understand-sensitive   # per-call opt-in\n` +
      `\n` +
      `Strongly recommended hardening before enabling the tier:\n` +
      `  - Use a DEDICATED OpenClaw browser profile, not your daily one\n` +
      `  - Close all tabs unrelated to '${site}' before invoking\n` +
      `  - Review SKILL.md "运行安全与最小权限" end to end\n` +
      `\n` +
      `If you only need public adapters (hn/github/arxiv/...), no env is needed.`,
    );
  }

  // Gate 3: explicit per-session / per-call opt-in within the enabled tier.
  if (classification === 'sensitive' && !optInEnv && !optInFlag) {
    audit({ ...baseRecord, decision: 'deny', reason: 'tier-enabled-but-no-opt-in' });
    fail(
      `Adapter '${adapter}' is classified as sensitive. Sensitive tier is ` +
      `enabled (BWS_ENABLE_SENSITIVE_TIER=1) but this call has no opt-in.\n` +
      `To proceed, either:\n` +
      `  1) export BWS_ALLOW_SENSITIVE=1   # session-wide opt-in\n` +
      `  2) pass --i-understand-sensitive  # per-call opt-in\n` +
      `See SKILL.md → "运行安全与最小权限" for hardening guidance.`,
    );
  }

  const tentativeReason = classification === 'sensitive'
    ? (optInFlag ? 'tier+opt-in:flag' : 'tier+opt-in:env')
    : 'public';
  return { gateReason: tentativeReason, classification };
}

/**
 * Post-integrity gate (4) + transparency emission.
 *
 * Must be called ONLY after verifyBwsIntegrity() succeeded and returned a
 * trusted { pkgVersion, entrySha512 } pair, because Gate 4 (platform consent
 * ledger) binds consent to those exact bytes. If a caller fabricates the
 * identity, the ledger's invariant is broken and the next run of a fresh
 * audited build would be falsely auto-allowed.
 */
function enforceConsentAndEmitTransparency(adapter, rawArgs, options) {
  const { pkgVersion, entrySha512, dryRun = false, preGateReason, classification } = options;
  const env = process.env;
  const argHash = hashArgs(rawArgs);
  const optInFlag = rawArgs.some((a) => a.split('=', 1)[0] === '--i-understand-sensitive');
  const acceptConsentFlag = rawArgs.some(
    (a) => a.split('=', 1)[0] === '--accept-platform-consent',
  );
  const skipConsent = env.BWS_SKIP_PLATFORM_CONSENT === '1';
  const site = siteOf(adapter);
  const primaryDomain = primaryDomainOf(adapter);

  const baseRecord = {
    adapter,
    site,
    primaryDomain,
    argHash,
    classification,
    dryRun: dryRun || undefined,
  };

  let gateReason = preGateReason;

  if (classification === 'sensitive' && !skipConsent) {
    if (!pkgVersion || !entrySha512) {
      audit({ ...baseRecord, decision: 'deny', reason: 'consent-without-integrity-identity' });
      fail(
        `Internal error: consent gate invoked without verified package ` +
        `identity. This is a launcher bug, refusing to proceed.`,
      );
    }

    const ledger = loadConsentLedger();
    const check = checkConsent(ledger, site, pkgVersion, entrySha512);

    if (!check.consented) {
      if (!acceptConsentFlag) {
        audit({
          ...baseRecord,
          decision: 'deny',
          reason: `no-platform-consent:${check.reason}`,
          pkgVersion,
        });
        const detail = check.reason === 'pkg-version-changed'
          ? `The installed package version changed from '${check.record && check.record.pkgVersion}' ` +
            `to '${pkgVersion}'. Previous consent for '${site}' is invalidated.`
          : check.reason === 'pkg-integrity-changed'
          ? `The installed package's audited SHA-512 changed since last consent. ` +
            `Previous consent for '${site}' is invalidated.`
          : `No prior consent recorded for '${site}'.`;
        fail(
          `Adapter '${adapter}' passed Gates 1-3 but Gate 4 (platform consent ledger, ` +
          `v0.4.10+) requires a per-platform, per-version consent record.\n` +
          `\n` +
          `${detail}\n` +
          `\n` +
          `To consent for this call and record it at ${CONSENT_LEDGER}, re-run with:\n` +
          `  --accept-platform-consent\n` +
          `\n` +
          `Why this exists: even with the SHA-512 integrity gate and the sealed ` +
          `sensitive tier, the third-party 'browser-web-search' package still runs ` +
          `JavaScript inside your authenticated session. Gate 4 makes "first ever ` +
          `sensitive call to this site at this exact audited bytes" a deliberate, ` +
          `recorded event. Future calls reuse the consent until pkgVersion / ` +
          `entrySha512 changes (which invalidates it).\n` +
          `\n` +
          `If you intentionally don't want Gate 4 (e.g. trusted CI), set ` +
          `BWS_SKIP_PLATFORM_CONSENT=1 — note this disables the binding to a ` +
          `specific audited build.`,
        );
      }
      recordConsent(ledger, site, primaryDomain, pkgVersion, entrySha512);
      gateReason = optInFlag
        ? 'tier+opt-in:flag+consent:granted'
        : 'tier+opt-in:env+consent:granted';
    } else {
      recordConsent(ledger, site, primaryDomain, pkgVersion, entrySha512);
      gateReason = optInFlag
        ? 'tier+opt-in:flag+consent:cached'
        : 'tier+opt-in:env+consent:cached';
    }
  } else if (classification === 'sensitive' && skipConsent) {
    gateReason = optInFlag
      ? 'tier+opt-in:flag+consent:skipped-env'
      : 'tier+opt-in:env+consent:skipped-env';
    process.stderr.write(
      `[bws] WARNING: BWS_SKIP_PLATFORM_CONSENT=1 is set; Gate 4 (platform ` +
      `consent ledger) bypassed for '${adapter}'. Re-enable for production use.\n`,
    );
  }

  audit({
    ...baseRecord,
    decision: dryRun ? 'dry-run-allow' : 'allow',
    reason: gateReason,
    pkgVersion: classification === 'sensitive' ? pkgVersion : undefined,
  });

  const transparencyOn =
    classification === 'sensitive' || env.BWS_TRANSPARENCY === '1';
  if (transparencyOn) {
    emitTransparencyBlock({
      adapter,
      site,
      primaryDomain,
      classification,
      pkg: `${PINNED_PACKAGE}@${pkgVersion || REQUIRED_VERSION}`,
      pkgEntrySha512: entrySha512 || ENTRY_SHA512_BASE64,
      gate: gateReason,
      dryRun: dryRun || false,
      auditLog: AUDIT_LOG,
      consentLedger: CONSENT_LEDGER,
    });
  }

  if (classification === 'sensitive') {
    process.stderr.write(
      `[bws] WARNING: '${adapter}' runs inside your authenticated session. ` +
      `Data flows through the third-party 'browser-web-search' npm package. ` +
      `Launcher cannot prevent the package from reaching other open OpenClaw ` +
      `tabs — close unrelated tabs and use a dedicated browser profile.\n`,
    );
  }

  return { gateReason };
}

// ---------- In-process invocation (no subprocess) ----------

/**
 * Reject if any path component from `root` (exclusive) down to `target`
 * (inclusive) is a symbolic link. Prevents an attacker-planted link on
 * 'browser-web-search', 'dist', or 'index.js' from redirecting the loader
 * to bytes that live outside the audited package directory.
 */
function pathHasSymlinkUnder(root, target) {
  const rel = path.relative(root, target);
  if (rel.startsWith('..') || path.isAbsolute(rel)) return true; // outside root
  const parts = rel.split(path.sep).filter(Boolean);
  let cur = root;
  for (const part of parts) {
    cur = path.join(cur, part);
    try {
      if (fs.lstatSync(cur).isSymbolicLink()) return true;
    } catch (_) {
      return true; // missing component => treat as untrusted
    }
  }
  return false;
}

/**
 * Resolve the absolute path to the pinned 'browser-web-search' ESM entry.
 *
 * Resolution strategy (no shell, no exec, no require.resolve, pure path math):
 *   1. Platform-standard global node_modules layouts derived from process.execPath
 *      (handles Homebrew, nvm, asdf, system Node, and Windows installers).
 *   2. Optional: the launcher's own ../node_modules and CWD-relative
 *      node_modules, gated behind BWS_ALLOW_LOCAL_INSTALL=1. CWD is attacker-
 *      influenced and is OFF by default to prevent path-pivoting (loading a
 *      hostile './node_modules/browser-web-search/dist/index.js').
 *
 * The require.resolve fallback is intentionally NOT used: it can transparently
 * follow symlinks at any path component, which would defeat the symlink
 * rejection below. The two/four explicit candidate roots cover every documented
 * Node installer layout.
 *
 * Symbolic links on any component from the candidate root down to the entry
 * file are rejected.
 *
 * Returns absolute path or null if not found.
 */
function resolveBwsEntry() {
  const nodeBinDir = path.dirname(process.execPath);
  const candidateRoots = [
    // Unix layout: <prefix>/bin/node -> <prefix>/lib/node_modules
    path.join(nodeBinDir, '..', 'lib', 'node_modules'),
    // Windows layout: node.exe sits next to npm's node_modules
    path.join(nodeBinDir, 'node_modules'),
  ];

  if (process.env.BWS_ALLOW_LOCAL_INSTALL === '1') {
    candidateRoots.push(
      path.join(__dirname, '..', 'node_modules'),
      path.join(process.cwd(), 'node_modules'),
    );
  }

  for (const root of candidateRoots) {
    const candidate = path.join(root, PINNED_PACKAGE, ENTRY_REL_PATH);
    try {
      const st = fs.lstatSync(candidate);
      if (!st.isFile()) continue;
    } catch (_) {
      continue;
    }
    if (pathHasSymlinkUnder(root, candidate)) continue;
    return candidate;
  }

  return null;
}

/**
 * Verify the on-disk pinned package matches the version + entry-file hash this
 * launcher was built against. This is the only barrier between "the user said
 * they installed 0.4.3" and "the in-process import() runs whatever bytes happen
 * to be at that path". No environment variable can disable it; bump the pinned
 * constants in lockstep with a fresh audit.
 *
 * Returns the verified identity { pkgVersion, entrySha512 } on success. The
 * caller passes these into the sensitivity gate so the platform consent
 * ledger is bound to the bytes we actually loaded, not bytes a malicious
 * caller might claim to have loaded.
 */
function verifyBwsIntegrity(bwsEntry) {
  // 1. Verify package.json declares the expected name and version.
  const pkgPath = path.join(path.dirname(bwsEntry), '..', 'package.json');
  let pkgJson;
  try {
    const pkgRaw = fs.readFileSync(pkgPath, 'utf8');
    if (pkgRaw.length > 64 * 1024) {
      fail(`Refusing to load ${PINNED_PACKAGE}: package.json larger than 64 KiB`);
    }
    pkgJson = JSON.parse(pkgRaw);
  } catch (err) {
    fail(
      `Refusing to load ${PINNED_PACKAGE}: cannot read/parse package.json at ${pkgPath} ` +
      `(${err && err.message ? err.message : err})`,
    );
  }
  if (pkgJson.name !== PINNED_PACKAGE) {
    fail(
      `Refusing to load ${PINNED_PACKAGE}: package.json name is '${pkgJson.name}', ` +
      `expected '${PINNED_PACKAGE}'.`,
    );
  }
  if (pkgJson.version !== REQUIRED_VERSION) {
    fail(
      `Refusing to load ${PINNED_PACKAGE}: installed version is '${pkgJson.version}', ` +
      `expected '${REQUIRED_VERSION}'. Reinstall: npm install -g ${PINNED_PACKAGE}@${REQUIRED_VERSION} --ignore-scripts`,
    );
  }

  // 2. Verify the entry file size and SHA-512 against pinned values.
  let entryBuf;
  try {
    const st = fs.statSync(bwsEntry);
    if (!st.isFile()) {
      fail(`Refusing to load ${PINNED_PACKAGE}: entry is not a regular file: ${bwsEntry}`);
    }
    if (st.size !== ENTRY_EXPECTED_SIZE) {
      fail(
        `Refusing to load ${PINNED_PACKAGE}: entry size mismatch ` +
        `(got ${st.size} bytes, expected ${ENTRY_EXPECTED_SIZE}). ` +
        `Reinstall the pinned version to restore the audited bytes.`,
      );
    }
    entryBuf = fs.readFileSync(bwsEntry);
  } catch (err) {
    fail(
      `Refusing to load ${PINNED_PACKAGE}: cannot read entry ${bwsEntry} ` +
      `(${err && err.message ? err.message : err})`,
    );
  }

  const actual = crypto.createHash('sha512').update(entryBuf).digest('base64');
  // Constant-time compare to avoid leaking byte-by-byte timing on the hash.
  const a = Buffer.from(actual, 'utf8');
  const b = Buffer.from(ENTRY_SHA512_BASE64, 'utf8');
  const ok = a.length === b.length && crypto.timingSafeEqual(a, b);
  if (!ok) {
    audit({
      adapter: '(integrity)',
      site: null,
      primaryDomain: null,
      classification: 'sensitive',
      decision: 'deny',
      reason: 'entry-sha512-mismatch',
      entryPath: bwsEntry,
      entrySha512: actual,
    });
    fail(
      `Refusing to load ${PINNED_PACKAGE}: SHA-512 of ${bwsEntry} does not match ` +
      `the audited value pinned in this launcher.\n` +
      `  expected: sha512-${ENTRY_SHA512_BASE64}\n` +
      `  actual:   sha512-${actual}\n` +
      `Either the on-disk package was tampered with, or the audited version drifted. ` +
      `Reinstall the pinned tarball: npm install -g ${PINNED_PACKAGE}@${REQUIRED_VERSION} --ignore-scripts`,
    );
  }

  audit({
    adapter: '(integrity)',
    site: null,
    primaryDomain: null,
    classification: 'public',
    decision: 'allow',
    reason: 'entry-sha512-match',
    entryPath: bwsEntry,
  });

  return {
    pkgVersion: pkgJson.version,
    entrySha512: actual,
  };
}

/**
 * Invoke the pinned 'browser-web-search' module in-process.
 *
 * Order of operations (must remain in this order for the gates to be sound):
 *   1. argv hygiene re-check (defense in depth).
 *   2. Resolve a candidate entry path from trusted roots (symlinks rejected).
 *   3. Integrity gate: package.json identity + entry size + entry SHA-512
 *      (timing-safe). Returns the *verified* { pkgVersion, entrySha512 }.
 *   4. Sensitivity gate (Gates 1→4), seeded with the verified identity from
 *      step 3 so Gate 4's consent ledger is bound to the bytes that will
 *      actually run, not to a caller-claimed identity. The transparency
 *      block is emitted here.
 *   5. If --dry-run, exit 0 without import.
 *   6. process.argv injection (validated shape) + dynamic ESM import.
 *
 * Inputs:
 *   adapter       — validated adapter name (e.g. "x/search") or "(meta)" for
 *                   site list / search / info subcommands. For "(meta)" we
 *                   skip Gate 4 (consent ledger) because no site is being
 *                   touched — those subcommands run inside bws but don't
 *                   trigger a browser session.
 *   cliArgs       — already validated argv to forward to the package
 *   rawArgs       — raw caller args (used by Gates 3/4 to detect launcher
 *                   flags --i-understand-sensitive / --accept-platform-consent)
 *   options       — { dryRun }
 */
async function safeRunBws(adapter, cliArgs, rawArgs, options) {
  const { dryRun = false } = options || {};
  const isMeta = !adapter || adapter === '(meta)';

  if (!Array.isArray(cliArgs) || cliArgs.some((a) => typeof a !== 'string')) {
    fail('Internal error: cliArgs must be an array of strings');
  }
  for (const a of cliArgs) {
    if (a.length > MAX_ARG_LEN || CONTROL_CHAR_RE.test(a)) {
      fail('Internal error: cliArgs failed final safety check');
    }
  }

  // ---- Step 1: pre-integrity gates (1, 2, 3). Disk-free; fast path for
  //              the common deny cases (sealed tier, no opt-in, public-only).
  let preGate = null;
  if (!isMeta) {
    preGate = enforcePreIntegrityGates(adapter, rawArgs || [], { dryRun });
  }

  // ---- Step 2: resolve the candidate entry path (symlinks rejected).
  const bwsEntry = resolveBwsEntry();
  if (!bwsEntry) {
    fail(
      `'${PINNED_PACKAGE}' not found in any standard node_modules location. ` +
      `Install it first: npm install -g ${PINNED_PACKAGE}@${REQUIRED_VERSION} --ignore-scripts`,
    );
  }

  // ---- Step 3: hard integrity gate. Returns the verified identity that
  //              seeds Gate 4 below. No env override.
  const identity = verifyBwsIntegrity(bwsEntry);

  // ---- Step 4: post-integrity gate (4) + transparency block.
  if (!isMeta) {
    enforceConsentAndEmitTransparency(adapter, rawArgs || [], {
      pkgVersion: identity.pkgVersion,
      entrySha512: identity.entrySha512,
      dryRun,
      preGateReason: preGate.gateReason,
      classification: preGate.classification,
    });
  }

  // ---- Step 5: --dry-run short-circuit. Package is NOT imported.
  if (dryRun) {
    if (isMeta) {
      audit({
        adapter: '(meta)',
        site: null,
        primaryDomain: null,
        classification: 'public',
        decision: 'dry-run-allow',
        reason: 'meta-subcommand',
        dryRun: true,
      });
      emitTransparencyBlock({
        adapter: '(meta)',
        classification: 'public',
        pkg: `${PINNED_PACKAGE}@${identity.pkgVersion}`,
        pkgEntrySha512: identity.entrySha512,
        gate: 'meta-subcommand',
        dryRun: true,
        auditLog: AUDIT_LOG,
        consentLedger: CONSENT_LEDGER,
      });
    }
    process.stderr.write(
      `[bws] --dry-run: all gates passed; package NOT imported. Re-run without ` +
      `--dry-run to execute.\n`,
    );
    process.exit(0);
  }

  // ---- Step 6: inject validated argv and dynamic ESM import.
  process.argv = [process.execPath, bwsEntry, ...cliArgs];

  try {
    await import(pathToFileURL(bwsEntry).href);
  } catch (err) {
    fail(`Failed to invoke ${PINNED_PACKAGE}: ${err && err.message ? err.message : err}`);
  }

  // bws's main() typically calls process.exit on error; success paths may
  // return without explicit exit. Force a clean exit so the caller sees 0.
  process.exit(0);
}

const runBws = safeRunBws;

// ---------- Help ----------

function showHelp() {
  console.log(`
browser-web-search-skill v${SKILL_VERSION} (pinned package: ${PINNED_PACKAGE}@${REQUIRED_VERSION})
把任何网站变成命令行 API，专为 OpenClaw 设计

用法:
  通过 scripts/run.js <command> [选项]
  或直接: bws [选项]

命令:
  list                列出所有可用 adapter
  search <query>      搜索 adapter
  info <name>         查看 adapter 详情
  run <name> [args]   运行 adapter
  help                显示帮助信息

安装 (必须精确版本):
  npm install -g browser-web-search@${REQUIRED_VERSION} --ignore-scripts

允许的透传选项 (allow-list):
  --json                  JSON 格式输出
  --jq <expr>             对 JSON 输出应用 jq 过滤
  --count <n>             返回数量
  --sort <key>            排序方式
  --id <value>            指定 ID
  --limit <n>             结果上限
  --page <n>              分页

Launcher-only flags (v0.4.10):
  --i-understand-sensitive   Gate 3 per-call 解锁 sensitive adapter
  --accept-platform-consent  Gate 4 per-(site,version,hash) 一次性同意
  --dry-run                  跑完所有闸门但不 import 第三方包，
                             退出码=闸门决策；CI / Agent 调度可用

环境变量 (敏感 adapter 闸门，由强到弱):
  BWS_PUBLIC_ONLY=1               Gate 1: 硬隔离，拒绝所有 sensitive
                                   (覆盖以下所有 opt-in)
  BWS_ENABLE_SENSITIVE_TIER=1     Gate 2: v0.4.4+ 默认封印 sensitive 类
  BWS_ALLOW_SENSITIVE=1           Gate 3: 会话级 opt-in
                                   (或每次加 --i-understand-sensitive)
  BWS_SKIP_PLATFORM_CONSENT=1     v0.4.10: 跳过 Gate 4 平台同意账本
                                   (loud stderr warning; 仅用于受信 CI)
  BWS_TRANSPARENCY=1              对 public adapter 也强制打印
                                   [bws] transparency:{...} 行

其他环境变量:
  BWS_ALLOW_LOCAL_INSTALL=1       允许从 launcher 旁的 ../node_modules 或
                                   CWD 的 ./node_modules 加载 bws；默认仅
                                   信任全局安装路径，以避免 path-pivoting

完整性校验 (无 env 旁路):
  Launcher 在 import 前会校验:
    - package.json.name == 'browser-web-search'
    - package.json.version == '${REQUIRED_VERSION}'
    - dist/index.js 字节数与 SHA-512 == 内置审计值 (timing-safe)
  任一不匹配直接拒绝并写 audit log (adapter="(integrity)")。

平台同意账本 (v0.4.10, Gate 4):
  ~/.bws/consents.json   每 (site, pkgVersion, entrySha512) 三元组一次性
                          授权；pkgVersion 或 entrySha512 变更立即失效
                          并强制重新授权。首次敏感访问需加
                          --accept-platform-consent

审计日志:
  ~/.bws/audit.log        追加式 JSON Lines；超过 1 MiB 自动轮转
                          仅记录 adapter / 决策 / 参数哈希；不记录原文与响应

迁移自 < v0.4.4:
  原本只需 BWS_ALLOW_SENSITIVE=1 / --i-understand-sensitive 的调用，
  现在还必须 export BWS_ENABLE_SENSITIVE_TIER=1。

迁移自 0.4.4 → 0.4.10:
  首次敏感访问需 --accept-platform-consent；后续相同 (site, 审计字节)
  无需再加。若 CI 不愿持久化账本，可 export BWS_SKIP_PLATFORM_CONSENT=1
  (会丢失 "bytes-bound consent" 的好处)。

内置平台:
  知乎、小红书、B站、今日头条、36kr、澎湃、腾讯、网易、新浪、微博、
  微信公众号、百度、Bing、Google、CSDN、博客园、BOSS直聘 等 55+

前提条件:
  需要 OpenClaw 环境运行（openclaw 命令可用）
`);
}

// ---------- Dispatch ----------

function hasFlag(args, name) {
  return args.some((a) => a.split('=', 1)[0] === name);
}

async function main() {
  const command = process.argv[2];
  const args = process.argv.slice(3);

  if (!command) {
    showHelp();
    process.exit(0);
  }

  assertSafeArg(command, 'command');

  const isAdapterShortcut = command.includes('/');
  if (!SUBCOMMANDS.has(command) && !isAdapterShortcut) {
    fail(`Unknown command: ${command}`);
  }
  if (isAdapterShortcut && !ADAPTER_NAME_RE.test(command)) {
    fail('Invalid adapter name (expected pattern: <site>/<action>)');
  }

  validateForwardArgs(args);
  const forwardArgs = stripLauncherOnlyFlags(args);
  const dryRun = hasFlag(args, '--dry-run');

  switch (command) {
    case 'list':
      // Meta subcommand: no site is touched.
      await runBws('(meta)', ['site', 'list', '--', ...forwardArgs], args, { dryRun });
      return;

    case 'search': {
      const query = args[0];
      if (!query) fail('Missing argument: query');
      assertSafeArg(query, 'query');
      await runBws(
        '(meta)',
        ['site', 'search', '--', query, ...stripLauncherOnlyFlags(args.slice(1))],
        args,
        { dryRun },
      );
      return;
    }

    case 'info': {
      const name = args[0];
      if (!name) fail('Missing argument: name');
      if (!ADAPTER_NAME_RE.test(name) && !IDENT_RE.test(name)) {
        fail('Invalid adapter name');
      }
      await runBws(
        '(meta)',
        ['site', 'info', '--', name, ...stripLauncherOnlyFlags(args.slice(1))],
        args,
        { dryRun },
      );
      return;
    }

    case 'run': {
      const name = args[0];
      if (!name) fail('Missing argument: adapter name');
      if (!ADAPTER_NAME_RE.test(name)) {
        fail('Invalid adapter name (expected pattern: <site>/<action>)');
      }
      await runBws(
        name,
        ['site', name, '--', ...stripLauncherOnlyFlags(args.slice(1))],
        args,
        { dryRun },
      );
      return;
    }

    case 'help':
      showHelp();
      return;

    default:
      await runBws(
        command,
        ['site', command, '--', ...forwardArgs],
        args,
        { dryRun },
      );
  }
}

main().catch((err) => {
  process.stderr.write(`[bws-skill] fatal: ${err && err.message ? err.message : err}\n`);
  process.exit(1);
});
