# Checklists and Scoring Rules

## Similarity Filtering Checklist

For each candidate paper found through citation mining:

### Technology overlap
- [ ] Does the paper address the SAME technical problem?
- [ ] Does it use the SAME or SIMILAR approach family?
- [ ] Are the reported metrics directly comparable to the anchor paper?
- [ ] Is the application domain the same?

### Independence check
- [ ] Different institution from anchor group?
- [ ] No shared co-authors with anchor group?
- [ ] No acknowledged collaboration with anchor group?
- [ ] Research group lead is a different person?

### Signal strength
- [ ] Paper explicitly compares results against anchor paper?
- [ ] Paper uses anchor paper as baseline for improvement?
- [ ] Paper cites anchor paper multiple times (not just once in intro)?
- [ ] Paper was published in a competitive timeframe (within 1-3 years of anchor)?

Scoring: >=2 technology overlap + >=2 independence + >=2 signal strength → retain.

## Commercialization Indicators Checklist

For each retained competitor candidate, check:

### Patent evidence
- [ ] Researcher holds patents in the technology domain?
- [ ] Patent filing date is before or after key paper publication?
- [ ] Patent family size (single CN patent vs. international PCT family)?
- [ ] Patent is assigned to an institution (university) or a company?

### Company evidence
- [ ] Researcher is 法定代表人/股东/高管 of any company?
- [ ] Company business scope overlaps with technology domain?
- [ ] Company registration date (how long ago)?
- [ ] Company has a website / product page?

### Funding evidence
- [ ] Company has raised funding? (seed/A/B round)?
- [ ] Funding amount and investors?
- [ ] Government grants (NSFC, 863/973, provincial S&T)?
- [ ] University technology transfer office involved?

### Product evidence
- [ ] Product announced or launched?
- [ ] Customers or partnerships announced?
- [ ] Conference demos or trade show presence?
- [ ] Pricing or sales volume disclosed?

### Commercialization scoring
- 0 indicators → Level 0: Papers only
- 1-2 indicators → Level 1: Early-stage exploration
- 3-4 indicators → Level 2: Pre-commercialization
- 5-6 indicators → Level 3: Active commercialization
- 7+ indicators → Level 4: Commercialized

## Competitor Threat Assessment

| Factor | Weight | Scoring |
|--------|--------|---------|
| Technology performance vs. anchor | 30% | Better=3, Comparable=2, Worse=1 |
| Performance improvement rate | 20% | Accelerating=3, Steady=2, Stagnant=1 |
| Commercialization progress | 30% | Level 3-4=3, Level 2=2, Level 0-1=1 |
| IP protection strength | 20% | International patents=3, CN patents=2, No patents=1 |

**Threat level**: Weighted score ≥ 2.5 → High, 1.5-2.4 → Medium, <1.5 → Low

## Integration with patent-gap-supply-chain

When a discovered competitor shows commercialization signals (Level 3+), optionally invoke the `patent-gap-supply-chain` skill to:

- Check if the competitor has patent gaps suggesting supply-chain dependencies
- Identify the competitor's potential suppliers and customers
- Cross-validate the competitor's technology claims against patent evidence

Bridge trigger: "Also run patent-gap-supply-chain on [discovered competitor company] to check their supply chain dependencies."
