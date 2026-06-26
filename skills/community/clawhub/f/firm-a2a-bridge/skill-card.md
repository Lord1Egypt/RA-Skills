## Description: <br>
Firm A2a Bridge provides an Agent-to-Agent Protocol RC v1.0 bridge for OpenClaw agents, covering agent cards, task lifecycle management, push notifications, cancellation, discovery, and SSE subscriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent engineers use this skill to connect OpenClaw agents with A2A-compatible agents, generate and validate agent cards, send and monitor tasks, configure push notifications, cancel tasks, and subscribe to task updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill involves network, webhook, local file, and token-related behavior as part of A2A interoperability. <br>
Mitigation: Install only when the referenced MCP extension is trusted, use trusted agent, webhook, and callback URLs, and avoid sending sensitive task content to unknown agents. <br>
Risk: Authentication tokens or signing keys may be used for push delivery or agent card signing. <br>
Mitigation: Provide only scoped tokens or signing keys and rotate them if they are exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/firm-a2a-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce agent-card JSON files, task records, webhook configuration, and SSE subscription outputs through the referenced MCP extension.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
