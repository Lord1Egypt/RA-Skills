## Description:

Provides 48 Zodiac personality analysis and dual compatibility readings from month-day inputs or zone IDs, with tool-grounded output and no API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niukesi](https://clawhub.ai/user/niukesi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect minimal month-day birthday inputs or 48-Zodiac IDs, retrieve single-person zodiac profiles or two-person compatibility readings, and present grounded relationship guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command templates may allow unsafe local command execution if a runner invokes templated arguments through a shell.

Mitigation: Use a runner that passes arguments safely without a shell, or require strict input validation and structured command arguments before installation.

Risk: Users may provide unnecessary personal data when asking for zodiac readings.

Mitigation: Collect only month and day values, and avoid requesting birth year, birth time, contact details, addresses, credentials, or unrelated personal information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niukesi/skills/48-zodiac-cyber-reader)
- [Artifact README](artifact/README.md)
- [OpenAPI specification](artifact/openapi.json)
- [System prompt](artifact/system_prompt.md)
- [Read-only Zodiac API endpoint](https://zodiac-48-api.712991518.workers.dev)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, guidance]

**Output Format:** [Markdown prose grounded in JSON API responses, with local shell command templates for tool invocation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses month-day strings or 48-Zodiac IDs as inputs; API responses may be translated into the user's language.]

## Skill Version(s):

1.0.14 (source: server evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
