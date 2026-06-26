## Description: <br>
Douyin is a video upload tool that supports signing in to a Douyin account, uploading videos, and managing login state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lancelin111](https://clawhub.ai/user/lancelin111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, social media operators, and developers use this skill to log in to Douyin Creator Platform, upload video content with titles, descriptions, and tags, and inspect or clear saved local login data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Douyin session cookies are stored in the skill directory and reused for automated login. <br>
Mitigation: Use the skill only on trusted machines and accounts, protect the workspace files, and run the clear command when the session should no longer persist. <br>
Risk: Visible browser sessions grant Douyin pages broad permissions including location, clipboard, camera, and microphone. <br>
Mitigation: Review before installing, run only where those permissions are acceptable, and avoid exposing sensitive clipboard, camera, or microphone data during the session. <br>
Risk: The upload flow can publish content automatically by default. <br>
Mitigation: Use --no-publish when content should be saved as a draft for review before publication. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/lancelin111/douyin-2) <br>
- [Metadata Homepage](https://github.com/lancelin111/douyin-mcp-server) <br>
- [Douyin Creator Platform](https://creator.douyin.com) <br>
- [Douyin](https://www.douyin.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can create local Douyin cookie and Chromium profile files and can save drafts or publish videos through Puppeteer automation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 2.1.0 and package.json reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
