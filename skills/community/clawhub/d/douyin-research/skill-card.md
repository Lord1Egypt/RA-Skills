## Description:

使用抖音公开数据分析视频、达人、评论和热榜，为市场调研与经营判断提供结构化数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

运营人员、市场研究者和分析人员可用关键词搜索、热榜、作品详情、公开达人作品及评论数据，整理选题、趋势、竞品和舆情分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send submitted keywords, links, or IDs to the third-party service described by the scanner.

Mitigation: Use public-data queries and avoid submitting sensitive or confidential information; check that the provider is appropriate for the data being sent.

Risk: ClawScan reports medium confidence and partial inspection; keyword-based account discovery is not clearly covered by the listed capabilities.

Mitigation: Review account-search behavior and results before relying on them, and confirm the query matches the intended public-data analysis.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/douyin-research)
- [Guaikei service and token access](https://www.guaikei.com)
- [Usage and command options](artifact/references/options.md)
- [Output contract](artifact/references/contract.md)
- [Demand mining guidance](artifact/references/demand-mining.md)
- [Customer acquisition guidance](artifact/references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON records; synthesized findings may be presented as Markdown or tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records can include video, creator, engagement, comment, and trend fields for downstream analysis.]

## Skill Version(s):

1.5.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
