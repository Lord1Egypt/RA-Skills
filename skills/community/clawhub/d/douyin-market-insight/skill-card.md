## Description:

分析抖音公开视频、达人作品、评论和热榜数据，帮助运营、营销和分析人员识别市场趋势、机会与风险。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External users, operators, marketers, and analysts use this skill to query public Douyin data for topic research, competitor monitoring, creator analysis, comment review, and real-time trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin keywords or links and the GUAIKEI_API_TOKEN to www.guaikei.com.

Mitigation: Install and run it only when that third-party data transfer is acceptable, and keep the token in a protected environment variable.

Risk: Some command results are saved under the skill's logs folder and may contain retained analytics data from comments or competitor research.

Mitigation: Delete or protect generated logs on shared machines and avoid storing sensitive internal research in shared workspaces.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/why20261/skills/douyin-market-insight)
- [Options Reference](references/options.md)
- [Changelog](references/changelog.md)
- [Guaikei API Token and Help](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output from the skill tools.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Node.js 16.14.0+ and GUAIKEI_API_TOKEN; successful CLI calls emit structured JSON envelopes for search, hot list, creator posts, and comments.]

## Skill Version(s):

1.3.0 (source: frontmatter, package.json, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
