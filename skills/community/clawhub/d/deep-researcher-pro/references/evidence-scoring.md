# Evidence Scoring Criteria
# For: Deep Researcher v1
# Purpose: Define how to classify evidence strength for claims

***

## Evidence Levels

### HIGH — Strong Evidence
**Definition**: Repeated across strong or primary sources. Can be treated as established fact for decision purposes.

**Required conditions** (ALL must be met):
- 2+ independent authoritative sources agree
- Sources are primary (original report, official data, direct practitioner account) or high-quality secondary analysis
- No credible contradiction found
- Information is current (within relevant timeframe for the domain)

**Examples**:
- Market size from 2+ industry reports
- Technical specification from official documentation
- Regulatory requirement from government source
- Widely-reported event from multiple news outlets

**How to mark**: `[HIGH]` prefix + source references

***

### MEDIUM — Moderate Evidence
**Definition**: Plausible and partially supported, but not yet fully verified or has limited contradiction.

**Typical conditions** (meets SOME but not all HIGH criteria):
- Only 1 authoritative source + 1 supporting source
- Multiple sources but some are secondary or less authoritative
- Generally consistent but with minor contradictions
- Information is somewhat dated but not obviously stale

**Examples**:
- Market trend reported by 1 major outlet + mentioned by a practitioner
- Technical claim supported by documentation but contradicted by user reports
- Industry estimate from a single reputable analyst

**How to mark**: `[MEDIUM]` prefix + source references

**Special note**: When a claim has equal supporting and contradicting evidence, treat it as MEDIUM at best and move it to DIVERGENCES.

***

### LOW — Weak Evidence
**Definition**: Anecdotal, emerging, or weakly verified. Should not be the sole basis for a decision.

**Typical conditions**:
- Single source only
- Source is informal (blog post, forum comment, social media)
- Emerging trend with limited data
- Self-reported or self-interested source (vendor claims, marketing materials)
- No independent verification possible

**Examples**:
- A single user's experience report
- Vendor's claimed performance numbers (not independently verified)
- Early-stage research with no replication
- Community speculation or rumor

**How to mark**: `[LOW]` prefix + source references

**Required action**: Any LOW evidence used in the output MUST be accompanied by an explicit warning:
> ⚠️ This claim is based on a single or weak source — treat with caution when making decisions.

***

## Source Type Classification

| Type | Definition | Default Evidence Weight |
|------|------------|------------------------|
| Authoritative Report | Government data, industry reports, academic papers, official documentation | HIGH baseline |
| Practitioner | First-hand experience, case studies, technical write-ups from domain practitioners | MEDIUM baseline |
| Public Web | News media, encyclopedias, commercial analysis | MEDIUM baseline |
| Community | Forums, social media, user comments | LOW baseline |

**Note**: Source type is a starting point, not a ceiling. A practitioner account with specific, verifiable details can be elevated. An authoritative report that is clearly outdated can be downgraded.

***

## Special Cases

### Single Source Rule
Any claim supported by only one source, regardless of source type, is capped at MEDIUM.
If the single source is non-authoritative, it defaults to LOW.

### Recency Discount
- Data older than the domain's typical update cycle should be downgraded one level
- Example: In fast-moving tech domains, data > 2 years old should be marked down
- Example: In regulated industries, regulatory data remains HIGH regardless of age

### Conflict of Interest
- Vendor claims about own products: **start at LOW unless independently verified by a third party**
  - This includes: vendor-announced GMV, user counts, performance benchmarks, market share claims
  - Only upgrade from LOW when an independent source corroborates the specific claim
  - Partial verification (e.g., "analyst estimates roughly align") can upgrade to MEDIUM, never directly to HIGH
- Consultant reports commissioned by a stakeholder: start at MEDIUM unless methodology is transparent
- Academic research funded by industry: note the funding source, no automatic downgrade but flag it
- **Enforcement rule**: When you encounter a vendor claim, explicitly check: "Is this independently verified?" If not → LOW + ⚠️ warning

### Numbers and Statistics
- Any specific number must have an explicit source citation
- Ranges are preferred over point estimates when sources disagree
- If the number comes from a model/estimate (not measurement), mark as [ESTIMATED]
- **Forecast/prediction numbers must ALWAYS be marked [ESTIMATED]**: market size projections, growth rates, future adoption rates, revenue forecasts — even from authoritative sources
- **Vendor self-reported numbers must ALWAYS be marked [ESTIMATED]** and start at LOW evidence level (see Conflict of Interest rule)
- Format: `[ESTIMATED] $150B (2025 forecast) [source: URL]`
- If a number's time horizon is ambiguous (e.g., "market size $150B" without year), clarify or mark [ESTIMATED]

***

## Scoring in --mode=compare

When comparing A vs B:
- Apply the SAME evidence standard to both sides
- If A has 3 HIGH sources and B has 1 MEDIUM source for the same dimension, note the asymmetry
- Never upgrade B's evidence just to "balance" the comparison
- Asymmetric evidence quality IS a valid finding — it means one side is less understood or less transparent
