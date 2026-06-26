## Description: <br>
Free Brave API alternative for OpenClaw. Completely FREE web search. Secure localhost-only deployment. Supports hidden --dev flag. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pipepi](https://clawhub.ai/user/pipepi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run a local SearXNG-backed web search service as a no-API-key alternative to Brave Search. It helps agents issue web searches against a localhost service while avoiding paid search API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation runs a persistent local SearXNG Docker container and replaces any existing container named searxng-local. <br>
Mitigation: Install only when Docker use is acceptable, check for an existing searxng-local container first, and remove it with docker rm -f searxng-local when no longer needed. <br>
Risk: Setting SEARXNG_BASE_URL can send searches to a remote endpoint instead of localhost. <br>
Mitigation: Leave SEARXNG_BASE_URL unset unless the remote SearXNG endpoint is intentionally selected and trusted. <br>
Risk: The --dev install mode reduces safety controls by disabling safe_search and the limiter. <br>
Mitigation: Use --dev only for local development where reduced filtering and rate limiting are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pipepi/brave-api-free-search) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Install script](artifact/scripts/install.py) <br>
- [Search script](artifact/scripts/search.py) <br>
- [Healthcheck script](artifact/scripts/healthcheck.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text search results and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker, python3, and the Python requests package; queries default to a localhost SearXNG service unless SEARXNG_BASE_URL is set.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
