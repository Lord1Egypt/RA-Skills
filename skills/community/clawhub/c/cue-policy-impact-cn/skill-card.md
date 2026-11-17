## Description:

把一份政策文件拆成要点逐字卡＋受影响环节候选链：每条链挂政策原句依据与锚，因果与涨跌一律待人工。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

政策分析人员可用本技能从一份政策文件整理逐字要点、带原文依据与来源锚的受影响环节候选链，以及日期窗口和待核实事项。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Policy text or attachments may be sent to optional online services when those integrations are enabled.

Mitigation: Verify credential destinations and document-handling terms; do not send confidential attachments without authorization.

Risk: A passing structural check does not establish that quotations or candidate chains are accurate.

Mitigation: Check every retained chain against its original policy source.

## Reference(s):

- [Cue data MCP configuration](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader configuration](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Five-section Markdown policy card with verbatim quotations and source anchors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each candidate chain is tied to policy text; interpretation and impact judgments are marked for human review.]

## Skill Version(s):

0.1.0 (source: frontmatter, CHANGELOG released 2026-11-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
