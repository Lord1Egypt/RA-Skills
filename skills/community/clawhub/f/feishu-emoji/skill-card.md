## Description: <br>
Enables an OpenClaw agent to send inline emoji images in Feishu chats by downloading public emoji images into the OpenClaw media directory and sending them with the message tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DearChenzj](https://clawhub.ai/user/DearChenzj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and Feishu workspace participants use this skill to enrich chat replies with inline emoji images for lightweight confirmations, reactions, and informal conversation. It is not intended for formal documents, sensitive chats without review, or commercial reuse of scraped emoji images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches images from third-party sites before sending them into Feishu chats. <br>
Mitigation: Use known image sources and review the selected image and message before sending in sensitive chats. <br>
Risk: Downloaded emoji files are stored in the OpenClaw media folder and can accumulate over time. <br>
Mitigation: Periodically clean the media directory and avoid retaining images that are no longer needed. <br>
Risk: Scraped emoji images may have copyright or usage restrictions. <br>
Mitigation: Avoid commercial reuse of scraped images unless rights are confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DearChenzj/feishu-emoji) <br>
- [Publisher profile](https://clawhub.ai/user/DearChenzj) <br>
- [fabiaoqing.com emoji source](https://fabiaoqing.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional Python helper usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local media file paths and message tool call guidance for sending Feishu inline images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
