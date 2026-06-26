## Description: <br>
Automates publishing prepared videos to the Bilibili Creator Center through browser automation, including upload, metadata entry, cover setup, submission, and verification guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnyxu820](https://clawhub.ai/user/Johnnyxu820) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators or operators use this skill to have an agent publish a prepared MP4 video to a logged-in Bilibili account with the desired title, description, category, tags, and cover image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may use a logged-in Bilibili account to publish public content. <br>
Mitigation: Require the agent to show the exact account, file, title, description, category, tags, cover, and final publish action, then wait for explicit user approval before submitting. <br>
Risk: The artifact instructs the agent to append an unrelated forced sentence to the public video description. <br>
Mitigation: Remove or override the forced sentence before publishing and verify the final description shown in the browser. <br>
Risk: Slow Bilibili upload and transcoding can make publication status uncertain and could lead to duplicate submissions. <br>
Mitigation: Check Bilibili draft or submission management after upload and avoid repeat submissions until status is confirmed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Johnnyxu820/bilibili-video-publish) <br>
- [Bilibili Creator Center upload page](https://member.bilibili.com/platform/upload/video/frame?page_from=creative_home_top_upload) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance] <br>
**Output Format:** [Markdown or text instructions for browser automation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Bilibili account, Chrome browser automation through the OpenClaw Chrome extension, a local MP4 video, publishing metadata, and optional cover image input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
