## Description:

Author repeated task logic once via ATP (paid per call, no account) and reuse it safely, instead of re-reasoning through the same steps every run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[petroshong](https://clawhub.ai/user/petroshong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to route stable, repeatable task shapes through paid ATP calls, so later calls can reuse authored logic instead of re-reasoning from scratch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid ATP calls can spend funds from the configured wallet.

Mitigation: Require explicit approval before agents run the helper for paid requests, and use a fresh wallet with minimal testnet funds.

Risk: The wallet private key in ATP_WALLET_PRIVATE_KEY could be exposed if placed in broad shell environments or committed accidentally.

Mitigation: Keep the key scoped to the execution environment that needs it, avoid broad shell exports when possible, and never store it in project files.

Risk: The helper relies on the x402 dependency stack to sign payment requests.

Mitigation: Review or pin the x402 dependency stack before deployment.

## Reference(s):

- [ATP](https://useatp.com)
- [OpenClaw](https://openclaw.ai)
- [OpenClaw Creating Skills](https://docs.openclaw.ai/tools/creating-skills)
- [OpenClaw Skills](https://docs.openclaw.ai/tools/skills)
- [ClawHub ATP Skill](https://clawhub.ai/petroshong/skills/atp)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with an inline shell command and JSON request body; runtime responses are JSON text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the x402 Python package, and ATP_WALLET_PRIVATE_KEY; calls are paid and currently target Base Sepolia testnet USDC.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
