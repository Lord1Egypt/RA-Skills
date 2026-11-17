## Description:

Helps authorized 1688 merchants analyze competing shops, competing products, buyer loss, keywords, price bands, and buyer structure using Accio Desktop merchant analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

1688 merchants and their agents use this skill to identify relevant competitors, compare shop-level and product-level performance, inspect buyer loss, and decide where deeper competitive analysis is warranted. It is intended for use only with the currently authorized merchant account in Accio Desktop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read sensitive 1688 merchant analytics for the currently authorized shop.

Mitigation: Install and run it only for merchant accounts where the operator is authorized to view competition and buyer-loss analytics.

Risk: The raw merchant-data query path is broader than the main competition-analysis workflow.

Mitigation: Prefer the documented competition and customer-loss commands, and restrict or review raw query use before deploying in shared or high-trust environments.

Risk: Competitive conclusions may be misleading if unavailable data, unmonitored competitors, or relative index values are treated as absolute facts.

Mitigation: Require outputs to separate returned facts from interpretation, disclose missing data, and avoid conclusions when required competitor or product monitoring is not available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-shop-compete-analysis)
- [1688 competition API reference](artifact/references/api/compete-api.md)
- [Competitor analysis rules](artifact/references/competitor-analysis-rules.md)
- [Customer analysis and conversion rules](artifact/references/customer-analysis-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [JSON command results with Markdown summaries and Chinese competitive-analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Accio Desktop, current merchant authorization, and available 1688 competition or buyer-loss data; some performance values are relative indices for comparison rather than absolute counts.]

## Skill Version(s):

0.1.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
