## Description:

Call Craftsman Agent API OneKey Router to generate a Minecraft 3D scene build plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Minecraft creators use this skill to request a Craftsman Agent build plan for a 3D Minecraft scene from a text prompt and optional reference image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions use mutable third-party packages, including a global npm package and an apparently unused Python package.

Mitigation: Review dependencies before installation, use an isolated environment, avoid elevated privileges, and pin package versions where possible.

Risk: Prompts and reference image URLs are sent to a third-party remote API.

Mitigation: Do not send secrets, personal data, sensitive prompts, or private image URLs unless third-party exposure is acceptable.

Risk: The skill requires an API key in DEEPNLP_ONEKEY_ROUTER_ACCESS.

Mitigation: Store the key as a secret environment variable and avoid exposing it in command history, logs, or shared output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ai-hub-admin/skills/generate-minecraft-3d-build-plan)
- [DeepNLP Workspace Keys](https://www.deepnlp.org/workspace/keys)
- [OneKey Agent Router Endpoint](https://agent.deepnlp.org/agent_router)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands; API responses are JSON that can include text and hosted image URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPNLP_ONEKEY_ROUTER_ACCESS and calls a third-party remote API.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
