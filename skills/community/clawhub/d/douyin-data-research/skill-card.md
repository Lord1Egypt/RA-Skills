## Description:

Provides structured access to public Douyin search, trending topics, creator posts, video details, and comments for content and market research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, and analysts use the skill to gather public Douyin data for topic research, competitor monitoring, trend tracking, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided search terms and links to the third-party data API at guaikei.com.

Mitigation: Use it only with data and query details that are appropriate to share with that service; the skill documentation limits use to public Douyin data and internal analysis.

Risk: The security review is incomplete: only 24 of 43 components were fully inspected, and tool misuse analysis was degraded.

Mitigation: Review the skill before installation and consider the scan's stated uncertainty when deciding whether to run it.

## Reference(s):

- [Douyin Data Assistant website](https://www.guaikei.com)
- [Comment demand mining guide](artifact/references/demand-mining.md)
- [Command options](artifact/references/options.md)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-data-research)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON records, with concise Markdown analysis when summarizing comments.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and GUAIKEI_API_TOKEN. Results are saved locally. Request limits depend on the token plan.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, package.json, changelog released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
