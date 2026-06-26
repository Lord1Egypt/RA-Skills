## Description: <br>
AgentMFA requests human approval before sensitive actions using MCP tools for registration, identity, and approval flows in Claude Code, Cursor, OpenClaw, and other MCP-compatible clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leiarenee](https://clawhub.ai/user/leiarenee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add an explicit human approval checkpoint before sensitive or irreversible agent actions such as production deployments, infrastructure changes, bulk deletion, messaging, or financial operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external AgentMFA approval service and sends approval data to that service. <br>
Mitigation: Install it only when that approval service is intended for the workflow, and review the CLI source, account setup, and service policy before deployment. <br>
Risk: AgentMFA does not automatically intercept sensitive actions; the agent must explicitly request approval. <br>
Mitigation: Define clear agent rules for sensitive operations and require the approval flow before proceeding with production, destructive, financial, messaging, or infrastructure changes. <br>
Risk: One-time approval tokens or codes are sensitive audit proofs. <br>
Mitigation: Avoid logging or pasting approval tokens into chat, never reuse codes, and treat expired or rejected requests as denied. <br>


## Reference(s): <br>
- [AgentMFA homepage](https://agentmfa.ai) <br>
- [AgentMFA source code](https://github.com/agentmfa/agentmfa) <br>
- [AgentMFA MCP Examples](references/examples.md) <br>
- [AgentMFA Error Handling](references/errors.md) <br>
- [ClawHub skill page](https://clawhub.ai/leiarenee/agentmfa) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown instructions with inline shell commands and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the agentmfa CLI, OAuth login, and an AgentMFA approval service connection.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
