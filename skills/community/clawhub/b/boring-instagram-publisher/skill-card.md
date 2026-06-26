## Description: <br>
Publishes or schedules Instagram photos, carousels, and Reels through Boring for connected Instagram Business or Creator accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to prepare, publish, schedule, list, and cancel Instagram posts through a Boring MCP connector. It is intended for workflows where the user has connected an Instagram Business or Creator account and has media ready for publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP Connector link contains an embedded authentication token that can authorize Instagram publishing actions. <br>
Mitigation: Keep the connector link private, treat it like a password, and regenerate it if exposed. <br>
Risk: The skill can publish, schedule, or cancel public Instagram content through Boring. <br>
Mitigation: Confirm the Instagram account, media, caption, and scheduled time before taking publishing or cancellation actions. <br>
Risk: Local files or external media may be uploaded to Boring-hosted storage so Instagram can access them. <br>
Mitigation: Use only media intended for publication and avoid uploading private or sensitive files. <br>


## Reference(s): <br>
- [Boring MCP setup documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [Boring documentation](https://boring-doc.aiagent-me.com) <br>
- [Boring application](https://boring.aiagent-me.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown with tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Instagram post IDs, scheduled times, and confirmation or error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
