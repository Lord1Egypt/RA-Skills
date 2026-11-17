## Description:

Helps agents query Dogecoin Core node status and perform basic wallet RPC lookups, including balances and transaction history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, Dogecoin node operators, and automation teams use this skill to inspect Dogecoin Core sync and network status, wallet balances, unspent outputs, generated receiving addresses, and recent transaction history through agent-proposed CLI/RPC commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The trigger text is broad and mismatched, including database, SQL, analytics, and reporting language outside the Dogecoin node-management use case.

Mitigation: Constrain activation to explicit Dogecoin Core node or wallet RPC requests and avoid using the skill for generic database, SQL, analytics, or reporting work.

Risk: The skill can propose command execution against a local Dogecoin Core node, which may expose wallet balances, addresses, transaction history, or local RPC configuration details.

Mitigation: Review commands before execution, keep Dogecoin RPC bound to localhost, avoid exposing RPC credentials, and redact sensitive wallet or transaction details from shared outputs.

Risk: Generating a new wallet address is under-disclosed relative to the mainly read-oriented positioning of the skill.

Mitigation: Require explicit confirmation before generating new receiving addresses or displaying wallet balances and transaction history.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before execution because the skill may propose local Dogecoin Core RPC commands that expose wallet balances, addresses, or transaction history.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact metadata: 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
