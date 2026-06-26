# Explain findings to the user

Use this 5-section structure when explaining any finding.

---

## 1. Explanation Structure

For L1 rules with detailed explanations, load `{baseDir}/references/rule-deep-explainers.md` and use the matching section as the basis for sections C and D below. Adapt the tone and length to the user's question.

### A. One-liner (max 20 words)
Plain language summary of the problem. No jargon.

### B. Severity Context
- **CRITICAL** = "Highest risk, fix immediately"
- **HIGH** = "High risk, fix soon"
- **MEDIUM** = "Medium risk, plan to fix"
- **LOW** = "Low risk improvement suggestion"

### C. Why It Matters (2-3 sentences)
State what bad thing happens if not fixed. Use concrete subjects:
- Write "an attacker can..." not "there may be a risk."
- End with a user-perceivable consequence (data loss, takeover, exposure).

### D. Attack Scenario
- If `finding.attackScenario` exists, present as a 3-step chain: **Entry -> Exploit -> Impact**.
- If empty, construct a simplified scenario from `description`. Prefix with "One possible scenario:"

### E. How to Fix
- List `fixSuggestion` steps or remediation text.
- If `configBefore`/`configAfter` exist, show a diff.
- If `alternativeFix` exists, present as "Alternative approach:"

After presenting the fix suggestion, ask: "Would you like me to apply this fix?"

### F. Compensating Controls (if present)
Format: "Your setup already has [control] which [effectiveness] mitigates this, but root fix is still recommended."

---

## 2. Terminology Translation Table

Substitute these terms when explaining findings to users.

| Technical Term | Plain Language |
|---|---|
| bind to 0.0.0.0 | your AI gateway is open to the entire network, not just this machine |
| auth disabled / auth.mode = none | anyone can connect without a password |
| exec tool unrestricted | the AI can run any command on your computer with no limits |
| plaintext API key in config | your secret key is stored in plain text like a postcard anyone can read |
| allowlist / denylist | whitelist (only allow specific items) / blacklist (block specific items) |
| SSRF | the AI was tricked into accessing internal servers it shouldn't reach |
| DNS rebinding | an attacker tricks your browser into thinking it's visiting a safe site while actually accessing your internal network |
| prompt injection | someone hid instructions in input that tricked the AI into doing something it shouldn't |
| sandbox / isolation | a fence around the AI limiting what it can access |
| compensating control | a backup safety measure that partially covers the gap |
| token authentication | using a random secret key to verify identity (like a keycard) |
| loopback / localhost | only this machine can access itself; external devices cannot connect |
| CDP endpoint | Chrome DevTools Protocol -- a remote control interface for the browser |
| TLS | encrypted connection (like HTTPS) |
| CORS | rules controlling which websites can talk to your server |
| dangerouslyAllowNameMatching | using display names for identity -- anyone can fake a name to impersonate someone |
| session key / defaultSessionKey | a secret that separates different conversation sessions -- without it, sessions can bleed into each other |
| wildcard (*) in allowFrom | allowing literally anyone to send messages, no filtering at all |
| SBOM (Software Bill of Materials) | a list of all software components in your system, like an ingredients list |

---

## 3. "Can I Ignore This?" Response Logic

Never say "safe to ignore" even for LOW findings.

- **CRITICAL**: "Do not ignore. [one-liner]. Attackers need no special access to exploit this. Fix now -- usually one config line change."
- **HIGH**: "Serious risk. [explain the specific danger]. Fix this week."
- **MEDIUM**: "Improvement suggestion. OK to defer if in dev/test, but fix before production."
- **LOW**: "Best practice. Low priority but easy to fix. Handle when convenient."
- If `compensatingControls` with `effectiveness=full`: "Your [control] fully mitigates this for now, but still fix the root cause."
- If `relatedRuleEffects` with `amplifies`: "Also linked to [ruleId] -- fixing both together is more effective."

---

## 4. Cross-Rule Context

Check `relatedRuleEffects` when explaining any finding:

- **amplifies**: "This issue makes [other ruleId] worse."
- **mitigates**: "This partially covers [other ruleId]."
- **conflicts**: "Fixing this may conflict with [other ruleId]."

---

## 5. Environment-Aware Framing

If `environmentHint.environment` exists, adjust framing:

- **production** + confidence > 0.7: "In your production environment, this means..."
- **development**: "In your dev setup this is lower risk, but would be critical in production."
