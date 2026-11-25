## Description:

Send goals to Deacon from a web app so the founder's dashboard counts the moments that matter, such as sign ups, paywall hits and upgrades. Use when asked to add Deacon goals or tracking events to a site that already carries the Deacon widget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewcathcart](https://clawhub.ai/user/andrewcathcart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Deacon goal tracking to a web app that already loads the Deacon widget. It helps them instrument meaningful product events, such as sign ups, paywall views, and upgrades, using the founder's goal names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A sign-up tracking example may count a rejected registration as a successful sign-up.

Mitigation: Send the sign-up goal only after account creation succeeds, such as from a confirmed success page or handler.

Risk: The security scan is incomplete because some local references could not be resolved.

Mitigation: Review unresolved local references during implementation before relying on the scan as a complete assessment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andrewcathcart/skills/deacon-goals)
- [Deacon recent goals verification endpoint](https://heydeacon.com/api/goals/recent?k=SITE_KEY)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Framework-specific code snippets and implementation guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Goal names should match the founder's names exactly; event details must not include personal data.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
