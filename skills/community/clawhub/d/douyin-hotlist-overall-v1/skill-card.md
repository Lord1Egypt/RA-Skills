## Description:

Retrieves public Douyin hot lists, keyword-matched videos and accounts, creator posts, work details, and comments as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content strategists, marketers, analysts, and support teams use this skill to retrieve public Douyin trends, videos, creator posts, and comments for topic research, competitor monitoring, and sentiment or demand analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send supplied keywords, links, or IDs to the Guaikei third-party API.

Mitigation: Use only query details appropriate to share with that service, and confirm before sending a user's supplied link or ID when their intent is unclear.

Risk: The security scan inspected only part of the release (31 of 53 components), with medium confidence.

Mitigation: Review the full release and its account-search capability before deployment, especially if that feature is outside the intended use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-hotlist-overall-v1)
- [Guaikei service](https://www.guaikei.com)
- [Output contract](artifact/references/contract.md)
- [Command options](artifact/references/options.md)
- [Errors and retry guidance](artifact/references/errors.md)
- [Environment FAQ](artifact/references/faq.md)
- [Comment demand analysis](artifact/references/demand-mining.md)
- [Customer acquisition guidance](artifact/references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown]

**Output Format:** [Structured JSON results with concise Markdown summaries or tables when analysis is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands save JSON results locally. Public data is retrieved through a third-party service; media and share links may expire.]

## Skill Version(s):

1.5.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
