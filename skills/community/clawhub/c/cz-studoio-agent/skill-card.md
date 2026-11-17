## Description:

Bridge OpenClaw to a remote Studio Agent over WebSocket using a local JSONL proxy CLI for streaming, stop, and multi-turn ClickZetta Studio or Lakehouse task requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luketalent](https://clawhub.ai/user/luketalent)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to connect OpenClaw to a configured ClickZetta Studio Agent and relay user requests through a local Node.js proxy. It supports setup guidance, one-shot request execution, streaming/debug proxy mode, and structured error reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests and identity metadata to the configured Studio WebSocket endpoint.

Mitigation: Install and run it only with a trusted endpoint, and keep Studio configuration private.

Risk: The default interrupt decision mode can approve remote action requests automatically.

Mitigation: Set `CZ_INTERRUPT_DECISION_MODE` to `off` or `auto_reject` unless automatic approval is explicitly intended.

Risk: Token-bearing `CZ_AGENT_WS_URL` values can appear in local config output or shared transcripts.

Mitigation: Do not paste validate/apply output into logs or support chats, and rotate any token that has already been exposed.

Risk: Broad `CZ_ALWAYS_ALLOW_TOOLS` settings can expand remote tool execution without per-request review.

Mitigation: Avoid broad always-allow tool lists and keep allowed tools narrowly scoped to the workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luketalent/skills/cz-studoio-agent)
- [ClawHub Publisher Profile](https://clawhub.ai/user/luketalent)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-line proxy or one-shot runner responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a configured Studio WebSocket endpoint; normal one-shot execution returns one JSON object containing either assistant content or a structured error.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
