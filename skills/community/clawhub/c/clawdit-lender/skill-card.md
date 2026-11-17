## Description:

Clawdit-lender guides an agent through autonomous P2P crypto lending with a WDK smart wallet, using ERC-8004 reputation and revenue signals to evaluate loan requests, disburse USDT, track loans, and collect repayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[natx223](https://clawhub.ai/user/natx223)

### License/Terms of Use:

MIT-0

## Use Case:

External operators and agent developers use this skill to configure an autonomous lending agent that evaluates borrower agents, sends loans from a smart wallet, monitors loan status, and initiates repayment collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can initiate recurring wallet transactions for loan disbursement and repayment collection.

Mitigation: Require manual approval before each disbursement or collection, set explicit caps and expiry for any scheduled workflow, and keep audit logs.

Risk: The agentCode grants transaction authority and is displayed only once during registration.

Mitigation: Store the agentCode only in an approved secret store or operator-controlled vault, and do not place it in ordinary chat or long-term agent memory.

Risk: Autonomous lending can lose funds through bad borrower selection, default, or unsafe loan sizing.

Mitigation: Use only funds prepared for loss, start with conservative risk settings, cap maximum loan size, and monitor balances and loan history before increasing automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/natx223/skills/clawdit-lender)
- [ClawHub publisher profile](https://clawhub.ai/user/natx223)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, configuration]

**Output Format:** [Markdown with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for wallet setup, lending strategy, loan disbursement, repayment collection, and loan-history review.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
