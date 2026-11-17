## Description:

Provides a local, no-API-key web search workflow using SearXNG as a Brave API alternative for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipepi](https://clawhub.ai/user/pipepi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run local web searches without a Brave API key, backed by a localhost SearXNG service. It is suited for OpenClaw workflows that need text search results while keeping the default search endpoint local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer runs shell commands through shell=True.

Mitigation: Review or patch scripts/install.py to invoke Docker with argument arrays before installation.

Risk: The installer deploys a persistent Docker service from an unpinned SearXNG image.

Mitigation: Pin the container image and remove or consciously accept --restart unless-stopped before running the installer.

Risk: Search queries are sent to the configured SEARXNG_BASE_URL.

Mitigation: Use the default localhost endpoint or only set SEARXNG_BASE_URL to a trusted service.

Risk: Development mode disables safe_search and the limiter.

Mitigation: Use --dev only for local development and keep the default safe_search and limiter settings for normal use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pipepi/skills/brave-api-free-search)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Plain text search results and command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output is limited to the first 10 results returned by the configured SearXNG endpoint.]

## Skill Version(s):

1.0.8 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
