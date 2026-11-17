## Description:

This skill helps an agent plan home canning and food preservation batches, validate recipes against USDA/NCHFP-style safety guidance, calculate altitude-adjusted processing details, and produce checklists, inventory records, and reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

Home food preservers and self-reliance users use this skill to plan shelf-stable batches from surplus produce, foraged items, or bulk food purchases. It supports recipe safety checks, altitude-adjusted batch planning, inventory tracking, and rotation reminders while the human performs all physical food handling and canner operation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Safety-critical canning advice could be wrong if generalized pressure or processing-time formulas are used for a specific food, jar size, pack method, canner type, gauge type, or altitude.

Mitigation: Require the agent and user to verify every recipe and processing parameter against authoritative, current USDA/NCHFP tested guidance before canning.

Risk: The skill may write recipe, checklist, and inventory files without the user clearly confirming the destination and retained food-inventory details.

Mitigation: Confirm the target folder and the inventory fields before file creation, and keep batch records in a user-approved local location.

Risk: Reminder channels can expose food inventory or household planning details if email or external notifications are enabled without review.

Mitigation: Enable reminder delivery only after the user explicitly chooses the channel and reviews the reminder content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/canning-food-preservation)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, JSON inventory records, reminder text, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local batch files such as recipe, checklist, and inventory records when filesystem access is available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
