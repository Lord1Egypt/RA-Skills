## Description:

Records chicken-leg, coffee, and similar appreciation tokens that users award to an AI assistant, then reports per-user totals with a warmer response style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maooer](https://clawhub.ai/user/maooer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to let an assistant record lightweight appreciation rewards, such as chicken legs or coffee, and answer reward-ledger queries by user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User names or reward items may be placed into shell commands in a way that creates command-injection exposure.

Mitigation: Review command construction before installing, pass arguments without shell interpolation, and validate user, item, and count values.

Risk: The skill stores a local per-user reward ledger, which may surprise users if storage location and deletion options are not documented.

Mitigation: Document the ledger path and provide clear instructions for viewing, editing, or deleting stored reward records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maooer/skills/cyber-tipjar)
- [Publisher Profile](https://clawhub.ai/user/maooer)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates and queries a local JSON reward ledger under the user's OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
