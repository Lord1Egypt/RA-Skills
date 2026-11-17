## Description:

把截图或列表转成仓位、权重、集中度和约束的组合工作包。

This skill is ready for commercial/non-commercial use.

## Publisher:

[minguncle](https://clawhub.ai/user/minguncle)

### License/Terms of Use:

MIT-0

## Use Case:

投资者、顾问或分析型代理在收到A股账户截图或持仓列表后，用它先整理账户快照、持仓权重、集中度、主题暴露、执行约束和待确认缺口，再交给后续分析或动作路由。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots or holdings lists may contain account numbers, names, broker identifiers, or other personal details.

Mitigation: Redact unnecessary personal details before using the skill.

Risk: Portfolio diagnostics may be mistaken for trading instructions.

Mitigation: Treat outputs as structure analysis only and require separate review before any buy, sell, or rebalance decision.

Risk: Unreadable screenshots or incomplete holdings data can lead to missing or uncertain fields.

Mitigation: Mark unclear values as gaps and ask for confirmation instead of guessing.

## Reference(s):

- [Calibration Template](references/calibration-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown structured portfolio packet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes account snapshot, normalized holdings table, concentration metrics, theme and style exposure, constraints, and missing information.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
