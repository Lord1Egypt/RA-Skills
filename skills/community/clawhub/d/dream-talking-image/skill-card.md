## Description: <br>
Generate talking videos from images using Talking Image API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hy-1990](https://clawhub.ai/user/Hy-1990) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure Dream/Newport API access and generate talking-video requests from image and audio URLs, including non-human faces such as pets or animated characters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided image and audio URLs may expose private, biometric, regulated, confidential, copyrighted, or signed media to a third-party service. <br>
Mitigation: Use only media URLs appropriate for Dream/Newport processing, avoid sensitive or expiring URLs, and confirm third-party data handling requirements before use. <br>
Risk: The API key can incur provider usage or spending if misused. <br>
Mitigation: Use a provider key with appropriate spending or usage limits and store it only in the configured DREAMTALKINGIMAGE_API_KEY environment setting. <br>
Risk: Long audio inputs may fail or cause memory errors. <br>
Mitigation: Keep audio under the recommended two-minute duration and prefer the documented m4a format when practical. <br>


## Reference(s): <br>
- [Dream Talking Image API Reference](https://api.newportai.com/api-reference/talking-image) <br>
- [DreamAPI Get Started](https://api.newportai.com/api-reference/get-started) <br>
- [Dreamface AI Tools](https://tools.dreamfaceapp.com/home) <br>
- [ClawHub Skill Page](https://clawhub.ai/Hy-1990/dream-talking-image) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DREAMTALKINGIMAGE_API_KEY and user-provided image and audio URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
