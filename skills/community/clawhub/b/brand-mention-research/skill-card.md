## Description:

Build a sourced brand-mention and reputation brief from bounded Reddit, TikTok, and YouTube searches and comment samples through Crawlora. Use to resolve brand aliases, deduplicate mentions, compare discussion themes, or inspect a product issue with explicit sampling limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Brand researchers, product teams, and marketers use this skill to review public discussion about a brand, product, or campaign and prepare a sourced brief. It helps compare themes and inspect product issues while showing the search scope, selected evidence, and sampling limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries could contain confidential information.

Mitigation: Keep confidential information out of queries and use a Crawlora key you control.

Risk: A small or uneven public sample could be mistaken for broad reputation, audience reach, or market share.

Mitigation: Set collection and credit limits, preserve source details, report sample sizes and denominators, and describe platform coverage limits.

## Reference(s):

- [Endpoint reference](reference/endpoints.md)
- [Crawlora API v1](https://api.crawlora.net/api/v1)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/brand-mention-research)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Tables, Guidance]

**Output Format:** [Markdown research brief with a coverage ledger and evidence table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports source IDs and URLs, retrieval and publication dates when available, sample counts, denominators, and platform coverage limits.]

## Skill Version(s):

1.0.3 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
