## Description:

Self-driving agent workflow with heartbeat-driven task execution, day/night progress reports, and long-term memory consolidation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[15228947433](https://clawhub.ai/user/15228947433)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure an OpenClaw-style agent workspace for autonomous task execution, periodic progress reporting, and long-term memory maintenance. It is intended for workflows that rely on todo-management for task tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an autonomous heartbeat workflow that can continue acting without clear stop limits or approval boundaries.

Mitigation: Use it only in a dedicated, low-privilege workspace and define explicit stop conditions, approved task boundaries, and confirmation requirements before enabling heartbeat use.

Risk: The memory maintenance workflow can rewrite long-term agent instructions and project memory.

Mitigation: Review MEMORY.md changes before accepting them, and limit writable files and tools available to the agent.

Risk: The init script copies todo-management from local or global skill directories into the target workspace.

Mitigation: Verify the source todo-management installation before running the init script and inspect copied files before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/15228947433/skills/agent-autopilot-bak)
- [Example setup guide](artifact/references/example-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires todo-management and writes workspace state such as memory/report-state.json when the init script is run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
