# Reporting Examples

## Security Finding

```markdown
## [SEC-001] User-supplied redirect URL is trusted after login

- Category: security
- Location: `src/auth/login.ts:42-58`
- Severity: High
- Confidence: Medium
- Effort: S
- Priority: P1
- Refactorability Score: N/A

### Description
The login flow redirects to a request parameter without validating that it is an internal path.

### Evidence
The handler reads `next` from the query string and passes it directly to the redirect response.

### Impact
An attacker could craft a login URL that sends users to a malicious site after authentication.

### Recommendation
Allow only relative application paths or maintain an allowlist of trusted return hosts.

### Suggested Example
Parse the value with a safe URL helper and fallback to the dashboard when validation fails.

### Possible False Positive
This is lower risk if upstream middleware already rejects absolute URLs before this handler runs.
```

## Pattern Finding

```markdown
## [PAT-001] Payment provider branching is becoming a Strategy candidate

- Category: patterns
- Location: `src/billing/payments.ts:80-190`
- Severity: Medium
- Confidence: Medium
- Effort: M
- Priority: P2
- Refactorability Score: 68

### Description
Provider-specific behavior is mixed into one function with repeated branching for authorization, capture, refund, and error mapping.

### Evidence
The same `provider` switch appears across multiple payment operations and each branch calls different SDK methods.

### Impact
Adding a provider requires changing several branches in one high-risk file, increasing regression risk.

### Recommendation
Introduce a small provider strategy interface only for the repeated operations. Keep the current function as the orchestrator during migration.

### Suggested Example
Create `PaymentProviderStrategy` implementations for existing providers and move one operation at a time behind the interface.

### Possible False Positive
If no additional providers are planned and this code rarely changes, a smaller extraction may be enough.
```
