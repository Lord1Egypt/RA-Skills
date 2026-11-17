## Description:

Comfyui V8 helps agents support ComfyUI Aki bundle workflows, including environment checks, local startup guidance, workflow JSON generation, parameter tuning, troubleshooting, batch generation, and model management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ComfyUI users use this skill to generate ComfyUI workflow JSON, inspect an Aki bundle installation, tune common generation parameters, and get troubleshooting guidance for local image-generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch local executables from a configurable ComfyUI path.

Mitigation: Install and run it only with a trusted local ComfyUI Aki bundle, verify the configured directory and files before startup actions, and avoid running the launcher with administrator privileges.

Risk: The artifact includes troubleshooting advice to run as administrator or disable antivirus.

Mitigation: Do not disable antivirus based solely on this skill's advice, and prefer normal user privileges while investigating startup failures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smseow001/skills/comfyui-v8)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, and ComfyUI workflow JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write workflow JSON files into the configured ComfyUI workflows directory and may launch a local ComfyUI executable or batch file when startup actions are used.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
