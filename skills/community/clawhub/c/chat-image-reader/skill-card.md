## Description: <br>
Reads and analyzes images from messages across 10+ chat platforms using platform-specific APIs and unified image processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zqy15306762317](https://clawhub.ai/user/zqy15306762317) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to retrieve chat image attachments from supported platforms and pass them to an image analysis workflow for OCR, screenshot review, chart extraction, and general image description. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles chat bot or app credentials that can read messages and download attachments. <br>
Mitigation: Use least-privilege platform scopes, restrict the bot or app to required chats and workspaces, and keep credentials in environment variables or managed secret storage. <br>
Risk: Downloaded chat images can contain sensitive local files or message attachments. <br>
Mitigation: Treat downloaded images as sensitive, store them only in controlled temporary locations, and remove them after analysis when retention is not required. <br>
Risk: Broad direct URL inputs or attachment downloads can retrieve untrusted files. <br>
Mitigation: Limit direct URL use to trusted chat platform URLs or approved domains, and review file type and size before analysis. <br>


## Reference(s): <br>
- [Chat Platform Image API Reference](references/platform-api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zqy15306762317/chat-image-reader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with code blocks and local file-path output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires platform credentials and chat or attachment permissions; downloaded images may be stored temporarily before analysis.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
