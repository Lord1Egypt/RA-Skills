## Description: <br>
Generates AI images through the Doubao web interface using browser automation, then saves and can deliver the selected images to a requested destination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanxi-ju](https://clawhub.ai/user/fanxi-ju) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to produce visual assets from prompts when API-based image generation is unavailable or too costly, then save or send the selected images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation against Doubao may be subject to service limits or terms, especially when behavior is designed to avoid bot detection. <br>
Mitigation: Check whether the intended use is allowed by the service, use only authorized accounts and workloads, and stop if the service blocks automation. <br>
Risk: Prompts, generated images, or saved files may be sent to external destinations such as Feishu or another requested channel. <br>
Mitigation: Avoid sensitive prompts or images, review generated content before delivery, and confirm the exact destination before sending. <br>
Risk: Saved images can persist in /workspace/ai_images/doubao/ after use. <br>
Mitigation: Delete files that are no longer needed and follow the user's or organization's retention requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fanxi-ju/doubao-ai-image) <br>
- [Doubao web interface](https://www.doubao.com/chat/) <br>


## Skill Output: <br>
**Output Type(s):** [files, guidance] <br>
**Output Format:** [Markdown instructions with browser actions and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved under /workspace/ai_images/doubao/ and may be sent to a specified destination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
