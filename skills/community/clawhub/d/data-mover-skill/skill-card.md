## Description:

跨系统数据自动搬运工 - OCR 识别 + 自动复制粘贴 + 多系统支持

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams use this skill to extract data from screens, documents, spreadsheets, email, and web forms and move it between business systems with OCR, field mapping, and validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests screen capture and clipboard access, which can expose sensitive information.

Mitigation: Use only with authorized, non-sensitive screens or test data unless explicit consent prompts and scoped capture controls are added.

Risk: Captured screen data may remain on disk.

Mitigation: Add screenshot cleanup or encrypted storage before use with sensitive data.

Risk: The release overstates some safeguards and automation behavior.

Mitigation: Confirm dry-run behavior and update documentation to match implemented protections before deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sxliuyu/skills/data-mover-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also describe generated local data files, logs, validation results, and progress reports.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
