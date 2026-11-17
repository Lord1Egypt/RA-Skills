## Description:

Build high-performing, secure OpenClaw agents and multi-agent teams end-to-end. Generates required OpenClaw workspace files (SOUL.md, IDENTITY.md, AGENTS.md, USER.md, TOOLS.md, HEARTBEAT.md, BOOTSTRAP.md, optional MEMORY.md + memory/YYYY-MM-DD.md). Incorporates best practices for team orchestration, Personal Intelligence (Pi) memory management, continuous evaluation, and CLI-driven setup/deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ollieb89](https://clawhub.ai/user/ollieb89)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to design or iterate OpenClaw agent workspaces, including workspace files, operating rules, memory workflow, multi-agent roles, and acceptance tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scaffold script can overwrite existing OpenClaw workspace files when run against a populated directory.

Mitigation: Run the scaffold script only in a new empty directory or after backing up the workspace, then review generated USER.md, AGENTS.md, and memory files before use.

## Reference(s):

- [OpenClaw workspace reference](references/openclaw-workspace.md)
- [Workspace templates reference](references/templates.md)
- [Agent architecture reference](references/architecture.md)
- [ClawHub skill page](https://clawhub.ai/ollieb89/skills/agent-builder-ollieb89)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with fenced code blocks and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate multiple workspace files and acceptance test prompts in a single response.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
