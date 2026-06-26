## Description: <br>
AgentMemo gives AI agents persistent cloud memory and human-in-the-loop approval across sessions, models, and MCP or REST integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iiamit](https://clawhub.ai/user/iiamit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use AgentMemo to give agents cloud-backed memory across sessions and to request human approval before sensitive or irreversible actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory content and approval context are sent to and stored by AgentMemo cloud services. <br>
Mitigation: Use the skill only when cloud-backed memory is acceptable, avoid storing secrets or regulated data unless policy permits it, and delete stored data when it is no longer needed. <br>
Risk: The AgentMemo API key enables authenticated access to account memory and approval operations. <br>
Mitigation: Store AGENTMEMO_API_KEY in managed environment configuration, avoid exposing it in logs or prompts, and rotate it if it may have been disclosed. <br>
Risk: The optional MCP setup installs and runs an external npm package. <br>
Mitigation: Install agentmemo-mcp only for MCP client workflows; use REST or SDK access when the MCP server is not required. <br>


## Reference(s): <br>
- [AgentMemo website](https://agentmemo.net) <br>
- [AgentMemo API base URL](https://api.agentmemo.net) <br>
- [AgentMemo MCP npm package](https://www.npmjs.com/package/agentmemo-mcp) <br>
- [AgentMemo privacy policy](https://agentmemo.net/privacy) <br>
- [ClawHub skill page](https://clawhub.ai/iiamit/agentmemo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON, bash, curl, and TypeScript examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTMEMO_API_KEY and network access to api.agentmemo.net; the agentmemo-mcp npm package is optional for MCP client workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
