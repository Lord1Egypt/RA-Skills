## Description:

Take camera snapshots from the default webcam and save them to disk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can invoke this skill when they want an agent to capture a single image from the default webcam and return the saved local file path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access the default webcam when invoked.

Mitigation: Install and run it only in contexts where webcam capture is expected and authorized.

Risk: Captured images are saved in the current workspace and may be exposed if the destination folder is shared or writable by others.

Mitigation: Use a private working directory and review output paths before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Plain text status with a local image file path and a saved image file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Images are saved locally within the current working directory using safe image extensions.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
