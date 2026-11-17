## Description:

Quickly generate dynamic short videos from reference images using Wan 2.6 Flash.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to invoke dLazy's hosted Wan 2.6 Flash workflow for fast reference-image-to-video generation from prompts, images, and generation options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a third-party npm CLI package.

Mitigation: Use the pinned @dlazy/cli version, prefer npx when possible, review the package before installation, and avoid running npm as administrator or root.

Risk: The workflow requires a dLazy API key that may be stored locally or passed through the environment.

Mitigation: Use a revocable or limited API key, protect the local config and environment variables, and rotate or revoke the key when access changes.

Risk: Prompts and selected media files are sent to dLazy cloud endpoints for generation.

Mitigation: Only submit media intended for third-party processing and confirm that uploaded content is appropriate for the user's privacy and usage requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/dlazy-wan2-6-r2v-flash)
- [dLazy CLI homepage](https://github.com/dlazyai/cli)
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The invoked CLI returns generated media URLs or, for asynchronous runs, a task identifier that can be polled.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
