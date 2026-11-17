## Description:

Orchestrates multi-agent teams by defining roles, task lifecycles, handoff protocols, communication patterns, and review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team leads use this skill to set up sustained multi-agent workflows with clear roles, shared artifacts, structured task state, handoffs, and review gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared directories can expose sensitive specs, reviews, or artifacts if every agent receives broad read and write access.

Mitigation: Define per-role access boundaries before installation and keep deliverables in agreed shared paths with only the permissions each role needs.

Risk: Recurring ops workflows can run at the wrong cadence or act on stale task state if schedules and triggers are vague.

Mitigation: Define exact schedules or trigger conditions, require task comments for state changes, and review recurring summaries before acting on them.

Risk: Spawned agents may receive tools or credentials beyond the needs of their assigned role.

Mitigation: Grant only the model capabilities, tools, and credential access required for the task, and require escalation when access is missing.

Risk: Poor handoffs can lead to lost artifacts, unverified work, or unclear next actions.

Mitigation: Require every handoff to include what was done, exact artifact paths, verification steps, known issues, and the next owner.

## Reference(s):

- [Team Setup](references/team-setup.md)
- [Task Lifecycle](references/task-lifecycle.md)
- [Communication](references/communication.md)
- [Patterns](references/patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with templates, checklists, and example workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; outputs may include role definitions, task states, handoff notes, artifact conventions, and review workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
