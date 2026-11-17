## Description:

Provides AMap Open Platform geocoding, reverse geocoding, POI search, route planning, and distance measurement through a Python command-line helper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronjager92](https://clawhub.ai/user/aaronjager92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up addresses, coordinates, nearby places, route options, and distances using AMap geospatial services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location queries, addresses, coordinates, POI keywords, and route endpoints are sent to AMap.

Mitigation: Use the skill only when sharing that location data with AMap is acceptable for the user and deployment context.

Risk: The skill requires an AMap API key and may use a secret key for signed requests.

Mitigation: Prefer environment variables or a secret manager, avoid committing config.txt, and rotate credentials if exposure is suspected.

Risk: The Python helper depends on the requests package.

Mitigation: Install dependencies in a virtual environment and pin versions for managed deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaronjager92/skills/amap-geoservice)
- [Artifact reference README](artifact/references/README.md)
- [AMap API key console](https://console.amap.com/dev/key/app)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AMap API key and may require an AMap secret key for signed route and distance requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
