## Description:

Guides agents through Agent2Agent protocol concepts, AgentCard publishing, task delegation, streaming updates, push notifications, and local mock-server testing for interoperable agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build A2A-aware agents, publish AgentCards, send and track tasks across remote agents, handle streaming or push delivery, and test interactions with a local mock A2A server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The mock A2A server can expose task data if run in an untrusted network environment.

Mitigation: Run it only in a trusted local environment, or modify it to bind to 127.0.0.1 and require authentication before shared use.

Risk: Remote A2A agents and webhook callback URLs are external systems that may receive task content or callback payloads.

Mitigation: Avoid sending secrets or confidential data unless intended, validate destination agents and callback URLs, and use the target agent's declared authentication scheme.

Risk: Published AgentCards can disclose endpoint, capability, and authentication details.

Mitigation: Review generated AgentCards before publishing and omit internal memory, private tool details, proprietary state, or unnecessary operational metadata.

## Reference(s):

- [A2A Protocol Specification](https://a2a-protocol.org/latest/specification/)
- [A2A GitHub Repository](https://github.com/a2aproject/A2A)
- [A2A Python SDK](https://github.com/a2aproject/a2a-python)
- [ClawHub Skill Page](https://clawhub.ai/wangjipeng977/skills/a2a-agent-protocol)
- [A2A Protocol Overview](artifact/references/a2a-overview.md)
- [A2A Data Model Reference](artifact/references/data-model.md)
- [A2A Operations Reference](artifact/references/operations.md)
- [AgentCard Template](artifact/references/agent-card-template.md)
- [A2A Quickstart](artifact/references/quickstart.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON AgentCard examples, Python or shell commands, configuration snippets, and structured task artifact parts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write agent-card.json or start a local mock HTTP server when the corresponding mode is used; task modes should return artifacts[].parts instead of raw task objects.]

## Skill Version(s):

1.0.0 (source: server release metadata and README badge)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
