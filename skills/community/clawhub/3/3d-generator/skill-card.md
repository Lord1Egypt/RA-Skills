## Description:

AI Generated 3D Models using SOTA APIs such as Tripo/Meshy/TripoSR/etc served on OneKey Agent Gateway by Craftsman Agent, useful for AI Game, Figurine, Stuffed Toy Generation

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and builders use this skill to create and poll 3D model generation tasks from text prompts, single images, or multi-view image inputs through OneKey Gateway-backed providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, image URLs, and generated-asset metadata through OneKey Gateway and downstream 3D providers.

Mitigation: Use it only when that data sharing is acceptable for the intended content and environment.

Risk: The examples include unpinned npx command execution while an API key is in use.

Mitigation: Prefer the direct HTTPS API examples or a pinned, reviewed onekey version before using CLI commands.

Risk: The OneKey Gateway access key can be exposed through logs or shell history.

Mitigation: Keep `DEEPNLP_ONEKEY_ROUTER_ACCESS` out of logs and shell history where possible, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/3d-generator)
- [Publisher profile](https://clawhub.ai/user/ai-hub-admin)
- [Craftsman 3D Generator](https://craftsman-agent.aiagenta2z.com/app/3d-generator)
- [Craftsman gallery](https://craftsman-agent.aiagenta2z.com/gallery/3d_generator)
- [AI Agent Marketplace keys](https://deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill documents task creation and polling flows that can return 3D model URLs, preview image URLs, progress, metadata, credits, and provider raw output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
