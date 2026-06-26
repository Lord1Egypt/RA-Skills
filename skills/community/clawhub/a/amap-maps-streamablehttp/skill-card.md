## Description: <br>
Auto-generated skill for amap-maps-streamableHTTP tools via OneKey Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-Hub-Admin](https://clawhub.ai/user/AI-Hub-Admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Amap mapping tools through OneKey Gateway for route planning, geocoding, reverse geocoding, POI search, distance lookup, weather lookup, IP location, and generated Amap client links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location-related inputs such as map queries, coordinates, routes, addresses, POI searches, weather locations, or IP lookups are sent to OneKey Gateway/Amap. <br>
Mitigation: Use the skill only when that data sharing is acceptable for the task and organization. <br>
Risk: The scripts can fall back to a demo access key when DEEPNLP_ONEKEY_ROUTER_ACCESS is not configured. <br>
Mitigation: Configure your own DEEPNLP_ONEKEY_ROUTER_ACCESS key before use, especially for production or sensitive workflows. <br>
Risk: Runtime dependencies are installed from external package registries. <br>
Mitigation: Use pinned dependencies or an isolated environment for production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AI-Hub-Admin/amap-maps-streamablehttp) <br>
- [OneKey MCP Router Doc](https://www.deepnlp.org/doc/onekey_mcp_router) <br>
- [OneKey Gateway Doc](https://deepnlp.org/doc/onekey_agent_router) <br>
- [OneKey Gateway Keys](https://www.deepnlp.org/workspace/keys) <br>
- [AI Agent Marketplace GitHub](https://github.com/aiagenta2z/ai-agent-marketplace) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [JSON responses from tool calls, shell command examples, Python wrapper scripts, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool calls require JSON payloads and a DEEPNLP_ONEKEY_ROUTER_ACCESS key; scripts print JSON results.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
