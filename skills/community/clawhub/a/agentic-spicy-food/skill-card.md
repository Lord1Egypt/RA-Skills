## Description:

Brand-specific commerce skill that helps agents browse, recommend, cart, and order Lafeitu Sichuan spicy foods through the official https://lafeitu.cn API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nowloady](https://clawhub.ai/user/nowloady)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents use this skill to search Lafeitu products, compare variants, pricing, and promotions, manage cart and account workflows, and create orders for user payment handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Lafeitu account credentials, profile data, carts, and order creation.

Mitigation: Install only if this level of shopping-account access is acceptable, confirm cart and shipping details before protected actions, and leave payment completion to the user.

Risk: Entering real passwords as command-line arguments can expose them through shell history, process lists, or logs.

Mitigation: Prefer the website flow or a safer secret-input mechanism for credentials, and use logout or delete local credentials when finished.

Risk: The server-provided security verdict is suspicious because account and order workflows have weaknesses users should review.

Mitigation: Review and scan the skill before deployment, and avoid using it with sensitive accounts until the security concerns are accepted or resolved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nowloady/skills/agentic-spicy-food)
- [Skill Homepage](https://github.com/NowLoadY/agentic-spicy-food)
- [Official Lafeitu Website](https://lafeitu.cn)
- [Official Lafeitu API](https://lafeitu.cn/api/v1)
- [Lafeitu AI Agent Guide](https://lafeitu.cn/ai-agent-guide)
- [Reference Commerce Engine](https://github.com/NowLoadY/agent-commerce-engine)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands plus JSON or localized text from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product, cart, account, profile, promotion, and order details; final payment is handed off to the user.]

## Skill Version(s):

1.9.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
