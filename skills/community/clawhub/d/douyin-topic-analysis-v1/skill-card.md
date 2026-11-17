## Description:

Searches public Douyin videos, trends, creator posts, and comments to support short-video topic research and content analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content creators, social media operators, and brand researchers use this skill to find topic ideas and review public Douyin content, creator activity, and audience comments. Comment based pain point analysis follows the supplied demand mining guide.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Douyin links are sent to the external guaikei.com API service.

Mitigation: Use only public Douyin data, confirm the data sharing is appropriate, and keep GUAIKEI_API_TOKEN private.

Risk: ClawScan reports a benign verdict with medium confidence and partial coverage; 24 of 42 components were fully inspected.

Mitigation: For stronger assurance, review the executable files before installation; the scan is not a complete safety guarantee.

## Reference(s):

- [ClawHub release](https://clawhub.ai/why20261/skills/douyin-topic-analysis-v1)
- [Service and token setup](https://www.guaikei.com)
- [Skill instructions](artifact/SKILL.md)
- [Usage options](artifact/references/options.md)
- [Comment demand mining guide](artifact/references/demand-mining.md)

## Skill Output:

**Output Type(s):** [JSON data, Analysis, Text guidance]

**Output Format:** [Structured JSON with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports topic research, creator comparisons, trend monitoring, and comment summaries. Requires Node.js 16.14+ and GUAIKEI_API_TOKEN.]

## Skill Version(s):

1.4.2 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
