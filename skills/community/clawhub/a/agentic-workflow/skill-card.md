## Description:

Enables the Agentic Workflow (Kanban + Heartbeat + QA Subagent). Use this when instructed to set up a continuous, asynchronous task system for any agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mashirops](https://clawhub.ai/user/mashirops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up a heartbeat-driven task board workflow with QA subagent review for asynchronous work tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sets up a persistent heartbeat-driven task executor with broad recurring authority.

Mitigation: Require explicit confirmation before enabling it, keep the executor below higher-priority safety and workspace policies, and document how to disable or remove the HEARTBEAT.md changes.

Risk: The skill suppresses routine progress updates, which can reduce visibility into sensitive queued actions.

Mitigation: Restrict what queued tasks may do and add visible audit logs or progress notices for sensitive actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mashirops/skills/agentic-workflow)
- [Publisher Profile](https://clawhub.ai/user/mashirops)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with YAML and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace task-board and heartbeat guidance for an agent; no separate binary artifact is produced.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
