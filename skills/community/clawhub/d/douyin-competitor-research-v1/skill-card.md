## Description:

抖音竞品研究 helps brands, MCNs, content operators, and creators retrieve public Douyin search, hot-list, creator-post, and comment data for competitor research, content strategy comparison, social listening, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users, marketers, MCNs, content operators, and creators use this skill to collect structured public Douyin data for competitor research, topic discovery, creator monitoring, hot-list tracking, and comment analysis. It requires a GUAIKEI_API_TOKEN and does not support private or login-only data or write actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Douyin search terms, profile/video URLs, public comments, and GUAIKEI_API_TOKEN are sent to guaikei.com.

Mitigation: Use the skill only when this data sharing is acceptable, keep the token secret, and rotate it immediately if it is exposed.

Risk: Retrieved datasets may be saved locally after use.

Mitigation: Review, protect, or delete generated logs, especially in shared, synced, or backed-up workspaces.

## Reference(s):

- [Server-resolved GitHub provenance: why20261/douyin-competitor-research-v1](https://github.com/why20261/douyin-competitor-research-v1)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-competitor-research-v1)
- [Guaikei API token and service site](https://www.guaikei.com)
- [Changelog](references/changelog.md)
- [Options Reference](references/options.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON data from command-line tools, with optional Markdown summaries or analysis produced by the calling agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command stdout is structured JSON; logs and banners are written to stderr, and retrieved datasets may also be saved locally.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter/package version 1.2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
