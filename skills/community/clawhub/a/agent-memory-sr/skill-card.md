## Description:

Stop your AI agent from forgetting everything between sessions. Three-tier memory architecture (long-term owner namespace / daily logs / session handoff), cross-channel isolation so group chats never contaminate private sessions, and MASTER_MAP navigation. One command sets up the complete structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to initialize a file-based persistent memory workspace for agents, including user profile, session handoff, daily logs, long-term memory, and navigation files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Editable workspace memory files can become persistent agent instructions and may contain personal or project context.

Mitigation: Review and edit the startup protocol before use, treat HANDOFF.md, daily logs, and MEMORY.md as untrusted notes, and avoid storing secrets or sensitive personal data.

Risk: Remembered instructions could cause an agent to run commands, change files, access credentials, delete data, or contact external services.

Mitigation: Require explicit confirmation before acting on remembered instructions that perform sensitive actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/agent-memory-sr)
- [README](README.md)
- [QUICKSTART](QUICKSTART.md)
- [LIMITATIONS](LIMITATIONS.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and a Python setup script that creates Markdown workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates plain Markdown memory files and directories in the selected workspace; no external dependencies are required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
