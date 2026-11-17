## Description:

Orchestrate multi-agent teams with defined roles, task lifecycles, handoff protocols, and review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nuradil](https://clawhub.ai/user/nuradil)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to set up sustained multi-agent workflows with clear roles, task states, handoffs, artifact paths, and review gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coordinating multiple sub-agents can expand the number of actors that read or write project files.

Mitigation: Keep agent permissions narrow, use explicit shared output paths, and verify artifact locations before accepting a handoff.

Risk: Scheduled dispatch or health-check patterns can act on stale or incorrect task state if enabled without oversight.

Mitigation: Require orchestrator-owned state transitions, timestamped comments, and review before enabling recurring automation.

Risk: Quality can drift when builders approve their own work or review gates are skipped.

Mitigation: Use cross-role reviews and concrete verification steps before marking multi-agent work done.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nuradil/skills/agent-team-orchestration-1)
- [Team Setup](references/team-setup.md)
- [Task Lifecycle](references/task-lifecycle.md)
- [Communication](references/communication.md)
- [Patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with examples, templates, and inline command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no executable code or hidden behavior identified by the security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
