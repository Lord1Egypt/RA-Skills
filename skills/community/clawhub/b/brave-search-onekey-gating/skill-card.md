## Description: <br>
Auto-generated skill for brave-search tools via OneKey Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-Hub-Admin](https://clawhub.ai/user/AI-Hub-Admin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Brave web searches and local business or place searches through OneKey Gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds and documents a shared fallback credential path for search requests. <br>
Mitigation: Configure a user-controlled DEEPNLP_ONEKEY_ROUTER_ACCESS key before use and prefer a release that removes the hardcoded fallback credential. <br>
Risk: Search queries may be sent through a shared or default credential path. <br>
Mitigation: Avoid submitting sensitive search terms unless the credential path and receiving service are understood and acceptable. <br>


## Reference(s): <br>
- [OneKey Gateway Keys](https://www.deepnlp.org/workspace/keys) <br>
- [OneKey MCP Router Documentation](https://www.deepnlp.org/doc/onekey_mcp_router) <br>
- [OneKey Gateway Documentation](https://deepnlp.org/doc/onekey_agent_router) <br>
- [AI Agent Marketplace](https://www.deepnlp.org/store/ai-agent) <br>
- [Skills Marketplace](https://www.deepnlp.org/store/skills) <br>
- [AI Agent Marketplace GitHub Repository](https://github.com/aiagenta2z/ai-agent-marketplace) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results and Markdown usage guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results depend on the OneKey Gateway and the Brave Search tool invoked.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
