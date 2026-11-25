## Description:

读取可见的 B 站合集或收藏夹资料，并按学习目标与每日时间预算生成带来源和缺项标记的观看顺序与日计划。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

External learners can use this skill to turn an accessible Bilibili playlist or favorites list into a goal-led viewing order and daily time plan, based only on page-visible information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented installer command is unpinned, and the security scan has medium confidence with partial coverage.

Mitigation: Review the package contents and version before running it; do not treat the clean scan verdict as a complete inspection.

## Reference(s):

- [Easy WebBridge](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)
- [OpenCLI Bilibili adapter documentation](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/bilibili.md)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Markdown table and daily plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Up to 100 ordered items; retains visible sources and marks missing details. Unknown durations are excluded from daily time totals, and titles are not treated as proof of video content.]

## Skill Version(s):

1.0.1 (source: release evidence and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
