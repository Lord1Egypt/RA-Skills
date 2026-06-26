## Description: <br>
生成包含文本、URL 或 WiFi 信息的二维码图片，支持自定义尺寸、颜色和保存路径。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanxianghua](https://clawhub.ai/user/lanxianghua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to convert text, URLs, or WiFi configuration strings into QR-code image files and save them to a chosen local path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automatically install qrcode and Pillow and can write files to user-provided paths. <br>
Mitigation: Review before installing, prefer pinned dependencies outside the skill runtime, and choose non-sensitive save paths that can be overwritten safely. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanxianghua/fireflylan-qr-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, guidance] <br>
**Output Format:** [Text status message and generated image file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a QR-code PNG file and reports the save path or an error message.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
