## Description:

Gateway-only ACP negotiation skill with optional OpenClaw model-driven turn decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to run buyer or seller participants in an ACP-style market negotiation through a trusted gateway. It supports rule-based decisions or optional local OpenClaw model decisions for each negotiation turn.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically negotiate through a gateway while exposing tokens.

Mitigation: Use only a trusted local or HTTPS gateway and replace default tokens with unique secrets.

Risk: Passing API keys or authentication tokens on the command line can expose secrets.

Mitigation: Prefer environment-based provider keys, avoid direct command-line secrets, and rotate any exposed credentials.

Risk: The OpenClaw decision engine may send negotiation or session data to a model provider.

Mitigation: Avoid sensitive negotiation data unless the configured provider and data handling controls are approved.

Risk: The security guidance warns against real financial or business negotiations until token handling, TLS guidance, and policy checks are tightened.

Mitigation: Limit use to reviewed sandbox scenarios or require human approval before acting on generated decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luoqianchenguni-max/skills/a2a-market-acp-lite-negotiation)

## Skill Output:

**Output Type(s):** [json, shell commands, configuration, guidance]

**Output Format:** [Newline-delimited JSON status events and structured negotiation response JSON, with Markdown command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Gateway loop mode registers an agent, pulls messages, responds to negotiation turns, and can auto-start a session.]

## Skill Version(s):

0.2.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
