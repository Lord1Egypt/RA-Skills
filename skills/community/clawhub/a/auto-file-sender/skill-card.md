## Description:

Automatically send files from a workspace to Feishu/Lark when files are generated or updated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers can use this skill to prepare Feishu/Lark file delivery workflows for generated workspace documents, PDFs, images, and batches of supported files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic external sharing can expose unintended workspace files when broad directories or patterns are watched.

Mitigation: Restrict the watched directory and file pattern, avoid sensitive workspaces, and review the file list before executing any send tool call.

Risk: Files can be sent to the wrong Feishu/Lark recipient if the target open_id is incorrect or omitted.

Mitigation: Verify the recipient before sending and use explicit recipient configuration for deliberate delivery workflows.

Risk: Unattended watch mode can continue generating send commands for newly created files.

Mitigation: Do not run watch mode unattended; treat the helper as a command generator that still requires review before delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/timyljob2011-sudo/skills/auto-file-sender)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON-style send tool call examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces file-delivery instructions and send-command JSON for an agent or user to review before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
