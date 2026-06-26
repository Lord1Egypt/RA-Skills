## Description: <br>
ComfyUI V8 Aki bundle assistant for installation checks, local startup, workflow generation, parameter optimization, troubleshooting, batch generation, and model management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and ComfyUI operators use this skill to inspect a local ComfyUI V8/Aki installation, generate common image workflow JSON, tune runtime parameters, and troubleshoot local setup issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The startup helper can run a local ComfyUI launcher or batch file from the configured bundle path. <br>
Mitigation: Point the skill only at a ComfyUI installation whose files and launcher scripts you trust before using startup commands. <br>
Risk: Generated workflows can overwrite or add files in the configured ComfyUI workflow directory. <br>
Mitigation: Review the workflow save location and keep backups if preserving existing workflows matters. <br>
Risk: InstantID workflows process face images. <br>
Mitigation: Use InstantID only with face images you are allowed to process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smseow001/comfyui-v8) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with JSON workflow snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write ComfyUI workflow JSON files under the configured local ComfyUI workflows directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
