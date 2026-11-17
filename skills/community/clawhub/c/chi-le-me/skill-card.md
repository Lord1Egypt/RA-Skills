## Description:

吃了么外卖 Agent：自动搜索附近外卖，根据口味/性价比/好评推荐，支持下单

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiamidavid00](https://clawhub.ai/user/xiamidavid00)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to compare nearby food-delivery options, receive meal recommendations based on taste, budget, ratings, and delivery details, and get guided through cart and checkout steps without the agent completing payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store food preferences and order history.

Mitigation: Use it only when the user consents to preference and order-history memory, and keep stored data reviewable and removable.

Risk: The skill declares broad local command execution without a clearly scoped script need.

Mitigation: Avoid granting local command execution unless commands are limited to specific, necessary scripts and require explicit user approval.

Risk: The skill guides delivery-site checkout flows that can involve address and payment decisions.

Mitigation: Keep final address confirmation and payment actions under direct user control; the skill should only assist with selection and navigation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiamidavid00/skills/chi-le-me)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown recommendations, comparison tables, and step-by-step order guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save user food preferences and order history when memory tools are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
