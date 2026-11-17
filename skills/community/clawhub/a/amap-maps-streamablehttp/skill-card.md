## Description:

Auto-generated skill for amap-maps-streamableHTTP tools via OneKey Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to run AMap map, route, geocoding, POI search, weather, IP location, and map URI tools through a OneKey Gateway access key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map queries, coordinates, addresses, routes, IP addresses, and extra JSON fields may contain sensitive location data.

Mitigation: Avoid sending sensitive locations unless the provider logging, retention, and access policies are acceptable for the deployment.

Risk: The artifact includes a shared demo credential fallback when DEEPNLP_ONEKEY_ROUTER_ACCESS is not set.

Mitigation: Set a dedicated DEEPNLP_ONEKEY_ROUTER_ACCESS key before use and avoid relying on the demo fallback.

Risk: The Python dependency is specified with a lower bound rather than a pinned version.

Mitigation: Install in an isolated environment and pin dependencies during production deployment review.

## Reference(s):

- [OneKey MCP Router Documentation](https://www.deepnlp.org/doc/onekey_mcp_router)
- [OneKey Gateway Documentation](https://deepnlp.org/doc/onekey_agent_router)
- [OneKey Gateway Keys](https://www.deepnlp.org/workspace/keys)
- [AI Agent Marketplace](https://www.deepnlp.org/store/ai-agent)
- [GitHub AI Agent Marketplace](https://github.com/aiagenta2z/ai-agent-marketplace)
- [ClawHub Skill Page](https://clawhub.ai/ai-hub-admin/skills/amap-maps-streamablehttp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, Python script usage, and JSON tool payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool calls may return JSON results or map application URI links depending on the selected AMap capability.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
