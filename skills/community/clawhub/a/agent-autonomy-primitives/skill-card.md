## Description:

Build long-running autonomous agent loops using ClawVault primitives (tasks, projects, memory types, templates, heartbeats).

This skill is ready for commercial/non-commercial use.

## Publisher:

[g9pedro](https://clawhub.ai/user/g9pedro)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to organize autonomous agents around typed memory, task files, project grouping, configurable schemas, and heartbeat-driven work queues. It also guides adaptation across OpenClaw, LangChain, CrewAI, AutoGen, custom loops, and shared-vault multi-agent setups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous heartbeat loops can execute queued work outside the user's intended scope.

Mitigation: Restrict the task queue to approved work, run agents in a least-privileged sandbox, and require human approval for destructive, external, financial, credential-related, or irreversible actions.

Risk: An unpinned global ClawVault installation can change behavior across environments.

Mitigation: Pin and verify the ClawVault package before installation, and avoid global or privileged installs where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/g9pedro/skills/agent-autonomy-primitives)
- [Adaptation Guide](references/adaptation-guide.md)
- [Template Customization Guide](references/template-customization.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow guidance for creating ClawVault-backed memory, tasks, projects, schemas, and heartbeat loops.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
