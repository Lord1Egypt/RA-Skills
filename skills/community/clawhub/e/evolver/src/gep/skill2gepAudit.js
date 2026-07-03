'use strict';

// skill2gepAudit.js -- Mechanical leakage audit for skill2gep.
//
// This is a JS port of Gene-Bench's Stage-3 leakage audit
// (eval/evolve_genes_v3.py: build_private_vocab / find_mechanical_leakage /
// redact_private_literals). It is a PURELY mechanical set-difference: it never
// reasons about meaning, only about literals.
//
//   private tokens = (hard literals that appear in the run's HIDDEN text:
//                     the final solution, verifier feedback, raw stdout/stderr)
//                  - (hard literals that already appear in the PUBLIC SKILL.md)
//
// Any Gene string containing a private token is either redacted (default) or
// reported so the caller can refuse to publish. "Hard" literals are the ones
// most likely to encode an answer or a private contract constant:
//   - multi-digit numbers (single digits are ubiquitous scaffolding),
//   - quoted strings that look structured (identifiers, paths, enums),
//   - CLI flags (--foo),
//   - bare structured tokens (snake_case, dotted, slashed, SCREAMING_CASE).
//
// Public code contracts (file names, column names, CLI flags that appear in
// the Skill itself) are deliberately allowed through: forbidding them would
// make code Genes too vague to be useful, exactly as the reference notes.

const NUM_RE = /-?\d+(?:\.\d+)?/g;
const QUOTED_RE = /['"]([^'"]{2,64})['"]/g;
const CODE_SPAN_RE = /(?<!`)`([^`\n]{2,80})`(?!`)/g;
const FLAG_RE = /--[a-z][a-z0-9_-]*[a-z0-9]/g;
const WORD_RE = /[A-Za-z][A-Za-z0-9_]{2,}/g;
const BARE_STRUCTURED_RE =
  /(?<![A-Za-z0-9_./\\-])[A-Za-z0-9][A-Za-z0-9_./\\-]{1,80}(?![A-Za-z0-9_./\\-])/g;

// Generic English / Python / benchmark-scaffold stopwords. NOT domain-specific.
// Mirrors the reference _STOPWORDS set so the audit behaves the same.
const STOPWORDS = new Set([
  'the', 'and', 'for', 'with', 'that', 'this', 'from', 'into', 'your', 'you',
  'are', 'not', 'use', 'using', 'must', 'should', 'will', 'can', 'may', 'any',
  'all', 'each', 'one', 'two', 'given', 'input', 'output', 'value', 'values',
  'result', 'results', 'return', 'returns', 'function', 'functions', 'code',
  'task', 'tasks', 'test', 'tests', 'assert', 'import', 'def', 'class', 'self',
  'true', 'false', 'none', 'print', 'data', 'list', 'dict', 'string', 'str',
  'int', 'float', 'bool', 'file', 'files', 'path', 'line', 'lines', 'answer',
  'analysis', 'solution', 'program', 'python', 'run', 'running', 'expected',
  'actual', 'case', 'cases', 'example', 'examples', 'following', 'above',
  'below', 'number', 'numbers', 'set', 'get', 'name', 'names', 'format',
  'required', 'exactly', 'scenario', 'problem', 'compute', 'calculate',
]);

function isTrivialNumber(tok) {
  // Single-digit integers are loop bounds / "step 1" scaffolding and almost
  // always appear in the public text too; treating them as private only
  // creates false positives.
  if (tok.indexOf('.') !== -1) return false;
  const n = Number(tok);
  return Number.isInteger(n) && Math.abs(n) < 10;
}

function isStructuredLiteral(tok) {
  const s = String(tok || '').trim();
  if (!s) return false;
  if (new RegExp('^' + escapeRe(s) + '$').test(s) && NUM_RE_full(s)) {
    return !isTrivialNumber(s);
  }
  if (s.startsWith('--')) return true;
  if (/[0-9]/.test(s)) return true;
  if (s.indexOf('_') !== -1 || s.indexOf('.') !== -1 || s.indexOf('/') !== -1 || s.indexOf('\\') !== -1) return true;
  if (/^[A-Z][A-Z0-9_-]{2,}$/.test(s)) return true;
  return false;
}

// Helper: does the whole string parse as a single number? (re.fullmatch on _NUM_RE)
function NUM_RE_full(s) {
  return /^-?\d+(?:\.\d+)?$/.test(s);
}

function escapeRe(s) {
  return String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function words(text) {
  const out = new Set();
  const matches = String(text || '').match(WORD_RE) || [];
  for (const w of matches) {
    const lw = w.toLowerCase();
    if (!STOPWORDS.has(lw)) out.add(lw);
  }
  return out;
}

function alnumCount(s) {
  const m = String(s).match(/[a-z0-9]/gi);
  return m ? m.length : 0;
}

// Return { words: Set, hard: Set } where hard are leakage-relevant literals.
function contentTokens(text) {
  const t = String(text || '');
  const w = words(t);
  const hard = new Set();

  let m;
  NUM_RE.lastIndex = 0;
  while ((m = NUM_RE.exec(t)) !== null) {
    if (!isTrivialNumber(m[0])) hard.add(m[0]);
  }
  QUOTED_RE.lastIndex = 0;
  while ((m = QUOTED_RE.exec(t)) !== null) {
    const q = m[1].trim().toLowerCase();
    if (alnumCount(q) >= 3 && !STOPWORDS.has(q) && isStructuredLiteral(q)) hard.add(q);
  }
  CODE_SPAN_RE.lastIndex = 0;
  while ((m = CODE_SPAN_RE.exec(t)) !== null) {
    const q = m[1].trim().toLowerCase();
    if (alnumCount(q) >= 3 && !STOPWORDS.has(q) && isStructuredLiteral(q)) hard.add(q);
  }
  const flags = t.toLowerCase().match(FLAG_RE) || [];
  for (const f of flags) hard.add(f);

  return { words: w, hard: hard };
}

// Hard literals visible in the public SKILL.md. Public contracts are often
// written as bare structured strings (headings, prose), not just code spans,
// so we treat those as public too -- otherwise the audit would falsely reject
// useful code Genes that mention a file/column the solver is allowed to see.
function publicHardTokens(text) {
  const { hard } = contentTokens(text);
  const t = String(text || '');
  let m;
  BARE_STRUCTURED_RE.lastIndex = 0;
  while ((m = BARE_STRUCTURED_RE.exec(t)) !== null) {
    const tok = m[0].replace(/^[`'".,:;()[\]{}<>]+|[`'".,:;()[\]{}<>]+$/g, '').toLowerCase();
    if (alnumCount(tok) >= 2 && !STOPWORDS.has(tok) && isStructuredLiteral(tok)) hard.add(tok);
  }
  return hard;
}

// Concatenate the run's hidden text: the final solution plus any verifier
// feedback / stdout / stderr captured in the execution trace. These are the
// surfaces from which an agent might copy an answer constant into the Gene.
function hiddenBlob(execution) {
  const ex = execution || {};
  const parts = [];
  if (ex.final_solution) parts.push(String(ex.final_solution));
  if (ex.content_summary) parts.push(String(ex.content_summary));
  const trace = Array.isArray(ex.trace) ? ex.trace : [];
  for (const t of trace) {
    if (t && t.stdout_tail) parts.push(String(t.stdout_tail));
    if (t && t.stderr_tail) parts.push(String(t.stderr_tail));
  }
  const rollouts = Array.isArray(ex.rollouts) ? ex.rollouts : [];
  for (const r of rollouts) {
    if (r && r.feedback_tail) parts.push(String(r.feedback_tail));
  }
  // mutation_log error categories are copied verbatim into _source.overcame_errors
  // and paraphrased into preconditions, so any private constant embedded in an
  // error label (e.g. "threshold_202_exceeded") must be treated as a hidden
  // source. Plain snake_case names are not "hard" literals and never enter the
  // vocab, so this only catches genuinely private embedded constants.
  const mutationLog = Array.isArray(ex.mutation_log) ? ex.mutation_log : [];
  for (const e of mutationLog) parts.push(String(e || ''));
  return parts.join('\n');
}

// private = hidden hard tokens - public hard tokens.
function buildPrivateVocab(skillMd, execution) {
  const publicHard = publicHardTokens(skillMd);
  const { hard: hiddenHard } = contentTokens(hiddenBlob(execution));
  const out = new Set();
  for (const tok of hiddenHard) {
    if (!publicHard.has(tok)) out.add(tok);
  }
  return out;
}

// Walk every leaf string in a Gene payload, yielding [location, value].
function iterPayloadStrings(payload) {
  const out = [];
  const fields = ['summary', 'category'];
  for (const f of fields) {
    if (typeof payload[f] === 'string') out.push([f, payload[f]]);
  }
  for (const f of ['signals_match', 'strategy', 'preconditions', 'avoid', 'validation']) {
    const arr = payload[f];
    if (Array.isArray(arr)) {
      arr.forEach((v, i) => { if (typeof v === 'string') out.push([f + '[' + i + ']', v]); });
    }
  }
  // _source.overcame_errors is published metadata copied straight from
  // mutation_log; scan it too so an embedded private constant cannot ride
  // through there after the visible fields are redacted.
  const src = payload._source;
  if (src && Array.isArray(src.overcame_errors)) {
    src.overcame_errors.forEach((v, i) => {
      if (typeof v === 'string') out.push(['_source.overcame_errors[' + i + ']', v]);
    });
  }
  return out;
}

function tokenHits(value, tok) {
  const low = String(value).toLowerCase();
  if (alnumCount(tok) < 2) return false;
  if (/[a-z]/i.test(tok)) {
    return new RegExp('(?<![A-Za-z0-9_])' + escapeRe(tok) + '(?![A-Za-z0-9_])', 'i').test(low);
  }
  return new RegExp('(?<![A-Za-z0-9_.])' + escapeRe(tok) + '(?![A-Za-z0-9_.])').test(String(value));
}

// Return [{ token, location }] for every private literal found in the Gene.
function findLeakage(payload, privateVocab) {
  if (!privateVocab || privateVocab.size === 0) return [];
  const leaks = [];
  const seen = new Set();
  for (const [loc, value] of iterPayloadStrings(payload)) {
    for (const tok of privateVocab) {
      if (tokenHits(value, tok)) {
        const key = tok + '|' + loc;
        if (!seen.has(key)) { seen.add(key); leaks.push({ token: tok, location: loc }); }
      }
    }
  }
  return leaks;
}

function literalReplacement(tok) {
  if (NUM_RE_full(tok)) return 'the task-specific numeric value';
  if (tok.indexOf('/') !== -1 || tok.indexOf('\\') !== -1 || tok.indexOf('.') !== -1) return 'the task-specified file or path';
  if (tok.indexOf('_') !== -1) return 'the task-specific field';
  return 'the task-specific term';
}

function replaceLiteral(text, tok) {
  const replacement = literalReplacement(tok);
  if (/[a-z]/i.test(tok)) {
    return String(text).replace(new RegExp('(?<![A-Za-z0-9_])' + escapeRe(tok) + '(?![A-Za-z0-9_])', 'ig'), replacement);
  }
  return String(text).replace(new RegExp('(?<![A-Za-z0-9_.])' + escapeRe(tok) + '(?![A-Za-z0-9_.])', 'g'), replacement);
}

// Return a copy of the Gene with every private literal generalized. Longer
// tokens are replaced first so a shorter token can't partially clobber a
// longer one. Used only after a leak is detected; safer than discarding an
// otherwise-reusable payload.
function redactPrivateLiterals(payload, privateVocab) {
  const out = JSON.parse(JSON.stringify(payload));
  const toks = Array.from(privateVocab || []).sort((a, b) => b.length - a.length);
  // String fields. `category` is an enum so it never actually leaks, but we
  // process it anyway to stay symmetric with findLeakage (which scans it).
  for (const f of ['summary', 'category']) {
    if (typeof out[f] === 'string') {
      for (const tok of toks) out[f] = replaceLiteral(out[f], tok);
    }
  }
  for (const f of ['signals_match', 'strategy', 'preconditions', 'avoid']) {
    if (Array.isArray(out[f])) {
      out[f] = out[f].map((item) => {
        if (typeof item !== 'string') return item;
        let v = item;
        for (const tok of toks) v = replaceLiteral(v, tok);
        return v;
      });
    }
  }
  // Validation commands must stay runnable, so we cannot rewrite a private
  // literal into prose. Instead drop any command that contains one -- an empty
  // validation list is the correct, safe outcome (matches the Gene-Bench
  // contract that a Gene may legitimately have no validation).
  if (Array.isArray(out.validation)) {
    out.validation = out.validation.filter((cmd) => {
      if (typeof cmd !== 'string') return false;
      return !toks.some((tok) => tokenHits(cmd, tok));
    });
  }
  // _source.overcame_errors mirrors mutation_log; generalize private literals
  // embedded in an error label so the published metadata cannot leak them.
  if (out._source && Array.isArray(out._source.overcame_errors)) {
    out._source.overcame_errors = out._source.overcame_errors.map((item) => {
      if (typeof item !== 'string') return item;
      let v = item;
      for (const tok of toks) v = replaceLiteral(v, tok);
      return v;
    });
  }
  // Keep summary within the schema's 300-char ceiling after substitution.
  if (typeof out.summary === 'string' && out.summary.length > 300) {
    out.summary = out.summary.slice(0, 297).replace(/\s+$/, '') + '...';
  }
  return out;
}

module.exports = {
  contentTokens,
  publicHardTokens,
  buildPrivateVocab,
  iterPayloadStrings,
  findLeakage,
  redactPrivateLiterals,
  // exported for unit tests
  isStructuredLiteral,
  isTrivialNumber,
};
