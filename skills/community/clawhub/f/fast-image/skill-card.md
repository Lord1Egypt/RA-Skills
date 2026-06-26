## Description: <br>
Quickly send local images to channel. Auto-compress large images, copy small images directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DeadLining](https://clawhub.ai/user/DeadLining) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send local image files to a specified channel and target, with automatic copying for small images and compression for larger images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper sends local image files to external channels. <br>
Mitigation: Use only with intended local files, channels, targets, and message text, and confirm the destination before sending. <br>
Risk: Shell metacharacters in image paths, channel names, targets, or messages can cause unintended local shell command execution. <br>
Mitigation: Avoid untrusted inputs until the helper removes shell:true and validates destination and message arguments. <br>


## Reference(s): <br>
- [Fast Image on ClawHub](https://clawhub.ai/DeadLining/fast-image) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Text] <br>
**Output Format:** [Markdown with inline shell commands and script behavior guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Node.js helper, sharp for compression of images 10MB or larger, and the openclaw CLI to send media.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
