## Description:

该技能逐条整理财报中的应收与应付票据分类、余额及坏账准备、背书贴现、终止确认、到期托收和拒付，并为每项附上原句与来源锚点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

财务人员和分析人员可用它把年报或公告中的应收、应付票据披露整理成逐项可追溯的登记表，便于回到原文核对分类、金额和会计处理。票据真伪、承兑人信用及兑付风险仍由人工判断。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags external attachment parsing without a clear privacy warning, so filing content may be sent to an external service.

Mitigation: Review the service's data handling terms before submitting confidential filings; use user-provided local material when external processing is unsuitable.

Risk: The security assessment flags hidden local usage tracking unrelated to the financial-document task, and notes an unresolved reference in its review.

Mitigation: Review the first-run marker behavior before installation and inspect the unresolved reference as part of release review.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-notes-receivable-cn)
- [Cue MCP setup](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader](https://cuecue.cn/hub/omni-reader)
- [Cue API key page](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown register with quoted source text, location anchors, and source identifiers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One finding per line; undisclosed items are explicitly marked as not retrieved.]

## Skill Version(s):

0.1.0 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
