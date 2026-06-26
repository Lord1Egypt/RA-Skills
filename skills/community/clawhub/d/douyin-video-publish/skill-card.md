## Description: <br>
Guides an agent using browser automation to publish videos through the Douyin Creator Platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Johnnyxu820](https://clawhub.ai/user/Johnnyxu820) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators or operators with a logged-in Douyin creator account use this skill to upload a video, add title text, hashtags, cover, and location, publish the post, and confirm it appears in content management. <br>

### Deployment Geography for Use: <br>
Global where Douyin Creator Platform access is available <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate a real public Douyin publishing action from a logged-in creator account. <br>
Mitigation: Require the agent to show the final video, title, hashtags, cover, account, and location before publishing, and allow the publish click only after explicit approval. <br>
Risk: The artifact includes a fixed location value of "苏州中心" that may be incorrect for the user's post. <br>
Mitigation: Override or remove the fixed location unless the user specifically wants that location attached. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Johnnyxu820/douyin-video-publish) <br>
- [Douyin Creator video publish page](https://creator.douyin.com/creator-micro/content/post/video?enter_from=publish_page) <br>
- [Douyin Creator content management page](https://creator.douyin.com/creator-micro/content/manage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, browser automation steps] <br>
**Output Format:** [Markdown instructions and checklist-style guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected browser profile and a logged-in Douyin creator account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
