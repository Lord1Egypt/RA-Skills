## Description: <br>
Gajago Sns helps create Korean SNS copy, images, and 20-second videos for Instagram, Facebook, and Band from /가자고 text, keywords, or images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sang-su0916](https://clawhub.ai/user/sang-su0916) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External communications and education-support staff can use this skill to transform source text, keywords, and optional images into channel-specific Korean promotional posts for Instagram, Facebook, and Band. It also supports image and short video asset generation workflows for campaign publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact exposes a Gemini API key. <br>
Mitigation: Remove the key from the skill, rotate the exposed credential, and require users to provide their own secret through environment configuration. <br>
Risk: The skill can run local tools, start a local web app, and rely on fixed personal filesystem paths. <br>
Mitigation: Replace hardcoded personal paths with user-selected inputs, document required dependencies, and require explicit user confirmation before starting local services or opening folders. <br>
Risk: Generated content may be sent externally through Telegram or other publishing workflows. <br>
Mitigation: Require a clear review and confirmation step before sending or publishing any generated copy, image, or video asset. <br>
Risk: The skill references external services and downloadable media. <br>
Mitigation: Declare external service dependencies and network downloads so installers can review data flow, licensing, and operational requirements before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sang-su0916/gajago-sns) <br>
- [Publisher profile](https://clawhub.ai/user/sang-su0916) <br>
- [SoundHelix sample music dependency](https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown instructions with inline shell commands and generated SNS copy, image, video, and text file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates platform-specific copy for Instagram, Facebook, and Band; may create PNG images, MP4 video, and text summaries when supporting tools and local assets are available.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
