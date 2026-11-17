## Description:

Batch desensitize docx/xlsx files via keyword and regex rules, with one-click reversible restoration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longjf25](https://clawhub.ai/user/longjf25)

### License/Terms of Use:

MIT

## Use Case:

Developers and document operators use this skill to sanitize Word and Excel workspaces by replacing configured sensitive terms, regex matches, and filenames with placeholders, then restore originals from the generated mapping record when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The restoration record can expose original sensitive values needed to undo redaction.

Mitigation: Keep _sanitize_record.json out of source control and shared folders, review it before use, and delete it when restoration is no longer needed.

Risk: File-writing and conversion behavior can affect workspace outputs or invoke external converters.

Mitigation: Run only in a controlled workspace, review _sanitize_config.json before execution, and avoid --auto-convert unless the external converter skill is trusted and unchanged.

## Reference(s):

- [Document Sanitizer ClawHub release](https://clawhub.ai/longjf25/skills/document-sanitizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for running a sanitizer script that writes sanitized files, restored files, and a sensitive mapping record in the target workspace.]

## Skill Version(s):

1.5.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
