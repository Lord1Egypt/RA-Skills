## Description:

Compose a personalized morning briefing using the latest fulcra-context skill for sleep, biometrics, calendar, activity, and weather context. Adapts tone and detail to how the human actually slept.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arc-claw-bot](https://clawhub.ai/user/arc-claw-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to collect Fulcra sleep, biometric, calendar, activity, and weather context and compose a morning briefing calibrated to sleep quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles sensitive Fulcra health, activity, calendar, and location-derived context.

Mitigation: Install only when this access is acceptable, run the workflow as an unprivileged user, and avoid sharing briefing details outside a trusted private channel.

Risk: Shell-based collection and the FULCRA_CLI_COMMAND override can increase supply-chain or command execution risk.

Mitigation: Pin the Fulcra CLI version where practical and avoid FULCRA_CLI_COMMAND unless the command path and arguments are fully controlled.

Risk: Briefing output may persist sensitive data if written to shared temporary paths.

Mitigation: Use a private 0700 directory instead of /tmp/briefing.json for stored briefing data.

Risk: Weather lookup sends the configured location to wttr.in.

Mitigation: Use only a location granularity the user is comfortable disclosing to that external weather service.

## Reference(s):

- [Fulcra Platform](https://fulcradynamics.com)
- [Fulcra Developer Docs](https://docs.fulcradynamics.com)
- [Fulcra Python Client](https://github.com/fulcradynamics/fulcra-api-python)
- [Fulcra Context MCP Server](https://github.com/fulcradynamics/fulcra-context-mcp)
- [Context iOS App](https://apps.apple.com/app/id1633037434)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefing guidance with shell commands and JSON collector output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Collector output includes sleep, heart rate, HRV, steps, calendar, weather, and compact data freshness fields.]

## Skill Version(s):

1.1.10 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
