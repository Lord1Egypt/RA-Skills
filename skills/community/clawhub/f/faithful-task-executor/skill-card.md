## Description:

Faithful Task Executor helps agents preserve user task rules across multi-step work, subagent coordination, and compliance checks to reduce hallucination and execution drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[endcy](https://clawhub.ai/user/endcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn an initial task request into persistent rules, task plans, subagent instructions, compliance checklists, and final summaries. It is intended for complex or concurrent work where the agent must keep outputs traceable to the original requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates local task rule files that may capture sensitive task details.

Mitigation: Review generated rule files before using the workflow on sensitive tasks and avoid storing secrets or private data in task rules.

Risk: Subagent coordination can increase cost, latency, or operational complexity when too many workers run in parallel.

Mitigation: Keep subagent concurrency within limits appropriate for the task and review the planned parallel work before execution.

Risk: Over-broad activation may add unnecessary process steps or steer a simple task into a larger workflow.

Mitigation: Confirm when the skill should activate and use it for multi-step or rule-sensitive work rather than routine single-step requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/endcy/skills/faithful-task-executor)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, JSON]

**Output Format:** [Markdown templates and structured JSON-style status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local task rule, task plan, checklist, subagent task, and summary artifacts for agent workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
