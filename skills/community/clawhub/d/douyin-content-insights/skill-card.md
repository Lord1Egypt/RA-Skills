## Description:

通过怪奇 API 查询抖音公开内容，包括关键词与用户搜索、博主作品、单条作品详情、评论和实时热榜，并返回结构化 JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

抖音内容运营、品牌与市场分析人员可用它搜索公开作品和账号、查看作品互动与评论、跟踪热榜，并将结构化结果用于选题、竞品观察和舆情分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and supplied Douyin links or IDs are sent to the third-party API; the security review also notes account search as an undeclared capability.

Mitigation: Avoid sending sensitive identifiers, use only public data you are authorized to analyze, and confirm the account-search capability and data sharing fit your needs before use.

## Reference(s):

- [怪奇 API 服务](https://www.guaikei.com)
- [命令与参数说明](artifact/readme.md)
- [输出契约](artifact/references/contract.md)
- [常见问题与环境配置](artifact/references/faq.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown, Tables]

**Output Format:** [Structured JSON data with concise summaries, tables, or reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result fields vary by command; collected results may be saved in the skill's logs directory.]

## Skill Version(s):

1.5.0 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
