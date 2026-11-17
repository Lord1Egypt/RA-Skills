## Description:

Reads figure prompts from a paper-analysis file, uses Gemini through browser automation to generate scientific diagrams, and saves the images to a fixed local directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m1ss-cell](https://clawhub.ai/user/m1ss-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to turn figure prompts extracted from parsed paper files into scientific diagram images. It is intended for workflows where local paper-analysis text can be sent to Gemini for image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local paper-analysis content may be sent to Gemini during diagram generation.

Mitigation: Use the skill only with content approved for third-party processing, and avoid sensitive or unpublished material unless policy permits it.

Risk: Generated files are written under a hard-coded desktop images path and may collide with existing output.

Mitigation: Check the target output directory before running and keep input basenames simple and trusted.

Risk: Browser-driven image generation depends on Gemini availability, UI behavior, and response completion.

Mitigation: Review generated diagrams before use and stop the workflow when an expected state or image output is missing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/m1ss-cell/skills/draw-paper)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [State messages and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved under a fixed local output directory organized by input filename.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
