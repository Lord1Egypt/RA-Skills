# 🛡️ AgentVerif — OpenClaw Skill

OWASP LLM Top 10 scanner + cryptographic verification for every skill you install or distribute.

Install in one line:

```bash
npx clawhub@latest install agentverif
```

**Requires agentverif-sign (install once):**

```bash
pip install agentverif-sign
```

This skill never installs packages automatically. You stay in control of your environment.

---

## Commands

| Command | What it does |
|---------|-------------|
| `/security scan` | Scan current session for OWASP LLM Top 10 violations (score 0–100) |
| `/security verify <license_id_or_zip>` | Verify a skill certificate — VERIFIED / TAMPERED / UNSIGNED / REVOKED |
| `/security sign <zip_path>` | Sign a skill ZIP (OWASP scan runs first, score ≥ 70 required) |
| `/security revoke <license_id>` | Revoke a license instantly (requires AGENTVERIF_API_KEY) |
| `/security status` | Agent trust score, active violations, session fingerprint |
| `/security report` | Full violation report grouped by severity |
| `/security taint-check <text>` | Check a string for LLM01 prompt injection |
| `/security output-check <text>` | Check agent output for LLM02 insecure patterns |
| `/security diff <session1> <session2>` | Compare two scan sessions for regressions |
| `/security badge` | Get your ✅ AgentVerif Certified badge |

---

## OWASP Coverage

| Layer | What it catches | OWASP |
|-------|----------------|-------|
| **SCAN** | Prompt injection, credential leaks, insecure output, tool-call injection | LLM01, LLM02, LLM06, LLM08 |
| **SIGN** | Cryptographic hash + License ID | — |
| **VERIFY** | Tamper detection before execution | — |
| **REVOKE** | Kill a license instantly | — |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Clean — no violations, certificate valid |
| 1 | Violations detected or certificate invalid |
| 2 | Error — agentverif-sign not installed or bad arguments |

---

## Requirements

- OpenClaw ≥ 0.1
- Python ≥ 3.11
- `agentverif-sign >= 0.2.0`: `pip install agentverif-sign`

---

Built by [agentverif.com](https://agentverif.com)
