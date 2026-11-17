## Description:

Discovers public page URLs and site entry points through the AI Web API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users use this skill to discover page URLs from a public website and collect site-wide entry points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs are sent to Dataify, and returned addresses can consume credits.

Mitigation: Use public, non-sensitive URLs and choose a result limit appropriate to the task.

Risk: The API token authorizes requests, and a replacement gateway receives the token.

Mitigation: Keep the token out of chat and use the default HTTPS gateway unless you trust the replacement.

## Reference(s):

- [map-api.md](references/map-api.md)
- [AI Web API map endpoint](https://aiwebapi.dataify.com/map)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON array of discovered URL objects, or null when no URLs are found]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The entry URL is excluded from Map billing; other returned addresses use the gateway tool unit price.]

## Skill Version(s):

2.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
