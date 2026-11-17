## Description:

agentcard.ai helps agents purchase and manage prepaid virtual Visa cards for secure payments at US online merchants through the agentcard CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[florrdv](https://clawhub.ai/user/florrdv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, power users, and agents use this skill to authenticate with AgentCard, create prepaid cards, retrieve card details when needed, check balances, and refund unused funds for online purchases such as API credits, SaaS subscriptions, domains, and cloud resources.

### Deployment Geography for Use:

Global use with US-based online merchants only.

## Known Risks and Mitigations:

Risk: The skill can help an agent initiate real prepaid card purchases and refunds.

Mitigation: Keep user confirmation enabled, use low card amounts, and set conservative purchase limits before using it for real payments.

Risk: The workflow may expose full virtual card details during checkout support.

Mitigation: Retrieve card details only when needed, avoid showing full card details in chat unless the user explicitly asks, and do not persist them locally.

Risk: The skill asks the user to install a mutable global CLI.

Mitigation: Prefer a pinned or isolated CLI install and confirm the installed CLI before using it for payment activity.

Risk: Cards are limited to US-based online merchants and may be declined elsewhere.

Mitigation: Confirm the merchant is US-based before creating or using a card.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/florrdv/skills/agentcardai)
- [AgentCard CLI and Package](https://agentcard.ai)
- [agentcard npm Package Code](https://www.npmjs.com/package/agentcard?activeTab=code)
- [npm Provenance Statements](https://docs.npmjs.com/generating-provenance-statements)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive payment workflow guidance; card details should be treated as transient secrets.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
