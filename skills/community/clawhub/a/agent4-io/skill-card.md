## Description:

Build and run grounded business agents on agent4.io over MCP — agents, knowledge bases, load-on-demand skills, stateful Storylines and page playbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellojixian](https://clawhub.ai/user/hellojixian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and tenant operators use this skill to connect an agent to agent4.io, then create and configure agents, knowledge bases, load-on-demand skills, Storylines, page playbooks, usage checks, and related tenant workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tenant configuration, knowledge-base material, and queries may be sent to agent4.io when the skill is used.

Mitigation: Tell the user before sending data and send only tenant material they explicitly provide.

Risk: The AGENT4_API_KEY grants access to administer the connected agent4.io tenant.

Mitigation: Keep the key restricted, avoid exposing it in logs or shared output, and revoke it when no longer needed.

Risk: MCP or REST actions can change agents, knowledge bases, Storylines, page playbooks, or other tenant state.

Mitigation: Confirm the intended tenant and user intent before state-changing actions, and use tenant_info() to verify the connection.

## Reference(s):

- [agent4.io Cookbook](https://agent4.io/cookbook)
- [agent4.io](https://agent4.io)
- [agent4.io MCP endpoint](https://api.agent4.io/v1/mcp)
- [ClawHub skill page](https://clawhub.ai/hellojixian/skills/agent4-io)
- [ClawHub publisher profile](https://clawhub.ai/user/hellojixian)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown, Code]

**Output Format:** [Markdown guidance with inline shell, text, JSON, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AGENT4_API_KEY and may guide state-changing tenant administration actions.]

## Skill Version(s):

1.1.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
