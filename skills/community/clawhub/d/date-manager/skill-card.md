## Description:

私人日期管家，用于管理生日、纪念日、祭日和祭祖日期，支持公历和农历转换、提醒、节气和假日查询，并要求通过脚本执行日期计算。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chanvging](https://clawhub.ai/user/chanvging)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to record, search, update, and delete personal date records such as birthdays, anniversaries, memorial days, and ancestor-remembrance dates. It also supports date calculations, lunar-calendar conversion, solar-term lookup, holiday countdowns, reminders, and empathetic reminder text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal dates, relationships, and notes are stored in a local plaintext JSON file.

Mitigation: Use the skill only where local plaintext storage is acceptable, avoid entering highly sensitive details, and protect the skill directory with appropriate file-system access controls.

Risk: Optional dependencies affect lunar conversion, solar-term calculation, and holiday lookup behavior.

Mitigation: Install optional dependencies in a virtual environment and pin versions for repeatable results; review date results when dependencies are missing because fallback solar-term data can be approximate.

Risk: Delete commands do not provide an undo flow or explicit confirmation step.

Mitigation: Review record IDs before deletion and back up the local dates JSON file before significant maintenance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chanvging/skills/date-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI output tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local plaintext JSON date records under the skill directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
