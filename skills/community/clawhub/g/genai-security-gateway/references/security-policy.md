# Security Policy

## Block Immediately

Block prompts that include likely API keys, direct requests to ignore previous instructions, developer-mode activation, DAN-style unrestricted behavior, hidden system prompt extraction, or roleplay that removes model memory and restrictions.

Reject non-string input and block inputs above the configured maximum length to reduce resource abuse in public deployments.

Fail closed when semantic scoring times out or raises an exception. Public gateways should prefer a conservative `BLOCK` over waiting indefinitely or forwarding unscored prompt content.

## Risk Levels

- `CRITICAL`: secret or credential leakage.
- `HIGH`: direct jailbreak, static bypass phrase, or semantic jailbreak score at or above threshold.
- `NONE`: no configured detector found a clear issue.
- `INVALID`: request shape is unsupported and should be corrected by the caller.

## Default Threshold

Use `0.78` for multilingual semantic similarity. Raise the threshold to reduce false positives; lower it to catch broader paraphrases.

## Result Contract

All checks should return:

- `is_safe`: boolean
- `risk_level`: string
- `reason`: human-readable explanation
- `suggested_action`: `PASS` or `BLOCK`
- `detector`: detector that produced the decision
- `semantic_score`: score when semantic scoring ran
- `semantic_threshold`: configured threshold
- `matched_template`: closest template when available
- `semantic_timeout_seconds`: configured semantic timeout

## Public Deployment Notes

Do not treat this detector as a complete security boundary. Use it as one layer before downstream LLM calls, and pair it with provider-side safety settings, output filtering, rate limits, request logging, abuse monitoring, and human review for high-risk workflows.
