## Description:

Check USDC balance across supported Base and Solana networks when a user wants to view funds, verify wallet balance, or see how much USDC is available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to check USDC balances across Base and Solana networks through the Agnic CLI. It helps verify available funds before wallet or x402 payment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable npm package while handling wallet credentials and financial balance data.

Mitigation: Install only after reviewing the agnic npm package and its update process, prefer a version-pinned command, and run balance checks in a restricted environment.

Risk: Authentication may rely on AGNIC_TOKEN or an explicit token argument.

Mitigation: Use a narrow, revocable token and avoid exposing broader environment secrets to the command environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Agnic CLI authentication through browser login, AGNIC_TOKEN, or an explicit token argument.]

## Skill Version(s):

2.0.2 (source: server evidence release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
