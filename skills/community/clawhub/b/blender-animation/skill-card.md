## Description:

Generate and render 3D animations using Blender headless mode, including scene setup, object and camera animation, lighting, and output to MP4 video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vignesh8164](https://clawhub.ai/user/vignesh8164)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical artists use this skill to generate Blender Python scenes, run Blender headlessly, and return rendered MP4 animations, scripts, and logs for controlled 3D animation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runner can execute a caller-supplied Blender Python script with Blender process permissions.

Mitigation: Use a contained runtime with limited filesystem access, no sensitive credentials, resource limits, and a fixed validated script path when handling untrusted prompts or files.

Risk: The documentation claims stronger execution limits than the runner enforces.

Mitigation: Review generated Blender scripts before execution and enforce filesystem, network, and duration constraints through the surrounding sandbox or container.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vignesh8164/skills/blender-animation)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Blender Python code, file paths, and execution logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce /tmp/blender_script.py and /tmp/output.mp4 when executed in a configured Blender environment.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact/SKILL.md version note)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
