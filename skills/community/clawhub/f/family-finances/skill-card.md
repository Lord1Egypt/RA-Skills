## Description:

家庭财务管理系统，用于跟踪资产负债表、现金流量表、投资组合并生成财务健康报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosmos180](https://clawhub.ai/user/cosmos180)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to record household assets, liabilities, monthly income and expenses, and investment holdings, then generate Chinese-language summaries and financial health reports. It is intended for local personal finance tracking with user-provided data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Household financial records are stored as local plaintext JSON.

Mitigation: Restrict permissions on ~/.openclaw/workspace/data/family-finances/, avoid storing highly sensitive account identifiers in notes, and delete records that are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cosmos180/skills/family-finances)
- [Publisher profile](https://clawhub.ai/user/cosmos180)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown guidance with JSON command output from local scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Financial records are stored locally as JSON files under ~/.openclaw/workspace/data/family-finances/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
