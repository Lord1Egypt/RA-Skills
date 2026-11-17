## Description:

Recommends a surprise sealed book and helps users place an order for themselves or as a gift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shujip](https://clawhub.ai/user/shujip)

### License/Terms of Use:

MIT-0

## Use Case:

People looking for a book or gift can receive a masked recommendation and order a sealed book through chat. The skill collects delivery details, verifies an account by phone or email code, and provides a card-payment link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delivery and contact details are shared with the AnswerBox service to place an order.

Mitigation: Use only if comfortable sharing shipping and contact information with the service; review details before ordering.

Risk: Account verification codes are entered in chat, and reusable account tokens are stored locally.

Mitigation: Review the in-chat verification flow and protect access to the local session file.

Risk: The skill creates orders and provides card-payment links, not just recommendations.

Mitigation: Confirm the order and price with the user before paying, and use only the trusted checkout page.

## Reference(s):

- [AnswerBox on ClawHub](https://clawhub.ai/shujip/skills/answerbox)
- [AnswerBox website](https://answerbox.playable.today)
- [AnswerBox agent API](artifact/api.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Payment links]

**Output Format:** [Chat text with a masked book recommendation and a checkout link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes book hints, pricing and shipping details, and order status; the book title remains sealed until delivery.]

## Skill Version(s):

1.0.2 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
