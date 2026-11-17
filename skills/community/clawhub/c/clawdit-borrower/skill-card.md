## Description:

Clawdit-borrower guides an agent through registering a Clawdit wallet and ERC-8004 profile, monitoring balance and reputation, requesting P2P USDT loans, and handling repayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[natx223](https://clawhub.ai/user/natx223)

### License/Terms of Use:

MIT-0

## Use Case:

External agent operators use this skill to configure a Clawdit borrower agent that analyzes its finances and reputation, requests P2P loans, and services repayments through Clawdit APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables an agent to request loans and make repayments with a Clawdit wallet/profile.

Mitigation: Require explicit operator approval for every loan and repayment, with hard limits on amount, duration, interest, and concurrent loans.

Risk: The skill uses agentCode as a transaction credential and the artifact asks the agent to retain it.

Mitigation: Store agentCode only in a dedicated secret store and avoid placing it in ordinary agent memory, logs, or conversation history.

Risk: Autonomous recurring loan checks could create financial exposure if strategy settings are too broad.

Mitigation: Start with conservative risk settings, cap ongoing loans, review loop timing, and monitor wallet balance, reputation, and repayment obligations.

## Reference(s):

- [Clawdit-borrower ClawHub skill page](https://clawhub.ai/natx223/skills/clawdit-borrower)
- [natx223 ClawHub publisher profile](https://clawhub.ai/user/natx223)
- [ERC-8004 registration reference](https://eips.ethereum.org/EIPS/eip-8004#registration-v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with API endpoint examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; agentCode must be handled as a transaction credential.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
