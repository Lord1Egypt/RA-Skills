## Description:

Detects phone use from Ezviz camera snapshots and, when detected, generates and sends a voice alert for playback on the configured device.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezviz-open](https://clawhub.ai/user/ezviz-open)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor authorized classroom, exam-room, meeting-room, or similar camera feeds for phone-use behavior and trigger an automatic voice warning through Ezviz devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes surveillance images and can issue device playback alerts.

Mitigation: Use only with explicit authorization for the monitored area and confirm local privacy, notice, and retention requirements before deployment.

Risk: The skill requires Ezviz app credentials and device identifiers.

Mitigation: Create restricted Ezviz credentials limited to the required APIs and devices, avoid main account credentials, restrict access where supported, and rotate credentials regularly.

Risk: The security evidence reports realistic credential examples and a suspicious verdict.

Mitigation: Review before installing and rotate any exposed-looking sample credentials if they were ever real.

Risk: The script includes a duplicate alert path and fallback sample-audio download behavior.

Mitigation: Remove or patch the duplicate alert block and undisclosed fallback download before production use.

## Reference(s):

- [Ezviz API docs](references/ezviz-api-docs.md)
- [ClawHub skill page](https://clawhub.ai/ezviz-open/skills/ezviz-open-capture)
- [Ezviz access token API](https://open.ys7.com/help/81)
- [Ezviz device capture API](https://open.ys7.com/help/687)
- [Ezviz phone detection API](https://open.ys7.com/help/3956)
- [Ezviz voice upload API](https://open.ys7.com/help/1241)
- [Ezviz voice send API](https://open.ys7.com/help/1253)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and console output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Ezviz app credentials, device serial numbers, network access to Ezviz services, and TTS dependencies.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
