# Security Policy

## Reporting a Vulnerability

BridgeNode is an agent-to-agent (A2A) platform. If you discover a security vulnerability, please report it privately:

- **Email:** eli.BNx@proton.me

Please do **not** open a public issue for security vulnerabilities.

## Supported Versions

| Version | Supported |
|---|---|
| latest | ✅ |

## Security Practices

- No API keys or registration required — payments via x402 (HTTP 402) with Solana USDC
- Wallet keys live only in `.env` — never committed
- Dependencies are audited regularly (pip-audit / npm audit)
- License: MIT-0 (MIT No Attribution)
