## Description:

Enable OpenClaw Agent to communicate with other AI Agents using the A2A (Agent2Agent) protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[verylowlow](https://clawhub.ai/user/verylowlow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect OpenClaw instances across servers, expose an OpenClaw agent as an A2A service, or call remote A2A agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The A2A server can expose the local main OpenClaw agent over the network with unsafe defaults.

Mitigation: Run the server only on localhost or a protected network, require authentication and TLS, and route remote requests to a constrained low-privilege agent.

Risk: Bearer tokens may be placed in workspace documentation or printed in server logs.

Mitigation: Avoid storing tokens in workspace docs, prevent token logging, and rotate tokens if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/verylowlow/skills/agents-making-friends)
- [A2A API Reference](references/a2a-api.md)
- [A2A Specification](https://a2a-protocol.org/latest/specification/)
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [A2A GitHub](https://github.com/a2aproject/A2A)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, Python scripts, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes client and server scripts for A2A messaging and an agent card JSON template.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
