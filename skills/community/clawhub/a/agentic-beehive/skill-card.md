## Description:

Agentic Engineering helps an agent choose between task-delivery and state-maintenance operating patterns, then route work through coding, composing, supervising, quantitative trading, MCP, or AI daily-report branches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hon27hon](https://clawhub.ai/user/hon27hon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to structure multi-agent engineering work, select an execution posture, produce coding handoffs, supervise agent collaboration, support quantitative-trading workflows, and operate a local MCP coordination service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent MCP services and endpoint probing can interact with endpoints registered by the user.

Mitigation: Review the MCP server behavior before installation, run it in an isolated environment, and avoid registering internal or sensitive endpoints.

Risk: Optional report sending can disclose report content or recipient identifiers outside the local environment.

Mitigation: Remove the hardcoded Feishu recipient before sending reports and rotate any real credentials copied from the docs.

Risk: AutoGen Studio or gateway-managed services can be exposed if bound to public interfaces.

Mitigation: Keep these services on trusted local interfaces and do not bind AutoGen Studio to public interfaces.

Risk: Unreviewed dependencies can expand the execution and network surface of the MCP server.

Mitigation: Pin and review dependencies before enabling the gateway-managed server.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hon27hon/skills/agentic-beehive)
- [Agentic Engineering Skill](artifact/SKILL.md)
- [Coding Branch](artifact/coding/SKILL.md)
- [PACT Loop Protocol](artifact/coding/protocol.md)
- [MCP Server README](artifact/mcp-server/README.md)
- [Evolution Rules](artifact/evolution-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, configuration snippets, and optional generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local memory notes, handoff documents, MCP server state, and AI market-report artifacts when the relevant branch is used.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
