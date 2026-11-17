## Description:

抖音视频发布。使用浏览器自动化在抖音创作者平台发布视频。当用户说"发布视频到抖音"、"发抖音"时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to guide browser automation for uploading and publishing videos through Douyin Creator Center, including title, hashtag, cover, location, and post-publication checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish publicly from a logged-in Douyin creator account without a clear final confirmation.

Mitigation: Require an explicit final confirmation showing the account, video, title, hashtags, cover, and location before clicking publish.

Risk: The workflow presets the location to Suzhou Center, which may be inaccurate or unwanted for a given post.

Mitigation: Remove or override the preset location unless the publisher explicitly approves that location.

Risk: Repeated publish clicks can create duplicate posts.

Mitigation: Check the Douyin content management page before publishing and stop immediately after a successful publish action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/skills/douyin-video-publish-zhouli)
- [Publisher Profile](https://clawhub.ai/user/onlyloveher)
- [Douyin Creator Video Publish](https://creator.douyin.com/creator-micro/content/post/video?enter_from=publish_page)
- [Douyin Creator Content Management](https://creator.douyin.com/creator-micro/content/manage)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown instructions and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent through browser-based publishing steps; does not produce standalone executable code.]

## Skill Version(s):

1.0.0 (source: release evidence, artifact metadata, skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
