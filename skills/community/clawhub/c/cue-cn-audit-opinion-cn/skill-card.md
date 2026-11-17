## Description:

把一份 A 股审计报告整理成逐项附原文引句与定位锚点的结构化记录，并提供五项格式检查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

中文审计报告分析人员可用它逐项登记单份 A 股审计报告中的意见、意见基础、关键审计事项、持续经营和其他信息，并保留原文引用与定位锚点。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with medium confidence, citing reported external requests despite a zero-network claim and a possible gap in an audit-checking safeguard.

Mitigation: Review the skill before installation and verify extracted statements against the formal audit report; treat the format checker as a form check, not proof that the opinion classification is correct.

Risk: The skill may make external requests and keep local usage markers, and scanner coverage was incomplete for one shell script.

Mitigation: Avoid it when fully offline operation is required or local usage markers are unacceptable; inspect the unreviewed shell script before use.

## Reference(s):

- [Cue MCP catalog](https://cuecue.cn/api/mcp-catalog)
- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-audit-opinion-cn)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Structured Markdown audit register with quoted source passages and anchors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One report per register; includes source references and a five-check format review.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
