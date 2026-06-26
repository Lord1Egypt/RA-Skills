## Description: <br>
Generate high-quality images using Doubao AI image generation for artwork, illustrations, and other visual content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[herry-zhu](https://clawhub.ai/user/herry-zhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate images through a logged-in Doubao browser session, download generated assets, and optionally send image files back to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in Doubao browser session to submit prompts and retrieve generated images. <br>
Mitigation: Use a dedicated browser profile when possible, avoid sensitive prompts, and confirm account/session state before running generation. <br>
Risk: Generated images are saved locally and may be sent through BlueBubbles/iMessage. <br>
Mitigation: Confirm the saved file path and intended recipient before sending attachments. <br>
Risk: Doubao CDN image URLs use time-limited signatures, so direct downloads can fail or produce the wrong asset variant. <br>
Mitigation: Verify the downloaded image before delivery and use the documented browser extraction fallback when direct download fails. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/herry-zhu/doubao-img) <br>
- [Publisher Profile](https://clawhub.ai/user/herry-zhu) <br>
- [Doubao](https://www.doubao.com) <br>
- [Doubao Image Creation](https://www.doubao.com/chat/create-image) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown guidance with browser actions, code snippets, shell commands, and downloaded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local image files downloaded from Doubao and may send them as message attachments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
