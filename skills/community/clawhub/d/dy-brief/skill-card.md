## Description:

以只读方式获取抖音公开数据，并输出可用于日报、周报和内容分析的结构化 JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

内容运营、品牌和数据分析人员可用它查询抖音公开作品、账号、评论和热榜数据，再汇总成日报、周报、选题或竞品分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send supplied links or IDs to a third-party API; scanner coverage was partial and runtime permissions were not verified.

Mitigation: Submit only links or IDs appropriate to share with Guaikei, and review the required runtime permissions before granting access.

## Reference(s):

- [Guaikei API service](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/guaikei/skills/dy-brief)
- [Usage options](references/options.md)
- [Comment demand analysis guide](references/demand-mining.md)
- [Customer acquisition guide](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [Structured data, JSON]

**Output Format:** [JSON records for Douyin search results, user profiles, posts, comments, and hot lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fields and result limits vary by query and subscription plan.]

## Skill Version(s):

1.5.1 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
