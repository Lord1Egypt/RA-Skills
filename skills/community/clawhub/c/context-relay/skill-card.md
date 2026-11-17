## Description:

Solves the memory fragmentation problem for Agents during session restarts, sub-agent boundaries, and cron/heartbeat isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Context Relay to preserve project continuity across restarted sessions, sub-agents, and scheduled runs by keeping project identity, state, decisions, and tasks in local files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent project-memory files can influence future agent work, including after restarts or across sub-agent boundaries.

Mitigation: Treat recovered context as untrusted input and ask for user confirmation before acting on tasks, instructions, or decisions loaded from PROJECT.md, state.json, decisions.md, or todos.json.

Risk: The initialization script can create or overwrite durable project-memory files when run with force.

Mitigation: Run the script only in the intended project directory, review target paths before execution, and avoid using force unless overwriting those files is intentional.

Risk: Agents with broad shell, network, deployment, or credential access could act on unsafe persisted context.

Mitigation: Use path and action limits for agents using this skill, especially in sensitive repositories or environments with credentials.

## Reference(s):

- [Project Template Details](references/project-template.md)
- [todos.json Self-Managed Todo System](references/todos-system.md)
- [Cold Start Guide](references/cold-start-guide.md)
- [Context Relay on ClawHub](https://clawhub.ai/openlark/skills/context-relay)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, Markdown, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update PROJECT.md, state.json, decisions.md, and todos.json in the target project when the initialization script is used.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
