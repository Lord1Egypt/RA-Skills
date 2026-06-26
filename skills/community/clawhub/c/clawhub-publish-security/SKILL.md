# ClawHub Publish Security Skill 🔒

## Description

Mandatory security scanner for ClawHub skill publication. Automatically detects and prevents accidental exposure of sensitive information in skills before publication.

## When to Use This Skill

**ALWAYS run before `clawhub publish`:**

- Publishing your first skill
- Updating existing skills
- Any skill that contains configuration examples
- Scripts that handle credentials or paths

## Installation

```bash
# Install via ClawHub
clawhub install clawhub-publish-security

# The skill installs:
# - security-scan.py (automated scanner)
# - README.md (complete security guide)
# - SKILL.md (this file)
```

## Usage

### Quick Scan

```bash
# Scan a skill before publication
python skills/clawhub-publish-security/security-scan.py skills/your-skill

# Or from skill directory
cd skills/your-skill
python ../clawhub-publish-security/security-scan.py .
```

### Pre-Publish Workflow

```bash
# 1. Create your skill
cd skills/my-awesome-skill

# 2. Run security scan
python ../clawhub-publish-security/security-scan.py .

# 3. Fix any issues found

# 4. Re-run scan until clean
python ../clawhub-publish-security/security-scan.py .

# 5. Publish only when scan passes
clawhub publish . --slug my-awesome-skill
```

## What It Checks

### ❌ Blocked Patterns (Will Fail Scan)

| Type | Pattern | Example (❌ BAD) | Fix (✅ GOOD) |
|------|---------|-----------------|---------------|
| **Phone Numbers** | `+420...`, `+1...` | `+420XXXXXXXXX` | `<YOUR_PHONE_NUMBER>` |
| **Personal Paths** | `Users\name\` | `C:\COMFYUI` | `C:\ComfyUI` |
| **API Keys** | `api_key=XXX` | `api_key=sk-XXX` | `os.environ.get("API_KEY")` |
| **Tokens** | `token=XXX` | `token=ghp_XXX` | `<YOUR_TOKEN>` |
| **Emails** | `XXX@XXX.com` | `placeholder@placeholder.com` | `<YOUR_EMAIL>` |
| **Passwords** | `password=XXX` | `password=XXX` | `<YOUR_PASSWORD>` |
| **Secrets** | `secret=XXX` | `secret=XXX` | `<YOUR_SECRET>` |

### ✅ Allowed Patterns (Safe)

| Type | Example | Status |
|------|---------|--------|
| Placeholders | `<YOUR_PHONE_NUMBER>` | ✅ Safe |
| Env vars | `os.environ.get("API_KEY")` | ✅ Safe |
| Generic paths | `C:\ComfyUI`, `~/.openclaw` | ✅ Safe |
| Author name | `"author": "Name (user)"` | ✅ Safe |
| Public URLs | `https://github.com/...` | ✅ Safe |

## Output Examples

### Clean Scan ✅

```
============================================================
[LOCK] ClawHub Publish Security Scanner
============================================================

[DIR] Scanning: C:\Users\vilda\.openclaw\workspace\skills\your-skill

[OK] Phone Numbers:     CLEAN (0 found)
[OK] Personal Paths:    CLEAN (0 found)
[OK] API Keys:          CLEAN (0 found)
[OK] Tokens:            CLEAN (0 found)
[OK] Emails:            CLEAN (0 found)
[OK] Passwords:         CLEAN (0 found)
[OK] Secrets:           CLEAN (0 found)

[PASS] ALL CHECKS PASSED - Ready for publication!

[OK] You can now safely run: clawhub publish
```

### Failed Scan ❌

```
============================================================
[LOCK] ClawHub Publish Security Scanner
============================================================

[DIR] Scanning: C:\Users\vilda\.openclaw\workspace\skills\your-skill

[FAIL] Phone Numbers:     FOUND (1 issue)
   - config.json:15: "+420XXXXXXXXX"

[OK] Personal Paths:    CLEAN (0 found)
[OK] API Keys:          CLEAN (0 found)
...

============================================================
[FAIL] SECURITY ISSUES FOUND - Do NOT publish!
   Total issues: 1
============================================================

[INFO] How to fix:
   - Phone numbers: Replace with <YOUR_PHONE_NUMBER>

[FAIL] After fixing, re-run: python security-scan.py /path/to/skill
[OK] Only publish when ALL checks pass!
```

## Files to Scan

### Always Scan These:

| File | Risk Level | Common Issues |
|------|------------|---------------|
| `*.py`, `*.js` | 🔴 High | Hardcoded credentials |
| `config.json` | 🔴 High | API keys, tokens |
| `*.sh`, `*.ps1` | 🔴 High | Personal paths |
| `README.md` | 🟡 Medium | Example values |
| `SKILL.md` | 🟡 Medium | Config examples |

### Safe to Skip:

| File | Reason |
|------|--------|
| `*.md` (docs only) | Low risk, but still scanned |
| `LICENSE` | No credentials |
| `.gitignore` | No credentials |

## Integration

### OpenClaw Pre-Publish Hook

Add to your workflow:

```bash
# Before every publish
alias clawhub-publish="python skills/clawhub-publish-security/security-scan.py . && clawhub publish"

# Usage
clawhub-publish . --slug my-skill
```

### CI/CD Pipeline

```yaml
# GitHub Actions example
- name: Security Scan
  run: python skills/clawhub-publish-security/security-scan.py ./skills/my-skill

- name: Publish to ClawHub
  if: success()
  run: clawhub publish ./skills/my-skill
```

## Best Practices

### DO ✅

```python
# Environment variables
api_key = os.environ.get("API_KEY")

# Generic paths
comfyui_path = r"C:\ComfyUI"

# Placeholders in docs
"target": "<YOUR_PHONE_NUMBER>"

# Author attribution
"author": "Name (username)"
```

### DON'T ❌

```python
# Hardcoded credentials
api_key = "sk-XXX"

# Personal paths
comfyui_path = r"C:\<name>\ComfyUI"

# Real values in examples
"target": "+420XXXXXXXXX"
```

## Troubleshooting

### False Positive: Email in Author Field

**Problem:** Scanner flags email in author attribution

**Solution:** This is intentional - emails should not be in published skills. Use:
```json
"author": "Name (username)"
```

### False Positive: Generic Path

**Problem:** `C:\Program Files` flagged

**Solution:** This is a system path, should be safe. If flagged, report as bug.

### Scan Hangs

**Problem:** Scan takes too long

**Solution:** Check for large files or binary files. Add to `.gitignore`.

## Related Skills

- **clawhub-smart-updater** - Safe skill updates
- **openclaw-safe-audit** - Security audit for OpenClaw
- **edgeone-clawscan** - Tencent security scanner

## License

MIT-0 - Free to use, modify, and redistribute without attribution.

## Author

**Klepeto 🦞** (vilda)  
Created: 2026-05-07  
Purpose: Prevent security incidents in published ClawHub skills

## Changelog

### 1.0.0 (2026-05-07)
- Initial release
- Automated security scanning
- Pattern detection for 7 sensitive data types
- Pre-publish checklist
- CI/CD integration support
