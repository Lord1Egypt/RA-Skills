## Description:

Get comprehensive context about a location including nearby places, area description, and optional weather.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to request location-aware context for trip planning, meeting locations, local recommendations, and weather-aware planning from Camino's context API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends coordinates, optional context text, and the Camino API key to Camino's API.

Mitigation: Use it only when that data sharing is acceptable, and avoid including sensitive personal details in the optional context field unless needed.

Risk: The bundled script requires a Camino API key and local curl and jq binaries.

Mitigation: Confirm CAMINO_API_KEY, curl, and jq are available before running the script, or use an alternate Camino-compatible client path.

Risk: No server-resolved GitHub import provenance is available for this release.

Mitigation: Prefer a pinned release or reviewed commit when installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/skills/camino-context)
- [Camino API key activation](https://app.getcamino.ai/skills/activate)
- [Camino Context API endpoint](https://api.getcamino.ai/context)
- [x402 payment protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [JSON responses and Markdown usage guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, a JSON input payload with location coordinates, and CAMINO_API_KEY for the bundled script path.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
