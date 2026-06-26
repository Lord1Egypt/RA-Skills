## Description: <br>
Puppeteer-based Douyin Creator Platform automation for logging in, checking session status, and uploading or publishing videos from local command-line scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chongjie-ran](https://clawhub.ai/user/chongjie-ran) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent operators use this skill to automate Douyin Creator Platform login management and video uploads with title, description, tag, draft, and publish controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved Douyin cookies and browser session data can allow account access if the skill directory is exposed. <br>
Mitigation: Keep the skill directory private and run the clear command when the saved Douyin session is no longer needed. <br>
Risk: Uploads publish by default, which can post unintended content to the connected Douyin account. <br>
Mitigation: Use the draft option for review workflows and verify the video, title, description, and tags before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chongjie-ran/douyin-automation) <br>
- [Project homepage](https://github.com/lancelin111/douyin-mcp-server) <br>
- [Publisher profile](https://clawhub.ai/user/chongjie-ran) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command-line examples and CLI status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Douyin cookie and browser session files; upload defaults to publishing unless the draft option is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter; package.json reports 2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
