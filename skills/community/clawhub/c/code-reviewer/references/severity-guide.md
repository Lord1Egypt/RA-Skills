# Severity Classification Guide

## Overview

Every finding in a code review must be assigned a severity level. This guide defines the criteria for each level and provides examples to ensure consistent classification.

## Severity Levels

### Critical

**Definition:** Issues that allow attackers to execute arbitrary code, access unauthorized data, or cause system compromise. Must be fixed before merge/deploy.

**Criteria:**
- Remote Code Execution (RCE)
- SQL Injection with user-controllable input
- Authentication/Authorization bypass
- Hardcoded production credentials/secrets
- Deserialization of untrusted data leading to RCE
- Path traversal allowing arbitrary file read/write
- SSRF leading to internal network access

**Example:**
```javascript
// CRITICAL: SQL Injection - user input directly in query
app.get('/users', (req, res) => {
    db.query("SELECT * FROM users WHERE name = '" + req.query.name + "'");
});

// CRITICAL: Command Injection
const { exec } = require('child_process');
exec(`ls ${req.query.dir}`, (err, stdout) => { ... });

// CRITICAL: Hardcoded production database credentials
const DB_PASSWORD = "prod_db_p@ssw0rd_2024";
```

**Action Required:** Block merge. Fix immediately.

---

### High

**Definition:** Issues that could lead to data breaches, privilege escalation, or significant security weaknesses under certain conditions. Should be fixed before merge.

**Criteria:**
- Sensitive data exposure (PII, tokens, passwords in logs/responses)
- Missing authentication on sensitive endpoints
- Insecure deserialization (may not directly lead to RCE)
- Cross-Site Scripting (XSS) with user impact
- Missing input validation leading to unexpected behavior
- Race conditions in security-sensitive code
- Use of deprecated/insecure cryptographic functions for sensitive data

**Example:**
```python
# HIGH: Sensitive data logged
logger.info(f"User login attempt: email={user.email}, password={password}")

# HIGH: Missing auth on admin endpoint
@app.route('/admin/users/delete', methods=['POST'])
def delete_user():
    User.query.filter_by(id=request.json['id']).delete()
    db.session.commit()

# HIGH: XSS via dangerouslySetInnerHTML
<div dangerouslySetInnerHTML={{ __html: userProvidedContent }} />
```

**Action Required:** Strong recommendation to fix before merge. Justify any exceptions.

---

### Medium

**Definition:** Issues that degrade code quality, maintainability, or introduce minor security/performance concerns. Should be fixed but may not block merge if tracked.

**Criteria:**
- Weak password hashing (MD5/SHA1 for passwords)
- Missing rate limiting on authentication endpoints
- Debug mode enabled in configuration files
- N+1 query patterns
- Functions with high cyclomatic complexity (>15)
- Missing error handling for external calls
- Overly permissive CORS configuration
- Missing input length/format validation (non-security context)

**Example:**
```javascript
// MEDIUM: N+1 query pattern
users.forEach(user => {
    const orders = await db.query(`SELECT * FROM orders WHERE user_id = ${user.id}`);
});

// MEDIUM: Missing rate limiting on login
app.post('/login', loginHandler); // No rate limit middleware

// MEDIUM: Weak hashing
const hashedPassword = crypto.createHash('md5').update(password).digest('hex');
```

**Action Required:** Should fix in this PR or create a tracked follow-up issue.

---

### Low

**Definition:** Minor improvements to code quality, readability, or maintainability. Good to fix but not urgent.

**Criteria:**
- Naming inconsistencies (variable/function names)
- Missing or incomplete code comments/documentation
- Dead code (unused imports, variables, functions)
- Code duplication (small blocks)
- Magic numbers / strings
- Missing security headers (non-critical)
- Overly verbose implementation (can be simplified)
- Missing `.gitignore` entries for generated files

**Example:**
```javascript
// LOW: Dead code - unused import
import _ from 'lodash';  // never used in this file

// LOW: Magic number
if (retryCount > 3) { ... }  // What does 3 mean? Use MAX_RETRIES constant

// LOW: Naming inconsistency
const usrData = getUserData();  // should be userData or just userData
```

**Action Required:** Suggestion. Fix if convenient, otherwise note for future cleanup.

---

### Info

**Definition:** Observations, suggestions, and positive notes that don't require changes.

**Criteria:**
- Architectural suggestions for future consideration
- Alternative approaches worth considering
- Positive callouts (well-written code, good patterns)
- Questions about design decisions (not issues, just curiosity)
- Notes about technology updates or deprecations to be aware of
- Style preferences (not violations, just alternatives)

**Example:**
```
// INFO: Consider using a Set for O(1) lookups if this list grows large
const allowedUsers = ['alice', 'bob', 'charlie'];

// INFO: Good use of the repository pattern here - clean separation

// INFO: React 18's useTransition hook could improve UX for this heavy render
```

**Action Required:** No action needed. For the author's consideration.

---

## Severity Matrix

| Dimension | Critical | High | Medium | Low | Info |
|-----------|----------|------|--------|-----|------|
| **Security** | RCE, SQLi, Auth bypass | Data exposure, XSS | Weak crypto, no rate limit | Missing headers | Security best practice tip |
| **Performance** | - | Unbounded memory growth | N+1 queries, O(n^2) in hot path | Unnecessary computation | Algorithm optimization tip |
| **Code Quality** | - | - | High complexity, deep nesting | Dead code, naming | Alternative pattern suggestion |
| **Error Handling** | - | Unhandled critical path errors | Empty catch blocks | Missing error context | Custom error type suggestion |
| **Testing** | - | No tests on critical paths | Missing edge case tests | Test naming | Test organization tip |
| **Documentation** | - | - | Missing API docs on public interface | Missing inline comments | Doc improvement suggestion |

## Decision Flow

1. **Can this be exploited by an attacker to compromise the system?** → Critical
2. **Can this lead to data breach or unauthorized access?** → High
3. **Does this degrade security/performance/quality significantly?** → Medium
4. **Is this a minor quality or readability issue?** → Low
5. **Is this an observation or suggestion?** → Info
