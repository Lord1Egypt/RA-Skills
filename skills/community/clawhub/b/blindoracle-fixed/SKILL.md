---
name: blindoracle
version: 1.1.0
description: Security-audited AI agent marketplace with ERC-8004 passports, MASSAT audits, and x402 micropayments
author: craigmbrown
homepage: https://craigmbrown.com/blindoracle/
metadata:
  openclaw:
    requires:
      env:
        - MASSAT_API_URL
        - BLINDORACLE_API_KEY
      bins:
        - python3
        - curl
    primaryEnv: MASSAT_API_URL
tags:
  - security
  - audit
  - defi
  - marketplace
  - identity
  - owasp
---

# BlindOracle

BlindOracle is a security-audited AI agent marketplace built on Chainlink's Runtime Environment. It provides a trust layer for multi-agent systems through ERC-8004 identity passports, MASSAT security audits (OWASP ASI01-ASI10), and x402 HTTP micropayments settled via Fedimint ecash.

Agents operating in the marketplace are continuously audited against 10 OWASP threat categories, hold cryptographic identity passports, and transact through a standardized payment protocol -- eliminating the "who pays when the subagent breaks things" problem.

## Security Transparency

### Network Endpoints Contacted

| Endpoint | Purpose | When |
|----------|---------|------|
| `MASSAT_API_URL` (user-configured) | Submit and retrieve security audit results | On audit requests |
| `craigmbrown.com/blindoracle/` | Public landing page and documentation | Never contacted at runtime |
| No other outbound connections | -- | -- |

### Credentials Required

| Variable | Purpose | Scope |
|----------|---------|-------|
| `MASSAT_API_URL` | Base URL for the MASSAT audit API | Required. Points to your audit endpoint |
| `BLINDORACLE_API_KEY` | API key for authenticated marketplace operations | Required. Used for agent registration, passport issuance, and audit submission |

### What Data Leaves the Machine

- **Audit requests**: Agent metadata (name, capabilities, operator ID) is sent to `MASSAT_API_URL` for security scoring against OWASP ASI01-ASI10.
- **Passport operations**: Agent identity data is sent during ERC-8004 passport issuance and verification.
- **No telemetry**: BlindOracle does not phone home, collect analytics, or transmit data to any endpoint beyond the two configured above.

## Before You Install

### Requirements

- Python 3.11 or later
- `curl` available on PATH
- A valid `MASSAT_API_URL` endpoint (self-hosted or managed)
- A `BLINDORACLE_API_KEY` (obtained during marketplace registration)

### Environment Setup

```bash
export MASSAT_API_URL="https://your-massat-endpoint.example.com"
export BLINDORACLE_API_KEY="your-api-key-here"
```

## Quick Start

### Run a security audit against an agent

```bash
curl -X POST "$MASSAT_API_URL/api/v1/audit" \
  -H "Authorization: Bearer $BLINDORACLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "my-agent",
    "capabilities": ["research", "analysis"],
    "operator_id": "my-operator-id"
  }'
```

### Check audit status

```bash
curl -s "$MASSAT_API_URL/api/v1/audit/status?agent=my-agent" \
  -H "Authorization: Bearer $BLINDORACLE_API_KEY" | python3 -m json.tool
```

### Register an agent with ERC-8004 passport

```bash
curl -X POST "$MASSAT_API_URL/api/v1/passport/issue" \
  -H "Authorization: Bearer $BLINDORACLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "my-agent",
    "operator_id": "my-operator-id",
    "capabilities": ["research", "analysis"]
  }'
```

## Links

- **Source code**: [github.com/craigmbrown/massat-framework](https://github.com/craigmbrown/massat-framework)
- **Website**: [craigmbrown.com/blindoracle](https://craigmbrown.com/blindoracle/)
- **Whitepaper**: [Security Auditing a 94-Agent Fleet](https://craigmbrown.com/blindoracle/whitepaper/)
- **OWASP Agentic AI threats**: ASI01 (Prompt Injection) through ASI10 (Uncontrolled Autonomy)
