# 🔍 clawguard

> Scan before you install. Every time.

![ClawHub](https://img.shields.io/badge/ClawHub-skill-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)
![No External Calls](https://img.shields.io/badge/external%20calls-none-brightgreen)
![Stdlib Only](https://img.shields.io/badge/dependencies-stdlib%20only-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

The ClawHavoc attack (February 2026) put over 1,100 malicious skills on ClawHub — stealing SSH keys, crypto wallets, and opening reverse shells. 91% combined code malware with prompt injection. ClawGuard makes sure you never install one blindly.

**Install this first. Then use it to audit every skill after.**

---

## Install

```bash
clawhub install clawguard
```

---

## Usage

### Via OpenClaw (natural language)
```
"Scan the skill at ./skills/some-skill before I install it"
"Is the gog skill safe to install?"
"Audit all my installed skills"
"Check this skill directory for malicious patterns"
```

### Via CLI (direct)
```bash
# Scan a single skill
python3 skills/clawguard/scripts/scan.py ./path/to/skill-folder

# Scan all installed skills at once
python3 skills/clawguard/scripts/scan.py ./skills --all

# JSON output (for scripting/CI)
python3 skills/clawguard/scripts/scan.py ./path/to/skill --json

# Exit code 1 on WARN (for strict CI pipelines)
python3 skills/clawguard/scripts/scan.py ./path/to/skill --fail-on-warn
```

---

## What It Checks

| Check | Severity | Catches |
|---|---|---|
| Prompt injection | 🔴 Critical | Jailbreak instructions hidden in SKILL.md |
| Reverse shells | 🔴 Critical | bash /dev/tcp, netcat -e, mkfifo patterns |
| Data exfiltration | 🔴 Critical | curl/wget uploads of local files to unknown hosts |
| Credential theft | 🔴 Critical | Access to ~/.ssh, ~/.aws, crypto wallets |
| Obfuscated execution | 🔴 Critical | eval base64 -d, encoded command substitution |
| Endpoint mismatch | 🟡 Medium | URLs in scripts not declared in SKILL.md |
| Shell injection risk | 🟡 Medium | Unquoted variables in curl URLs |
| Missing `set -euo pipefail` | 🟡 Medium | Scripts that hide errors |
| Missing security manifest | 🟠 Low | Undeclared file/network access scope |
| Metadata compliance | ℹ️ Info | Wrong key (`openclaw` vs `clawdbot`), missing homepage |

---

## Output Example

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 CLAWGUARD REPORT — some-skill v1.2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERDICT: ✅ PASS

CHECKS PASSED:
  ✅ No prompt injection patterns detected
  ✅ No data exfiltration or reverse shell patterns detected
  ✅ No shell injection risks detected
  ✅ External endpoints declared and cross-checked
  ✅ No sensitive file access patterns detected

RECOMMENDATION:
  This skill passed all critical checks. Safe to install.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Verdicts

- **✅ PASS** — All critical checks pass. Safe to install.
- **⚠️ WARN** — No critical failures, but manual review recommended.
- **❌ FAIL** — Critical security issue detected. Do not install. Report it on ClawHub.

---

## Security

ClawGuard is deliberately minimal and transparent:

- **Zero external calls.** All analysis is local. Nothing leaves your machine.
- **No credentials required.** No API keys, tokens, or env vars.
- **Read-only.** Never modifies the skill it's scanning.
- **Stdlib only.** `scan.py` uses Python 3 standard library. No pip installs.
- **Auditable.** Read `scripts/scan.py` before trusting it — it's ~400 lines of plain Python.

ClawGuard passes its own audit. Run it on itself: `python3 skills/clawguard/scripts/scan.py ./skills/clawguard`

---

## File Structure

```
clawguard/
├── SKILL.md          ← Core skill instructions for OpenClaw
├── README.md         ← This file
└── scripts/
    └── scan.py       ← Core scanner (Python 3 stdlib only)
```

---

## CI/CD Integration

Use ClawGuard in automated pipelines to gate skill installs:

```bash
# In your CI pipeline — fail if any skill has critical issues
python3 skills/clawguard/scripts/scan.py ./skills/new-skill
if [ $? -eq 2 ]; then
  echo "❌ Skill failed security scan. Blocking install."
  exit 1
fi
```

Exit codes: `0` = PASS, `1` = WARN (only with `--fail-on-warn`), `2` = FAIL

---

## License

MIT — use freely, modify, share, contribute.

---

## Contributing

Add new detection patterns, improve false positive handling, or add new check categories. Open a PR. Keep it stdlib-only and local-only — no external dependencies, ever.
