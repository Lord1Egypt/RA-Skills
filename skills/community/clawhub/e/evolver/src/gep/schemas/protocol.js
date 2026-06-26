'use strict';

// ---------------------------------------------------------------------------
// Protocol Schema — single source of truth for ALL string literal enums that
// appear both in code (validation/normalization) and in the LLM prompt schema.
//
// Why this file exists: prior to 2026-05-16 the GEP prompt template (prompt.js)
// hardcoded its own copies of category/intent/risk_level/outcome.status enums.
// They drifted from src/gep/schemas/gene.js's VALID_CATEGORIES — when 'explore'
// was added to the engine's whitelist, it was silently dropped from the LLM
// prompt for months. v1.80.8 patched the literal; this module makes that class
// of bug structurally impossible by routing every prompt enum through here.
//
// Rule: if a string literal enum is referenced both in JS validation code AND
// in the prompt template, it MUST be defined here. NEVER duplicate it inline.
// ---------------------------------------------------------------------------

const {
  VALID_CATEGORIES,
  VALID_ROUTING_TIERS,
  VALID_REASONING_LEVELS,
  VALID_TOOL_POLICY_SEVERITIES,
} = require('./gene');
const { VALID_OUTCOME_STATUSES } = require('./capsule');

const VALID_RISK_LEVELS = ['low', 'medium', 'high'];
const VALID_TRACE_STAGES = ['build', 'validate', 'canary'];

// renderEnum: format an enum array as a pipe-joined string for prompt schemas.
// Example: ['repair', 'optimize', ...] -> 'repair|optimize|...'
function renderEnum(arr) {
  return arr.join('|');
}

// renderEnumList: format an enum array as a quoted JSON-ish list for prompt schemas.
// Example: ['build', 'validate', 'canary'] -> '"build","validate","canary"'
function renderEnumList(arr) {
  return arr.map((s) => '"' + s + '"').join(',');
}

module.exports = {
  VALID_CATEGORIES,
  VALID_OUTCOME_STATUSES,
  VALID_RISK_LEVELS,
  VALID_TRACE_STAGES,
  VALID_ROUTING_TIERS,
  VALID_REASONING_LEVELS,
  VALID_TOOL_POLICY_SEVERITIES,
  renderEnum,
  renderEnumList,
};
