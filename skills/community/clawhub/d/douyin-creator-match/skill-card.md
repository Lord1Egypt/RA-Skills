## Description:

根据抖音公开内容、作者互动和评论数据筛选带货达人候选，并支持热点与市场分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

营销团队、内容运营者和数据分析人员可用它筛选抖音达人候选，查看公开作品表现、热点和评论，以支持内容与市场研究。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review confidence is medium; 19 of 43 components received only partial analysis, so some behavior remains unverified.

Mitigation: Review the partially analyzed components and their behavior before relying on the skill in a sensitive workflow.

Risk: Queries send keywords or links to the Guaikei API, and execution requires an API token.

Mitigation: Use only authorized public-data queries, avoid sending sensitive information, and keep GUAIKEI_API_TOKEN confidential.

## Reference(s):

- [抖音数据服务](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/why20261/skills/douyin-creator-match)
- [options.md](references/options.md)
- [demand-mining.md](references/demand-mining.md)
- [changelog.md](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance, Shell commands]

**Output Format:** [Structured JSON with concise Chinese analysis or reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public-data results; selected commands save JSON output for later analysis.]

## Skill Version(s):

1.4.2 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
