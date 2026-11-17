## Description:

Give your AI agent persistent memory and human-in-the-loop approval across sessions and models through the AgentMemo cloud API and optional MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iiamit](https://clawhub.ai/user/iiamit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use AgentMemo to give agents persistent cloud-backed memory and a human approval workflow for sensitive actions. It is appropriate when users are comfortable sending selected memories to AgentMemo and configuring an AgentMemo API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected agent memories are sent to and stored by AgentMemo's cloud service.

Mitigation: Use the skill only when cloud storage is acceptable, and avoid storing secrets, private credentials, or sensitive personal data as memories.

Risk: The optional MCP setup runs an npm package with access to the user's AgentMemo API key.

Mitigation: Pin npm packages to reviewed exact versions and restrict the MCP process environment to the required API key.

## Reference(s):

- [AgentMemo website](https://agentmemo.net)
- [AgentMemo API endpoint](https://api.agentmemo.net)
- [AgentMemo MCP npm package](https://www.npmjs.com/package/agentmemo-mcp)
- [AgentMemo SDK npm package](https://www.npmjs.com/package/agentmemo)
- [AgentMemo privacy policy](https://agentmemo.net/privacy)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls, Code]

**Output Format:** [Markdown with inline JSON, bash, TypeScript, and REST examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENTMEMO_API_KEY and network access to api.agentmemo.net.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
