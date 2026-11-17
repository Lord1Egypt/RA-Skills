## Description:

Geo Push Policy helps agents manage event notification decisions with cooldown windows, watch-pool handling, push-count limits, event state tracking, and rate-limit protection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liweijie0709-cmyk](https://clawhub.ai/user/liweijie0709-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to add a Chinese-language notification policy layer that decides when scored events should be pushed, watched, retried, or suppressed. It is suited for agents that need local JSON state tracking and caller-provided delivery functions for alert workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cooldown and push-count rules may suppress important alerts or allow duplicate notifications if thresholds do not match the deployment workflow.

Mitigation: Review and test the cooldown, watch-pool, threshold, and max-push settings with representative events before relying on the skill for important alerts.

Risk: The helper persists event state and failed messages in a local JSON file, including dead-letter queue content that can be resent through a caller-provided send function.

Mitigation: Use a limited local state-file path, control file permissions, and review retained dead-letter content before enabling resend behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liweijie0709-cmyk/skills/geo-push-policy)
- [SKILL.md](artifact/SKILL.md)
- [geo_push_policy.py](artifact/geo_push_policy.py)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration, Shell commands]

**Output Format:** [Markdown guidance with Python API examples and JSON state structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces notification policy decisions, reason strings, local state updates, and retry/dead-letter queue handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
