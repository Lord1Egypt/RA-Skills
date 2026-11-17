## Description:

A skill to interact with Gaode Map (AMap) for location search and route planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beelkic](https://clawhub.ai/user/beelkic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to search points of interest, geocode addresses, and plan routes through Gaode Map (AMap). It is intended for location lookup and route-planning workflows that can send queries and route endpoints to AMap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map searches, addresses, route endpoints, and geocoding inputs are sent to Gaode/AMap.

Mitigation: Use the skill only when that data sharing is acceptable for the deployment context.

Risk: The AMap API key may be exposed if passed on the command line or stored insecurely.

Mitigation: Prefer AMAP_API_KEY from a protected environment or secret manager and avoid passing the key with --key.

Risk: The Python dependency list does not pin requests.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [AMap Console](https://console.amap.com/)
- [AMap REST API endpoint](https://restapi.amap.com/v3)
- [ClawHub skill page](https://clawhub.ai/beelkic/skills/gaodemapskill-conflict)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON responses from a Python command-line tool, with Markdown command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python, requests, and AMAP_API_KEY; supports search and route actions with driving, walking, bicycling, and transit modes.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
