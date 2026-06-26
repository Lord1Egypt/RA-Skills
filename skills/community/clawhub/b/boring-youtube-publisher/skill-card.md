## Description: <br>
Upload videos and Shorts to YouTube using Boring with support for titles, descriptions, tags, thumbnails, and captions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators use this skill to publish videos or Shorts to a connected YouTube channel through Boring, including metadata, thumbnails, and captions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP Connector URL contains an embedded authentication token. <br>
Mitigation: Keep the connector URL private, treat it like a password, and regenerate it if it may have been exposed. <br>
Risk: The skill can publish videos publicly to YouTube through Boring. <br>
Mitigation: Verify the target channel, title, description, media, thumbnail, captions, and desired visibility before publishing. <br>
Risk: Video and thumbnail files may be uploaded or re-hosted so YouTube can access them. <br>
Mitigation: Confirm the media is appropriate to share with Boring and to make accessible for the upload workflow. <br>


## Reference(s): <br>
- [Boring MCP documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [Boring documentation](https://boring-doc.aiagent-me.com) <br>
- [ClawHub skill listing](https://clawhub.ai/snoopyrain/boring-youtube-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration, text] <br>
**Output Format:** [Markdown guidance with MCP tool-call examples and publishing status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a private MCP Connector link and a connected YouTube account.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
