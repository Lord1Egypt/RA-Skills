## Description:

A system for designing and managing multi-level subagent hierarchies in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to plan and coordinate explicit multi-level subagent hierarchies, map work to appropriate capability levels, and supervise escalation, quality gates, and resource use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose broad subagent hierarchy changes, including creation, reactivation, escalation, and tool grants.

Mitigation: Treat each proposed agent lifecycle action and tool grant as a separate operator approval decision before execution.

Risk: Higher hierarchy levels describe broad or custom tool access that could expand the operational impact of a delegated task.

Mitigation: Grant only the specific tools needed for the confirmed task, with extra review for high-level agents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/agent-hierarchy-100)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [Hierarchy orchestrator](artifact/orchestrator/SKILL.md)
- [Hierarchy tests](artifact/tests/hierarchy-tests.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces hierarchy plans, level mappings, delegation guidance, quality checks, and configuration-oriented text; it does not include executable code.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
