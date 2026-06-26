## Description: <br>
Multi-source flight aggregation for tickets, nonstop and connecting routes, round trips, cabin classes, flight prices, and flight status without requiring user login or an API key. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[qizha](https://clawhub.ai/user/qizha) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
External users and developers use this skill to query flight status, schedules, prices, route options, cabin classes, and nonstop or connecting flights through an OpenClaw agent or Python CLI. It is suited for flight information lookup and comparison, with results requiring user verification before travel decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight search details are sent to third-party flight data services. <br>
Mitigation: Use the skill only when sharing those query details with disclosed flight data services is acceptable. <br>
Risk: The built-in Fliggy signing credential is a shared public integration credential, not a private user secret. <br>
Mitigation: Do not treat the built-in credential as sensitive personal infrastructure, and avoid adding personal API keys to config.yaml unless the skill and local environment are trusted. <br>
Risk: Flight prices, availability, and status can vary across public sources and regions. <br>
Mitigation: Treat returned results as reference information and verify important itinerary or price details before booking or operational use. <br>


## Reference(s): <br>
- [Flyclaw Bak on ClawHub](https://clawhub.ai/qizha/flyclaw-bak) <br>
- [FlyClaw GitHub Project](https://github.com/AI4MSE/FlyClaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration] <br>
**Output Format:** [JSON by default, with optional human-readable table output and stderr diagnostics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prices default to CNY; users can request USD or original currency when supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact source version 0.4.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
