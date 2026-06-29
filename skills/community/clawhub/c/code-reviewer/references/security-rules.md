# Security Vulnerability Detection Rules

## OWASP Top 10 Quick Reference

### A01 - Broken Access Control
| Pattern | Indicators | Languages |
|---------|-----------|-----------|
| Missing auth check | Route handler without auth middleware | All |
| IDOR | Direct object reference from user input without ownership check | All |
| Privilege escalation | Role check missing before sensitive operation | All |
| Force browsing | No authorization on API endpoints | All |

**Detection patterns:**
- Route definitions without `auth` / `requireAuth` / `@login_required` / `@Authorized`
- `req.params.id` / `request.getParameter("id")` used directly in DB query without ownership validation
- `isAdmin` check only on frontend, not backend

### A02 - Cryptographic Failures
| Pattern | Indicators | Languages |
|---------|-----------|-----------|
| Weak hashing | MD5, SHA1 used for passwords | All |
| Hardcoded secrets | API keys in source code | All |
| No encryption | Sensitive data stored/transmitted in plaintext | All |
| Weak randomness | `Math.random()` / `random.random()` for security tokens | All |

**Detection patterns (regex):**
```
# Hardcoded API keys
(api[_-]?key|secret|token|password)\s*[:=]\s*['"][A-Za-z0-9]{16,}['"]

# Weak hash algorithms
\b(MD5|SHA1|md5|sha1)\b.*password

# Insecure random
\b(Math\.random|random\.random)\(\).*token|session|password|key
```

### A03 - Injection
| Pattern | Indicators | Languages |
|---------|-----------|-----------|
| SQL Injection | String concatenation in SQL queries | All |
| Command Injection | User input in shell commands | All |
| LDAP Injection | String concat in LDAP queries | All |
| Template Injection | User input in template engine | All |

**Detection patterns:**
```
# SQL injection
(SELECT|INSERT|UPDATE|DELETE|DROP).*\+.*\$_(GET|POST|REQUEST)
query\s*\+\s*['"].*['"]\s*\+
execute\s*\(\s*['"].*\{.*\}.*['"]\s*\)

# Command injection
(os\.system|subprocess\.call|exec|child_process\.exec)\s*\(.*\+.*(input|req|param)
```

### A04 - Insecure Design
- Missing rate limiting on authentication endpoints
- No account lockout after failed login attempts
- Predictable URL patterns for sensitive resources
- Missing input validation (length, type, format, range)

### A05 - Security Misconfiguration
- Debug mode enabled in production (`DEBUG=True`)
- Detailed error pages in production (stack traces exposed)
- Default credentials not changed
- Unnecessary features enabled (directory listing, HTTP methods)

### A07 - Identification & Authentication Failures
- Weak password policy (no minimum length, complexity)
- Session ID in URL parameters
- Session fixation (session not regenerated after login)
- No session timeout

### A08 - Software & Data Integrity Failures
- Unsigned software updates
- Deserialization of untrusted data (`pickle.loads`, `yaml.load` without SafeLoader)
- Dependencies from untrusted sources

### A09 - Logging & Monitoring Failures
- Security events not logged (login, logout, password change, privilege changes)
- Logs not protected against tampering
- No alerting on suspicious activities

### A10 - Server-Side Request Forgery (SSRF)
- User-controlled URLs fetched server-side without validation
- No allowlist for outbound HTTP requests
- Internal IP ranges not blocked (`127.0.0.1`, `10.x`, `172.16-31.x`, `169.254.x`)

---

## Language-Specific Security Patterns

### JavaScript / TypeScript / Node.js
- `eval()` with any non-literal argument
- `child_process.exec` with string concatenation
- `dangerouslySetInnerHTML` with dynamic content
- `req.query` / `req.body` used in MongoDB queries without sanitization (NoSQL injection)
- `crypto.createHash('md5')` or `crypto.createHash('sha1')` for passwords
- `res.header('Access-Control-Allow-Origin', '*')` with credentials
- `express.static` without proper path restrictions
- Prototype pollution: `Object.assign` / spread operator with user input
- `new Function()` with user input
- `vm.runInNewContext()` with untrusted code

### Python
- `pickle.loads()` with untrusted data
- `yaml.load()` without `Loader=yaml.SafeLoader`
- `os.system()` / `subprocess.call(shell=True)` with user input
- `eval()` / `exec()` with user input
- `django.core.serializers` deserialization without validation
- `SECRET_KEY` hardcoded in settings
- `DEBUG = True` in production settings
- `makemigrations` with sensitive data in initial migrations
- `random` module used for security-sensitive operations (use `secrets`)

### Java
- `Runtime.getRuntime().exec()` with user input
- `Statement` instead of `PreparedStatement` for SQL
- `ObjectInputStream.readObject()` on untrusted data
- `XMLReader` without disabling external entities (XXE)
- `Spring` `@RequestMapping` without CSRF protection
- Hardcoded `DataSource` credentials
- `System.setProperty("com.sun.jndi.ldap.object.trustURLCodebase", "true")`

### Go
- `text/template` instead of `html/template` for HTML output
- `exec.Command` with user input as shell string
- `database/sql` with `fmt.Sprintf` for query construction
- `crypto/md5` or `crypto/sha1` for password hashing
- `ioutil.ReadFile` on user-controlled paths without validation

### PHP
- `mysql_query()` with string concatenation (use PDO prepared statements)
- `eval()`, `assert()`, `preg_replace` with `/e` modifier
- `unserialize()` on user input
- `$_GET` / `$_POST` / `$_REQUEST` used directly in SQL queries
- `file_get_contents()` on user-controlled URLs (SSRF)
- `extract()` on `$_GET` / `$_POST` (variable injection)

### C / C++
- `strcpy`, `strcat`, `sprintf` (use `strncpy`, `strncat`, `snprintf`)
- `gets()` (removed in C11, but legacy code may still use it)
- `system()` / `popen()` with user input
- `memcpy` without bounds checking
- Format string vulnerabilities: `printf(user_input)` instead of `printf("%s", user_input)`
- Buffer overflow: stack-allocated buffers with unchecked input size

### Rust
- `unsafe` blocks without safety justification comments
- `Command::new()` with user input without validation
- Raw pointer dereference without bounds checking
- `std::mem::transmute` misuse

---

## Secret Detection Patterns

### API Keys & Tokens
```
# AWS
AKIA[0-9A-Z]{16}
aws_secret_access_key\s*[:=]\s*['"][A-Za-z0-9/+=]{40}['"]

# GitHub
gh[pousr]_[A-Za-z0-9]{36}
github_token\s*[:=]\s*['"][A-Za-z0-9]{40}['"]

# Google
AIza[0-9A-Za-z\-_]{35}
ya29\.[0-9A-Za-z\-_]+

# Slack
xox[baprs]-[0-9A-Za-z-]+

# Stripe
sk_live_[0-9a-zA-Z]{24}
rk_live_[0-9a-zA-Z]{24}

# Generic
(api[_-]?key|secret|token|password|passwd|pwd)\s*[:=]\s*['"][^\s'"]{12,}['"]
-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----
```

### Database Connection Strings
```
(mongodb|postgresql|postgres|mysql|redis)://[^\s'"]*:[^\s'"]*@
```

---

## Severity Classification for Security Issues

| Severity | Criteria | Examples |
|----------|----------|---------|
| **Critical** | Remote code execution, SQL injection, auth bypass, hardcoded prod secrets | `eval(user_input)`, `os.system(req.query.cmd)` |
| **High** | Sensitive data exposure, privilege escalation, SSRF, deserialization flaws | `pickle.loads(request_data)`, missing auth on admin endpoints |
| **Medium** | Missing rate limiting, weak crypto, information disclosure | `md5(password)`, `DEBUG=True` in config |
| **Low** | Missing security headers, overly permissive CORS, minor info leak | `X-Frame-Options` missing, verbose error messages |
