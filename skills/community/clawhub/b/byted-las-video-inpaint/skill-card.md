## Description:

Removes unwanted visual elements from videos using AI-powered inpainting through Volcengine LAS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video workflow operators use this skill to submit Volcengine LAS video inpainting jobs for removing fixed visual overlays such as watermarks, subtitles, logos, text, and other obstructing regions.

### Deployment Geography for Use:

Volcengine LAS regions documented by the skill: cn-beijing and cn-shanghai.

## Known Risks and Mitigations:

Risk: Videos and metadata are sent to Volcengine LAS/TOS for processing.

Mitigation: Use the skill only for content approved for Volcengine processing and confirm the selected LAS region and TOS bucket meet the user's data handling requirements.

Risk: The environment setup can install SDK code from a remote wheel.

Mitigation: Review the remote SDK installation path before running setup and execute it only in a controlled environment.

Risk: Credentials may be exposed if stored in project-local plaintext files.

Mitigation: Supply short-lived, least-privileged credentials through a secure environment mechanism and avoid plaintext key files in the project directory.

Risk: The background polling script can continue running without a built-in timeout.

Mitigation: Run background polling only with external timeout or cancellation controls and monitor task output directories.

## Reference(s):

- [las_video_inpaint API reference](references/api.md)
- [Pricing reference](references/prices.md)
- [Volcengine LAS pricing](https://www.volcengine.com/docs/6492/1544808)
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-las-video-inpaint)
- [Publisher profile](https://clawhub.ai/user/volcengine-skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with JSON examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides asynchronous submit and poll workflows, price estimation, credential checks, and result reporting for Volcengine LAS video inpainting.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
