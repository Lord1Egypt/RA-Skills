## Description: <br>
Provides web access operating profiles, caching helpers, and local observation logs so agents can avoid repeated API rate-limit failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[highnoonoffice](https://clawhub.ai/user/highnoonoffice) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Agent Tollbooth to check observed service profiles before external API calls, reuse cached price data, and log web-access outcomes for later profile updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local logs and caches may contain service names, request details, or operational context. <br>
Mitigation: Avoid putting secrets, private hostnames, or sensitive account details into service names or log details, and review local data under $OPENCLAW_WORKSPACE/data/agent-tollbooth/ before sharing. <br>
Risk: The bundled service profiles include credential-related notes for third-party services such as Stripe, GitHub, Ghost, and ClawHub. <br>
Mitigation: Review any suggested credential use or write operation before allowing an agent to act, especially for services that can spend money, modify production systems, or publish content. <br>
Risk: Auto-drafted profiles are based on observed events and may be incomplete or misleading until reviewed. <br>
Mitigation: Treat promoted profile drafts as review material and verify endpoint, authentication, rate-limit, and caching guidance before relying on them. <br>


## Reference(s): <br>
- [Agent Tollbooth ClawHub page](https://clawhub.ai/highnoonoffice/agent-tollbooth) <br>
- [highnoonoffice publisher profile](https://clawhub.ai/user/highnoonoffice) <br>
- [Project homepage](https://github.com/highnoonoffice/agent-tollbooth) <br>
- [Service Profiles](references/profiles.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, and JSON outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts may write local logs and cache files under $OPENCLAW_WORKSPACE/data/agent-tollbooth/.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
