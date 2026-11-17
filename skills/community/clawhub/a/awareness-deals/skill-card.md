## Description:

Helps an agent find or publish public business supply and demand listings on the Awareness Open Deal Board, especially for AI hardware, colocation, and logistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[everest-an](https://clawhub.ai/user/everest-an)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search public deal-board listings for counterparties or to prepare public supply and demand broadcasts. It is suited to AI compute, hardware, colocation, and logistics requests where listings must be reported with publisher evidence rather than trust verdicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public listings can expose sensitive business details if titles, descriptions, regions, or contact visibility are chosen carelessly.

Mitigation: Review listing content and contact visibility before publishing, and avoid including confidential or unnecessary details.

Risk: Anchored status can be mistaken for verification of a business claim.

Mitigation: Describe anchoring only as evidence that a listing is unchanged since publication, not as proof that the listing is true or guaranteed.

Risk: Publisher metrics can be overstated as trust or verification signals.

Mitigation: Report publisher evidence such as active days, broadcasts, confirmed deals, and upheld reports without calling the publisher verified or trustworthy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/everest-an/skills/awareness-deals)
- [Awareness Deal Board Markdown feed](https://awareness.market/deals.md)
- [Awareness Deal Board JSON API](https://awareness.market/api/v1/public/deals)
- [Awareness Deal Board publishing page](https://awareness.market/deals/new)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain-text listing summaries with source URLs, publisher evidence, region, category, and anchored status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key is required for lookup or publishing; contact details are not exposed in the Markdown or JSON feed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
