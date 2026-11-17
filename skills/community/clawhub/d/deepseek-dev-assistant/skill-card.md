## Description:

Read DeepSeek chat share links and continue development from extracted code and docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fhekg](https://clawhub.ai/user/fhekg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn DeepSeek shared chats into local project files, README/TODO summaries, and follow-on implementation work. It is intended for workflows where chat-generated code and project structure need to be extracted, reviewed, and continued in an agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote DeepSeek chat content can influence local file creation and modification.

Mitigation: Use an isolated workspace and review proposed paths, overwrites, and generated files before allowing writes.

Risk: Extracted chats may contain untrusted code or sensitive material.

Mitigation: Avoid chats containing secrets and review extracted code, dependencies, and commands before execution.

Risk: The workflow may request dependency installation, command execution, or persistent memory updates.

Mitigation: Approve dependency installation, command execution, overwrites, and memory persistence only when they are expected for the task.

## Reference(s):

- [DeepSeek Share Page Structure](artifact/references/deepseek-page-structure.md)
- [Example: Extracting and continuing from a DeepSeek chat](artifact/references/example.md)
- [ClawHub skill page](https://clawhub.ai/fhekg/skills/deepseek-dev-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, shell commands, configuration, guidance]

**Output Format:** [Markdown status summaries, local project files, code fragments, README/TODO files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node for the browser-based extraction workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
