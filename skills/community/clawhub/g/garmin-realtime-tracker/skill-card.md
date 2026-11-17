## Description:

Facilitates real-time tracking and automated data delivery from Garmin devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kritsanan1](https://clawhub.ai/user/kritsanan1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration teams use this skill to choose Garmin data delivery approaches for live location, activity data, and sensor streams, including official SDK/API options and cautions around unofficial LiveTrack methods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated forwarding of live location or sensor data can expose sensitive personal information without adequate consent or scoping.

Mitigation: Require explicit consent from the tracked user, send only the minimum necessary fields, and define retention and access controls before forwarding data.

Risk: Unofficial LiveTrack approaches may depend on session-token scraping or unstable reverse-engineered behavior.

Mitigation: Prefer official Garmin SDKs and APIs for important integrations, and avoid unofficial session-token scraping for production or sensitive use cases.

Risk: External delivery endpoints can receive high-frequency activity or location updates.

Mitigation: Use trusted authenticated endpoints and review network, privacy, and access controls before deployment.

## Reference(s):

- [Garmin Connect IQ Positioning](https://developer.garmin.com/connect-iq/core-topics/positioning)
- [Garmin ActivityMonitor.Info API](https://developer.garmin.com/connect-iq/api-docs/Toybox/ActivityMonitor/Info.html)
- [Garmin Connect Developer Program Overview](https://developer.garmin.com/gc-developer-program/overview/)
- [Garmin Connect Activity API](https://developer.garmin.com/gc-developer-program/activity-api/)
- [Garmin Connect Health API](https://developer.garmin.com/gc-developer-program/health-api/)
- [Garmin Health SDK Overview](https://developer.garmin.com/health-sdk/overview/)
- [renarsvilnis/garmin-livetrack](https://github.com/renarsvilnis/garmin-livetrack)
- [ClawHub skill page](https://clawhub.ai/kritsanan1/skills/garmin-realtime-tracker)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guidance with API, SDK, webhook, and implementation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include example code or configuration suggestions for forwarding Garmin location, activity, or sensor data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
