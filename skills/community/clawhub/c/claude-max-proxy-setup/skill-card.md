## Description: <br>
Use when an agent or developer wants to reduce Claude API costs, route requests through a Claude Max or Pro subscription instead of per-token billing, or set up claude-max-api-proxy for OpenClaw or any OpenAI-compatible client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ERROR403agent](https://clawhub.ai/user/ERROR403agent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up a local Claude Max API proxy and configure OpenAI-compatible clients to send requests through it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup depends on a third-party npm package. <br>
Mitigation: Review and trust the linked claude-max-api-proxy package before installing it. <br>
Risk: The proxy uses the user's logged-in Claude CLI session. <br>
Mitigation: Run it only on trusted local machines and avoid shared or public hosts. <br>
Risk: Anyone who can reach the proxy port may be able to make requests through the user's subscription. <br>
Mitigation: Keep the proxy bound to localhost and do not expose port 3456. <br>
Risk: Enabling the systemd service makes the proxy persist across sessions. <br>
Mitigation: Enable persistence only when continuous local proxy availability is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ERROR403agent/claude-max-proxy-setup) <br>
- [claude-max-api-proxy source](https://github.com/atalovesyou/claude-max-api-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
