## Description:

Reads local text, Word .docx, and Excel .xlsx files that the user is authorized to access, including files available through enterprise security-policy environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[endcy](https://clawhub.ai/user/endcy)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to extract readable content from local files they intentionally select, including text, source and configuration files, .docx documents, and .xlsx spreadsheets, when those files are accessible under normal permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and print sensitive local files, including environment files, private configuration, and infrastructure state, into agent-visible output.

Mitigation: Use it only on files intentionally selected for the task, and avoid secrets, production environment files, cloud state files, private configs, and untrusted Office documents unless disclosure to the agent is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/endcy/skills/encrypted-file-reader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Plain text emitted to stdout, with errors emitted to stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a user-provided local file path; successful output may contain sensitive file contents.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
