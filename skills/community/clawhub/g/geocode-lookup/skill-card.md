## Description:

Forward/reverse geocoding and great-circle distance calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutthemustard](https://clawhub.ai/user/cutthemustard)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to turn addresses into coordinates, turn coordinates into addresses, and calculate great-circle distances between locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Address or coordinate queries are sent to an external geocoding service.

Mitigation: Avoid sending private home addresses or sensitive locations unless the user has explicitly consented.

Risk: The service's no-logging statement is a publisher claim rather than a verified property of the artifact.

Mitigation: Treat the service as an external data processor and avoid including sensitive location details unless necessary.

## Reference(s):

- [Geocode Lookup on ClawHub](https://clawhub.ai/cutthemustard/skills/geocode-lookup)
- [CutTheMustard publisher profile](https://clawhub.ai/user/cutthemustard)
- [Geocode service homepage](https://geocode.agentutil.net)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API calls, JSON]

**Output Format:** [Markdown instructions with curl examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls an external geocoding service; the publisher describes a free tier of 10 queries per day and optional paid usage via x402.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
