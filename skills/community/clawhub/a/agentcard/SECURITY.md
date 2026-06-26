# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.3.x   | ✅ Current |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly.

**DO NOT** open a public GitHub issue for security vulnerabilities.

### How to Report

1. Email: **<security@asgcard.dev>**
2. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

| Action | SLA |
|--------|-----|
| Acknowledgement | 24 hours |
| Initial assessment | 48 hours |
| Fix deployed | 7 business days (critical) |

### Scope

In scope:

- API endpoints (`api.asgcard.dev`)
- x402 payment flow
- Wallet signature authentication
- SDK (`@asgcard/sdk`)

Out of scope:

- Stellar network issues
- Third-party facilitator bugs
- Social engineering

## Security Practices

- All secrets managed via Vercel environment variables (never committed)
- HMAC webhook signature verification
- Ed25519 wallet signature authentication
- Kill-switch and rollback capability
- Gitleaks CI scanning on every push
