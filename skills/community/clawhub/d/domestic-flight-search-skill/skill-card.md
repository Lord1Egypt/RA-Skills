## Description:

Query China domestic flights with schedules, airline details, airport resolution, and Juhe reference prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baizhexue](https://clawhub.ai/user/baizhexue)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up China domestic flight options for a specific date, resolve Chinese city or airport names to IATA-style codes, and summarize airline, schedule, airport, duration, and reference fare details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional local HTTP mode is under-protected and can expose API quota use if reachable by others.

Mitigation: Prefer CLI mode; when using HTTP mode, bind only to 127.0.0.1 and do not expose the port to a network.

Risk: The skill depends on a user-provided Juhe API key.

Mitigation: Use a dedicated low-quota Juhe key, keep it in JUHE_FLIGHT_API_KEY or JUHE_API_KEY, and revoke it if exposure is suspected.

Risk: Provider fares are reference prices and may not match final ticketing availability or cost.

Mitigation: Present ticket_price as a reference fare and direct users to verify booking conditions with the provider or booking channel.

## Reference(s):

- [Juhe Flight API Documentation](https://www.juhe.cn/docs/api/id/818)
- [Juhe Provider Notes](references/provider-juhe.md)
- [Domestic Flight Search ClawHub Release](https://clawhub.ai/baizhexue/skills/domestic-flight-search-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON flight-search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live searches require a user-provided Juhe API key; flight prices are reference fares rather than guaranteed bookable fares.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
