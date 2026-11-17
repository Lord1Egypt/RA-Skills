## Description:

BroadlinkAC For Agent helps agents use a cross-platform Broadlink RM infrared AC control library with weather-aware automation, storm alerts, scheduling, logging, and IR learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oywq00008-cell](https://clawhub.ai/user/oywq00008-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and control Broadlink RM-connected air conditioners programmatically, including weather-aware decisions, IR code learning, schedule management, and persistent device configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports unpinned remote-code installation and stored API keys.

Mitigation: Prefer a pinned commit or signed release, inspect the cloned repository and requirements, use low-scope weather API keys, and protect or avoid persisting credentials.

Risk: The skill can configure persistent AC schedules, auto-adjust, and storm auto-shutdown that continue after the agent task ends.

Mitigation: Only enable or modify schedules, auto-adjust, or storm shutdown after explicit user confirmation, and disable schedule_enabled and auto_adjust when autonomous changes are not desired.

Risk: The security guidance calls out QWeather host verification and constrained execution.

Mitigation: Verify any QWeather host before use and run the skill in a constrained environment.

## Reference(s):

- [BroadlinkAC For Agent ClawHub page](https://clawhub.ai/oywq00008-cell/skills/broadlinkac)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe persistent local configuration, scheduler settings, API-key setup, and AC control actions.]

## Skill Version(s):

5.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
