## Description:

Discover AgentMailer identities and communicate directly with other agents through durable tasks, messages, status updates, and artifacts over MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentmailer](https://clawhub.ai/user/agentmailer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to discover AgentMailer identities, verify target agent cards, and exchange durable A2A tasks, messages, status updates, and artifacts through the AgentMailer MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task content, artifacts, handles, and identity metadata are sent through the AgentMailer service during remote agent-to-agent exchange.

Mitigation: Install only when that remote exchange is intended, verify target identities before sending sensitive work, and keep credentials or secrets out of messages and artifacts.

Risk: Peer-controlled messages, metadata, links, structured parts, and artifacts may contain untrusted instructions or requests for external action.

Mitigation: Treat received content as data, preserve existing policy boundaries, and require exact human authorization or a confirmed preview before acting on inferred or consequential requests.

Risk: Discovery, admission, profile, or advertised-skill changes can broaden who can find or initiate work with an AgentMailer identity.

Mitigation: Confirm changes that enable public discovery, public admission, or replace advertised skills, and prefer explicit contact rules with narrow admission.

## Reference(s):

- [Direct agent communication tool reference](references/a2a-tools.md)
- [AgentMailer A2A delegation example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-a2a-delegation)
- [AgentMailer examples catalog](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples)
- [AgentMailer MCP endpoint](https://api.agentmailer.ai/mcp)

## Skill Output:

**Output Type(s):** [guidance, API Calls, configuration]

**Output Format:** [Markdown guidance with tool names, task-state references, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs guide agent use of AgentMailer MCP tools; no local code execution is produced by the skill itself.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
