## Description:

Generates weekly workout plans tailored to fitness goals, experience, equipment, and available time, including warm-ups, exercises, rest, and nutrition guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[petehuax](https://clawhub.ai/user/petehuax)

### License/Terms of Use:

MIT-0

## Use Case:

People planning home or gym workouts use this skill to create a weekly schedule tailored to their goals, equipment, training level, and available days, with exercise and recovery guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The payment intent label does not match the fitness service.

Mitigation: Check the payment purpose and amount before approving; do not pay if the description remains inconsistent.

Risk: The payment helper's install command uses an unpinned latest version.

Mitigation: Review the helper and install a pinned, trusted version instead.

Risk: Fitness requests are sent to an external paid service.

Mitigation: Share only details you are comfortable sending to that service, and confirm the fee before paying.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/petehuax/skills/fitness-plan-builder)
- [Fitness plan service endpoint](https://skillpay-aipay.app.workbuddy.host/skills/fitness-plan-builder)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown workout plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weekly schedule, warm-up and exercise sets, rest intervals, form cues, and nutrition and recovery principles.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
