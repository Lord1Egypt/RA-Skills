## Description:

Provides weather queries through dxmpay.com and supports account initialization, order, quota, purchase detail, and usage-log lookups for the weather service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duxiaoman](https://clawhub.ai/user/duxiaoman)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent for city/date weather information and inspect their weather-service orders, quota, purchase details, and API usage records. The skill is intended for workflows that are comfortable using dxmpay.com for service access and payment-related flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service provider receives weather queries, account metadata, purchase details, and QR-related content handled by the package.

Mitigation: Install only when dxmpay.com is trusted for those data categories, and keep SP_WEATHER_BASE unset unless the replacement endpoint is fully controlled and trusted.

Risk: The private-key password can be exposed if placed directly in command text, logs, or shell history.

Mitigation: Provide the password through an interactive prompt when possible and avoid sharing commands that inline SP_WEATHER_PASSWORD.

Risk: Generated QR files are persistent local artifacts.

Mitigation: Review the output directory after payment flows and delete QR files that should not remain on disk.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duxiaoman/skills/dxm-sp-weather)
- [Publisher profile](https://clawhub.ai/user/duxiaoman)
- [dxmpay weather service endpoint](https://www.dxmpay.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [JSON command responses summarized as user-facing text or Markdown, with shell command invocations when the agent runs the bundled CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create an encrypted local sp-weather-config.json and persistent QR PNG artifacts that users may need to clean up.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
