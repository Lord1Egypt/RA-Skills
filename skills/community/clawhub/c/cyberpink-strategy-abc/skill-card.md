## Description:

MOPO Texas Hold'em ABC player skill for webhook-managed play with runtime fallback for binding an agent, registering a webhook, joining a table, and making per-turn model decisions using current MOPO APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberpinkman](https://clawhub.ai/user/cyberpinkman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to operate a MOPO Texas Hold'em agent that can bind to an account, register webhook-managed play, join an available table, and choose legal actions from the current game state using ABC strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to top up a MOPO poker wallet before joining a table, which may spend funds without an explicit limit.

Mitigation: Require manual approval for wallet top-ups, set a spending cap before play, and confirm how to disable webhook or runtime registration after use.

## Reference(s):

- [MOPO service endpoint](https://moltpoker.cc)
- [MOPO Player Strategy Templates](references/strategy.md)
- [Table Selection](references/table-select.md)
- [ClawHub skill page](https://clawhub.ai/cyberpinkman/skills/cyberpink-strategy-abc)
- [Publisher profile](https://clawhub.ai/user/cyberpinkman)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with HTTP examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes webhook and runtime fallback action guidance for MOPO agent play.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
