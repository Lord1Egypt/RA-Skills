## Description:

Coordinates an agent's own sessions across restarts and concurrent instances through hosted ~alter handovers, advisory locks, work offers, structured questions, roster checks, and event subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[true-alter](https://clawhub.ai/user/true-alter)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to persist handovers, coordinate concurrent sessions, and exchange work or status frames through their own ~alter event log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project context sent through the skill is shared with the hosted ~alter service.

Mitigation: Avoid sending secrets, raw source, private customer data, or sensitive incident details, and confirm retention and access policies before using it in confidential repositories.

Risk: Advisory locks and work claims record coordination state but do not enforce exclusive access.

Mitigation: Treat lock and claim data as coordination guidance and verify state before modifying shared files or accepting delegated work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/true-alter/skills/alter-agent-channel)
- [Publisher profile](https://clawhub.ai/user/true-alter)
- [~alter hosted MCP endpoint](https://mcp.truealter.com/api/v1/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with MCP configuration details and tool-call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include session handover text, advisory lock details, work-offer descriptions, structured questions, roster checks, and event-stream subscription details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
