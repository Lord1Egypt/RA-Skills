## Description:

Generates toy multi-view sheets and 3D model generation tasks for figurines, stuffed toys, 3D printing, game assets, and architecture toys through the OneKey Agent Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use this skill to guide agents through prompt/image-to-draft, 3D task creation, and polling workflows for toy-style assets and previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI examples run an unpinned npm package while using an API key.

Mitigation: Prefer the direct REST examples, or pin and verify the `onekey` CLI package version before use.

Risk: Prompts, image URLs, and generated asset data may be sent to the gateway and downstream providers.

Mitigation: Do not submit secrets, confidential prompts, private image URLs, or regulated data unless those services are trusted for the intended use.

Risk: The skill requires a gateway API key for use.

Mitigation: Use a scoped, revocable API key and run any CLI client with least privilege.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/game-asset-generator)
- [OneKey Agent Gateway endpoint](https://agent.deepnlp.org/agent_router)
- [Craftsman 3D Generator](https://craftsman-agent.aiagenta2z.com/app/3d-generator)
- [Craftsman website](https://craftsman-agent.aiagenta2z.com)
- [DeepNLP workspace keys](https://deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with REST, CLI, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference external URLs for generated images, previews, and GLB model files returned by the gateway.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
