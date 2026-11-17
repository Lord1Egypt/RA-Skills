## Description:

Architecture Generator helps agents draft toy design sheets and guide 3D toy model generation through OneKey Agent Gateway APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to guide text or image prompt workflows that create toy design drafts, multi-view sheets, 3D generation tasks, and polling commands for generated model outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports a suspicious verdict because CLI examples use an unpinned npm package while an API key is in scope.

Mitigation: Prefer the REST curl examples, or run a pinned and verified onekey package version in an isolated environment with only the required OneKey key exposed.

Risk: Prompts and source image URLs may be sent to the gateway and downstream generation providers.

Mitigation: Do not submit confidential prompts, private images, or regulated data unless the gateway and downstream providers are approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/architecture-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/ai-hub-admin)
- [OneKey Agent Gateway endpoint](https://agent.deepnlp.org/agent_router)
- [Craftsman 3D Generator](https://craftsman-agent.aiagenta2z.com/app/3d-generator)
- [OneKey workspace keys](https://deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl and npx command examples plus JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a registered OneKey Gateway access key and references generated image, preview, and 3D model URLs returned by the gateway.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
