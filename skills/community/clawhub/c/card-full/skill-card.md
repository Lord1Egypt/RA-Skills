## Description:

Return a compact full report for one major-US credit card - fees, welcome offer, earning rates, redemption, credits, travel benefits, protections, mechanics, eligibility, and strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiahongc](https://clawhub.ai/user/jiahongc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to research a supported major U.S. credit card and receive a concise report covering fees, welcome offers, rewards, credits, benefits, eligibility, comparable cards, strategy, confidence notes, and sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credit-card offers, fees, benefits, and eligibility terms change frequently, and fetched pages can expose stale or conflicting welcome-offer information.

Mitigation: The skill requires issuer-first research, approved secondary-source checks, freshness checks, confidence notes, and explicit unresolved-offer language; users should independently verify current terms before applying.

Risk: The skill may use a Brave API key when available to search public web sources.

Mitigation: Installers should understand the optional Brave search behavior and provide the API key only in environments where that external search use is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiahongc/skills/card-full)
- [Chase Sapphire Preferred 2026 Refresh / Offer Extraction Note](references/chase-sapphire-preferred-2026-refresh.md)
- [Delta Reserve Offer Staleness - Anchoring Failure](references/delta-reserve-2026-offer-staleness.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Compact Markdown report with section headings, numbered lists, confidence notes, and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include uncertainty or conflict notes when current card offers cannot be verified from issuer and approved secondary sources.]

## Skill Version(s):

1.0.12 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
