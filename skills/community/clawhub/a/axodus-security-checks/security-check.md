# SKILL: security-check

## Purpose
Perform a security-focused review of code changes or a subsystem: secrets exposure, auth issues, injection risks, unsafe dependencies, and unsafe execution paths.

## When to Use
- Before deployment of a feature handling user input, money, or credentials.
- When introducing new dependencies or external integrations.
- After any authentication/authorization changes.

## Inputs
- `scope` (required, string): files/modules/diff to inspect.
- `threat_model` (optional, string): assets at risk and attacker capabilities.
- `languages` (optional, string[]): e.g., `["ts","py","solidity"]`
- `constraints` (optional, string[]): compliance rules or governance boundaries.

## Steps
1. Secrets & config:
   - ensure no tokens/keys are committed
   - ensure `.env.example` does not contain real secrets
2. Input handling:
   - validate and sanitize untrusted inputs
   - enforce schema validation at boundaries
3. Auth/authz:
   - verify authorization checks at every privileged action
   - avoid insecure defaults
4. Injection and unsafe execution:
   - command injection
   - SQL/NoSQL injection
   - XSS/CSRF (frontend)
   - dynamic code execution without validation
5. Dependencies:
   - flag risky packages
   - ensure versions are pinned when required
6. Observability:
   - logs do not leak secrets/PII
   - audit trail exists for sensitive actions

## Validation
- Findings are evidence-based and include remediation.
- Risk severity is calibrated (critical/high/medium/low).
- Safety constraints are explicitly enforced (not “recommended”).

## Output
Security report (example schema):
```yaml
summary: "<top risks>"
findings:
  - id: "SEC-001"
    severity: "high|medium|low"
    issue: "<what>"
    location: ["..."]
    remediation: "<how>"
```

## Safety Rules
- Do not disclose secrets that appear in logs/config; redact.
- Do not recommend disabling security controls to “unblock”.
- Escalate when the change touches money movement or governance.

## Example
Scope: “new webhook handler”
Output: flags missing signature verification and recommends replay protection + audit logs.

