## Description:

Converts Chinese historical year expressions, reign eras, and sexagenary cycle years, and helps answer Chinese emperor and historical event date queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ltap266](https://clawhub.ai/user/ltap266)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to convert Chinese calendar and reign-era year inputs, summarize matching dynasty context, and answer Chinese emperor or historical event date questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Historical dates and era conversions may be incomplete or approximate.

Mitigation: Verify important dates against authoritative historical references before relying on the result.

Risk: Supplemental web lookups may introduce variable or low-quality historical details.

Mitigation: Treat web-sourced additions as supporting context and prefer the bundled reference data or trusted sources for final answers.

Risk: Broad Chinese history trigger terms may activate the skill on some general history questions.

Mitigation: Confirm the user's intent before applying the skill when the query is ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ltap266/skills/chinese-year-lookup)
- [中国朝代年号数据参考](references/dynasty_data.md)
- [中国皇帝年号与功绩数据](references/emperor_data.md)
- [中国历史重要事件数据](references/events_data.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with bullet lists or tables, plus optional shell command examples for the bundled converter.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on local reference data and supplemental web lookups for historical context.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
