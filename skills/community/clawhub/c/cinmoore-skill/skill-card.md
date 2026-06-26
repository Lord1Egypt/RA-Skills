## Description: <br>
Cinmoore Skill guides an agent through Cinmoore camera PTZ control, image and video capture, multimodal media analysis, image editing, object localization, Feishu notifications, event detection, and Vlog generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[buaalingming](https://clawhub.ai/user/buaalingming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to control Cinmoore cameras, collect and analyze image or video media, send Feishu updates, monitor custom events, and generate short Vlog outputs from analyzed footage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an unreviewed Python wheel that controls a camera and processes local media. <br>
Mitigation: Install only after independently verifying the wheel and publisher, and review commands before execution. <br>
Risk: The skill uses Feishu and DashScope secrets stored in a local configuration file. <br>
Mitigation: Use least-privilege credentials, protect cinmoore_config.yaml, and rotate credentials if exposed. <br>
Risk: Camera movement, recording, media analysis, and Feishu sharing can expose private footage or notify external recipients. <br>
Mitigation: Require user confirmation before moving the camera, recording footage, analyzing private media, or sending images and videos to Feishu. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/buaalingming/cinmoore-skill) <br>
- [DashScope console](https://dashscope.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Analysis, Media files] <br>
**Output Format:** [Markdown guidance with PowerShell commands, YAML configuration examples, text analysis, images, videos, GIF previews, and Vlog files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python, local cinmoore_config.yaml credentials, Cinmoore camera device configuration, Feishu credentials, and a DashScope API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
