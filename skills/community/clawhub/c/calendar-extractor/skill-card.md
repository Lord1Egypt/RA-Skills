## Description:

Finds calendar events in recent audio and typed transcripts and sends one reviewable event card per plan to HiJavis chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuel-wei](https://clawhub.ai/user/samuel-wei)

### License/Terms of Use:

MIT-0

## Use Case:

HiJavis users can find meetings and appointments mentioned in recent recordings or typed notes, either on demand or through automatic processing of completed units. Extracted events appear for review in the calendar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When enabled, the skill automatically analyzes completed recordings and typed inputs.

Mitigation: Use it within HiJavis and review each new event with Confirm or Discard; correcting a card in chat also confirms it.

Risk: The separate HiJavis app and server controls were not verified in the security review.

Mitigation: Validate those controls in the deployment; review the skill's resulting events before confirming them.

## Reference(s):

- [Calendar Extractor on ClawHub](https://clawhub.ai/samuel-wei/skills/calendar-extractor)
- [HiJavis on the App Store](https://apps.apple.com/us/app/hijavis/id6745134765)

## Skill Output:

**Output Type(s):** [Markdown, Calendar event data]

**Output Format:** [Markdown event cards and calendar entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One event per card; new entries remain pending until confirmed. On-demand runs also return a brief chat summary.]

## Skill Version(s):

0.7.4 (source: server release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
