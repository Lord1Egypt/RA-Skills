## Description:

Set up a Bird Buddy smart bird feeder integration with Home Assistant, including the ha-birdbuddy custom component, notification automations, a live camera entity, a dashboard, and Telegram routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mykclawd](https://clawhub.ai/user/mykclawd)

### License/Terms of Use:

MIT-0

## Use Case:

External Home Assistant users and developers use this skill to integrate a Bird Buddy feeder with Home Assistant, add a camera entity, import automations, route feeder alerts to Telegram, and create a dedicated dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included camera component was flagged as having security issues around media URLs, session IDs, URL allowlisting, and response-size limits.

Mitigation: Review or fix camera.py before installation; add URL allowlisting and response-size limits, and avoid exposing media URLs or session IDs in entity attributes and logs.

Risk: Home Assistant, Bird Buddy, and Telegram credentials may be exposed if pasted into shell history or plain configuration files.

Mitigation: Store tokens only in Home Assistant secrets or another protected secret store, and rotate any token pasted into shell or configuration history.

Risk: Telegram notifications can reveal household activity and feeder imagery links if sent to the wrong chat or topic.

Mitigation: Verify the Telegram chat ID and message thread before enabling automations, and limit recipients to trusted users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mykclawd/skills/birdbuddy-homeassistant)
- [ha-birdbuddy custom component](https://github.com/jhansche/ha-birdbuddy)
- [camera.py](artifact/references/camera.py)
- [automations.yaml](artifact/references/automations.yaml)
- [rest_commands.yaml](artifact/references/rest_commands.yaml)
- [dashboard_config.json](artifact/assets/dashboard_config.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown instructions with Python, YAML, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Home Assistant setup guidance, a camera entity file, automation templates, Telegram rest_command configuration, and dashboard configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
