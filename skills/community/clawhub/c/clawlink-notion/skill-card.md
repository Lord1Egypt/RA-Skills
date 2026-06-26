## Description: <br>
Search pages and databases, update content, and manage Notion workspace data from chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect a Notion workspace through ClawLink, search and read pages or databases, and prepare create, update, or delete operations for user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting a Notion account through ClawLink, which may expose pages and databases available to that connection. <br>
Mitigation: Install only when the user is comfortable with the connected workspace scope and review the active Notion connection before use. <br>
Risk: Create, update, or delete operations can change Notion workspace content. <br>
Mitigation: Preview write actions and require explicit user confirmation before approving changes or deletions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/notion-pages) <br>
- [Notion API Documentation](https://developers.notion.com/) <br>
- [Notion Integration Guide](https://www.notion.so/help/guides) <br>
- [ClawLink](https://claw-link.dev) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ClawLink Notion tools; write operations should be previewed and explicitly confirmed.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
