// ATP Question Composer
//
// Generates a natural-language buyer question from raw capability/signal
// inputs. autoBuyer previously concatenated signals into a string like
// "Capability gap detected by evolver: code_evolution,performance,..."
// which is uninformative to the merchant and produces poor answers.
//
// This module maps each known capability (or signal prefix) to a template
// that phrases the request as something a real buyer might ask. When no
// template matches, falls back to a generic "please help me with <caps>"
// phrasing. Templates deliberately stay concise (under 240 chars) so buyer
// budgets and merchant time are not wasted on padding.
//
// Templates are intentionally defensive: they never leak Evolver internals
// ("signals", "cycle", "mutation") into merchant-visible text.

const DEFAULT_MAX_LEN = 240;

const TEMPLATES = {
  code_evolution: [
    'I want to improve code quality on a small module. Please suggest one concrete, minimal patch I can apply, including the exact files, the change, and why it helps.',
    'I am iterating on a codebase and would like one high-leverage refactor suggestion. Be specific about the file, the current issue, and the proposed change.',
  ],
  performance: [
    'My app has a slow hot-path and I want one concrete optimization idea. Explain the likely bottleneck, propose a specific fix, and estimate the impact.',
    'I need help diagnosing a performance issue. Ask the right clarifying question if needed, or give me the top-3 most likely causes in priority order.',
  ],
  debugging: [
    'I am stuck on a bug and need a fresh pair of eyes. Walk me through a systematic debugging approach that would isolate the root cause in under an hour.',
    'Help me debug a tricky issue: please outline 3 reproduction strategies, each with the signals I should look for to confirm or rule out a hypothesis.',
  ],
  testing: [
    'I want to add tests to an under-tested module. Recommend the specific test cases (happy path, edge cases, regression) that give the best coverage per line of test code.',
    'Please review a typical testing gap for this kind of module and tell me the 3 test cases I probably missed.',
  ],
  documentation: [
    'I need to write user-facing documentation for a feature. Give me a concise outline and sample opening paragraph that sets expectations correctly.',
    'Help me rewrite a README section so it is clear to a first-time user. Focus on the smallest change that removes the most confusion.',
  ],
  refactoring: [
    'I want to refactor a module without changing behavior. Suggest the safest single-step refactor that reduces complexity, and what I should watch for during review.',
    'Please propose a refactoring plan I can apply in small commits, starting with the change that has the highest value/risk ratio.',
  ],
  security: [
    'Review a typical security concern for this kind of service and give me one actionable hardening I should implement first.',
    'I want a short security checklist for my app. List the top 5 issues to check in priority order, with the quickest mitigation for each.',
  ],
  data_analysis: [
    'I have a dataset and want to extract one useful insight. Recommend the analysis I should run first, the metric to compute, and how to interpret the result.',
    'Given a typical CSV of user events, which 3 analyses would most likely surface actionable patterns? Explain why for each.',
  ],
  architecture: [
    'Help me think through an architectural trade-off: I need to choose between two patterns for a small service. Give me the decision factors and a recommended default.',
    'I need a rough architecture sketch for a new feature. Describe the smallest viable design and list the 2 decisions that are easy to get wrong.',
  ],
  deployment: [
    'Help me set up a safe deployment path for my app. Outline the minimum CI/CD steps and the 3 most common pitfalls to avoid.',
    'I want to harden my deploy pipeline. Recommend the smallest change that most reduces the risk of a broken deploy reaching production.',
  ],
  general: [
    'I have a small task I would like an agent to help with. Please ask me the single most useful clarifying question, then outline how you would approach it.',
    'Please give me a concise, practical answer for a typical task in this capability. If context is needed, ask one focused clarifying question first.',
  ],
};

function _normalize(s) {
  return String(s || '').toLowerCase().replace(/[^a-z0-9_]+/g, '_').replace(/^_+|_+$/g, '');
}

function _pickTemplate(key, hashSeed) {
  const list = TEMPLATES[key] || TEMPLATES.general;
  if (!list || list.length === 0) return null;
  // Deterministic pick from a seed so the same signals yield the same
  // question across runs (plays nicely with autoBuyer's dedup hash).
  const n = Math.abs(Number(hashSeed) || 0) % list.length;
  return list[n];
}

function _hashFor(parts) {
  const s = Array.isArray(parts) ? parts.join('|') : String(parts || '');
  let h = 0;
  for (let i = 0; i < s.length; i++) {
    h = (h * 31 + s.charCodeAt(i)) | 0;
  }
  return h;
}

function _clip(s, maxLen) {
  const text = String(s || '').trim();
  const cap = Math.max(40, Number(maxLen) || DEFAULT_MAX_LEN);
  if (text.length <= cap) return text;
  return text.slice(0, cap - 3).replace(/\s+$/, '') + '...';
}

/**
 * Build a natural-language buyer question from capabilities + signals.
 *
 * @param {object} opts
 * @param {string[]} opts.capabilities -- buyer-side capability ids (first one picks the template)
 * @param {string[]} [opts.signals]    -- evolver signals (used as tiebreaker; never leaked verbatim)
 * @param {string}   [opts.fallback]   -- caller-provided fallback sentence
 * @param {number}   [opts.maxLen=240]
 * @returns {string} -- composed question (never empty)
 */
function compose(opts) {
  const capabilities = Array.isArray(opts && opts.capabilities) ? opts.capabilities : [];
  const signals = Array.isArray(opts && opts.signals) ? opts.signals : [];
  const maxLen = Number(opts && opts.maxLen) || DEFAULT_MAX_LEN;

  const keys = capabilities.map(_normalize).filter(Boolean);
  const primary = keys.find(function (k) { return TEMPLATES[k]; }) || keys[0] || 'general';
  const tmplKey = TEMPLATES[primary] ? primary : 'general';

  const seed = _hashFor(keys.concat(signals.slice(0, 4)));
  const tmpl = _pickTemplate(tmplKey, seed);

  if (tmpl) return _clip(tmpl, maxLen);

  // Generic fallback when TEMPLATES does not have `general` (defensive).
  const capsText = capabilities.length ? capabilities.slice(0, 3).join(', ') : 'a common task';
  const fb = (opts && opts.fallback && String(opts.fallback).trim())
    || 'I would like help with ' + capsText + '. Please provide one concrete, actionable answer.';
  return _clip(fb, maxLen);
}

module.exports = {
  compose,
  // exported for tests
  _normalize,
  _pickTemplate,
  _hashFor,
  TEMPLATES,
};
