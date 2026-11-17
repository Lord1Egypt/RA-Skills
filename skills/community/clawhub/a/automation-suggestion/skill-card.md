## Description:

Suggest automations only when they make sense, based on objective triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szpili](https://clawhub.ai/user/szpili)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent propose automation after repeated, time-consuming, or frustrating manual tasks while limiting suggestion frequency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses recent task history and simple sentiment cues to decide when to suggest automation.

Mitigation: Disclose this memory and sentiment use to installers, and keep the artifact's requirement to ask before configuring any automation.

Risk: Frustration detection may be incomplete outside the example Polish-language phrasing.

Mitigation: Expand and review locale-specific frustration phrases before relying on sentiment-triggered suggestions.

Risk: Automation suggestions can become intrusive if thresholds are too low.

Mitigation: Retain the daily suggestion limit and 30-day suppression after a user declines a similar suggestion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/szpili/skills/automation-suggestion)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with optional configuration values and suggested user-facing prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Suggestions are gated by trigger thresholds, daily limits, and cooldown rules.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
