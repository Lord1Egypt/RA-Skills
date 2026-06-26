## Description: <br>
A cross-platform Python toolkit for Doubao and Volcengine ARK APIs that supports text-to-image, image-to-image, text-to-video, image/video analysis, and task management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[systiger](https://clawhub.ai/user/systiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to configure and invoke Doubao/Volcengine ARK media-generation and vision-analysis workflows from Python or shell commands. It helps generate images and videos, analyze image or video inputs, and check asynchronous video task status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, generated-media requests, and selected local video files may be sent to Volcengine/Doubao APIs. <br>
Mitigation: Use only media and prompts that are permitted for third-party API processing; avoid confidential, regulated, proprietary, or third-party content unless permission and policy clearance are in place. <br>
Risk: Local video analysis can encode and transmit a user-selected video file without a separate point-of-use confirmation. <br>
Mitigation: Confirm the intended file, data classification, and user consent before running video analysis, especially in automated workflows. <br>
Risk: The toolkit depends on an ARK API key for authenticated calls. <br>
Mitigation: Store the key in the ARK_API_KEY environment variable, avoid hardcoding it in code or logs, and rotate it regularly. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/systiger/doubao-api-toolkit) <br>
- [Volcengine ARK Documentation](https://www.volcengine.com/docs/82379) <br>
- [Volcengine ARK Console](https://console.volcengine.com/ark) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with bash commands, Python usage, and JSON response examples; runtime commands may return text analysis, task status JSON, or downloaded media file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, the requests package, an ARK_API_KEY environment variable, network access to Volcengine ARK, and user-provided prompts or media inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, SKILL.md frontmatter, and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
