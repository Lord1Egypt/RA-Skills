## Description:

Lightweight temperature monitoring that checks local forecasts through Open-Meteo and sends frost or heat alerts through a local notification bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonyjb](https://clawhub.ai/user/tonyjb)

### License/Terms of Use:


## Use Case:

External OpenClaw users use this skill for basic residential or hobbyist monitoring of overnight frost and daytime heat risk at a configured location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a ZIP/postcode locally, converts it to coordinates, and sends those coordinates to Open-Meteo while the artifact documentation also claims data is never sent to a third-party server.

Mitigation: Review before installation; require clear location-data consent, corrected privacy wording, and deletion instructions for stored location settings before deployment.

Risk: Automated frost alerts may include promotional upgrade text, which can distract from operational safety messaging.

Mitigation: Keep safety alerts focused on the weather risk and route commercial upgrade messaging outside automated alert notifications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tonyjb/skills/frost-sentinel-lite)
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [text, configuration]

**Output Format:** [Plain-text notification messages and local JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends frost or heat alerts through a local notification bridge and stores the configured location in settings.json.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
