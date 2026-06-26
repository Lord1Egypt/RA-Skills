#!/usr/bin/env node
/**
 * A2WF Validator — validates siteai.json against the A2WF v1.0 spec.
 * Local validation only — no network requests.
 *
 * Usage:
 *   node validate.mjs /path/to/siteai.json
 *   node validate.mjs /path/to/siteai.json --audit
 *   echo '{"specVersion":"1.0",...}' | node validate.mjs --stdin
 */
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

// ── Known keys from the A2WF v1.0 spec ─────────────────────────
const READ_KEYS = ['productCatalog','pricing','availability','openingHours','contactInfo','reviews','faq','companyInfo'];
const ACTION_KEYS = ['search','addToCart','checkout','createAccount','submitReview','submitContactForm','bookAppointment','cancelOrder','requestRefund'];
const DATA_KEYS = ['customerRecords','orderHistory','paymentInfo','internalAnalytics','employeeData'];
const CORE_TOP = new Set(['@context','specVersion','identity','permissions','agentIdentification','scraping','defaults','humanVerification','legal','discovery','metadata','$schema']);
const REQUIRED_TOP = ['specVersion','identity','permissions'];
const REQUIRED_IDENTITY = ['domain','name','inLanguage'];

function isObj(v) { return v !== null && typeof v === 'object' && !Array.isArray(v); }
function isStr(v) { return typeof v === 'string' && v.trim().length > 0; }
function isUrl(v) { try { const u = new URL(v); return u.protocol.startsWith('http'); } catch { return false; } }

class Result {
  constructor() { this.errors = []; this.warnings = []; this.info = []; }
  e(path, msg) { this.errors.push({ severity: 'error', path, message: msg }); }
  w(path, msg) { this.warnings.push({ severity: 'warning', path, message: msg }); }
  i(path, msg) { this.info.push({ severity: 'info', path, message: msg }); }
  get valid() { return this.errors.length === 0; }
  get score() {
    const total = this.errors.length * 10 + this.warnings.length * 3 + this.info.length;
    return Math.max(0, 100 - total);
  }
}

function validate(doc, result) {
  if (!isObj(doc)) { result.e('$', 'Document must be a JSON object'); return; }
  for (const k of REQUIRED_TOP) {
    if (!(k in doc)) result.e(`$.${k}`, `Required field "${k}" is missing`);
  }
  if (doc.specVersion && doc.specVersion !== '1.0') {
    result.w('$.specVersion', `Expected "1.0", got "${doc.specVersion}"`);
  }
  if (isObj(doc.identity)) {
    for (const k of REQUIRED_IDENTITY) {
      if (!isStr(doc.identity[k])) result.e(`$.identity.${k}`, `Required field "${k}" is missing or empty`);
    }
    if (doc.identity.domain && !isUrl(doc.identity.domain)) result.w('$.identity.domain', 'Domain should be a valid HTTP(S) URL');
    if (!doc.identity.jurisdiction) result.w('$.identity.jurisdiction', 'No jurisdiction declared — reduces legal enforceability');
    if (!doc.identity.applicableLaw) result.i('$.identity.applicableLaw', 'Consider adding applicable laws (e.g., "GDPR", "EU AI Act")');
  }
  if (isObj(doc.permissions)) {
    validatePermGroup(result, 'read', doc.permissions.read, READ_KEYS);
    validatePermGroup(result, 'action', doc.permissions.action, ACTION_KEYS);
    validatePermGroup(result, 'data', doc.permissions.data, DATA_KEYS);
  }
  if (isObj(doc.defaults)) {
    if (doc.defaults.maxRequestsPerMinute !== undefined && (!Number.isInteger(doc.defaults.maxRequestsPerMinute) || doc.defaults.maxRequestsPerMinute < 0)) {
      result.e('$.defaults.maxRequestsPerMinute', 'Must be a non-negative integer');
    }
  }
  for (const k of Object.keys(doc)) {
    if (!CORE_TOP.has(k)) result.i(`$.${k}`, `Unknown top-level key "${k}" — agents must ignore it per spec`);
  }
}

function validatePermGroup(result, group, obj, knownKeys) {
  if (!obj) { result.i(`$.permissions.${group}`, `No "${group}" permissions defined`); return; }
  if (!isObj(obj)) { result.e(`$.permissions.${group}`, 'Must be an object'); return; }
  for (const [key, rule] of Object.entries(obj)) {
    const p = `$.permissions.${group}.${key}`;
    if (!knownKeys.includes(key)) result.w(p, `Unknown permission key "${key}" — agents must ignore per spec`);
    if (!isObj(rule)) { result.e(p, 'Permission rule must be an object'); continue; }
    if (typeof rule.allowed !== 'boolean') result.e(`${p}.allowed`, '"allowed" field is required and must be boolean');
    if (rule.rateLimit !== undefined && (!Number.isInteger(rule.rateLimit) || rule.rateLimit < 0)) {
      result.w(`${p}.rateLimit`, 'rateLimit should be a non-negative integer');
    }
  }
}

function audit(doc, result) {
  const critical = {
    'action.createAccount': doc.permissions?.action?.createAccount,
    'action.checkout': doc.permissions?.action?.checkout,
    'data.customerRecords': doc.permissions?.data?.customerRecords,
    'data.paymentInfo': doc.permissions?.data?.paymentInfo,
    'read.pricing': doc.permissions?.read?.pricing,
  };
  for (const [key, val] of Object.entries(critical)) {
    if (!val) result.w(`$.permissions.${key}`, `Critical permission "${key}" not explicitly set — defaults may not protect you`);
  }
  if (!doc.scraping) result.w('$.scraping', 'No scraping policy defined');
  if (!doc.legal) result.i('$.legal', 'No legal section — consider adding termsOfService and privacyPolicy URLs');
}

// ── CLI ─────────────────────────────────────────────────────────
const args = process.argv.slice(2);
const auditMode = args.includes('--audit');
const stdinMode = args.includes('--stdin');
const target = args.find(a => !a.startsWith('--'));

if (!target && !stdinMode) {
  console.error('Usage: node validate.mjs <file> [--audit]\n       echo \'...\' | node validate.mjs --stdin [--audit]');
  process.exit(2);
}

let doc;
try {
  let raw;
  if (stdinMode) {
    raw = readFileSync(0, 'utf-8'); // stdin
  } else {
    raw = readFileSync(resolve(target), 'utf-8');
  }
  doc = JSON.parse(raw);
} catch (err) {
  console.log(JSON.stringify({ valid: false, errors: [`Parse error: ${err.message}`] }, null, 2));
  process.exit(1);
}

const result = new Result();
validate(doc, result);
if (auditMode) audit(doc, result);

console.log(JSON.stringify({
  valid: result.valid,
  score: result.score,
  errors: result.errors,
  warnings: result.warnings,
  info: result.info,
  summary: result.valid
    ? `✅ Valid A2WF v1.0 document (score: ${result.score}/100)`
    : `❌ Invalid — ${result.errors.length} error(s) found`,
}, null, 2));
process.exit(result.valid ? 0 : 1);
