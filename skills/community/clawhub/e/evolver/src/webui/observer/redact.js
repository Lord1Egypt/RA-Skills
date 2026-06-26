'use strict';

const SECRET_KEY_RE = /(secret|token|api[_-]?key|authorization|cookie|oauth|password|private[_-]?key|node_secret)/i;
// Three alternation arms, each with one capturing group so the replace()
// callback can keep the prefix and only mask the value:
//   1) HTTP Bearer auth header
//   2) Env/INI/CLI style NAME=value (or NAME: value) where NAME ends in
//      SECRET / TOKEN / KEY / PASSWORD / PASSWD / PWD. The original
//      regex only matched SECRET / TOKEN; without KEY / PASSWORD a line
//      like `OPENAI_API_KEY=sk-...` or `DB_PASSWORD=hunter2` would slip
//      through to the /webui/logs/evolver tail, leaking live credentials.
//   3) Bare OpenAI/Anthropic-shape API keys (`sk-...` / `sk-ant-...`) for
//      cases where they appear as standalone tokens in log lines without
//      a NAME= prefix.
// Flagged /gi so lower-case variants (`password=...`, `bearer ...`,
// `sk-...`) are also caught; over-redacting harmless prose tokens like
// "monkey=" is acceptable, leaking a real key is not.
const SECRET_TEXT_RE = new RegExp([
  '(Bearer\\s+)[A-Za-z0-9._~+/-]+=*',
  '([A-Za-z0-9_]*(?:SECRET|TOKEN|KEY|PASSWORD|PASSWD|PWD)[A-Za-z0-9_]*\\s*[:=]\\s*)["\']?[^\\s,"\'`]+',
  '(sk-(?:ant-)?[A-Za-z0-9_-]{20,})',
].join('|'), 'gi');

function redactValue(value, depth = 0) {
  if (depth > 8) return '[REDACTED_DEPTH]';
  if (Array.isArray(value)) return value.map((entry) => redactValue(entry, depth + 1));
  if (!value || typeof value !== 'object') {
    return typeof value === 'string' ? redactText(value) : value;
  }

  const out = {};
  for (const [key, child] of Object.entries(value)) {
    if (SECRET_KEY_RE.test(key)) {
      out[key] = '[REDACTED]';
    } else if (isLargeSensitiveField(key, child)) {
      out[key] = '[REDACTED_SENSITIVE_DETAIL]';
    } else {
      out[key] = redactValue(child, depth + 1);
    }
  }
  return out;
}

function redactText(text) {
  if (typeof text !== 'string') return text;
  return text.replace(SECRET_TEXT_RE, (match, bearer, namedPrefix, bareKey) => {
    if (bearer) return `${bearer}[REDACTED]`;
    if (namedPrefix) return `${namedPrefix}[REDACTED]`;
    if (bareKey) return '[REDACTED]';
    return '[REDACTED]';
  });
}

function isLargeSensitiveField(key, value) {
  if (typeof value !== 'string') return false;
  if (!/(prompt|diff|content|transcript|message|raw)/i.test(key)) return false;
  return value.length > 500;
}

module.exports = {
  redactValue,
  redactText,
};
