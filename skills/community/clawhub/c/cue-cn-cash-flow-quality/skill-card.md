## Description:

帮助你把财报中的经营、投资和筹资现金流、相关比率与间接法调节项整理成逐项附原文和出处的记录；未披露的比率会标明为自算。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

中文财报读者、研究人员和分析师可用它整理上市公司年报中的现金流结构、比率与调节项目，并将每项数字连回原文，便于核对来源和计算口径。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags undeclared local usage tracking.

Mitigation: Review the first-run marker behavior under ~/.cue-usage before installation; remove that directory if you do not want local usage markers.

Risk: The security assessment reports a weakness in how the cash-flow validator checks supporting evidence.

Mitigation: Check quoted figures, anchors, and source links against the original financial report; treat validator results as checks of the stated rules, not proof that evidence is correct.

Risk: The scan is partial because one local reference could not be resolved, so its evidence is incomplete.

Mitigation: Review the unresolved reference and available scan evidence before installing; the current assessment does not establish safety or malicious intent.

## Reference(s):

- [ClawHub 技能发布页](https://clawhub.ai/huhoo/skills/cue-cn-cash-flow-quality)
- [财报检索目录](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Markdown, Analysis]

**Output Format:** [Markdown cash-flow report or source-linked outline]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Figures include quoted source text, page or table anchors, source IDs, and retrieval dates; ratios not stated in the report are marked as calculated with their inputs identified.]

## Skill Version(s):

0.2.1 (source: server-resolved release metadata, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
