## Description:

通过怪奇 API 查询抖音公开作品、作者、评论与热榜，并以结构化 JSON 支持内容研究和竞品分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

内容运营、市场分析与研究人员可用它搜索抖音公开视频和图文、查看作者作品与作品详情、读取评论及实时热榜，并据此整理选题、竞品观察或舆情摘要。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplied Douyin keywords, links, or IDs are sent to a third-party API.

Mitigation: Submit only information approved for external processing; avoid sensitive or personal data and confirm the sharing scope before use.

Risk: The security assessment was benign but had medium confidence and partial code inspection, so it did not establish that every executable file is safe.

Mitigation: Review the current release before running it, and begin with non-sensitive public queries.

## Reference(s):

- [需求挖掘指南](references/demand-mining.md)
- [命令参数说明](references/options.md)
- [更新日志](references/changelog.md)
- [怪奇 API 服务与使用帮助](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON data, Analysis, Guidance]

**Output Format:** [Structured JSON from the command-line tools, with summaries in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public-content results; some result links may expire.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
