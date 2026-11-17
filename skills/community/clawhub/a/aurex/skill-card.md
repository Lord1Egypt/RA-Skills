## Description:

Issue virtual crypto-funded cards and manage payments with the Aurex API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aurexcards](https://clawhub.ai/user/aurexcards)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to integrate Aurex card workflows, including user creation, wallet funding, virtual card issuance, card top-ups, transaction retrieval, and partner commission operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Aurex API keys and returned card details can expose financial secrets if logged, hardcoded, or stored in plaintext.

Mitigation: Store AUREX_API_KEY in environment variables, avoid logging or plaintext storage of card number, CVV, expiry, and OTP values, and request full card details only when necessary.

Risk: The skill describes financial operations such as issuing cards, topping up balances, changing partner markup, and retrieving full card details.

Mitigation: Require explicit user confirmation before performing card issuance, balance top-ups, markup changes, or full card detail retrieval.

Risk: Installing the latest SDK package can introduce unreviewed dependency changes.

Mitigation: Use a pinned, reviewed SDK version or an audited lockfile for @aurexcash/agent.

## Reference(s):

- [Aurex Skill Page](https://clawhub.ai/aurexcards/skills/aurex)
- [Aurex Website](https://aurex.cash)
- [Aurex Docs](https://docs.aurex.cash)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API request examples]

**Output Format:** [Markdown with bash, HTTP, and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes credential-handling guidance for AUREX_API_KEY and sensitive card details.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
