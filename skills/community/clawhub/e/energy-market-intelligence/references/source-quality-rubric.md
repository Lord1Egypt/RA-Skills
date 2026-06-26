# Source Quality Rubric — Alberta Energy Market

## Tier 1 — Authoritative (high confidence)

| Source | Type | Update cadence | Notes |
|--------|------|---------------|-------|
| AESO public API (api.aeso.ca) | Pool price, supply/demand, interchange, generation by fuel | Real-time / hourly | Primary data source. Requires API key for some endpoints. |
| AESO published reports | Annual Market Statistics, Long-term Outlook, Adequacy | Annual / periodic | Official forecasts and historical summaries. |
| AESO connection project list | Interconnection queue | Monthly | First-class input for queue pressure and supply pipeline. |
| AUC decisions and filings | Regulatory | As issued | Proceeding-specific. Always cite proceeding number. |
| ETS pool price settlement | Settlement data | Monthly | Final settled prices, not preliminary. |
| Alberta government gazette | Carbon pricing, legislation | As enacted | TIER compliance schedules, regulatory changes. |

## Tier 2 — Credible secondary (moderate confidence)

| Source | Type | Notes |
|--------|------|-------|
| AESO stakeholder consultations | Policy direction | Not enacted — label as "under consultation." |
| AUC hearing transcripts | Intervener evidence | Represents positions, not decisions. |
| Energy trade press (DOB, JWN, BNEF) | Analysis | Credible but not primary. Always cross-reference against tier-1. |
| Generator/utility investor filings | Corporate disclosures | TransAlta, Capital Power, ATCO, ENMAX quarterly reports. Useful for fleet plans. |

## Tier 3 — Context only (low confidence)

| Source | Type | Notes |
|--------|------|-------|
| General news coverage | Reporting | Only use when linking to a primary source within the article. |
| Analyst commentary | Forecasts | Must disclose methodology or label as opinion. |
| Social media / LinkedIn | Claims | Never use as sole evidence. Context only. |
| Conference remarks | Statements | Unverified unless backed by published material. |

## Rules

1. Never blend tier-3 material into confirmed facts.
2. Every claim must be tagged with its source tier in the evidence table.
3. If the only source for a claim is tier-3, downgrade the claim to "unverified" regardless of how plausible it sounds.
4. AESO API data is authoritative for the timestamp queried; it does not confirm future conditions.
5. When source tiers conflict, prefer higher-tier sources and note the disagreement.
6. Tier-1 data older than 90 days should be labeled "historical baseline — verify against current conditions before acting." Apply the stale data gate from SKILL.md when any user-provided data exceeds this threshold.
