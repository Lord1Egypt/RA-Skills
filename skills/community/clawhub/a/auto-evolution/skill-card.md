## Description:

Multi-agent auto-evolution system with hybrid mode that orchestrates review-execute-audit loops across Coordinator, Reviewer, Executor, and Auditor roles, with manual subtasks for simple tasks and Reviewer-generated subtasks for complex tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate autonomous multi-agent task execution, splitting goals into subtasks and cycling through review, execution, audit, and packaging steps. It is intended for workspaces that can isolate spawned agents and supervise task-state changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeated sub-agent execution can continue with weak operational boundaries.

Mitigation: Run the skill only in an isolated workspace with limited tools, no unnecessary credentials, and explicit human approval for sensitive file, command, network, or skill-modifying actions.

Risk: Untrusted task files or unsafe task-state handling can affect the review-execute-audit loop.

Mitigation: Trust and validate task files before enabling automation, fix filename and path handling, enforce iteration limits, and make review and audit parsing fail closed.

Risk: Unattended cron or heartbeat execution can magnify workflow errors.

Mitigation: Do not enable unattended cron or heartbeat operation until the security guidance has been addressed and the workflow has been reviewed in the target workspace.

## Reference(s):

- [OpenClaw](https://github.com/openclaw/openclaw)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)
- [Task Example](references/task-example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON-oriented task prompts with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces prompts and task-state updates for review, execution, audit, monitoring, and packaging workflows.]

## Skill Version(s):

2.0.0 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
