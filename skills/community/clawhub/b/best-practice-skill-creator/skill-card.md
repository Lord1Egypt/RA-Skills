## Description: <br>
Create OpenClaw skills from best practice videos or image sequences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diffusefuturetech](https://clawhub.ai/user/diffusefuturetech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation authors use this skill to turn workflow videos, screenshot sequences, and task descriptions into OpenClaw-compatible skill directories for review, installation, or publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Videos, screenshots, and task descriptions are sent to configured external multimodal model endpoints. <br>
Mitigation: Use only non-sensitive inputs unless the configured provider and endpoint are approved for the data being processed. <br>
Risk: The artifact includes an embedded API key and under-disclosed external model endpoint configuration. <br>
Mitigation: Replace the bundled API configuration with trusted provider settings and do not use the embedded key. <br>
Risk: Generated SKILL.md output may contain inaccurate steps, unsafe commands, or unsuitable publishing metadata. <br>
Mitigation: Manually review and scan every generated skill before installing, using, or publishing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diffusefuturetech/best-practice-skill-creator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Generated skill directory containing SKILL.md markdown and OpenClaw metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes video frames or screenshots with a configured multimodal model provider before writing the generated skill files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
