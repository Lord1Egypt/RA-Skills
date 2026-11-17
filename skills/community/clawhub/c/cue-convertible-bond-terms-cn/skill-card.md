## Description:

把一份 A 股可转债募集说明书或发行公告整理成八项带原句与来源锚的条款卡，并将收益与触发判断留待人工核验。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

面向需要核读 A 股可转债条款的用户，从募集说明书或发行公告提取八项条款原文和出处，辅助核对数字触发条件。

### Deployment Geography for Use:

China (A-share market)

## Known Risks and Mitigations:

Risk: The security assessment rates the release suspicious with medium confidence and cites an unexplained MCP discovery capability and unpinned installation commands.

Mitigation: Consider avoiding installation until the discovery behavior is explained or removed and the installer and source are pinned.

Risk: The assessment flags document-processing privacy expectations and a validator issue; scan coverage is partial because a referenced path was missing.

Mitigation: Clarify document-processing privacy expectations, address the validator issue, and review the missing path before relying on the assessment.

## Reference(s):

- [Convertible bond clause reference](artifact/references/cb-clauses.md)
- [Cue data leg configuration](https://cuecue.cn/hub/mcp)
- [Cue attachment parsing configuration](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown clause card with verbatim excerpts and source anchors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Eight named clauses, source comparison and missing-data sections; financial outcomes, trigger predictions, ratings, and target prices remain [待人工]; no subscription or conversion instructions.]

## Skill Version(s):

0.1.4 (source: server release evidence, artifact/SKILL.md, artifact/CHANGELOG.md; released 2026-11-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
