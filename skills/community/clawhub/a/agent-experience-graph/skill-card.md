## Description:

Use when an agent should learn from prior task-solving traces, recommend tools or skills for a new decomposed task, record reusable execution experience, or compare current subtasks with solved tasks from other agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yao23](https://clawhub.ai/user/yao23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to retrieve similar solved traces, recommend reusable tools, skills, workflow patterns, and warnings, and record sanitized traces for future agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trace libraries may contain secrets, private user data, proprietary snippets, or raw customer content.

Mitigation: Store only sanitized summaries and redact sensitive content before appending or sharing traces.

Risk: Recommendations from stale or untrusted traces can mislead an agent.

Mitigation: Treat retrieved traces as evidence, review matched subtasks and outcomes, and apply only recommendations that fit the current constraints.

Risk: Automatically following recommended tools, skills, or lessons from untrusted traces can transfer unsafe practices.

Mitigation: Require review before an agent follows recommendations from untrusted trace libraries.

## Reference(s):

- [Agent Experience Graph repository](https://github.com/yao23/agent-experience-graph)
- [Agent Experience Graph on ClawHub](https://clawhub.ai/yao23/skills/agent-experience-graph)
- [Trace Schema](references/trace_schema.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown instructions with JSON examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and a readable JSON trace library; network access is not required.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
