## Description: <br>
Feishu Image Sender helps an agent capture full-screen or selected-area screenshots, process local image files, and send those images to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AndersonHJB](https://clawhub.ai/user/AndersonHJB) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill when they need an agent to share screenshots or selected local image files into a Feishu workspace, including troubleshooting, demonstrations, tutorials, and remote support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots and selected local image files can include sensitive information before being uploaded to Feishu. <br>
Mitigation: Confirm the destination account or chat, review or crop images before sending, and avoid full-screen captures when secrets may be visible. <br>
Risk: Image files are copied locally during processing and may remain in workspace or temporary locations. <br>
Mitigation: Prefer versions or configurations that use temporary files, clean them up after sending, and limit copied images to the minimum needed. <br>
Risk: The security guidance flags a python -c path interpolation issue in the send path. <br>
Mitigation: Use a version that fixes path interpolation before handling untrusted or sensitive file paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AndersonHJB/feishu-image-sent) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Improved artifact SKILL.md](artifact/improved/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may invoke macOS screenshot commands, copy images into a workspace directory, optionally compress large images, and send one or more image versions to Feishu.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
