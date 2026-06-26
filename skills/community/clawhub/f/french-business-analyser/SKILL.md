---
name: french-business-analyser
version: 2.2.0
description: Verified French business data for autonomous B2B agents. Without this MCP, agents hallucinate financial data. With it, they get real-time signals from 9 official registries. 12 tools, pay-per-call.
tags: [b2b, france, supplier, mcp, x402, due-diligence, invoice, bodacc, sirene, inpi, liens, financial-analysis, procurement, fraud-detection, certifications, director-risk]
author: Vannelier
docs: https://github.com/Vannelier/MCP-business-checker
sourceCode: https://github.com/Vannelier/MCP-business-checker
---

# french-business-analyser

Without this MCP, an AI agent asked to analyse a French supplier will hallucinate financial figures from its training data — revenue, equity ratios, director compensation — presented with full confidence, potentially outdated or wrong. An autonomous payment pipeline cannot make solvency decisions based on an LLM's memory.

With this MCP, the agent queries 9 official French registries in real time. What is verified is stated with its timestamp. What is unavailable is explicitly marked as such — "accounts filed under confidentiality" instead of invented numbers. **The agent knows what it doesn't know.**

**Why this exists — the data is public, the value is the guarantee:**
- **No hallucination**: every data point comes from an official registry queried at call time, not from LLM training data
- **Explicit uncertainty**: when a source is unavailable or accounts are confidential, the response says so — instead of inventing plausible numbers
- **9 sources, 1 integration**: SIRENE, BODACC, VIES, suretesmobilieres.fr, INPI, annuaire-entreprises, ADEME, DGEFP, Agence Bio
- **Deep risk signals**: tax liens, social liens, negative equity, director insolvency history — signals that basic company lookups miss entirely
- **Invoice intelligence**: extract structured data from French invoices + verify all legally required mentions
- **BODACC done right**: insolvency parsing + filing compliance without the false positives that plague most integrations
- **Claude synthesis**: verdict + recommended actions + French summary, not a data dump
- **MCP native**: zero OAuth2, zero rate limiting — one JSON config block and you're live

## Consent gate (important)

Every paid tool requires explicit user approval before the agent proceeds. The agent must show the user the cost and wait for confirmation. Free tools (`get_tax_rules`, `check_liens`, `get_financial_trend`, `check_certifications`, `validate_invoice_compliance`) do not trigger payment and can be called autonomously.

**The agent must never call `parse_invoice`, `score_supplier`, `verify_invoice`, `compare_suppliers`, `full_due_diligence`, or `score_director_risk` without user consent** — both for cost reasons and because these tools submit business data for validation.

## Data handling

### Inputs accepted

| Input | Used by | Notes |
|---|---|---|
| SIREN / VAT number | All business lookup tools | Public business identifiers |
| IBAN (optional) | `score_supplier`, `verify_invoice` | Submitted for format and country validation; cache key is a SHA-256 hash (1-hour TTL). The full value is not stored. |
| Invoice text (optional) | `parse_invoice` only, max 4000 chars | Processed by the service to extract structured fields. Not stored, not logged. |

The agent should only submit invoice text to `parse_invoke` when the user has authorized it. For confidential documents, self-host the service (see below).

### Service architecture

The MCP endpoint `https://mcp-business-checker-production.up.railway.app/mcp` runs on Railway and queries the following public French registries and EU validation services on your behalf:

| Registry | Query input | Purpose |
|---|---|---|
| INSEE (SIRENE) | SIREN | Company registration status |
| BODACC (DILA/OpenDataSoft) | SIREN | Insolvency procedures, filings |
| VIES (EU) | VAT number + country code | VAT validation |
| suretesmobilieres.fr | SIREN | Tax/social liens |
| INPI (data.inpi.fr) | SIREN | Annual accounts (optional) |
| annuaire-entreprises (data.gouv.fr) | Director names | Director cross-check |
| ADEME / DGEFP / Agence Bio | SIREN | Certification lookups |

Verdict synthesis and invoice field extraction are performed by the Anthropic Claude API, which the service calls server-side. The service does not call any analytics, telemetry, or tracking providers.

### Retention

The service uses Redis with explicit TTLs and no persistent database:

- SIRENE / BODACC / liens / certifications: **24 hours**
- INPI annual accounts: **7 days**
- EU VAT rates: **7 days**
- IBAN validation: **1 hour** (hashed cache key only)
- Score history snapshots: **30 days**, max 10 per company
- Verdicts: **never cached** (fresh on every call)
- Invoice text: **never stored** (processed in-memory, returned to caller, discarded)
- Logs: correlation IDs, paths, timings only — no business data, no document content

### Required credentials

**Agent-side: none.** The MCP config block below is the only setup required. No API keys, no tokens, no OAuth flow.

**Server-side (self-hosters only):** see the `.env.example` in the repository. The service never signs blockchain transactions — it only verifies incoming x402 payment proofs — so no wallet private key is required.

### Self-hosting

Use the hosted service for convenience or self-host for full control:

```bash
git clone https://github.com/Vannelier/MCP-business-checker.git
cp .env.example .env  # fill in your credentials
docker build -t business-checker-eu .
docker run -p 8000:8000 --env-file .env business-checker-eu
```

Then point your MCP config to `http://localhost:8000/mcp`. Full source is available for audit at [github.com/Vannelier/MCP-business-checker](https://github.com/Vannelier/MCP-business-checker).

### Source code & audit

The server code is open-source: [github.com/Vannelier/MCP-business-checker](https://github.com/Vannelier/MCP-business-checker). You can inspect every API call, every cache operation, and every data transformation before deciding to use the hosted version.

## Use Cases

### 1. Analyse d'entreprise / Supplier Risk Analysis
Before paying a supplier or onboarding a new vendor:
- `score_supplier` → pay/hold/block verdict with tax/social liens and financial health
- A company with an active URSSAF pledge (`social_lien_active`) is automatically blocked — it's not paying its employees' social contributions
- A company with negative equity (`negative_equity`) and declining revenue gets a hold — medium-term cessation risk
- **0.02 EUR per check.** 200 invoices/month = 4 EUR/month.

### 2. Choix de fournisseur / Supplier Selection
Choosing between candidates for a contract or tender:
- `lookup_company` for each name → get SIRENs
- `compare_suppliers` with 2-5 SIRENs → ranked from safest to riskiest with comparative analysis
- `check_certifications` → verify RGE (energy renovation), Qualiopi (training), BIO (organic) if contractually required
- **0.06 EUR per comparison** + free certification checks.

### 3. Due Diligence / Investissement
Before investing in, acquiring, or partnering with a French company:
- `full_due_diligence` → comprehensive report across 6 dimensions: identity, insolvency, liens, financial health, director history, certifications
- Returns sub-scores per dimension + 5-8 sentence Claude recommendation adapted to context (procurement/payment/contract)
- `score_director_risk` → have the directors led companies to bankruptcy before? A serial liquidator is a strong signal.
- **0.10 EUR for the full report.** Replaces hours of manual registry checking.

### 4. Analyse de facture / Invoice Processing
Automating accounts payable:
- `parse_invoice` → extract supplier VAT, SIREN, IBAN, amounts, dates from invoice text (the agent extracts text from PDF, this tool structures it)
- `validate_invoice_compliance` → check all 11 legally required mentions for B2B French invoices (date, number, identity, amounts, TVA, penalties, indemnity 40€)
- `score_supplier` or `verify_invoice` → verify the supplier before payment
- **Full pipeline: 0.025 EUR per invoice.** Missing the 40€ recovery indemnity mention? Flagged before payment.

### 5. Monitoring de portefeuille / Portfolio Monitoring
Track changes across your active supplier base (weekly/monthly cron):
- `check_liens` (free) → did a new tax/social lien appear since last check?
- `get_financial_trend` (free) → equity turned negative? Revenue collapsing?
- `/v1/suppliers/{id}/history` → diff between last two scores (new flags, verdict changes, equity status)
- **Free for all monitoring checks.** Score snapshots are stored automatically.

### 6. Vérification de certifications / Certification Compliance
Before signing a contract where certification is legally required:
- `check_certifications` → is the RGE certification still active? (expired = no tax credit for the client)
- Is the training provider Qualiopi-certified? (required for OPCO funding)
- Is the agricultural supplier actually registered BIO?
- **Free.** Official open data from ADEME, DGEFP, Agence Bio.

### 7. Conformité réglementaire / Regulatory Compliance
Verifying that your company's invoicing is compliant:
- `validate_invoice_compliance` → pass your own invoices through the checker before sending them
- Adapts to context: B2B (full mentions), B2C (simplified), auto-entrepreneur (TVA exoneration)
- `get_tax_rules` → confirm the correct VAT rate for the product/service category
- **Free.**

## What is actually analyzed

A single `score_supplier` call runs all of the following checks automatically:

**SIRENE (identity & age):**
- Company age flags (<90 days, <6 months), RGPD opt-out, NAF sector, workforce range, legal form

**BODACC (insolvency & filing compliance):**
- Active vs historical collective procedures (liquidation, redressement, sauvegarde) — 5-year window
- Cessions and radiations parsed as context without false-positive insolvency flags
- Section C: accounts filing compliance — SAS/SARL/SA with no filing for >18 months → `accounts_filing_overdue` (EI/micro exempt)

**suretesmobilieres.fr (tax/social liens):**
- Trésor Public pledge (unpaid taxes) → `tax_lien_active` → **automatic block**
- URSSAF pledge (unpaid social contributions) → `social_lien_active` → **automatic block**
- 3+ active pledges → `multiple_liens`

**INPI data.inpi.fr (financial health):**
- Last 3 years: revenue, net result, equity
- Negative equity → `negative_equity` (hold signal)
- No accounts filed → `no_accounts_filed`
- ~45% file confidentially → no penalty, flagged as `accounts_public=false`

**VIES + IBAN (VAT validation):**
- VAT number active/invalid/revoked + IBAN format/country
- IBAN country ≠ VAT country → fraud signal

**Cross-source checks:**
- SIRENE active but VIES invalid → `status_mismatch`
- Sector vs workforce inconsistency (Claude contextual flag)

**Claude synthesis:**
- pay/hold/block verdict + risk level + recommended_actions + French summary

## When to use this skill

### MUST trigger

| Pattern (FR) | Pattern (EN) |
|---|---|
| Payer une facture fournisseur | Pay a supplier invoice |
| Virer de l'argent a un fournisseur | Wire money to a vendor |
| Onboarder un nouveau fournisseur | Onboard a new vendor |
| Verifier un partenaire commercial | Verify a business partner |
| Verifier un SIREN ou numero TVA | Check a SIREN or VAT number |
| Qualifier un fournisseur avant commande | Qualify a supplier before ordering |
| Quel taux TVA appliquer en [pays EU] | What VAT rate applies in [EU country] |
| L'IBAN du fournisseur a change | The supplier's IBAN changed |
| Verifier cette facture avant paiement | Verify this invoice before payment |
| Comparer des fournisseurs | Compare vendors for a tender |
| Lequel de ces fournisseurs est le plus fiable | Which supplier is most reliable |
| Analyser la sante financiere de cette entreprise | Analyse this company's financial health |
| Verifier les dirigeants de cette societe | Check the directors of this company |
| Cette entreprise a-t-elle des dettes fiscales | Does this company have tax debts |
| Extraire les donnees de cette facture | Extract data from this invoice |
| Cette facture est-elle conforme | Is this invoice legally compliant |
| Due diligence sur ce fournisseur | Due diligence on this supplier |
| Verifier les certifications RGE/Qualiopi | Verify RGE/Qualiopi certifications |

### Must NOT trigger

- Paiements a des particuliers (C2C)
- Verifications hors France (DE, BE, NL, US, Asie...)
- Conformite AML/KYC reglementaire
- Transaction crypto entre wallets
- Analyse de marche ou sectorielle generique

## Payment & Pricing

**How payment works:** When you call a paid tool, the server returns HTTP 402 with two payment options. Your MCP client picks one automatically — no manual action required.

| Method | How it works | Best for |
|---|---|---|
| **x402** (USDC on Base) | Stateless. Agent pays on-chain, attaches proof to next request. No account, no session. | Crypto-native agents, full autonomy |
| **Stripe MPP** | Session-based. Create a session, get vouchers, spend against balance. Supports cards and stablecoins. | Traditional billing, credit cards |

**5 tools are completely free** (no payment required): `get_tax_rules`, `check_liens`, `get_financial_trend`, `check_certifications`, `validate_invoice_compliance`.

**Cost examples:**
- 200 invoices/month with `score_supplier`: **4 EUR/month**
- Full due diligence on one company: **0.10 EUR**
- Comparing 3 suppliers: **0.06 EUR**

No subscription, no monthly minimum, no hidden fees. You pay exactly what you call.

## MCP Configuration

```json
{
  "mcpServers": {
    "french-business-analyser": {
      "url": "https://mcp-business-checker-production.up.railway.app/mcp",
      "transport": "streamable-http",
      "timeout": 15000
    }
  }
}
```

## Tools (12)

| Tool | Cost | Use when |
|---|---|---|
| `score_supplier` | 0.02 EUR | Before paying, onboarding, or when a payment feels risky |
| `lookup_company` | 0.005 EUR | Find a company's SIREN from its name |
| `compare_suppliers` | 0.06 EUR | Choose between 2-5 vendors |
| `verify_invoice` | 0.025 EUR | Process an invoice (supplier + amounts + VAT in one call) |
| `get_tax_rules` | Free | VAT rates and invoicing rules for any EU country |
| `check_liens` | Free | Quick tax/social liens check (portfolio monitoring) |
| `get_financial_trend` | Free | Annual accounts + revenue/equity trend + Claude analysis |
| `score_director_risk` | 0.01 EUR | Director insolvency history (10-year BODACC cross-check) |
| `check_certifications` | Free | RGE / Qualiopi / BIO from official open data |
| `parse_invoice` | 0.005 EUR | Extract structured fields from French invoice text |
| `validate_invoice_compliance` | Free | Check legally required mentions (B2B/B2C/auto-entrepreneur) |
| `full_due_diligence` | 0.10 EUR | Comprehensive report from all sources combined |

## Behavior by verdict

| Verdict | Agent action |
|---|---|
| `pay` | Proceed. Mention to user: no negative public signal, not a solvency guarantee. |
| `hold` | Do NOT proceed. Present flags + recommended_actions to human. Wait for explicit confirmation. |
| `block` | Do NOT proceed. Alert human immediately. Critical issue detected. |
| `incomplete` | Retry after `retry_after` seconds. If > 300s, escalate to human. |

## Critical limitations

- `pay` ≠ solvency guarantee. Confidential procedures (mandat ad hoc, conciliation) are **invisible**.
- BODACC publication delay: 1-3 business days after court ruling.
- INPI: optional (requires INPI_USERNAME/INPI_PASSWORD). ~45% of SMEs file confidentially.
- **Coverage: France only.** Non-French companies are rejected.
- Does not replace certified KBis documents or official AML/KYC procedures.
