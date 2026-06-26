## Description: <br>
Connect to a local Burp Suite MCP Server over SSE and list or call Burp tools from the workspace. Use when Burp Suite is running with the PortSwigger MCP extension enabled on http://127.0.0.1:9876/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nquangit](https://clawhub.ai/user/nquangit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security testers use this skill to let an agent inspect available local Burp Suite MCP tools and call selected tools from a workspace. It is intended for environments where Burp Suite and the PortSwigger MCP extension are already running locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Burp traffic, tokens, request bodies, and scanner findings may be exposed through tool output. <br>
Mitigation: Use the skill only in intended local testing environments, keep the SSE URL on localhost, and avoid printing or saving sensitive traffic unless it is needed. <br>
Risk: Some Burp MCP tools can change Burp settings, editor contents, intercept state, scanner behavior, or task execution state. <br>
Mitigation: Start with read-only history, scanner issue, and options-output tools, then require explicit human approval before any state-changing tool call. <br>
Risk: Tool names and input schemas can vary by MCP extension version. <br>
Mitigation: Run list-tools before tool calls and match arguments to the returned inputSchema. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nquangit/burp-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/nquangit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper prints raw MCP-shaped JSON; some Burp results may include text blocks that need a second parse step.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
