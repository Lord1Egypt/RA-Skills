'use strict';

// ---------------------------------------------------------------------------
// Capsule Schema — single source of truth for the Capsule object shape.
// All modules that create or consume Capsule objects should use
// createCapsule() and validateCapsule() rather than assuming field presence.
// ---------------------------------------------------------------------------

const { SCHEMA_VERSION } = require('../contentHash');

const VALID_OUTCOME_STATUSES = ['success', 'failed'];
const VALID_SOURCE_TYPES = ['generated', 'reused', 'reference', 'user_authored'];
const VALID_VISIBILITIES = ['private', 'unlisted', 'public'];
const VALID_COST_TIERS = ['cheap', 'standard', 'premium'];

const CAPSULE_DEFAULTS = {
  type: 'Capsule',
  id: null,
  schema_version: SCHEMA_VERSION,
  trigger: [],
  gene: null,
  summary: '',
  confidence: 0,
  blast_radius: { files: 0, lines: 0 },
  outcome: { status: 'failed', score: 0 },
  success_streak: 0,
  success_reason: null,
  gene_library_version: null,
  env_fingerprint: null,
  source_type: null,
  reused_asset_id: null,
  // Real measured token cost of deriving this capsule (input+output), captured
  // from the proxy trace meter at solidify time. null when the proxy was
  // inactive or usage was unobserved (consumers fall back to an estimate).
  // Shape: { input_tokens, output_tokens, total_tokens, basis:'measured' }.
  derivation_tokens: null,
  a2a: { eligible_to_broadcast: false },
  content: null,
  diff: null,
  strategy: [],
  execution_trace: [],
  asset_id: null,
  // Spec 1.8.0 §Appendix C user-authored fields. All default to null
  // so a generated capsule emits the same on-wire shape it always has;
  // /capsule save in evox sets these explicitly.
  visibility: null,
  scope: null,
  cost_tier: null,
  pack_of: null,
  author: null,
};

// createCapsule: merge partial with defaults and normalize array/object fields.
// Safe to call with a fully-formed Capsule (idempotent).
function createCapsule(partial) {
  const c = Object.assign({}, CAPSULE_DEFAULTS, partial);

  // Fresh array copies — never hold references to CAPSULE_DEFAULTS arrays.
  c.trigger         = Array.isArray(c.trigger)         ? c.trigger.slice()         : [];
  c.strategy        = Array.isArray(c.strategy)        ? c.strategy.slice()        : [];
  c.execution_trace = Array.isArray(c.execution_trace) ? c.execution_trace.slice() : [];

  // Normalize blast_radius
  if (!c.blast_radius || typeof c.blast_radius !== 'object') {
    c.blast_radius = { files: 0, lines: 0 };
  } else {
    c.blast_radius = Object.assign({ files: 0, lines: 0 }, c.blast_radius);
  }

  // Normalize outcome
  if (!c.outcome || typeof c.outcome !== 'object') {
    c.outcome = { status: 'failed', score: 0 };
  } else {
    c.outcome = Object.assign({ status: 'failed', score: 0 }, c.outcome);
    if (!VALID_OUTCOME_STATUSES.includes(c.outcome.status)) {
      c.outcome.status = 'failed';
    }
  }

  // Normalize a2a
  if (!c.a2a || typeof c.a2a !== 'object') {
    c.a2a = { eligible_to_broadcast: false };
  } else {
    c.a2a = Object.assign({ eligible_to_broadcast: false }, c.a2a);
  }

  // Normalize derivation_tokens (optional measured-cost object). Coerce a
  // malformed value to null so it never trips downstream schema validation.
  if (c.derivation_tokens != null) {
    const d = c.derivation_tokens;
    if (typeof d !== 'object' || Array.isArray(d)) {
      c.derivation_tokens = null;
    } else {
      const inp = Number(d.input_tokens);
      const out = Number(d.output_tokens);
      const tot = Number(d.total_tokens);
      const safeInp = Number.isFinite(inp) && inp >= 0 ? inp : 0;
      const safeOut = Number.isFinite(out) && out >= 0 ? out : 0;
      c.derivation_tokens = {
        input_tokens: safeInp,
        output_tokens: safeOut,
        total_tokens: Number.isFinite(tot) && tot >= 0 ? tot : safeInp + safeOut,
        basis: typeof d.basis === 'string' ? d.basis : 'measured',
      };
    }
  }

  // Normalize string fields
  if (typeof c.summary !== 'string')        c.summary = '';
  if (typeof c.schema_version !== 'string') c.schema_version = SCHEMA_VERSION;
  if (typeof c.confidence !== 'number')     c.confidence = 0;

  // Normalize spec 1.8.0 §Appendix C fields. Schema declares
  // additionalProperties:false so any unrecognized value here would
  // fail validation downstream — coerce malformed inputs to null
  // rather than letting them propagate.
  if (c.visibility != null && !VALID_VISIBILITIES.includes(c.visibility)) {
    c.visibility = null;
  }
  if (c.scope != null && !Array.isArray(c.scope)) {
    c.scope = null;
  } else if (Array.isArray(c.scope)) {
    c.scope = c.scope.slice();
  }
  if (c.cost_tier != null && !VALID_COST_TIERS.includes(c.cost_tier)) {
    c.cost_tier = null;
  }
  if (c.pack_of != null && !Array.isArray(c.pack_of)) {
    c.pack_of = null;
  } else if (Array.isArray(c.pack_of)) {
    c.pack_of = c.pack_of.slice();
  }
  // author: schema requires both `handle` and `evox_install_id` when
  // the field is present. A partial pair (e.g. handle without
  // install_id) would fail schema validation, so drop it.
  if (c.author != null) {
    if (typeof c.author !== 'object' || !c.author.handle || !c.author.evox_install_id) {
      c.author = null;
    } else {
      c.author = { handle: c.author.handle, evox_install_id: c.author.evox_install_id };
    }
  }

  return c;
}

// validateCapsule: throw if required fields are missing or malformed.
// Use before broadcasting/publishing a Capsule to the Hub or writing to disk.
function validateCapsule(c) {
  if (!c || typeof c !== 'object')          throw new Error('Capsule must be an object');
  if (c.type !== 'Capsule')                 throw new Error('Capsule.type must be "Capsule", got: ' + c.type);
  if (!c.id || typeof c.id !== 'string')    throw new Error('Capsule.id is required and must be a string');
  if (!c.outcome || typeof c.outcome !== 'object')
                                            throw new Error('Capsule.outcome must be an object');
  if (!VALID_OUTCOME_STATUSES.includes(c.outcome.status))
                                            throw new Error('Capsule.outcome.status must be one of: ' + VALID_OUTCOME_STATUSES.join(', ') + ', got: ' + c.outcome.status);
  if (!Array.isArray(c.trigger))            throw new Error('Capsule.trigger must be an array');
  if (!Array.isArray(c.execution_trace))    throw new Error('Capsule.execution_trace must be an array');
  return true;
}

module.exports = {
  createCapsule,
  validateCapsule,
  CAPSULE_DEFAULTS,
  VALID_OUTCOME_STATUSES,
  VALID_SOURCE_TYPES,
  VALID_VISIBILITIES,
  VALID_COST_TIERS,
};
