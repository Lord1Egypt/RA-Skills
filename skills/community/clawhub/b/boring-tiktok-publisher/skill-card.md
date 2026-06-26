## Description: <br>
Publish videos and photo carousels to TikTok using Boring. Use when the user says 'post to TikTok', 'upload TikTok video', 'create TikTok post', 'publish TikTok carousel', or wants to upload videos or photo slideshows to TikTok with privacy settings and draft mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and social media operators use this skill to publish TikTok videos or photo carousels through Boring, including draft-mode posts for review before going live. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP Connector link contains an embedded authentication token. <br>
Mitigation: Treat the connector URL as a credential, avoid sharing it publicly, and regenerate it if exposed. <br>
Risk: Publishing can send user media and captions through Boring to TikTok and may post publicly depending on selected privacy settings. <br>
Mitigation: Confirm the account, media, caption, privacy setting, and draft mode before publishing; use draft mode when approval or TikTok-native editing is needed. <br>
Risk: Uploaded media must meet TikTok constraints such as required media, video size, duration, format, and carousel image counts. <br>
Mitigation: Check media requirements before calling publish and surface documented errors such as MediaRequired, MediaTooLarge, TokenExpired, and PublishingFailed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snoopyrain/boring-tiktok-publisher) <br>
- [Boring MCP Connector setup](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [Boring documentation](https://boring-doc.aiagent-me.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with MCP tool-call parameters and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include TikTok account selection, uploaded media URLs, post IDs, success status, draft-mode reminders, privacy choices, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
