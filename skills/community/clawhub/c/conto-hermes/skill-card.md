## Description:

Enforce fine-grained spending policies on AI agent payments before transfers, swaps, bridges, and paid API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwattana](https://clawhub.ai/user/kwattana)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to require policy approval before an AI agent moves funds, executes swaps or bridges, or pays x402-style API endpoints. It also guides policy setup, payment confirmation, denial handling, and Conto dashboard workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent payment approval and policy-management authority.

Mitigation: Use a standard payment-approval key for normal operation, avoid admin policy commands from chat, and review each transfer before execution.

Risk: SDK keys may be written to the local Hermes environment file.

Mitigation: Protect the Hermes environment file and rotate any SDK key that may have been exposed.

Risk: A misconfigured API endpoint could send approval requests to the wrong service.

Mitigation: Keep CONTO_API_URL fixed to the real HTTPS Conto endpoint for production use.

Risk: Approved payment flows still involve final fund transfers.

Mitigation: Confirm every transfer yourself, stop on policy denials, and fail closed if the policy service is unavailable.

## Reference(s):

- [Conto Hermes Skill](https://clawhub.ai/kwattana/skills/conto-hermes)
- [Conto Homepage](https://conto.finance)
- [Conto SDK Docs - Hermes](https://conto.finance/docs/sdk/hermes)
- [Conto Policy Documentation](https://conto.finance/docs/policies)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline shell commands, JSON examples, and API request patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Conto account, network access to the Conto API, curl, jq, python3, and a CONTO_SDK_KEY for runtime use.]

## Skill Version(s):

1.8.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
