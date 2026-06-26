## Description: <br>
AI-optimized web search via Bailian(Alibaba ModelStdio) API. Returns multisourced, concise web search results for LLMs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent users use this skill to run concise, multi-source web searches through Alibaba Bailian WebSearch when an agent needs current external information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Alibaba Cloud using the user's DashScope API key, so private personal, credential, financial, or business context in a query may be disclosed to a third party. <br>
Mitigation: Keep queries generic, remove sensitive details before searching, and install only when this external search behavior is acceptable. <br>
Risk: The skill requires DASHSCOPE_API_KEY, and exposing the key in prompts, commands, logs, or responses could compromise the user's Alibaba Cloud account. <br>
Mitigation: Store the key in the environment, use the provided script rather than raw API calls, and never echo or include the key in agent output. <br>
Risk: Large repeated searches can consume API quota or create unexpected cost because quota controls are mostly documented rather than enforced by the script. <br>
Mitigation: Respect the documented result count limit and confirm with the user before issuing many searches in one conversation. <br>


## Reference(s): <br>
- [Bailian WebSearch MCP listing](https://bailian.console.aliyun.com/cn-beijing?tab=app#/mcp-market/detail/WebSearch) <br>
- [Faberlens safety evaluation](https://faberlens.ai) <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/bailian-web-search-hardened) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with shell command examples and JSON search responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, jq, and DASHSCOPE_API_KEY; default result count is 5 and documented maximum is 20.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
