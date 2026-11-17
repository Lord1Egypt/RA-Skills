## Description:

Generate diverse design style images with Recraft v3, supporting text-to-image and image-to-image workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to generate design-style images through the dLazy Recraft v3 CLI. It supports prompt-based image generation and image-to-image workflows that return hosted image outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, selected media files, and generated outputs through a third-party cloud service.

Mitigation: Use the skill only when cloud processing is acceptable, and do not pass private files unless they are intended for upload to dLazy.

Risk: The skill depends on the dLazy npm CLI and stores or reads a dLazy API key for authenticated requests.

Mitigation: Prefer the pinned npx invocation when possible, review the upstream package or source before use, and rotate or revoke API keys from the dLazy dashboard when needed.

## Reference(s):

- [dLazy CLI source](https://github.com/dlazyai/cli)
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy homepage](https://dlazy.com)
- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/dlazy-recraft-v3)
- [ClawHub publisher profile](https://clawhub.ai/user/dlazyai)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image results are returned as dLazy-hosted output URLs; asynchronous calls may return a task identifier for polling.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
