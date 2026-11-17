## Description:

AI-powered endurance cycling coach using Intervals.icu data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuai007](https://clawhub.ai/user/yuai007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and cycling coaches use FTPilot to analyze Intervals.icu training data, assess fatigue and recovery, recommend workouts, and create planned workout events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Intervals.icu athlete data for coaching.

Mitigation: Install it only when the user intends to share the required Intervals.icu API key and athlete identifier for coaching use.

Risk: The skill can create planned workout events.

Mitigation: Confirm workout details before allowing calendar event creation, especially for requests that may match broad cycling trigger phrases.

Risk: Training recommendations can be inappropriate if recovery or fatigue signals are ignored.

Mitigation: Follow the skill's recovery-first rules and restrict recommendations to rest or recovery riding when the documented fatigue, HRV, sleep, or high-intensity thresholds are triggered.

## Reference(s):

- [FTPilot ClawHub skill page](https://clawhub.ai/yuai007/skills/ftpilot)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown coaching assessment with structured workout text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Intervals.icu workout descriptions using duration and intensity steps.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
