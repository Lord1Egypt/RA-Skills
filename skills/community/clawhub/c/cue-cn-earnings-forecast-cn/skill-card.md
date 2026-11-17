## Description:

将单份 A 股业绩预告或业绩快报的六项披露内容逐条引用原文登记，标明缺失项，不自行计算或推断数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

面向需要核对 A 股公司业绩预告或快报的分析人员，按原始披露逐项登记预告类型、区间、同比变动、原因、修正情况和披露日期，并为每项保留来源。

### Deployment Geography for Use:

China (A-share listed companies)

## Known Risks and Mitigations:

Risk: ClawScan reports a possible mismatch between the stated zero-network workflow and external service discovery, notes a revision-status issue, and indicates that its analysis was partial; its suspicious verdict is a review finding, not proof of malicious intent.

Mitigation: Review network and tool-discovery behavior before execution, and verify revision status against the original filing; limit execution until that review is complete.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-earnings-forecast-cn)
- [Cue MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Markdown]

**Output Format:** [Markdown structured note with six sections, quoted disclosure text, and numbered source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One filing per note; missing items are named; no derived midpoint or change calculations.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, CHANGELOG.md; released 2026-11-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
