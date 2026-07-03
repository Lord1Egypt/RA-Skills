'use strict';

// Shared classifier for unrecoverable host/LLM-provider *client* errors.
//
// When the host Agent layer (the IDE / agent that runs evolver) gets a 4xx-class
// rejection from its own LLM provider -- a malformed request (`field MaxTokens
// invalid, should be in [1, 65536]`), an auth failure (401), a hard quota /
// rate-limit denial -- every evolution attempt fails for a reason that has
// nothing to do with the Gene being run. Two subsystems must treat these the
// same way, so the classifier lives here as a single source of truth:
//
//   - issueReporter.js  -> does NOT file a public GitHub issue for them
//                          (it is not an evolver bug).
//   - signals.js        -> does NOT count them toward the consecutive-failure
//                          streak and does NOT ban the Gene; emits the
//                          actionable `host_llm_client_error` signal instead
//                          (see #571, follow-up to #534).
//
// None of the provider-specific strings below are emitted by evolver core
// (verified: no "LLM ERROR" / "MaxTokens" in src/), so their presence in a
// failure corpus means the host's provider call failed. The explicit 4xx
// markers are deliberately scoped to HTTP/status context (or an adjacent
// request/auth word) so a bare "400" elsewhere in a log cannot false-positive.
const HOST_PROVIDER_ERR_RE = /\bLLM ERROR\b|\bMaxTokens\b|field MaxTokens|max_tokens[^\n]{0,24}invalid|insufficient_quota|invalid_api_key|\brate limit(?:ed| exceeded)?\b|quota exceeded|context length exceeded|maximum context length|\bHTTP\s*4\d\d\b|\bstatus(?:\s*code)?\s*[:=]?\s*4\d\d\b|\b4\d\d\s+(?:bad request|unauthorized|forbidden)\b|\b(?:unauthorized|forbidden)\s*[:(]?\s*4\d\d\b/i;

// True when `text` contains a marker of an unrecoverable host/LLM client error.
// Stateless: HOST_PROVIDER_ERR_RE carries no /g flag, so .test() has no
// lastIndex side effect across calls.
function isHostClientError(text) {
  if (text == null) return false;
  return HOST_PROVIDER_ERR_RE.test(String(text));
}

module.exports = { HOST_PROVIDER_ERR_RE, isHostClientError };
