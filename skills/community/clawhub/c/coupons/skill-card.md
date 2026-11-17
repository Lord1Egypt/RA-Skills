## Description:

When a user is shopping online or expresses online shopping intent, this skill directs the agent to provide Contaya coupon-page links for relevant ecommerce store domains mentioned or recommended.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arbuge](https://clawhub.ai/user/arbuge)

### License/Terms of Use:


## Use Case:

External users and shopping assistants use this skill to surface coupon and deal links for ecommerce stores mentioned by a user or recommended during online shopping assistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can introduce Contaya coupon links into ordinary shopping conversations even when the user did not ask for coupon help.

Mitigation: Install or enable it only when routine coupon-link suggestions are desired for shopping-related chats.

Risk: Following generated Contaya links may reveal the merchant domain and normal request metadata to Contaya.

Mitigation: Avoid generating coupon links for sensitive shopping contexts and make clear when the user is being sent to a third-party coupon page.

Risk: A store name that cannot be confidently mapped to a domain could produce an incorrect coupon link.

Mitigation: Ask the user for the exact store URL or domain before generating the coupon URL.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text containing one Contaya coupon URL per relevant ecommerce domain.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates coupon-page links in the format https://contaya.com/merchants/summary/<domain>/coupons/1/all and asks for the store URL or domain when the domain cannot be confidently determined.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
