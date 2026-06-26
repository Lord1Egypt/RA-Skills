# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.1.x   | ✅ Yes    |
| < 1.1.0 | ❌ No — upgrade immediately |

## Reporting a Vulnerability

If you discover a security vulnerability in FlowClaw, **do not open a public GitHub issue.**

Contact: [@vanhuelsing](https://github.com/vanhuelsing) via GitHub private message or email.

Please include:
- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

You can expect a response within 48 hours and a patch within 7 days for confirmed critical issues.

## Security Guarantees (v1.1.0+)

See the **Security** section in [README.md](README.md) for a full description of all validation rules, authentication, credential isolation, and logging guarantees.

## Known Non-Guarantees

- **QA scripts are user-authored.** FlowClaw validates that they are `.py` files within the workflow directory, but cannot sandbox their runtime behaviour. Only install workflows from sources you trust.
- **YAML workflow files are trusted input.** FlowClaw validates the values extracted from YAML (agent IDs, paths, timeouts), but workflow files themselves are not authenticated — keep your workflow directory protected.
- **The `vercel` CLI is a trusted dependency.** FlowClaw executes it with a static argument list but cannot control what Vercel does with credentials in the environment.
