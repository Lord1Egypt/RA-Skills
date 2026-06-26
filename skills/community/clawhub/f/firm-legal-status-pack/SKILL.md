---
name: firm-legal-status-pack
version: 1.0.0
description: >
  Legal status analysis and corporate structuring pack.
  Legal form comparison, tax simulation, social protection analysis,
  governance structuring, and compliance checklist. 5 legal status tools.
author: romainsantoli-web
license: MIT
metadata:
  openclaw:
    registry: ClawHub
    requires:
      - mcp-openclaw-extensions >= 3.2.0
tags:
  - legal-status
  - corporate-law
  - tax-optimization
  - governance
  - compliance
---

# firm-legal-status-pack

> ⚠️ Contenu généré par IA — validation humaine requise avant utilisation.

## Purpose

Provides a complete legal status analysis toolkit for the firm.
Enables structured comparison of legal forms (SAS, SARL, SASU, EURL, etc.),
tax simulations (IS vs IR, holding structures), social protection analysis,
governance recommendations, and post-creation compliance checklists.

Designed to produce professional documents readable by every department:
CEO (strategic structuring decisions), CFO (tax projections), Legal (statutory drafting),
HR (social protection implications), Market Research (regulatory landscape).

## Tools (5)

| Tool | Description | Category |
|------|-------------|----------|
| `openclaw_legal_status_compare` | Compare legal forms (SAS, SARL, SASU, EURL, etc.) with multi-criteria scoring matrix | legal |
| `openclaw_legal_tax_simulate` | Tax simulation IS vs IR, holding structures, rémunération optimization over 3-5 years | finance |
| `openclaw_legal_social_protection` | Social protection analysis — TNS vs assimilé salarié, prévoyance, retraite | legal |
| `openclaw_legal_governance_audit` | Governance structuring — statuts, pactes d'associés, organes de direction | legal |
| `openclaw_legal_creation_checklist` | Post-creation compliance checklist — démarches, coûts, obligations récurrentes | compliance |

## Usage

```yaml
skills:
  - firm-legal-status-pack

# Compare legal forms for a tech startup:
openclaw_legal_status_compare project_type="startup tech" founders=2 revenue_y1=200000 fundraising=true

# Tax simulation:
openclaw_legal_tax_simulate legal_form="SAS" revenue=200000 salary=50000 dividends=30000 horizon_years=3

# Social protection analysis:
openclaw_legal_social_protection status="assimile_salarie" salary=50000 include_options=true

# Governance audit:
openclaw_legal_governance_audit legal_form="SAS" founders=2 has_investors=true

# Creation checklist:
openclaw_legal_creation_checklist legal_form="SAS" sector="tech" geography="France"
```

## Cross-Department Integration

| Department | What they get | Tool |
|------------|--------------|------|
| **CEO** | Legal form recommendation with scoring matrix | `status_compare` |
| **CFO** | Tax simulations, rémunération optimization | `tax_simulate` |
| **Legal** | Governance clauses, statutory requirements | `governance_audit` |
| **HR** | Social protection implications by status | `social_protection` |
| **Operations** | Creation checklist and compliance calendar | `creation_checklist` |

## Requirements

- `mcp-openclaw-extensions >= 3.2.0`
