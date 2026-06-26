## Description: <br>
Auto-generated skill for bing-image-search-mcp tools via OneKey Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-Hub-Admin](https://clawhub.ai/user/AI-Hub-Admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to search Bing Images through OneKey Gateway, either for a single query or for a batch of image search queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image search queries are sent through OneKey Gateway and Bing, which may expose sensitive query text to third-party services. <br>
Mitigation: Do not submit secrets, private personal data, regulated information, or confidential business data in search queries. <br>
Risk: The scripts fall back to a disclosed shared demo key when DEEPNLP_ONEKEY_ROUTER_ACCESS is not set. <br>
Mitigation: Set a dedicated OneKey Gateway API key for accountable use and avoid relying on the demo key for normal operation. <br>
Risk: The skill depends on third-party packages and services outside NVIDIA control. <br>
Mitigation: Install only after reviewing the OneKey Gateway/Bing dependency posture and keep package installation aligned with local security policy. <br>


## Reference(s): <br>
- [OneKey Gateway Keys](https://www.deepnlp.org/workspace/keys) <br>
- [OneKey MCP Router Doc](https://www.deepnlp.org/doc/onekey_mcp_router) <br>
- [OneKey Gateway Doc](https://deepnlp.org/doc/onekey_agent_router) <br>
- [AI Agent Marketplace](https://www.deepnlp.org/store/ai-agent) <br>
- [GitHub AI Agent Marketplace](https://github.com/aiagenta2z/ai-agent-marketplace) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Configuration instructions] <br>
**Output Format:** [JSON image search results and Markdown usage guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include image titles, thumbnail URLs, and source URLs when returned by the upstream service.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
