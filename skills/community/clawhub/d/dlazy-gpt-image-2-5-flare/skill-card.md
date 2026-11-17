## Description:

Generates and edits images with GPT Image 2.5 Flare through the dLazy hosted API, with optional reference images, multiple aspect ratios, and quality levels up to max.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate images from prompts or edit images with optional reference images, aspect-ratio, and quality controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review did not assess the CLI package, and the evidence is incomplete despite a benign verdict with medium confidence.

Mitigation: Review the pinned CLI package and its login flow before installing or using it; use the pinned npx command if you prefer not to install it globally.

Risk: Prompts and local reference files are sent to dLazy services, and the CLI stores an API key in the user's configuration directory.

Mitigation: Send only content you are comfortable processing through dLazy, protect the local key, and rotate or revoke it from the organization dashboard when needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-gpt-image-2-5-flare)
- [dLazy](https://dlazy.com)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Images, JSON]

**Output Format:** [Generated image assets with JSON result metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports up to five reference images, aspect-ratio and quality settings, and asynchronous task IDs.]

## Skill Version(s):

1.2.31 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
