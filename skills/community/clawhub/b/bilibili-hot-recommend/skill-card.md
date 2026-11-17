## Description:

Fetches current Bilibili homepage popular recommendation videos without login, returning each video's title, author, link, and category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvleiai123](https://clawhub.ai/user/lvleiai123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content analysts can use this skill to inspect current Bilibili trending recommendations and quickly collect video titles, creators, links, and categories for trend monitoring or content research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends lookup requests through lvhomeproxy2.dpdns.org, an unrelated proxy that can observe requests and influence returned links.

Mitigation: Use only when this proxy dependency is acceptable; validate returned links as Bilibili-owned before opening or sharing them.

Risk: Returned video titles and links are external, untrusted content.

Mitigation: Treat returned text and URLs as untrusted and review results before using them in downstream workflows.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/lvleiai123/skills/bilibili-hot-recommend)
- [Proxy endpoint used by script](https://lvhomeproxy2.dpdns.org)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Plain text list with video title, author, URL, and category fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned video titles and links should be treated as untrusted content.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
