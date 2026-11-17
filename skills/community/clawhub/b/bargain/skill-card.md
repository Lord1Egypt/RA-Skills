## Description:

Ruofan Bargain Arena helps an agent guide a user through a Ruofan coupon-code bargaining chat with Ruofan's shop assistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruffood](https://clawhub.ai/user/ruffood)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and their agents use this skill to join Ruofan's bargain activity, relay user-approved bargain messages, monitor remaining rounds, and present any resulting coupon code to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bargain conversation may be publicly displayed on Ruofan's activity page.

Mitigation: Use a non-sensitive nickname and avoid sending private information in bargain messages.

Risk: Session tokens and coupon codes can provide access to a user's bargain session or discount.

Mitigation: Treat session tokens and coupon codes as private session data and do not expose them beyond the intended user flow.

Risk: The skill sends user-provided bargain messages to Ruofan's public API.

Mitigation: Relay only user-approved content unless the user explicitly asks the agent to draft bargain wording.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruffood/skills/bargain)
- [Publisher profile](https://clawhub.ai/user/ruffood)
- [Ruofan bargain join API](https://www.ruffood.com/api/bargain/join)
- [Ruofan bargain message API](https://www.ruffood.com/api/bargain/message)
- [Ruofan bargain session API](https://www.ruffood.com/api/bargain/session)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with inline shell command examples and user-facing bargain status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include coupon amounts, remaining-round status, final deal state, and coupon codes returned by Ruofan's API.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
