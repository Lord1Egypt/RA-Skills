## Description:

Helps agents check and record local action history to reduce duplicate external actions such as posts, messages, token sends, and deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wrentheai](https://clawhub.ai/user/wrentheai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to wrap irreversible or externally visible actions with a local check-before-act and record-after-success workflow. It is intended for actions such as social replies, messages, token sends, webhook triggers, and deployments where repeated execution would create user-visible or operational harm.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Concurrent agents or repeated automation can pass the check step before either run records completion, allowing duplicate irreversible actions.

Mitigation: Use it as a reminder log for low-stakes workflows; for money movement, public posting, production deploys, or other irreversible actions, require atomic reservations or locking before execution and record clear recovery behavior.

Risk: The local action ledger can be edited or removed by processes with access to the data directory.

Mitigation: Store the ledger in a restricted directory and review permissions before relying on it for operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wrentheai/skills/action-guard)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, text]

**Output Format:** [Markdown guidance with inline shell commands and JSONL action records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and reads a local .action-guard/actions.jsonl ledger when the guard script is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
