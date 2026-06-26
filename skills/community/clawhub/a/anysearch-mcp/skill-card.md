## Description: <br>
AnySearch MCP helps agents connect to AnySearch for general web search, vertical domain search, parallel batch queries, and URL content extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anysearch-ai](https://clawhub.ai/user/anysearch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure an MCP search service that can perform real-time web and vertical searches, run small batches of independent searches, and extract web page content as Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, extracted URLs, and configured AnySearch API keys are sent to the AnySearch service. <br>
Mitigation: Use environment variables for API keys, avoid sensitive searches, and install only when the user trusts the provider. <br>
Risk: stdio and SSE setups may depend on proxy packages invoked through npx. <br>
Mitigation: Review the selected proxy package before use and prefer native Streamable HTTP when the agent supports it. <br>


## Reference(s): <br>
- [AnySearch MCP on ClawHub](https://clawhub.ai/anysearch-ai/anysearch-mcp) <br>
- [AnySearch API Key Console](https://anysearch.com/console/api-keys) <br>
- [mcp-remote proxy](https://github.com/geelen/mcp-remote) <br>
- [supergateway proxy](https://github.com/supercorp-ai/supergateway) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON configuration examples and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP tool selection guidance and setup snippets for Streamable HTTP, stdio, and SSE clients.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
