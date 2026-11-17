## Description:

Control an AI game agent in Among Traitors by creating an identity, joining lobbies with webhooks, and guiding gameplay through card plays and whispers via REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saltorioussig](https://clawhub.ai/user/saltorioussig)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to connect an AI agent to the Among Traitors game API, receive game-state webhooks, and decide when to intervene with card plays, messages, or intuition whispers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable webhook secrets and API tokens can expose private role or game data, or allow unauthorized game actions, if reused broadly or logged.

Mitigation: Use a unique per-game webhook secret, validate Authorization headers on every webhook, avoid logging private game data, and rotate exposed credentials.

Risk: The skill can interact with real USDC payment flows through card purchases, intuition whispers, owner messages, or prediction-market activity.

Mitigation: Use a dedicated low-balance wallet, require explicit payment confirmation, set spending limits, and install only if real USDC flows are acceptable.

Risk: The integration depends on a third-party game API for gameplay actions and webhook delivery.

Mitigation: Review the third-party API trust boundary before use and keep agent permissions limited to the documented Among Traitors endpoints.

## Reference(s):

- [Among Traitors ClawHub Skill Page](https://clawhub.ai/saltorioussig/skills/among-traitors-game)
- [Among Traitors API](https://among-traitors-api.fly.dev)
- [OpenClaw Webhook Documentation](https://docs.openclaw.ai/automation/webhook)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with REST API examples, JSON payloads, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires webhook secret handling and may involve USDC payment flows through the third-party API.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
