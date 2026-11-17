## Description:

Use Cursor Agent for coding tasks through the local Cursor CLI or through a connected Cursor/VS Code IDE via the OpenClaw Node protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyaner0201](https://clawhub.ai/user/xiaoyaner0201)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to choose between Cursor CLI workflows and IDE-backed OpenClaw Node workflows for code generation, refactoring, diagnostics, testing, debugging, and Git operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes install instructions that pipe a remote Cursor installer into a shell.

Mitigation: Prefer a signed installer or package-manager installation path, and verify the installer source before execution.

Risk: Cursor Agent can modify files, run commands, and interact with Git.

Mitigation: Keep sandboxing enabled where possible, review changes in version control, and avoid force mode until proposed edits are understood.

Risk: Cloud handoff can move coding work outside the local environment.

Mitigation: Do not use cloud handoff with secrets, regulated data, or proprietary repositories unless that use is approved.

## Reference(s):

- [OpenClaw Node for VS Code](https://marketplace.visualstudio.com/items?itemName=xiaoyaner.openclaw-node-vscode)
- [vscode-node Skill](https://clawhub.ai/xiaoyaner0201/vscode-node)
- [Cursor Agent Cloud](https://cursor.com/agents)
- [Cursor CLI Installer](https://cursor.com/install)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to invoke local Cursor CLI commands or OpenClaw Node commands against a connected IDE.]

## Skill Version(s):

3.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
