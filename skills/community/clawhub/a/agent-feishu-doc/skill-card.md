## Description:

Guides OpenClaw agents through creating, reading, editing, and sharing Feishu/Lark documents with the Feishu API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmin1113](https://clawhub.ai/user/jmin1113)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, read, edit, and troubleshoot Feishu/Lark documents through Feishu APIs, including collaboration and sharing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public-editable document sharing can expose or allow modification of Feishu documents beyond the intended collaborators.

Mitigation: Prefer private documents, named collaborators, least-privilege roles, and temporary or read-only sharing unless an administrator explicitly approves broader access.

Risk: Global cross-agent session visibility can broaden document and session access between agents.

Mitigation: Do not enable global session visibility unless an administrator explicitly approves it; keep sharing scoped to the agents and documents that require collaboration.

## Reference(s):

- [Agent Feishu Doc ClawHub page](https://clawhub.ai/jmin1113/skills/agent-feishu-doc)
- [Agent Feishu Doc Guide](references/guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON and shell/API command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Feishu API endpoint patterns, permission guidance, and OpenClaw configuration snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
