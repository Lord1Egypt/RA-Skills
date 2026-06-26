## Description: <br>
Use OpenClaw's browser control to publish images or videos to Douyin creator platform by uploading a local media file, filling a title, and publishing through the web UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dream007007s](https://clawhub.ai/user/dream007007s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and automation-focused developers use this skill to publish local images or videos to Douyin Creator Center from an already logged-in Chrome session. It is intended for agent-assisted browser publishing where the user supplies the media file and title. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent control of a logged-in Douyin Creator Center browser session with publishing authority. <br>
Mitigation: Use a dedicated Chrome profile or account and verify the media file, title, destination account, and visibility before publishing. <br>
Risk: The workflow includes navigation via JavaScript evaluation to bypass a blocked navigate action. <br>
Mitigation: Review the navigation step carefully, keep it limited to the expected Douyin Creator Center URL, and close Chrome remote debugging after use. <br>
Risk: The artifact workflow clicks publish without documenting a clear final confirmation checkpoint. <br>
Mitigation: Require an explicit user confirmation immediately before the publish click in operational use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dream007007s/browser-douyin-post) <br>
- [Douyin Creator Platform](https://creator.douyin.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with browser tool calls and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Chrome remote debugging, an active Douyin Creator Center login, a local media path, and a title.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
