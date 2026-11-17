## Description:

Deploys and queries a localhost-only SearXNG web search service for OpenClaw without requiring an external search API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipepi](https://clawhub.ai/user/pipepi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, health-check, and query a local SearXNG service for agent web-search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer creates a persistent local Docker service named searxng-local.

Mitigation: Review before installing, check whether an existing searxng-local container belongs to you, and remove the container when it is no longer needed.

Risk: The Docker image is not pinned to a specific SearXNG version.

Mitigation: Prefer an approved, pinned SearXNG image tag before operational use.

Risk: SEARXNG_BASE_URL can redirect health checks and searches away from the expected local endpoint.

Mitigation: Keep the default localhost endpoint unless an override has been reviewed and validated.

Risk: The development flag disables safe search and the limiter.

Mitigation: Use development mode only for local development and keep the default safe-search and limiter settings for normal use.

Risk: Installer shell commands are sensitive to paths with spaces or shell metacharacters.

Mitigation: Run the installer from a trusted path without spaces or shell metacharacters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pipepi/skills/free-local-web-search)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text command output with JSON-backed search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 10 search results with title, URL, and content snippet; requires Docker, Python 3, and the Python requests package.]

## Skill Version(s):

1.0.7 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
