## Description:

Extracts goodwill balances, earn-out results, impairment-test assumptions, and provisions from a single disclosure into a source-anchored ledger, using only figures stated in the source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Investors and analysts use it to extract goodwill information from a Chinese A-share annual or semi-annual report or acquisition announcement, with each figure tied to its disclosure quote and location. It leaves impairment judgments, provision adequacy, ratings, and share-price forecasts for human review.

### Deployment Geography for Use:

China (A-share disclosure context)

## Known Risks and Mitigations:

Risk: The security scan marked the release suspicious with medium confidence, citing network and credential-handling behavior that may conflict with its offline-analysis description; the scan was partial.

Mitigation: CUE_API_KEY is optional. Use user-supplied reports without it where practical, and verify the catalog-selected service endpoint before enabling credentialed lookup.

## Reference(s):

- [ClawHub release](https://clawhub.ai/huhoo/skills/cue-cn-goodwill-impairment-risk)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Eight-section Markdown ledger with verbatim disclosure quotes and source anchors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Amounts and percentages are copied verbatim from their cited disclosure sentences; missing items are identified explicitly.]

## Skill Version(s):

0.1.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
