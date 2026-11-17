## Description:

Order food delivery via browser automation from calendar events, supporting Direct mode for a specific service and restaurant and Discovery mode for criteria-based search across DoorDash, Uber Eats, and Grubhub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thisisjeron](https://clawhub.ai/user/thisisjeron)

### License/Terms of Use:


## Use Case:

External users use this skill to turn self-created calendar events into browser-assisted food delivery orders. It supports direct restaurant ordering and comparison-based discovery while requiring explicit confirmation before a live purchase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real food orders through a logged-in browser profile with saved payment and delivery information.

Mitigation: Use a dedicated browser profile with limited saved data and require a fresh explicit confirmation before any final order click.

Risk: Calendar events from shared calendars or external invites may not represent the user's intent.

Mitigation: Only trigger the skill from calendar events the user created and controls, and verify event origin before proceeding.

Risk: Calendar descriptions may contain sensitive delivery details such as gate codes.

Mitigation: Avoid putting gate codes or other sensitive access details in calendar descriptions; provide them only at confirmation time when needed.

Risk: Food allergy or dietary constraints may be unsafe if menu information is ambiguous.

Mitigation: Skip items when allergen safety cannot be confirmed and choose clearly safe alternatives before presenting the checkout summary.

## Reference(s):

- [Food Calendar Order on ClawHub](https://clawhub.ai/thisisjeron/skills/food-cal-order)
- [DoorDash Browser Flow](references/doordash.md)
- [Uber Eats Browser Flow](references/ubereats.md)
- [Grubhub Browser Flow](references/grubhub.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown status reports with browser-action instructions and confirmation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce order summaries, restaurant comparisons, failure reports, and final order confirmation details.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
