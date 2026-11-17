## Description:

CreditClaw lets AI agents pay with owner-controlled virtual cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[creditclaw](https://clawhub.ai/user/creditclaw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use CreditClaw to register an agent, list linked owner-controlled virtual cards, mint fresh card numbers for approved online purchases, and stop for human intervention on payment challenges or declines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables real-money virtual-card payments by an agent.

Mitigation: Use owner-controlled cards with low limits and require the agent to show the merchant, item, total, and shipping details before each purchase.

Risk: CREDITCLAW_API_KEY functions like a payment credential.

Mitigation: Store it securely, send it only to creditclaw.com, and install the skill only from a trusted, reviewed source.

Risk: Unpinned package installation can pull changing code over time.

Mitigation: Prefer pinned installation or ClawHub-managed installation for normal use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/creditclaw/skills/creditclaw)
- [CreditClaw Website](https://creditclaw.com)
- [CreditClaw Agent Skill](https://creditclaw.com/SKILL.md)
- [CreditClaw API Base](https://creditclaw.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and human-confirmed payment context before use.]

## Skill Version(s):

3.0.1 (source: server release metadata; artifact frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
