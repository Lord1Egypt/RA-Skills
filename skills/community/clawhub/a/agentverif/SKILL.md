---
name: agentverif
description: "SCAN → SIGN → VERIFY. Certify your skill, detect tampering, revoke instantly. Full control over how your skill is distributed and run. Requires AGENTVERIF_API_KEY for revoke."
homepage: https://agentverif.com
user-invocable: true
metadata: {
  "openclaw": {
    "emoji": "✅",
    "badge": "✅ AgentVerif Certified",
    "requires": { "anyBins": ["python3", "python"] }
  }
}
---

# ✅ AgentVerif — OWASP Scan + Cryptographic Verification

---
✅ AgentVerif Certified
⭐ Score: 100/100 · 🔑 AC-FA10-EB04
clawhub.ai/agentverif
---

**AgentVerif** is the trust layer for OpenClaw skills.
Every skill you install or distribute is scanned against the
OWASP LLM Top 10 and cryptographically verified —
so you know it's authentic, unmodified, and safe to run.

The former **AgentCop Sentinel** is now **AgentVerif** —
same battle-tested OWASP scanner, now with cryptographic
signing, tamper detection, and license revocation built in.

Install in one line:
```
npx clawhub@latest install agentverif
```

**Requires agentverif-sign (install once):**
```
pip install agentverif-sign
```
This skill never installs packages automatically.
You stay in control of your environment.

---

## What AgentVerif does

| Layer | What it catches | OWASP |
|-------|----------------|-------|
| **SCAN** | Prompt injection, credential leaks, insecure output, tool-call injection | LLM01, LLM02, LLM06, LLM08 |
| **SIGN** | Cryptographic hash + License ID — proves the skill is yours | — |
| **VERIFY** | Tamper detection — catches modified versions before execution | — |
| **REVOKE** | Kill a license instantly if the skill gets redistributed | — |

---

## Slash commands

### /security scan [--last 1h|24h|7d] [--since ISO]
Scan current session for OWASP LLM Top 10 violations.
Score 0–100. Below 70 = refused. Shows exact violations + fixes.

### /security verify <license_id_or_zip>
Verify a skill certificate against the agentverif.com registry.
Returns: VERIFIED / TAMPERED / UNSIGNED / EXPIRED / REVOKED

### /security sign <zip_path>
Sign a skill ZIP. OWASP scan runs first (score ≥ 70 required).
Injects SIGNATURE.json. Issues a License ID.

### /security revoke <license_id>
Revoke a license. Verification fails immediately for all buyers.
Requires AGENTVERIF_API_KEY environment variable.

### /security status
Reports that this skill is stateless — no local session data stored.
Run `/security scan` to get a live score.

### /security report
Full violation report grouped by severity (CRITICAL → ERROR → WARN).
Reads from stdin — pipe session context or text to scan.

### /security taint-check <text>
Check a string for LLM01 prompt injection. Exit 1 if tainted.

### /security output-check <text>
Check agent output for LLM02 insecure patterns.

### /security diff <session1> <session2>
Not supported — this skill is stateless and stores no session history.

### /security badge
Get your ✅ AgentVerif Certified badge for your skill listing.

---

## Privacy & data

**Network calls:** `scan`, `sign`, and `verify` transmit
data to `api.agentverif.com` via the `agentverif-sign`
Python package:
- `scan`: sends the skill ZIP for OWASP analysis
- `sign`: sends the skill ZIP to generate a certificate
- `verify`: sends the license ID to check registry status

Do not scan or sign ZIPs containing secrets you cannot
share with agentverif.com.

**Local persistence:** This skill itself writes no local files.
The `agentverif-sign` package may cache scan results —
see its source at github.com/trusthandoff/agentverif.

**API key:** `revoke` requires AGENTVERIF_API_KEY.
Use a scoped key. Never store in plaintext. Rotate if exposed.

**Source code:** All behavior is auditable at
[github.com/trusthandoff/agentverif](https://github.com/trusthandoff/agentverif)

---

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Clean — no violations, certificate valid |
| 1 | Violations detected or certificate invalid |
| 2 | Error — agentverif-sign not installed or bad arguments |

---

## Requirements

- OpenClaw ≥ 0.1
- Python ≥ 3.11
- `agentverif-sign >= 0.2.0`:
  `pip install agentverif-sign`

This skill never auto-installs packages.

---

Built by [agentverif.com](https://agentverif.com)
Source: [github.com/trusthandoff/agentverif](https://github.com/trusthandoff/agentverif)

---
✅ AgentVerif Certified
⭐ Score: 100/100 · 🔑 AC-FA10-EB04
clawhub.ai/agentverif
