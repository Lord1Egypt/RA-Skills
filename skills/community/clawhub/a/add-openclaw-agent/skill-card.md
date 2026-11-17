## Description:

Create a new OpenClaw agent via exec (openclaw agents add) and configure its identity + operating rules by editing the new workspace files (IDENTITY.md, AGENTS.md).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiguazhiprince](https://clawhub.ai/user/xiguazhiprince)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create a new isolated OpenClaw agent, confirm the CLI action, and configure the agent's identity, role, task, and operating rules in its workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates persistent OpenClaw agents and writes operating rules into workspace files.

Mitigation: Review the final agent name, workspace path, optional flags, and IDENTITY.md or AGENTS.md content before allowing execution or file edits.

Risk: Shell command arguments for agent creation may be unsafe if names, paths, or flags are not checked carefully.

Mitigation: Use the non-interactive command only after explicit user confirmation, and verify normalized agent IDs, workspace paths, and optional flags before execution.

Risk: Identity and operating-rule files can persist sensitive or unintended content.

Mitigation: Avoid storing secrets in IDENTITY.md, AGENTS.md, or related workspace files.

## Reference(s):

- [Multi-Agent Routing](/concepts/multi-agent)
- [Agent workspace](/concepts/agent-workspace)
- [Agents CLI](/cli/agents)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before running agent creation commands; may edit persistent workspace files after creation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
