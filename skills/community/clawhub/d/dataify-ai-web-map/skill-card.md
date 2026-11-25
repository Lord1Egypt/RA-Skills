## Description:

Discovers page URLs from a public website through the AI Web Map API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use it to discover URLs across a public website and collect site-wide entry points for follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses environment and network access to call a web API, and the scan does not specify how the host enforces permissions.

Mitigation: Check the host's permission controls before use and keep DATAIFY_API_TOKEN in the environment; do not paste or print the token.

## Reference(s):

- [AI Web API Map reference](references/map-api.md)
- [AI Web API Map endpoint](https://aiwebapi.dataify.com/map)
- [AI Web Map release on ClawHub](https://clawhub.ai/dataify-server/skills/dataify-ai-web-map)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Array of discovered URL objects, or null when no URLs are found.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The result may include URL, title, and description fields.]

## Skill Version(s):

2.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
