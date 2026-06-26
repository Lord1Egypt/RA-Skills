---
name: clawguard
version: "1.0.0"
description: Security auditor for ClawHub skills. Run before installing ANY skill — scans SKILL.md and scripts for prompt injection, data exfiltration, shell injection, permission mismatches, and malicious patterns. Returns a PASS / WARN / FAIL verdict with a full breakdown. Triggers on phrases like "scan this skill", "is this skill safe", "audit skill", "check before installing", or "inspect clawhub skill".
homepage: https://github.com/Taha2053/clawguard
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      env: []
    files:
      - "scripts/*"
---

# ClawGuard — Security Auditor for ClawHub Skills

> **Scan before you install. Every time.**

The ClawHavoc attack (February 2026) put over 1,100 malicious skills on ClawHub — stealing SSH keys, crypto wallets, browser passwords, and opening reverse shells. 91% of them combined code malware with prompt injection. ClawGuard was built to make sure you never install one blindly.

ClawGuard is the first skill you install. Then use it to audit every skill after.

---

## External Endpoints

| Endpoint | Purpose | Data Sent |
|---|---|---|
| None | Fully local analysis | Nothing leaves your machine |

ClawGuard performs all analysis locally. No external API calls. No telemetry. No network access of any kind.

---

## Security & Privacy

- **Zero external calls.** All analysis happens on your local filesystem.
- **No credentials required.** No API keys, tokens, or env vars.
- **Read-only.** ClawGuard never writes to the target skill directory — it only reads.
- **Open source.** Every check is visible in `scripts/scan.py`. Read it before trusting it.

> **Trust Statement:** ClawGuard reads skill files on your local machine and outputs a report. Nothing is transmitted anywhere. You can verify this by reading `scripts/scan.py` before running.

---

## Model Invocation Note

ClawGuard is invoked when you ask OpenClaw to check, audit, scan, or inspect a skill before installing. You can also run it directly via `python3 skills/clawguard/scripts/scan.py <path-to-skill>`. OpenClaw will not invoke ClawGuard automatically without your request — it is always user-initiated.

---

## How to Use

### Via OpenClaw (natural language)
```
"Scan the skill at ./skills/some-skill before I install it"
"Is the weather skill safe to install?"
"Audit clawhub skill: capability-evolver"
"Check this skill directory for malicious patterns"
```

### Via CLI (direct)
```bash
python3 skills/clawguard/scripts/scan.py ./path/to/skill-folder
```

---

## What ClawGuard Checks

ClawGuard runs 7 checks across every skill it audits:

### 1. 🔴 Prompt Injection Detection
Scans SKILL.md for hidden instructions that try to hijack the AI agent — patterns like instruction-override patterns, jailbreak phrases, role-swap commands, and base64-encoded command strings.

### 2. 🔴 Data Exfiltration Detection
Scans all shell scripts for outbound data patterns — curl/wget to unknown domains, DNS tunneling, reverse shell patterns (bash -i, nc -e, /dev/tcp), and base64-encoded command execution.

### 3. 🔴 Shell Injection Risk
Checks for unsafe variable interpolation (unquoted $VAR in curl URLs), missing `set -euo pipefail`, raw user input passed to shell commands without sanitization.

### 4. 🟡 Permission Mismatch
Compares permissions declared in SKILL.md frontmatter against what scripts actually access. A skill that declares `env: []` but reads `$HOME/.ssh/` is a red flag.

### 5. 🟡 External Endpoint Audit
Extracts every URL and domain contacted in scripts. Cross-references against the External Endpoints table in SKILL.md. Flags undeclared endpoints.

### 6. 🟡 Repository Trust Score
Evaluates: GitHub account age (must be 7+ days), repo star count, commit history depth, number of contributors, and time since last commit.

### 7. 🟢 Structure Compliance
Verifies the skill follows the ClawHub spec: valid SKILL.md frontmatter, correct `clawdbot` metadata key (not `openclaw`), semver version, and declared `files` field.

---

## Output Format

ClawGuard outputs a clean, readable report:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 CLAWGUARD REPORT — some-skill v1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERDICT: ✅ PASS  (or ⚠️ WARN or ❌ FAIL)

CHECK RESULTS:
  ✅ No prompt injection patterns detected
  ✅ No data exfiltration patterns detected
  ✅ No shell injection risks detected
  ✅ Permissions match declared scope
  ⚠️  1 undeclared endpoint found: api.example.com
  ✅ Repository trust signals: OK
  ✅ Structure compliant

FINDINGS:
  [WARN] scripts/fetch.sh line 12: URL contacts api.example.com
         Not declared in SKILL.md External Endpoints table.
         Recommend: verify this domain before installing.

RECOMMENDATION:
  This skill passes all critical checks. One minor warning
  requires manual review before installing.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Verdict Rules
- **✅ PASS** — All critical checks pass, 0-1 minor warnings
- **⚠️ WARN** — No critical failures, but 2+ warnings or 1 medium-severity finding
- **❌ FAIL** — Any critical finding: prompt injection, confirmed exfiltration, reverse shell, or credential theft pattern

---

## Severity Reference

| Finding | Severity | Verdict Impact |
|---|---|---|
| Prompt injection instruction | 🔴 Critical | FAIL |
| Reverse shell pattern | 🔴 Critical | FAIL |
| Base64-encoded shell execution | 🔴 Critical | FAIL |
| Credential/key exfiltration | 🔴 Critical | FAIL |
| Undeclared external endpoint | 🟡 Medium | WARN |
| Missing `set -euo pipefail` | 🟡 Medium | WARN |
| Unquoted variable in curl URL | 🟡 Medium | WARN |
| Missing security manifest | 🟡 Low | WARN |
| Wrong metadata key (`openclaw` vs `clawdbot`) | 🟢 Info | Note |
| Missing `homepage` field | 🟢 Info | Note |

---

## Example Interactions

```
"Scan ./skills/new-skill I just downloaded"
→ Runs full audit, outputs structured report, gives install recommendation

"Is the gog skill safe?"
→ Locates installed gog skill, scans it, outputs verdict

"Check all my installed skills for issues"
→ Scans every directory under ./skills/, outputs summary table

"Scan this skill and explain any warnings in plain English"
→ Outputs report with plain-language explanations of each finding
```

---

## File Structure

```
clawguard/
├── SKILL.md              ← You are here
├── README.md             ← Install guide
└── scripts/
    └── scan.py           ← Core scanner (Python 3, stdlib only)
```

---

## Philosophy

ClawGuard is deliberately minimal:
- **One script.** `scan.py` uses Python 3 stdlib only — no pip installs, no dependencies.
- **Read-only.** It never modifies anything.
- **Local only.** It never phones home.
- **Transparent.** Every check is readable in plain Python. Audit the auditor.
