## Description: <br>
Publish social media posts to multiple platforms at once, including Facebook, Instagram, Threads, YouTube, TikTok, and X. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to prepare, adapt, publish, schedule, and report on cross-platform social media posts through Boring's MCP connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local media files may be transmitted to Boring's cloud service and potentially stored or hosted there. <br>
Mitigation: Upload only files intended for publication, avoid private or sensitive media, and review Boring's retention and sharing behavior before use. <br>
Risk: The MCP connector link contains an embedded authentication token with publish access to connected social accounts. <br>
Mitigation: Treat the connector link like a password, do not share it publicly, and revoke or regenerate it if exposure is suspected. <br>


## Reference(s): <br>
- [Boring MCP setup documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [ClawHub skill page](https://clawhub.ai/snoopyrain/boring-social-media-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration guidance] <br>
**Output Format:** [Markdown and tool-call guidance with publication status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include platform-specific content adaptations, scheduled publish times, post IDs, and failure reasons.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
