## Description:

Check your agent's on-chain ERC-8004 identity, trust score, and KYA credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to check an Agnic agent's on-chain identity, trust score, KYA credentials, and active or suspended status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a mutable third-party npm CLI that may handle authentication tokens.

Mitigation: Install only after reviewing the current Agnic CLI release, prefer a pinned CLI version, and avoid passing tokens on the command line.

Risk: Unrelated secrets in the agent environment could be exposed to the third-party CLI process.

Mitigation: Run the skill with the minimum required environment variables and avoid exposing unrelated credentials in the agent environment.

## Reference(s):

- [Agnic application](https://app.agnic.ai)
- [ClawHub skill page](https://clawhub.ai/agnicpay-prog/skills/get-agent-identity)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [JSON from the Agnic CLI with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Agnic authentication and may use AGNIC_TOKEN for headless operation.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
