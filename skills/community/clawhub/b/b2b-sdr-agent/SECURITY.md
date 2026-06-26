# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

**Email**: security@pulseagent.io

**Do NOT** open a public GitHub issue for security vulnerabilities.

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 1 week
- **Fix or mitigation**: Depends on severity, targeting within 2 weeks for critical issues

## Security Best Practices for Users

### API Keys & Credentials

- Store API keys in `.secrets/env` or environment variables, never in workspace files
- Set `config.sh` permissions to `600` (`chmod 600 config.sh`)
- Use SSH keys instead of passwords for deployment
- Rotate `GATEWAY_TOKEN` periodically

### Network Security

- Set `GATEWAY_BIND=loopback` if the dashboard doesn't need LAN access
- Use a reverse proxy (nginx/Caddy) with TLS for production deployments
- Enable firewall rules to restrict gateway port access

### WhatsApp IP Isolation

- Each tenant should have its own WARP proxy for IP isolation
- Monitor wireproxy service health

### Data Protection

- Customer data (CRM, conversation history) should be treated as sensitive
- Enable `redactSensitive` in openclaw.json logging config
- For EU customers, ensure GDPR compliance (see AGENTS.md for data handling rules)

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | Yes       |

## Scope

This security policy covers:
- Deployment scripts (`deploy/`)
- Workspace context files (`workspace/`)
- Skills (`skills/`)
- Configuration templates

Third-party services (OpenClaw, MemOS, ChromaDB, Jina) have their own security policies.
