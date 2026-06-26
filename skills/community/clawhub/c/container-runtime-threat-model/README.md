# Container Runtime Threat Model Generator 🐳🔍

Generate comprehensive STRIDE-based threat models for containerized applications. Analyzes container images, privileges, host access, network exposure, security controls, and data sensitivity to identify threats and prioritize mitigations.

## Features

- **Per-Component Analysis** — Threat assessment for each container
- **STRIDE Framework** — Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation of Privilege
- **Attack Surface Mapping** — Privileged mode, host access, volume mounts, capabilities
- **Security Controls Check** — Seccomp, AppArmor, admission controllers, image scanning
- **Data Sensitivity** — PII, payment data, credential handling analysis
- **Compliance Mapping** — PCI-DSS, SOC2, HIPAA, CIS Benchmarks

## Quick Start

```bash
# Install via OpenClaw
clawhub install container-runtime-threat-model

# Set your API key
export TOOLWEB_API_KEY="your-key-from-portal.toolweb.in"
```

## Example

Ask your AI agent:
> "Threat model our payment service running on EKS with Node.js, Redis, and PostgreSQL containers. It handles PCI data."

## API

```
POST https://portal.toolweb.in/apis/security/crtmg
```

## Pricing

- Free: 5 calls/day
- Developer $39/mo: 20 calls/day
- Professional $99/mo: 200 calls/day
- Enterprise $299/mo: 100K calls/day

## Author

**ToolWeb.in** — CISSP & CISM certified | 200+ Security APIs

- 🌐 https://toolweb.in
- 🔌 https://portal.toolweb.in
- 📺 https://youtube.com/@toolweb-009
