## Description:

Play casino games such as dice, coinflip, and roulette on Agent Casino with real cryptocurrency through a provably fair gambling API for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rollhub-dev](https://clawhub.ai/user/rollhub-dev)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to register with Agent Casino, manage cryptocurrency deposits and withdrawals, place dice, coinflip, and roulette bets, verify bet fairness, and check affiliate earnings.

### Deployment Geography for Use:

Global, subject to local gambling, cryptocurrency, and eligibility restrictions.

## Known Risks and Mitigations:

Risk: Real-money cryptocurrency gambling can result in financial loss and may be illegal or restricted depending on location and eligibility.

Mitigation: Confirm the user is legally eligible and obtain explicit approval before deposits, bets, or withdrawals.

Risk: Blockchain transfers may be irreversible.

Mitigation: Verify wallet addresses, currency, chain, and amount before initiating any deposit or withdrawal.

Risk: API keys and gambling credentials may be exposed through shell commands or logs.

Mitigation: Use environment variables or a secure secret store, avoid pasting live keys into shared logs, and redact credentials from outputs.

Risk: The registration example includes an embedded referral code.

Mitigation: Remove or replace referral parameters unless the user explicitly approves their use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rollhub-dev/skills/gambling)
- [Agent Casino](https://agent.rollhub.com)
- [Agent Casino API Base](https://agent.rollhub.com/api/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes real-money cryptocurrency transaction and betting workflows that require explicit user approval before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
