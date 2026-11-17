## Description:

A skill to interact with Gaode Map (AMap) for location search and route planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beelkic](https://clawhub.ai/user/beelkic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to let an agent search Gaode/AMap points of interest, geocode addresses, and plan routes for driving, walking, bicycling, or transit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location queries and route endpoints may send user-provided places, addresses, or coordinates to Gaode/AMap.

Mitigation: Use this skill only with location queries the user is comfortable sending to Gaode/AMap.

Risk: The AMAP_API_KEY is required for API access and could be exposed if handled carelessly.

Mitigation: Store AMAP_API_KEY in the agent environment or secret manager and avoid placing it in prompts, logs, or shared files.

Risk: The requests dependency is unpinned, which can reduce reproducibility across installs.

Mitigation: Pin or lock the requests dependency before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beelkic/skills/gaodemapskill-bak)
- [AMap Console](https://console.amap.com/)
- [AMap REST API endpoint](https://restapi.amap.com/v3)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AMAP_API_KEY and the Python requests dependency to call Gaode/AMap APIs.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
