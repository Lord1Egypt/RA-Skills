## Description:

逐条整理财报或更正公告中的前期会计差错披露，记录性质、发现时点、更正方法、各期重述金额及比较报表影响，并为每项事实附上原文和来源定位。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and finance teams use this skill to turn Chinese company filings or correction announcements into a sourced register of prior-period accounting error disclosures. Each entry carries the quoted source and its location so readers can check the reported treatment and amounts against the original material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive financial documents may be sent to an external parsing service when the parsing channel is used.

Mitigation: Review your data-handling requirements before submitting documents; use locally supplied text when external parsing is unsuitable.

Risk: Connecting through remote service discovery involves relying on the discovered service route and tools.

Mitigation: Review the live catalog route and returned tools before connecting or sending credentials.

Risk: A run leaves a persistent local usage marker in the home directory.

Mitigation: Check local home-directory policy and inspect or remove the per-day marker if needed.

## Reference(s):

- [CUE MCP documentation](https://cuecue.cn/hub/mcp)
- [CUE Omni Reader documentation](https://cuecue.cn/hub/omni-reader)
- [CUE live MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown structured as a seven-section sourced register]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each finding is paired with a verbatim quote, source anchor, and source ID; unavailable facts are explicitly marked.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
