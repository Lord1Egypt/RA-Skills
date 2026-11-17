## Description:

Feishu Doc Manager helps agents publish Markdown content to Feishu Docs with automatic formatting, table conversion, permission management, and batch writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuai-daidai](https://clawhub.ai/user/shuai-daidai)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to create, write, append, update, and manage Feishu Docs content from Markdown while handling collaborator permissions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document edits, deletions, overwrites, or collaborator permission changes could affect live Feishu content.

Mitigation: Use least-privilege Feishu credentials and confirm destructive edits, overwrites, and permission changes before allowing the agent to act.

Risk: Unpinned GitHub install instructions can install code that differs from the reviewed release.

Mitigation: Install from a reviewed version when possible, or pin and inspect the repository before placing it in the active skills directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuai-daidai/skills/feishu-doc-manager)
- [Project homepage](https://github.com/Shuai-DaiDai/feishu-doc-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls, Configuration]

**Output Format:** [Markdown and operational guidance for Feishu document actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify Feishu documents and collaborator permissions through configured Feishu credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
