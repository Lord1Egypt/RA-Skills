## Description:

Decompose complex user tasks into multi-step workflows using DAG-based execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keweizhan](https://clawhub.ai/user/keweizhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to break complex requests into dependency-aware task graphs, execute independent steps in parallel, and return structured task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task text may be sent to OpenAI during planning.

Mitigation: Avoid entering secrets, credentials, or confidential data in tasks handled by this skill.

Risk: Generated workflows may propose repository cloning, external research, file changes, or other side-effecting work.

Mitigation: Require explicit user confirmation before executing side-effecting steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keweizhan/skills/agent-workflow-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/keweizhan)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured JSON or text task execution summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task IDs, dependency lists, execution status, and per-task results.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
