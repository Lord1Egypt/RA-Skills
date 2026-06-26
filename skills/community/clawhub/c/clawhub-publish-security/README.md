# ClawHub Publish Security 🔒

**Mandatory security checklist before publishing any skill to ClawHub.**

This skill provides automated security scanning to prevent accidental exposure of sensitive information in published skills.

## ⚠️ CRITICAL RULES

**NEVER publish skills containing:**

| Category | Pattern | Example (❌ BAD) |
|----------|---------|-----------------|
| 📞 **Phone Numbers** | `+420`, `+1`, `+49`, etc. | `+420XXXXXXXXX` |
| 📁 **Personal Paths** | `Users\<name>`, `C:\<name>\` | `C:\<name>\ComfyUI` |
| 🔑 **API Keys** | `api_key=`, `apikey:`, `API_KEY=` | `api_key=sk-XXX...` |
| 🎫 **Tokens** | `token=`, `auth_token`, `bearer` | `token=ghp_XXX` |
| 📧 **Emails** | `*@*.com`, `*@*.cz` | `placeholder@placeholder.com` |
| 🔐 **Passwords** | `password=`, `passwd=`, `pwd=` | `password=XXX` |
| 🗝️ **Secrets** | `secret=`, `client_secret` | `secret=XXX` |

## 🚀 Quick Start

### Run Security Scan

```bash
# Scan a skill before publication
python skills/clawhub-publish-security/security-scan.py /path/to/skill

# Or from skill directory
cd skills/your-skill
python ../clawhub-publish-security/security-scan.py .
```

### Pre-Publish Checklist

Before running `clawhub publish`:

1. ✅ Run security scan
2. ✅ Review all config files
3. ✅ Check documentation examples
4. ✅ Verify code comments
5. ✅ Use placeholders for user-specific values

## 📋 Security Checklist

### 1. Phone Numbers ❌
```bash
# Search for phone patterns
Select-String -Path "skills/your-skill\*" -Pattern "\+420|\+1|\+49|\d{3}[-.]\d{3}[-.]\d{3}"
```

**Fix:** Replace with `<YOUR_PHONE_NUMBER>` or `<PHONE_NUMBER>`

### 2. Personal File Paths ❌
```bash
# Search for personal paths
Select-String -Path "skills/your-skill\*" -Pattern "Users\\[a-zA-Z]+|[a-zA-Z]+\\ComfyUI"
```

**Fix:** Use generic paths:
- ❌ `C:\<name>\ComfyUI`
- ✅ `C:\ComfyUI`
- ✅ `%COMFYUI_PATH%`
- ✅ `os.environ.get("COMFYUI_PATH")`

### 3. API Keys & Tokens ❌
```bash
# Search for API keys
Select-String -Path "skills/your-skill\*" -Pattern "api[_-]?key\s*[=:]\s*['\"][^'\"]+['\"]"
```

**Fix:** Use environment variables or placeholders:
- ❌ `api_key=sk-XXX`
- ✅ `api_key=os.environ.get("API_KEY")`
- ✅ `<YOUR_API_KEY>`

### 4. Email Addresses ❌
```bash
# Search for emails
Select-String -Path "skills/your-skill\*" -Pattern "[\w\.-]+@[\w\.-]+\.\w+"
```

**Fix:** Use placeholders:
- ❌ `placeholder@placeholder.com`
- ✅ `<YOUR_EMAIL>`

### 5. Passwords & Secrets ❌
```bash
# Search for passwords
Select-String -Path "skills/your-skill\*" -Pattern "password|passwd|pwd|secret"
```

**Fix:** Never include actual passwords:
- ❌ `password=XXX`
- ✅ `os.environ.get("PASSWORD")`
- ✅ `<YOUR_PASSWORD>`

## 🔍 Files to Review

### Always Check These Files:

| File Type | Risk | What to Look For |
|-----------|------|------------------|
| `*.py`, `*.js` | 🔴 High | Hardcoded credentials, paths |
| `*.json`, `*.yaml` | 🔴 High | Config values, API keys |
| `*.md` (docs) | 🟡 Medium | Examples with real values |
| `*.sh`, `*.ps1` | 🔴 High | Paths, credentials in scripts |
| `*.env.example` | 🟢 Safe | Should have placeholders |

### Safe to Include:

| Content | Status | Example |
|---------|--------|---------|
| Author name | ✅ OK | `"author": "Name (username)"` |
| Generic paths | ✅ OK | `C:\ComfyUI`, `~/.openclaw` |
| Placeholder values | ✅ OK | `<YOUR_API_KEY>`, `<YOUR_PHONE_NUMBER>` |
| Public URLs | ✅ OK | `https://github.com/...` |
| Environment variables | ✅ OK | `os.environ.get("API_KEY")` |

## 🛡️ Automated Scan

The `security-scan.py` script checks for:

```python
SENSITIVE_PATTERNS = {
    "phone_numbers": r"\+\d{1,3}[\s.-]?\d{3}[\s.-]?\d{3}[\s.-]?\d{3,4}",
    "personal_paths": r"Users\\[a-zA-Z]+|[a-zA-Z]+\\ComfyUI|/home/[a-zA-Z]+",
    "api_keys": r"(api[_-]?key|apikey)\s*[=:]\s*['\"][^'\"]+['\"]",
    "tokens": r"(token|auth_token|bearer|access_token)\s*[=:]\s*['\"][^'\"]+['\"]",
    "emails": r"[\w\.-]+@[\w\.-]+\.\w+",
    "passwords": r"(password|passwd|pwd|pass)\s*[=:]\s*['\"][^'\"]+['\"]",
    "secrets": r"(secret|client_secret|private_key)\s*[=:]\s*['\"][^'\"]+['\"]"
}
```

## 📊 Scan Output

### Clean Scan ✅
```
============================================================
[LOCK] ClawHub Publish Security Scanner
============================================================

[DIR] Scanning: skills/your-skill/

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

[DIR] Scanning: skills/your-skill/

[FAIL] Phone Numbers:     FOUND (1 issue)
   - config.json:15: "+420XXXXXXXXX"

[OK] Personal Paths:    CLEAN (0 found)
...

[FAIL] SECURITY ISSUES FOUND - Do NOT publish!
   Total issues: 1
============================================================

[INFO] How to fix:
   - Phone numbers: Replace with <YOUR_PHONE_NUMBER>

[FAIL] After fixing, re-run: python security-scan.py /path/to/skill
[OK] Only publish when ALL checks pass!
```

## 🚨 What to Do If Scan Fails

1. **DO NOT PUBLISH** - Fix issues first
2. **Replace with placeholders:**
   - Phone → `<YOUR_PHONE_NUMBER>`
   - Path → `C:\<APP>` or `%APP_PATH%`
   - API Key → `<YOUR_API_KEY>`
   - Email → `<YOUR_EMAIL>`
3. **Re-run scan** - Verify all issues fixed
4. **Then publish** - Only when scan is clean

## 📝 Pre-Publish Checklist

Before `clawhub publish`:

- [ ] Run `security-scan.py` - all checks pass
- [ ] Review `config.json` - no hardcoded values
- [ ] Review `skill.json` - no sensitive data
- [ ] Review `README.md` - examples use placeholders
- [ ] Review `SKILL.md` - examples use placeholders
- [ ] Review code files - no credentials
- [ ] Review scripts - no personal paths
- [ ] Test with fresh install - works without your data

## 🎯 Best Practices

### DO ✅
```python
# Use environment variables
api_key = os.environ.get("API_KEY")

# Use generic paths
comfyui_path = r"C:\ComfyUI"

# Use placeholders in docs
"target": "<YOUR_PHONE_NUMBER>"

# Use author attribution (safe)
"author": "Your Name (username)"
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

## 🔗 Related Tools

- **clawhub-smart-updater** - Update skills safely
- **openclaw-safe-audit** - Security audit for OpenClaw
- **edgeone-clawscan** - Tencent security scanner

## 📄 License

MIT-0 - Free to use, modify, and redistribute without attribution.

## 👥 Author

**Klepeto 🦞** (vilda)  
Created: 2026-05-07  
Purpose: Prevent security incidents in published skills

## Changelog

### 1.0.0 (2026-05-07)
- Initial release
- Automated security scanning
- Pre-publish checklist
- Pattern detection for sensitive data
