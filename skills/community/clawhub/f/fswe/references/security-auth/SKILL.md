# Security & Authentication

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| language | string | en | en, id |
| depth | string | standard | quick, standard, deep |
| auth-method | string | jwt | jwt, oauth2, session, api-key |

## Checklist

### Authentication
- [ ] Never store passwords in plain text — use bcrypt/argon2
- [ ] JWT: use short expiry (15min access, 7d refresh)
- [ ] Implement token rotation for refresh tokens
- [ ] Store tokens httpOnly + secure + sameSite
- [ ] Rate limit login attempts (5 per minute)
- [ ] Account lockout after repeated failures
- [ ] MFA for admin/privileged accounts

### Authorization
- [ ] Server-side role checks on every endpoint
- [ ] Never trust client-side role/permission claims
- [ ] Use RBAC or ABAC consistently
- [ ] Deny by default — explicit allow only
- [ ] Audit privilege escalation paths

### Input Validation
- [ ] Validate all input server-side (never trust client)
- [ ] Use schema validation (Zod, Joi, class-validator)
- [ ] Sanitize HTML to prevent XSS
- [ ] Parameterize SQL queries (never string concat)
- [ ] Limit request body size
- [ ] Validate Content-Type headers

### OWASP Top 10 Quick Check
| Risk | Mitigation |
|------|------------|
| Broken Access Control | Server-side auth checks on every route |
| Cryptographic Failures | Use TLS 1.3, strong ciphers |
| Injection | Parameterized queries, input validation |
| Insecure Design | Threat modeling, secure defaults |
| Security Misconfiguration | Hardened defaults, disable debug in prod |
| Vulnerable Components | `npm audit`, dependency scanning |
| Auth Failures | Rate limiting, MFA, secure session mgmt |
| Data Integrity | Signed commits, verified deps |
| Logging Failures | Audit logs for auth events |
| SSRF | Whitelist allowed URLs |

### Rate Limiting
```typescript
// Per-IP rate limiting
const limiter = new Map<string, { count: number; resetAt: number }>();

function checkRateLimit(ip: string, limit = 100, windowMs = 60_000): boolean {
  const now = Date.now();
  const entry = limiter.get(ip);
  if (!entry || now > entry.resetAt) {
    limiter.set(ip, { count: 1, resetAt: now + windowMs });
    return true;
  }
  if (entry.count >= limit) return false;
  entry.count++;
  return true;
}
```

### Security Headers
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `any` user input | Validate with Zod/Joi |
| Client-side auth checks | Always verify server-side |
| Long-lived JWT | 15min access, rotate refresh |
| Secrets in code | Use environment variables |
| No rate limiting | Implement per-IP/global limits |
