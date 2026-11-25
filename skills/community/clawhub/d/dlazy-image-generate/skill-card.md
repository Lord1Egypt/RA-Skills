## Description:

Image generation skill. Automatically selects the best dlazy CLI image model based on the prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators can use the skill to generate images from prompts and select an appropriate dlazy image model. It also describes image editing and processing workflows through the dlazy CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary notes that the instructions describe video and speech features in addition to image generation, so the scope may be broader than the release description suggests.

Mitigation: Review the selected command and media type before use, and provide only inputs intended for that operation.

Risk: The skill documentation says prompts and supplied media can be sent to dLazy hosted services.

Mitigation: Avoid submitting sensitive prompts or media unless that transfer is permitted for the intended use.

Risk: The security summary says some reference checks were incomplete, leaving the available evidence incomplete.

Mitigation: Review the linked package and service information before installation or use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dlazyai/skills/dlazy-image-generate)
- [dLazy website](https://dlazy.com)
- [@dlazy/cli npm package](https://www.npmjs.com/package/@dlazy/cli)
- [CLI project page listed in skill metadata](https://github.com/dlazy-ai/cli)

## Skill Output:

**Output Type(s):** [Image files, SVG files, URLs, Shell commands, Guidance]

**Output Format:** [CLI commands with JSON results and generated-media URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media may be hosted at dLazy URLs; available operations and output details depend on the selected model.]

## Skill Version(s):

1.3.45 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
