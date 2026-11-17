## Description:

Use this skill when you need to control or make actions on the user's chrome tab.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nmadeleidev](https://clawhub.ai/user/nmadeleidev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an agent-controlled CLI to a live local Chrome tab for observation, navigation, clicking, typing, scrolling, and troubleshooting browser connection state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad read and control access to a live Chrome session.

Mitigation: Use it only with tabs intended for agent inspection or control, run observe before actions, and stop the server and disable the extension when finished.

Risk: Weak or reused tokens could expose the bridge to unauthorized local control.

Mitigation: Generate fresh strong shared and operator tokens for each setup, keep the operator token private, and avoid copying example token values.

Risk: Non-local deployment can expose browser-control traffic if transport and secrets are not hardened.

Mitigation: Keep the bridge bound to localhost for normal use; if deployed beyond localhost, use TLS WebSocket connections and strong secrets.

Risk: Using unverified bridge components can increase supply-chain risk.

Mitigation: Prefer pinned, verified releases of the CLI and extension before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nmadeleidev/skills/browser-agent-bridge-cli)
- [Publisher profile](https://clawhub.ai/user/nmadeleidev)
- [Project repository](https://github.com/NmadeleiDev/browser_agent_bridge)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON command payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides setup and operation of a local browser bridge using generated tokens, localhost WebSocket endpoints, and repeated observe/action verification steps.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
