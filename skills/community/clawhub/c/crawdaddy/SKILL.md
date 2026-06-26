# CrawDaddy - Post-Quantum Security Scanner

Autonomous security scanner for post-quantum cryptography readiness, smart contracts, and agent credential exposure.

## Overview

CrawDaddy scans code repositories, blockchain contracts, and agent skill packages for quantum-unsafe ECDSA usage and emerging infrastructure vulnerabilities. Built by **Quantum Shield Labs**.

### Target Audience

- **Healthcare CISOs** protecting patient data (50+ year sensitivity)
- **Blockchain developers** securing smart contracts on Ethereum/Base
- **Agent builders** securing MCP skills and autonomous agent infrastructure
- **Compliance officers** implementing post-quantum readiness programs

## Features

### 1. **Smart Contract Auditing**
Scan Ethereum and Base L2 smart contracts for quantum-vulnerable cryptographic primitives:
- ECDSA signature vulnerabilities (Shor's algorithm breakage)
- Known expiration dates on cryptographic keys
- Risk assessment for long-lived contracts
- Compatibility analysis for post-quantum alternatives

### 2. **Cryptographic Repository Scanning**
Analyze code repositories for:
- Quantum-unsafe cryptographic dependencies (ECDSA, RSA)
- Crypto usage patterns vulnerable to "harvest now, decrypt later" attacks
- Migration paths to post-quantum algorithms (NIST FIPS 203/204/205)
- Data sensitivity mapping (50+ year lifetime assets)

### 3. **Agent Credential Exposure Detection**
Scan AI agent skills and MCP packages for:
- Unencrypted API keys and signing credentials
- Long-lived tokens vulnerable to retroactive decryption
- Credential injection attack vectors
- Authentication protocol weaknesses

### 4. **Audit Trail & Compliance Reports**
Generate auditable, timestamped reports including:
- Detailed vulnerability inventory
- Risk scoring and remediation paths
- NIST post-quantum readiness checklist
- Healthcare/HIPAA compliance mapping

## Pricing

**Variable pricing based on scan complexity:**
- **$0.50** - Small projects (<10K LOC)
- **$1.50** - Medium projects (10K-100K LOC)
- **$3.00** - Large projects (100K-1M LOC)
- **$5.00** - Enterprise assessments + compliance reporting

## Contact & Support

- **Email:** crawdaddy@quantumshieldlabs.dev
- **Website:** https://quantumshieldlabs.dev/agent/
- **Wallet:** 0x25B50fEd69175e474F9702C0613413F8323809a8

## How It Works

1. **Submit** code repository URL or smart contract address
2. **CrawDaddy scans** for quantum vulnerabilities and crypto threats
3. **Report generated** with risk assessment and remediation steps
4. **Ongoing monitoring** available for critical infrastructure

## Example Use Cases

### Healthcare Data Protection
Healthcare organizations storing patient genetic data (50+ year retention):
```
Patient data with 50-year sensitivity
→ CrawDaddy identifies ECDSA encryption
→ Recommends post-quantum upgrade path
→ Generates HIPAA-compliant audit trail
```

### Smart Contract Auditing
DeFi protocols deploying long-lived contracts:
```
Ethereum contract with ECDSA wallet signatures
→ Scan identifies quantum expiration date
→ Report shows Shor's algorithm impact
→ Recommends multi-sig + migration timeline
```

### Agent Security
AI agent platforms using MCP skills:
```
Agent credentials stored in Redis
→ Scan detects unencrypted API keys
→ Analysis of key rotation policies
→ Recommendations for ephemeral credentials
```

## Technical Details

- **Scanning Engine:** Static analysis + LLM-assisted semantic review
- **Coverage:** Python, JavaScript/TypeScript, Solidity, Java, Go, Rust, C/C++
- **Output Formats:** JSON, PDF, HTML reports
- **Integration:** GitHub, GitLab, Blockchain RPC endpoints, AI agent platforms
- **Compliance:** SOC 2, GDPR, HIPAA-ready reporting

## Tags

security scanning, post-quantum cryptography, smart contracts, agent security, compliance, NIST PQC, ECDSA, healthcare, blockchain

## License

CrawDaddy services are provided under the terms of service at quantumshieldlabs.dev. Reports are proprietary to the customer.
