## Description:

在抖音公开内容中搜索关键词和用户、查看作品与评论及热榜，并输出结构化 JSON，支持选题、竞品分析、舆情和需求研究。

This skill is ready for commercial/non-commercial use.

## Publisher:

[um-why](https://clawhub.ai/user/um-why)

### License/Terms of Use:

MIT

## Use Case:

内容运营、品牌和研究人员可用此技能搜索抖音公开视频与创作者，查看作品详情、评论和热榜，以支持选题、竞品分析、舆情跟踪及需求研究。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied Douyin links or IDs are sent to guaikei.com to retrieve results.

Mitigation: Use public content identifiers and non-sensitive search terms; avoid sending confidential or personal information.

Risk: ClawScan reports a benign verdict with medium confidence because some components were only partly inspected.

Mitigation: Review the skill and its scripts before installation if the scan's stated uncertainty is not acceptable for your use.

## Reference(s):

- [Guaikei 服务](https://www.guaikei.com)
- [ClawHub 发布页](https://clawhub.ai/um-why/skills/douyin-search-keyword)
- [Response contract](references/contract.md)
- [Demand mining guidance](references/demand-mining.md)
- [Customer acquisition guidance](references/customer-acquisition.md)
- [Error handling](references/errors.md)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON response envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are not saved to disk by default.]

## Skill Version(s):

1.5.2 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
