## Description:

Analyzes automotive service, tire, and lubricant brand store networks, regional coverage, and location profiles from Baidu Map address text and DDT published store snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business analysts use this skill to evaluate automotive aftermarket brand coverage, regional distribution, store surroundings, and nearby candidate locations using DDT's published store snapshot data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a DDT API key and calls the publisher's external API.

Mitigation: Store the key only in a controlled environment, never paste it into chat or logs, and review whether sending location-analysis queries to the external API is acceptable.

Risk: Store and location results are based on a limited published snapshot and may not represent a complete market record.

Mitigation: Present coverage, data-version context, truncation status, and unavailable fields explicitly instead of inferring missing metrics.

Risk: The skill references Baidu Map address text but is not an official Baidu Map product or data source.

Mitigation: Describe Baidu Map text only as user-provided location input and avoid implying partnership, authorization, or Baidu-sourced store conclusions.

## Reference(s):

- [DDT ClawHub API homepage](https://gotoshop-ai.com/ddtclaw/)
- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-baidu-map-auto-network)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown analysis with key metrics, coverage notes, data-version context, and limited requested store details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid API keys, storage IDs, supplier fields, internal fields, and unsupported metrics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
