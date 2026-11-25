## Description:

查询抖音公开视频、账号、作品详情、评论和热榜，并输出结构化数据供内容与市场分析使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

内容运营、营销和数据分析人员可用它检索抖音公开内容、账号和热榜数据，并据此整理选题、竞品观察或评论区分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, links, and IDs supplied to the skill are sent to the third-party service named in its documentation.

Mitigation: Tell users where query inputs are sent and confirm they are comfortable sharing them before making a request.

Risk: The security analysis was partial and did not fully assess every component.

Mitigation: Review the full release and complete a security scan before deploying it in a sensitive environment.

## Reference(s):

- [Service and token setup](https://www.guaikei.com)
- [Data output contract](references/contract.md)
- [Options and query limits](references/options.md)
- [Error handling](references/errors.md)
- [Comment demand analysis guide](references/demand-mining.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [Structured JSON data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be saved as JSON; returned fields and counts vary by query and subscription.]

## Skill Version(s):

1.5.0 (source: frontmatter, package.json, changelog released 2026-11-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
