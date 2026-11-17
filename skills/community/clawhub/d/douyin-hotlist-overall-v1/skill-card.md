## Description:

Searches Douyin videos and posts, retrieves trending lists, creator posts, work details, and comments, and returns structured data for content and audience analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, social media teams, and analysts use this skill to find Douyin trends, review public creator content, and analyze comments for content ideas, competitor monitoring, and audience signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Douyin links are sent to Guaikei's third-party data API.

Mitigation: Only submit query terms and links you are comfortable sharing, and use public content.

Risk: The API token could be exposed or misused if shared in prompts or logs.

Mitigation: Keep GUAIKEI_API_TOKEN in a private environment variable and do not disclose its value.

Risk: The security scan reports a benign verdict with medium confidence and incomplete coverage.

Mitigation: Review the disclosed data handling and inspect the skill before enabling it in a sensitive environment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/douyin-hotlist-overall-v1)
- [Guaikei data API and token information](https://www.guaikei.com)
- [Command options](references/options.md)
- [Comment demand-mining guidance](references/demand-mining.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results; four-part Markdown summary for comment demand analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports search, creator posts, work details, comments, and trending lists; retrieval limits vary by API token plan.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
