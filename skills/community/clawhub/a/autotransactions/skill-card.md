## Description:

Use Python to run a minimal authenticated Polymarket trading client with a private key loaded from private.env for market and limit buy/sell orders, order lookup, and cancellation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvnhaowen](https://clawhub.ai/user/jvnhaowen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading automation agents use this skill to configure and run a minimal Python client for authenticated Polymarket order placement, order queries, and cancellation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a raw wallet private key and can load it from private.env.

Mitigation: Use only a dedicated low-balance trading wallet, never a primary wallet, and keep private.env out of git and backups with restrictive permissions.

Risk: The skill can make live financial changes through order placement, allowance updates, and cancel-all commands.

Mitigation: Review the exact token ID, market, side, amount, price, approvals, and cancellation target before running live commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jvnhaowen/skills/autotransactions)
- [Python minimal mapping](artifact/references/poly-sdk-mapping.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Polymarket wallet private key and emits JSON responses from trading and order-management commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
