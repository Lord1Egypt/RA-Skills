## Description:

Guides an agent through a browser-based Doubao workflow to create a single AI image from a user-provided prompt, confirm candidate images with the user, and save the selected result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, designers, and individual users use this skill to generate a single Doubao image from a text prompt, review candidates, and save the chosen image. It is suited to lightweight social-media imagery, design inspiration, and AI drawing practice rather than deterministic or high-stakes decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's broad trigger and generic automation, file, API, and command claims could cause an agent to apply it outside its intended Doubao image-generation workflow.

Mitigation: Use the skill only for explicit Doubao image-generation tasks and scope browser, file, and command authority to the minimum needed by the platform.

Risk: The workflow downloads and copies generated image files, which can place files in unexpected locations if the save path is unclear.

Mitigation: Confirm the destination directory with the user before copying or saving generated images.

Risk: Prompts are submitted to the external Doubao service during browser-based generation.

Mitigation: Avoid including secrets, credentials, or sensitive personal data in prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/doubao-image-gen-tool-free)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with workflow steps and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one selected image file after user confirmation; default aspect ratio is 3:4 and batch generation is out of scope.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
