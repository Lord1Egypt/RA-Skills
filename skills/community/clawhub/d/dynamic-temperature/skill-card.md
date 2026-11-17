## Description:

Dynamic Temperature helps agents choose an LLM temperature for scheduling, communication, creative writing, irreversible actions, and other task types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this guidance-only skill to classify tasks and choose a corresponding model temperature. It keeps irreversible or factual work deterministic while allowing warmer communication and creative drafting where appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad temperature policy can affect many task types if copied into agent configuration or identity.

Mitigation: Review the desired task categories and apply config or frontmatter changes deliberately.

Risk: Irreversible actions such as sending messages or deleting data may be over-automated if temperature guidance is treated as permission to act.

Mitigation: Keep explicit confirmation requirements for sending, deleting, posting, or other irreversible actions.

Risk: The artifact is deprecated because the behavior was merged into SOUL.md; using it only as a triggered skill may miss cases where temperature policy should always apply.

Mitigation: Prefer the maintained SOUL.md temperature guide for global behavior, or document when this standalone skill should be invoked.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with task-to-temperature tables and decision rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution; recommends temperature values from 0.0 to 0.8.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
