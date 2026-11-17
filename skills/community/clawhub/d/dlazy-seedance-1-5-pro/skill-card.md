## Description:

Convert images into dynamic dance videos using Doubao Seedance 1.5 Pro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to invoke dLazy's hosted Doubao Seedance 1.5 Pro workflow from an agent, turning supplied images and prompts into generated motion or dance videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs a third-party npm CLI.

Mitigation: Install only if dLazy and the @dlazy/cli package are trusted; prefer the pinned npx form or a sandboxed environment.

Risk: The workflow stores and uses a dLazy API key.

Mitigation: Keep the API key revocable, use the documented dLazy authentication flow, and rotate or revoke the key if exposure is suspected.

Risk: Selected local media files may be uploaded to dLazy for cloud generation.

Mitigation: Confirm which media files will be sent before running billable generation commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlazyai/skills/dlazy-seedance-1-5-pro)
- [dLazy CLI source](https://github.com/dlazyai/cli)
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy homepage](https://dlazy.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The invoked CLI may return hosted media URLs, asynchronous task identifiers, and JSON status or error responses.]

## Skill Version(s):

1.1.2 (source: server release evidence; artifact frontmatter lists 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
