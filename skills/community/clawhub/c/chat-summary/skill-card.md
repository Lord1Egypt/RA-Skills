## Description: <br>
Chat Summary organizes chat records and conversation history into topic-clustered structured summaries with multilingual support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GaryYinClaw](https://clawhub.ai/user/GaryYinClaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to summarize daily discussions, meeting conversations, long chats, and multi-topic archives into concise topic-based notes. It supports local Markdown or plain-text output and optional Notion export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads chat content selected for summarization, which can expose private or sensitive conversation data. <br>
Mitigation: Use it only on chats appropriate for summarization, keep sensitive exports local by default, and avoid processing confidential or regulated content without approval. <br>
Risk: Optional Notion export or translation services can send summaries or source-derived content to external services. <br>
Mitigation: Review summaries before saving, use a limited Notion integration for export, and avoid third-party translation providers for confidential or regulated content unless approved. <br>


## Reference(s): <br>
- [Chat Summary ClawHub Page](https://clawhub.ai/GaryYinClaw/chat-summary) <br>
- [Clustering Rules](references/clustering-rules.md) <br>
- [Notion API Guide](references/notion-api.md) <br>
- [Translation Integration Guide](references/translation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, api calls, guidance] <br>
**Output Format:** [Markdown, plain text, or Notion page content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Topic count and summary length are configurable by scenario; output language can follow the source language or be user-selected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
