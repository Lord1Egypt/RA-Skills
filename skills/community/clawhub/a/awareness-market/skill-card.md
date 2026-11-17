## Description:

Awareness Market helps agents find public AI asset listings and business counterparties by fetching Awareness Market and Open Deal Board Markdown or JSON listings and reporting their evidence signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[everest-an](https://clawhub.ai/user/everest-an)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to browse or search public Awareness Market and Open Deal Board listings for installable AI assets, memory packs, and business counterparties, then report listing details and evidence signals without treating them as endorsements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public marketplace and deal-board listings are user-published content and may be inaccurate, incomplete, or unsuitable for a user's intended installation or business decision.

Mitigation: Report listing evidence, source URLs, and publisher signals without presenting listings as verified endorsements; advise users to review the listing source before installing or making business decisions.

Risk: On-chain anchoring or other listing evidence can show publication integrity without proving that listing claims are true.

Mitigation: Distinguish existence or integrity evidence from truth claims and avoid describing anchored listings as verified.

## Reference(s):

- [Awareness Agent Memory Market Markdown](https://awareness.market/market.md)
- [Awareness Agent Memory Market API](https://awareness.market/api/v1/market/listings)
- [Open Deal Board Markdown](https://awareness.market/deals.md)
- [Open Deal Board API](https://awareness.market/api/v1/public/deals)
- [ClawHub Skill Page](https://clawhub.ai/everest-an/skills/awareness-market)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text summaries with source URLs and evidence signals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key is required; contact details are not included in fetched Markdown or JSON.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
