## Description: <br>
Publishes user-confirmed videos to Douyin through browser automation, including titles, descriptions, topic tags, and optional cover handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Viv888-AI](https://clawhub.ai/user/Viv888-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to prepare and publish a video post to Douyin after confirming the video, title, description, tags, and optional cover. It can also open the browser for login or publishing checks without posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing through the skill can create real posts on a Douyin creator account. <br>
Mitigation: Require explicit confirmation of the exact video, title, description, tags, and cover before running the publishing command. <br>
Risk: The browser automation stores Douyin login state in a local persistent profile. <br>
Mitigation: Use the skill only on trusted machines and remove the saved browser profile when continued account access is no longer desired. <br>
Risk: Video URLs may be downloaded locally before upload. <br>
Mitigation: Use trusted local files or trusted URLs only, and avoid publishing media whose source or rights are unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Viv888-AI/douyin-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/Viv888-AI) <br>
- [Douyin Creator Platform](https://creator.douyin.com/) <br>
- [Douyin Creator Upload Page](https://creator.douyin.com/creator-micro/content/upload) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and concise success or failure status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch a Playwright browser session, reuse a local Douyin login profile, download a video URL to local storage, and publish only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
