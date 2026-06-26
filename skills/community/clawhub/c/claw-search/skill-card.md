## Description: <br>
Claw Search provides a web search API and CLI helper for AI agents, with optional Brave and Tavily backends and a local deployment path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanchao193](https://clawhub.ai/user/yuanchao193) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Claw Search to let agents submit web search queries through an API or CLI and receive structured search results. The artifact also includes deployment guidance for running the search service locally or in Docker. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search and content-extraction endpoints can generate external network traffic and may process sensitive or internal query terms. <br>
Mitigation: Avoid entering secrets or private internal terms, run the service behind authentication for shared deployments, and restrict URL extraction to approved destinations. <br>
Risk: The artifact includes shell command construction for the skillhub search backend. <br>
Mitigation: Remove shell-based command construction or replace it with a safe API or argument-array invocation before exposing the service to untrusted users. <br>
Risk: The artifact includes unauthenticated query history and suggestion behavior. <br>
Mitigation: Disable query history or protect it with authentication and retention controls before production use. <br>
Risk: Dependency and runtime setup require review before installation. <br>
Mitigation: Install dependencies only from trusted HTTPS registries, scan dependency lockfiles, and review the service before deployment. <br>


## Reference(s): <br>
- [Claw Search ClawHub listing](https://clawhub.ai/yuanchao193/claw-search) <br>
- [Publisher profile](https://clawhub.ai/user/yuanchao193) <br>
- [Tavily Search API](https://tavily.com) <br>
- [Brave Search API](https://brave.com/search/api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON API responses and terminal text, with Markdown documentation for command and deployment examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include titles, URLs, descriptions, source metadata, language or intent labels, latency, cache status, and optional free-API matches depending on the server entry point.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
