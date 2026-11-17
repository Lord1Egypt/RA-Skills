## Description:

Searches public Douyin videos, posts, trends, creator activity, and comments to support social-media research and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and marketing teams use this skill to investigate public Douyin content, compare creator performance, follow trending topics, and examine video comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, Douyin links, and the API token are sent to the third-party Guaikei service.

Mitigation: Use only when this data transfer is authorized; avoid sensitive search terms and links.

Risk: Local logs may retain searched topics, creator URLs, and returned public comments.

Mitigation: Review or delete local logs when those details are sensitive for your team.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/douyin-social-media-search)
- [Publisher profile](https://clawhub.ai/user/why20261)
- [Command options](references/options.md)
- [Guaikei API service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Analysis, Text, Shell commands]

**Output Format:** [Markdown guidance and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Douyin data only; command results include status and engagement metrics.]

## Skill Version(s):

1.3.0 (source: ClawHub release, skill frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
