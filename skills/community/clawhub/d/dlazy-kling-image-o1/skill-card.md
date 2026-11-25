## Description:

Generates images with the Kling o1 model from text prompts or reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate or edit images with Kling o1 from text prompts and optional reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial and medium confidence, with some install references missing.

Mitigation: Before installing, confirm the CLI login flow and pinned npm package/version are expected, and review the full skill instructions and referenced material.

Risk: Prompts and supplied local images are sent to dLazy-hosted services for processing.

Mitigation: Avoid sending sensitive prompts or images, and review dLazy's service terms before use.

## Reference(s):

- [dLazy homepage](https://dlazy.com)
- [CLI repository listed in skill metadata](https://github.com/dlazy-ai/cli)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Image files, JSON]

**Output Format:** [Generated image URLs or saved image files, with JSON task and result metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports asynchronous task IDs and optional saving to a local path.]

## Skill Version(s):

1.3.43 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
