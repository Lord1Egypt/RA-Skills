## Description:

Generates cat selfie image files by selecting a random or requested scene and calling the Volcengine Doubao Seedream image-generation workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romanticjojo](https://clawhub.ai/user/romanticjojo)

### License/Terms of Use:

MIT

## Use Case:

Agents and users use this skill to create themed cat selfie images, either randomly or from one of eight configured scenes, and save the generated image in the OpenClaw workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configurable scene prompts can be passed through a shell command, which creates a local command-injection risk if prompts come from untrusted sources.

Mitigation: Review custom scene configuration before use and prefer argument-array execution such as execFileSync or spawnSync when invoking the image-generation script.

Risk: Heartbeat integration can generate and send images automatically if connected to a messaging workflow.

Mitigation: Require explicit confirmation or rate limits before sending generated images and restrict access to the shared images directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romanticjojo/skills/cat-selfie)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG or JPG image files with console status text and image path metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are saved under ~/.openclaw/workspace/images/ with timestamped filenames.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
