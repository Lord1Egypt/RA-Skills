## Description:

AI 新闻聚合与热度排序工具，用于收集新产品发布、研究论文、行业动态、融资新闻、开源项目更新、社区病毒传播现象和 AI 工具/Agent 热门项目，并输出按热度排序的中文摘要列表和原文链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenxcomp](https://clawhub.ai/user/kenxcomp)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to request current AI-news briefings in Chinese. The skill guides an agent through multi-source web research, cross-checking, deduplication, heat ranking, and concise source-linked reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on broad web searches and external sources, so briefings may include incomplete, low-quality, inaccessible, or rapidly outdated information.

Mitigation: Cross-check high-impact items across multiple sources, prefer original or authoritative links, mark paywalled or inaccessible material, and review the final briefing before reuse.

## Reference(s):

- [AI 新闻源推荐列表](references/sources.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown news briefing with ranked items and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normally 15-25 deduplicated news items grouped by heat level, with collection count, search count, covered dimensions, and update time.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
