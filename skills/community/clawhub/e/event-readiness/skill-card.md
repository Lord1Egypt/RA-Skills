## Description:

Check whether a seller is actually ready for a marketplace event, promo spike, or campaign window before traffic is pushed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Marketplace sellers and operations teams use this skill to decide whether a promo, brand event, seasonal push, or campaign spike is ready to launch. It reviews inventory, pricing, creator support, content support, customer support, and fulfillment so the user can identify critical gaps before traffic is pushed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Event planning inputs may include sensitive inventory, pricing, creator support, content, customer support, or fulfillment data.

Mitigation: Share only the event details needed for the readiness review and avoid unnecessary confidential data.

Risk: Incomplete event inputs can make a readiness verdict overconfident.

Mitigation: Use checklist mode, call out unknowns as risk, and avoid marking the event ready unless the critical path is covered.

## Reference(s):

- [Event Readiness output template](artifact/references/output-template.md)
- [ClawHub skill page](https://clawhub.ai/leooooooow/skills/event-readiness)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown readiness verdict with prioritized gap and action lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes readiness verdict, critical gaps, must-fix sequence, secondary improvements, and final go/no-go note.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
