# french-business-analyser

Without this MCP, an AI agent asked to analyse a French supplier will hallucinate financial figures from its training data. With it, the agent queries 9 official French registries in real time. What is verified is stated. What is unavailable is explicitly marked. **The agent knows what it doesn't know.**

## Quick Start

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

## Consent & data handling

- **Agent-side credentials: none.** The MCP config block above is the only setup required.
- **Consent gate:** every paid tool (8 of 12) requires explicit user approval before the agent proceeds. Free tools can be called autonomously.
- **Inputs accepted:** SIREN, VAT number, IBAN (validated server-side, cache key is hashed), and optionally invoice text for extraction.
- **Service providers:** Railway (hosting), Anthropic Claude API (extraction + synthesis), and the official French registries. No analytics, no telemetry.
- **Retention:** Redis cache only with explicit TTLs (24h-30d). Verdicts are never cached. Invoice text is never stored — processed in-memory, returned to caller, discarded.
- **Open source.** Inspect the server code at [github.com/Vannelier/MCP-business-checker](https://github.com/Vannelier/MCP-business-checker).
- **Self-hosting available** for full infrastructure control — see SKILL.md.

## 12 Tools

| Tool | Cost | Description |
|---|---|---|
| `score_supplier` | 0.02 EUR | Payment risk verdict with liens + financial health |
| `lookup_company` | 0.005 EUR | Find company by name, SIREN, SIRET, or VAT |
| `compare_suppliers` | 0.06 EUR | Compare 2-5 vendors side-by-side |
| `verify_invoice` | 0.025 EUR | Supplier risk + VAT rate + amount coherence |
| `get_tax_rules` | Free | EU VAT rates and invoicing rules |
| `check_liens` | Free | Tax/social security liens check |
| `get_financial_trend` | Free | INPI annual accounts + Claude analysis |
| `score_director_risk` | 0.01 EUR | Director insolvency history (10yr) |
| `check_certifications` | Free | RGE / Qualiopi / BIO verification |
| `parse_invoice` | 0.005 EUR | Extract structured fields from invoice text |
| `validate_invoice_compliance` | Free | Check 11 legally required mentions |
| `full_due_diligence` | 0.10 EUR | Comprehensive report from all sources |

## Sources

SIRENE (INSEE), BODACC (DILA), VIES (EU), suretesmobilieres.fr, INPI (data.inpi.fr), annuaire-entreprises (data.gouv.fr), ADEME (RGE), DGEFP (Qualiopi), Agence Bio.

## Payment

x402 (USDC on Base) or Stripe MPP — pay per call, no subscription. 5 tools are free. No wallet private keys required on the agent side.
