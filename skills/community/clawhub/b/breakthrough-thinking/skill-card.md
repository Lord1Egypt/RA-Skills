## Description:

Breakthrough Thinking helps an agent recover from stalled problem solving by switching to a relevant mental model, applying it, and iterating until the task is solved or clearly bounded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1204tmax](https://clawhub.ai/user/1204tmax)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and agents use this skill when an agent appears stuck, repeats failed approaches, or is asked to rethink a problem. The skill prompts the agent to summarize the dead end, choose one relevant mental model, apply it directly, and continue with a different model if needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases such as "continue" or "try another way" may activate the skill unexpectedly.

Mitigation: Review or narrow trigger wording before deployment when precise activation control is required.

Risk: A forced shift in reasoning frame can produce plausible but incorrect guidance if the agent does not verify the result.

Mitigation: Require completion claims to include evidence, as specified by the skill, and review generated guidance before acting on it.

## Reference(s):

- [Mental Models for Breaking Through](references/mental-models.md)
- [Breakthrough Thinking ClawHub release](https://clawhub.ai/1204tmax/skills/breakthrough-thinking)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown using the [Breakthrough] summary format]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only guidance; the skill itself does not install code, access credentials, persist changes, or create hidden data flows.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
