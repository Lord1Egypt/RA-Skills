## Description: <br>
抖音视频发布。使用浏览器自动化在抖音创作者平台发布视频。当用户说"发布视频到抖音"、"发抖音"时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agent operators use this skill to publish a prepared local video to a logged-in Douyin creator account, including upload, title, hashtags, cover selection, location, and post-publication verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish video content from a logged-in Douyin creator account. <br>
Mitigation: Require the agent to show the exact account, video, title, hashtags, cover, visibility settings, and location before any publish action, and require explicit final approval. <br>
Risk: The workflow always selects the fixed location "苏州中心". <br>
Mitigation: Remove or change the location unless the operator intentionally wants that location attached to the post. <br>
Risk: Repeated publish clicks could create duplicate posts. <br>
Mitigation: Confirm the target video is not already present in content management before publishing and stop immediately after a successful publish. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/douyin-video-publish-zhouli) <br>
- [Douyin creator video publish page](https://creator.douyin.com/creator-micro/content/post/video?enter_from=publish_page) <br>
- [Douyin creator content management page](https://creator.douyin.com/creator-micro/content/manage) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown instructions for browser automation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Douyin creator account and a browser automation session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
