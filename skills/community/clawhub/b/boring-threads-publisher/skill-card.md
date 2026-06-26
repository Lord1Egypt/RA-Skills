## Description: <br>
Publish posts and threads to Threads (by Meta) using Boring. Use when the user says 'post to Threads', 'create a thread', 'publish thread', 'write a Threads post', 'reply on Threads', or wants to create text posts, photo/video posts, carousels, or multi-post threads on Threads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to publish Threads posts, replies, media posts, carousels, scheduled posts, and multi-post threads through a connected Boring MCP account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Boring MCP connector can publish, reply, upload media, or schedule posts to a connected Threads account. <br>
Mitigation: Require explicit final user confirmation before any post, reply, media upload, or scheduled post is sent. <br>
Risk: The MCP connector link contains an embedded authentication token. <br>
Mitigation: Treat the connector URL like a password, avoid sharing it publicly, and regenerate it if exposed. <br>
Risk: Media and post content are sent through Boring services before publication to Threads. <br>
Mitigation: Use the skill only for content and media that may be processed by Boring and published through the connected Threads account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snoopyrain/boring-threads-publisher) <br>
- [Boring MCP connector documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [Boring API documentation](https://boring-doc.aiagent-me.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown guidance with MCP tool-call examples and publication result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Threads post IDs, thread URLs, scheduling timestamps, media upload handling, and error summaries.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
