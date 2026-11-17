## Description:

Manage Coder workspaces and AI coding agent tasks via CLI. List, create, start, stop, and delete workspaces. SSH into workspaces to run commands. Create and monitor AI coding tasks with Claude Code, Aider, or other agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[developmentcats](https://clawhub.ai/user/developmentcats)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to manage Coder workspaces, run remote workspace commands, and create or monitor Coder AI coding tasks from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to use a Coder session token and connect to a configured Coder deployment.

Mitigation: Install only for trusted Coder deployments and provide session tokens through the expected agent environment rather than embedding them in prompts or files.

Risk: Delete, restart, and remote SSH commands can change or remove workspace state.

Mitigation: Review workspace and task names before destructive operations and treat remote commands as capable of modifying files or services inside the target workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/developmentcats/skills/coder-workspaces)
- [Coder Docs](https://coder.com/docs)
- [Coder CLI Docs](https://coder.com/docs/install/cli)
- [Coder Tasks](https://coder.com/docs/ai-coder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Coder CLI plus CODER_URL and CODER_SESSION_TOKEN in the agent environment.]

## Skill Version(s):

1.5.5 (source: server release metadata and changelog, released 2026-02-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
