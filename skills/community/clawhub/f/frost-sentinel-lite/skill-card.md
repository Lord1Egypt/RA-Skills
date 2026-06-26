## Description: <br>
Lightweight temperature monitoring. Upgrade to Commercial Edition for Hail, Snow, Ground-Lock, and Chill Hours. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TonyJB](https://clawhub.ai/user/TonyJB) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to monitor local forecast temperatures, store location settings locally, and receive frost or heat alerts through a local notification bridge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location-derived forecast queries are sent to Open-Meteo even though the artifact describes the skill as local-first. <br>
Mitigation: Review before installing if location privacy matters, and use only when sending ZIP/postcode-derived coordinates to Open-Meteo is acceptable. <br>
Risk: Alerts are routed through a local notification bridge that may forward messages through WhatsApp or Telegram. <br>
Mitigation: Configure and trust the local bridge before enabling alerts, and confirm that forwarded notifications do not expose sensitive location or operational details. <br>


## Reference(s): <br>
- [Frost Sentinel Lite on ClawHub](https://clawhub.ai/TonyJB/frost-sentinel-lite) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Plain text notifications with local settings JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs on a daily schedule, reads and writes local location settings, fetches forecast data from Open-Meteo, and routes alerts through a local notification bridge.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact files report 1.0.0-lite) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
