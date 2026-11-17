## Description:

Orchestrate multi-agent teams with defined roles, task lifecycles, handoff protocols, and review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team leads use this skill to set up recurring multi-agent workflows, route tasks, manage handoffs, and enforce review gates across orchestrator, builder, reviewer, and ops roles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Multi-agent workflows can give agents broader workspace visibility or write access than intended.

Mitigation: Define which agents may read or write each workspace and keep shared directories scoped to the project before using the skill.

Risk: Scheduled tasks, credential access, or high-impact changes may proceed without appropriate human oversight.

Mitigation: Require human approval for scheduled operations, credential access, and high-impact changes.

## Reference(s):

- [Team Setup](artifact/references/team-setup.md)
- [Task Lifecycle](artifact/references/task-lifecycle.md)
- [Communication](artifact/references/communication.md)
- [Patterns](artifact/references/patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/lean-zhouchao/skills/agent-team-orchestration-local-backup)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with structured workflow templates and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No automatic code execution or installation behavior; outputs depend on the agent applying the playbook to the current workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
