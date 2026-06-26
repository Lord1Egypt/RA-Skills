---
name: firm-fintech-pack
version: 1.0.0
description: >
  Curated skill bundle for fintech startups, neobanks, payment processors and
  wealth-management platforms. Activates the firm pyramid with Finance, Legal,
  Engineering and Compliance agents pre-configured for AML/KYC, financial modelling,
  regulatory reporting and payment infrastructure workflows.
author: romainsantoli-web
license: MIT
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    tools:
      - sessions_send
      - sessions_spawn
      - sessions_history
    primaryEnv: ""
tags:
  - fintech
  - neobank
  - payments
  - aml
  - kyc
  - psd2
  - firm-pack
  - sector
---

# firm-fintech-pack

Sector bundle for **fintech & financial services** environments.

## Activated departments

| Department | Services activated | Focus |
|---|---|---|
| Finance | FP&A · Pricing Strategy · Unit Economics · Billing | P&L, CAC/LTV, pricing models |
| Legal | Contracting · Privacy/Data · IP & Compliance | PSD2, MiCA, AML, KYC |
| Engineering | Backend · Data Engineering · AI Engineering · Integration | Core banking, APIs, ML models |
| Quality | Security · Compliance Auditing · Performance | Pen testing, SOC 2, load tests |
| Strategy | Architecture · Product Discovery · Roadmap | Product strategy, OKRs |
| Operations | SRE/Incident · DevOps | 99.99% uptime, incident response |

## Recommended ClawHub skills to install alongside

```bash
npx clawhub@latest install biz-reporter             # Financial KPI reporting
npx clawhub@latest install arc-security-audit       # SOC 2 / PCI-DSS audit
npx clawhub@latest install agent-audit-trail        # Tamper-evident transaction logs
npx clawhub@latest install arc-trust-verifier       # Counterparty verification
npx clawhub@latest install firm-orchestration       # A2A orchestration backbone
npx clawhub@latest install firm-delivery-export     # Output → report / ticket
```

## Firm configuration overlay

```json
{
  "agent": {
    "model": "anthropic/claude-opus-4-6",
    "workspace": "~/.openclaw/workspace/fintech-firm"
  },
  "agents": {
    "defaults": {
      "sandbox": { "mode": "non-main" }
    }
  }
}
```

## Prompt: AML suspicious activity review

```
Use firm-orchestration with:
  objective: "Review 23 flagged transactions from automated AML screening — Feb 28 batch"
  departments: ["legal", "finance", "quality"]
  constraints: ["anonymize customer IDs in output", "FATF Rec. 20 reference", "read-only"]
  definition_of_done: "SAR filing decisions per transaction with rationale"
  delivery_format: "structured_document"
```

## Prompt: pricing model update

```
Use firm-orchestration with:
  objective: "Redesign subscription tier pricing for B2B API product targeting SMBs"
  departments: ["finance", "commercial", "strategy"]
  constraints: ["current ARPU: €340/mo", "churn target < 3%", "competitor floor: €199/mo"]
  definition_of_done: "3-tier pricing proposal with margin analysis and migration plan"
  delivery_format: "project_brief"
```

## Regulatory coverage

| Regulation | Department | Service |
|---|---|---|
| PSD2 / Open Banking | Legal · Engineering | Compliance + Integration |
| MiCA (crypto) | Legal · Finance | IP & Compliance + FP&A |
| GDPR / ePrivacy | Legal | Privacy/Data Protection |
| AML 6AMLD | Legal · Quality | Contracting + Security |
| PCI-DSS | Quality · Engineering | Security · Backend |
| SOC 2 Type II | Quality · Operations | Compliance + DevOps |
| Basel III (credit) | Finance | Unit Economics & Reporting |

## Security notes

- Financial data is tier-1 sensitive: `SECURE_PRODUCTION_MODE=true` mandatory
- `AUDIT_ENABLED=true` with immutable JSONL audit trail
- `READ_ONLY_MODE=true` for all regulatory review workflows
- Sandbox all non-main sessions: `sandbox.mode: "non-main"`

---

## 💎 Support

Si ce skill vous est utile, vous pouvez soutenir le développement :

**Dogecoin** : `DQBggqFNWsRNTPb6kkiwppnMo1Hm8edfWq`
