## Description: <br>
Auto-generated skill for baidu-maps-sse tools via OneKey Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-Hub-Admin](https://clawhub.ai/user/AI-Hub-Admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call Baidu Maps and related geolocation tools through OneKey Gateway for geocoding, reverse geocoding, place search, place details, distance matrices, elevation lookups, and directions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map queries, addresses, coordinates, and travel locations are sent through OneKey Gateway and any downstream maps provider. <br>
Mitigation: Avoid submitting sensitive home, work, or private travel locations unless the provider data handling is acceptable. <br>
Risk: The artifact includes a shared demo access key fallback for testing. <br>
Mitigation: Set a dedicated DEEPNLP_ONEKEY_ROUTER_ACCESS key for normal use instead of relying on the shared demo fallback. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AI-Hub-Admin/baidu-maps-sse) <br>
- [OneKey MCP Router Doc](https://www.deepnlp.org/doc/onekey_mcp_router) <br>
- [OneKey Gateway Doc](https://deepnlp.org/doc/onekey_agent_router) <br>
- [OneKey Gateway Keys](https://www.deepnlp.org/workspace/keys) <br>
- [AI Agent Marketplace](https://www.deepnlp.org/store/ai-agent) <br>
- [Skills Marketplace](https://www.deepnlp.org/store/skills) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses from CLI or Python script invocations, with markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DEEPNLP_ONEKEY_ROUTER_ACCESS for normal use; scripts accept JSON input through --data or --data-file.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
