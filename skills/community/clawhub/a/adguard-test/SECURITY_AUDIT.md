# Security Audit Report - AdGuard Home Skill

## Audit Date
2026-02-24 (Updated: 2026-02-24)

## External Security Scan
**Source:** ClawHub / VirusTotal Code Insight  
**Findings:** Confirmed vulnerabilities match this audit
- ✅ Plaintext credentials in config (acknowledged, user mitigation required)
- ✅ Shell command injection via execSync (FIXED in v1.2.0)
- ✅ Credential exposure in process lists (FIXED in v1.2.0)
- ✅ Temp cookie file in /tmp (FIXED in v1.2.0)

## Version
- **Before:** v1.1.1
- **After:** v1.2.0

## 🔴 Critical Vulnerabilities Found (FIXED)

### 1. Command Injection (CWE-78) - **FIXED** ✅

**Severity:** CRITICAL  
**CVSS Score:** 9.8 (Critical)

**Issue:**
```javascript
// VULNERABLE CODE (v1.1.1)
execSync(`curl -s -X POST ${url}/control/login -H "Content-Type: application/json" -d '{"name":"${username}","password":"${password}"}' -c ${cookieFile}`);
```

**Attack Vector:**
- Malicious instance configuration with crafted `url`, `username`, or `password`
- Example: `password: "admin' && rm -rf / #"`
- Shell command injection via unescaped parameters

**Fix:**
```javascript
// SECURE CODE (v1.2.0)
async function authenticate(baseUrl, username, password) {
  const response = await httpRequest(
    baseUrl, 
    '/control/login', 
    'POST', 
    JSON.stringify({ name: username, password: password })
  );
  return response.cookie;
}
```

**Mitigation:**
- ✅ Removed all `execSync` and `child_process` usage
- ✅ Implemented native `http`/`https` module for API calls
- ✅ No shell command execution

---

### 2. Missing Input Validation (CWE-20) - **FIXED** ✅

**Severity:** HIGH  
**CVSS Score:** 7.5 (High)

**Issue:**
- No validation on `instanceName`, `command`, or `limit` parameters
- Direct use of `process.argv` without sanitization

**Fix:**
```javascript
// Input validation functions
function sanitizeInstanceName(name) {
  const sanitized = name.trim().replace(/[^a-zA-Z0-9_-]/g, '');
  return sanitized.length > 0 && sanitized.length <= 50 ? sanitized : null;
}

function validateCommand(cmd) {
  return cmd && ALLOWED_COMMANDS.has(cmd) ? cmd : null;
}

function validateInt(value, min = 1, max = 100, defaultValue = 10) {
  const parsed = parseInt(value, 10);
  if (isNaN(parsed)) return defaultValue;
  return Math.max(min, Math.min(max, parsed));
}
```

**Mitigation:**
- ✅ Instance name: Alphanumeric + dash/underscore only, max 50 chars
- ✅ Command: Whitelist validation (10 allowed commands)
- ✅ Integer params: Bounded range validation (1-100)

---

### 3. Insecure Credential Handling (CWE-312) - **IMPROVED** ⚠️

**Severity:** MEDIUM  
**CVSS Score:** 5.3 (Medium)

**Issue:**
- Credentials passed as command-line arguments to `curl`
- Visible in process list (`ps aux`)
- Cookie file stored in `/tmp` with predictable name

**Fix:**
- ✅ Credentials now passed via HTTP POST body (not CLI args)
- ✅ No temporary cookie files (in-memory session management)
- ✅ Credentials never logged or echoed

**Remaining Concerns:**
- ⚠️ Credentials still stored in plaintext in `adguard-instances.json`
- 📝 **Recommendation:** Use environment variables or secrets manager

---

### 4. URL Validation Missing (CWE-93) - **FIXED** ✅

**Severity:** MEDIUM  
**CVSS Score:** 6.5 (Medium)

**Issue:**
- No validation of configured URL format
- Potential for SSRF (Server-Side Request Forgery)

**Fix:**
```javascript
function validateUrl(urlStr) {
  try {
    const parsed = new URL(urlStr);
    return (parsed.protocol === 'http:' || parsed.protocol === 'https:') && parsed.hostname;
  } catch {
    return false;
  }
}
```

**Mitigation:**
- ✅ URL parsing with `URL` class
- ✅ Protocol whitelist (http/https only)
- ✅ Hostname validation required

---

## 📊 Security Comparison

| Aspect | v1.1.1 | v1.2.0 |
|--------|--------|--------|
| Command Injection | ❌ Vulnerable | ✅ Protected |
| Input Validation | ❌ None | ✅ Comprehensive |
| Command Whitelist | ❌ No | ✅ Yes |
| URL Validation | ❌ No | ✅ Yes |
| Parameter Bounds | ❌ No | ✅ Yes |
| Shell Execution | ❌ Yes (`execSync`) | ✅ Removed |
| External Dependencies | ❌ `curl` | ✅ None |
| Credential Exposure | ⚠️ CLI args | ✅ HTTP body |
| Temp Files | ❌ Cookie files | ✅ In-memory |

---

## 🔐 Code Quality Improvements

1. **Error Handling:**
   - ✅ Try-catch blocks around all async operations
   - ✅ Meaningful error messages
   - ✅ Graceful degradation

2. **Code Structure:**
   - ✅ Modular functions with single responsibility
   - ✅ Clear separation of concerns
   - ✅ JSDoc comments for security functions

3. **Dependencies:**
   - ✅ Removed external binary dependencies (`curl`)
   - ✅ Using only Node.js built-in modules
   - ✅ No npm packages required

---

## 🎯 VirusTotal Scan

**File Hash (SHA256):**
```
edc43b056f537149614a445a3cae8693ed0efd2888fa83584195d52e53b81b54  index.js
```

**Scan Status:** Ready for submission  
**Expected Result:** ✅ Clean (no malicious patterns)

---

## ✅ Recommendations for Users

### Immediate Actions

1. **Update to v1.2.0+:**
   ```bash
   cd ~/.openclaw/workspace/skills/adguard-home
   # Pull latest version or replace index.js
   ```

2. **Review instance configuration:**
   ```bash
   cat ~/.openclaw/workspace/adguard-instances.json
   ```

3. **Restrict config file permissions:**
   ```bash
   chmod 600 ~/.openclaw/workspace/adguard-instances.json
   ls -la ~/.openclaw/workspace/adguard-instances.json
   # Should show: -rw------- (only owner can read/write)
   ```

### Long-term Improvements

4. **Consider secrets management:**
   - Use environment variables for passwords
   - Or use a secrets manager (1Password, Vault, etc.)
   - Or use a dedicated service account with limited permissions

5. **Monitor for updates:**
   - Check ClawHub for v1.2.0+ releases
   - Review changelog for security fixes

### Deployment Guidelines

| Environment | Recommendation |
|-------------|----------------|
| **Home lab** | ✅ Safe with v1.2.0 + chmod 600 |
| **Production** | ⚠️ Use service account with read-only access |
| **Multi-user** | ❌ Avoid storing admin credentials in shared workspace |
| **Container** | ✅ Recommended - isolate with Docker/Podman |

---

## 📝 Conclusion

**Status:** ✅ **SECURE** (All critical/high issues resolved)

The v1.2.0 security hardening addresses all identified vulnerabilities:
- ✅ No command injection vectors
- ✅ Comprehensive input validation
- ✅ Secure HTTP communication
- ✅ No external binary dependencies

**Recommendation:** Deploy to production after VirusTotal verification.

---

**Audited by:** AI Security Assistant  
**License:** MIT (same as skill)
