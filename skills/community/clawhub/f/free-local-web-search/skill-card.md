## Description: <br>
100% FREE local web search for OpenClaw. Secure localhost-only SearXNG deployment. Supports hidden --dev flag. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pipepi](https://clawhub.ai/user/pipepi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to deploy and query a local SearXNG instance for free web search without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search requests can be sent to a non-local SearXNG endpoint if SEARXNG_BASE_URL is set. <br>
Mitigation: Leave SEARXNG_BASE_URL unset or set it only to a trusted loopback SearXNG URL. <br>
Risk: The --dev installer mode disables safe_search and the limiter. <br>
Mitigation: Avoid --dev except for deliberate local development where reduced search safety is acceptable. <br>
Risk: Installation replaces any Docker container named searxng-local and starts a persistent container. <br>
Mitigation: Check for an existing searxng-local container before installing and remove the container with docker rm -f searxng-local when no longer needed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/pipepi/free-local-web-search) <br>
- [Publisher profile](https://clawhub.ai/user/pipepi) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and JSON search results printed by shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires docker and python3; runtime scripts also require the Python requests package.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
