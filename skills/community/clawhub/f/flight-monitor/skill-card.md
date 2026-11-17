## Description:

Flight Monitor searches flight prices, tracks one-way or round-trip fares, manages threshold alerts and recurring monitors, and can send mobile notifications through Bark, ServerChan, or PushDeer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackzhao3925](https://clawhub.ai/user/jackzhao3925)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and assistants use this skill to search flight options, record fare history, configure low-price alerts, and manage recurring flight price monitors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring flight monitors can run local automation that repeatedly queries route and travel-date information.

Mitigation: Review generated automation tasks before enabling them and remove or pause monitors that are no longer needed.

Risk: Notification and optional API keys are stored in local WorkBuddy flight-monitor configuration without strong protection.

Mitigation: Use dedicated, revocable keys, avoid shared machines, and check permissions on the local flight-monitor configuration directory.

Risk: Flight routes, dates, prices, and alert content may be sent to Ctrip, zbape, Bark, ServerChan, PushDeer, or other configured services.

Mitigation: Install only if sharing this travel and alert data with the configured providers is acceptable.

## Reference(s):

- [City IATA Codes Reference](references/city_codes.md)
- [zbape API documentation](https://api.zbape.com/doc/54)
- [ServerChan notification service](https://sct.ftqq.com/)
- [PushDeer notification service](https://www.pushdeer.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tables with inline shell commands, booking links, alert text, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON history/configuration files and TOML automation tasks under the user's WorkBuddy directories.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
