## Description:

Send goals to Deacon from a web app so the founder's dashboard counts the moments that matter, such as sign ups, paywall hits and upgrades. Use when asked to add Deacon goals or tracking events to a site that already carries the Deacon widget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewcathcart](https://clawhub.ai/user/andrewcathcart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add and verify goal tracking in web apps that already include the Deacon widget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sign-up examples may record events for registrations that failed, making analytics misleading.

Mitigation: Send the goal only after confirmed account creation and verify failed registrations send no event.

Risk: Goal event properties or live checkout tests could expose personal data or create unintended purchases.

Mitigation: Keep personal data out of event properties and verify with development accounts and test checkout.

## Reference(s):

- [Deacon recent goals verification endpoint](https://heydeacon.com/api/goals/recent?k=SITE_KEY)
- [deacon-goals on ClawHub](https://clawhub.ai/andrewcathcart/skills/deacon-goals)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Implementation guidance]

**Output Format:** [Markdown with code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Framework-specific examples and verification steps]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
