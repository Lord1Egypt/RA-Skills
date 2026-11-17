## Description:

为 A 股未来限售解禁整理逐轮日历，记录日期、解禁方、股数、占总股本比例和成本区间，并为每项信息附上原始公告来源。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

External users researching A-share disclosures can use this skill to organize future restricted-share expiries into a sourced calendar and identify missing announcement details. It does not provide price forecasts or trading recommendations.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The security review flags remote tool discovery that is not clearly disclosed in the skill's data-channel guidance.

Mitigation: Review whether external tool discovery is needed and inspect the discovered tools before relying on them.

Risk: The security review flags inconsistencies in the skill's financial-data rules.

Mitigation: Check that percentage and cost-field handling fits the intended analysis, and verify figures against the original announcements.

Risk: The security review flags an install command that does not pin its source or version.

Mitigation: Inspect the install source and use a version you trust before installing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-lockup-expiry-pressure)
- [Cue MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Seven-section Markdown note with a sourced expiry calendar, pressure ratios, and named missing items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each factual row cites an original disclosure and retrieval date; no investment recommendations.]

## Skill Version(s):

0.1.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
