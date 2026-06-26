## Description: <br>
Import ChatGPT conversation history into OpenClaw's memory search. Use when migrating from ChatGPT, giving OpenClaw access to old conversations, or building a searchable archive of past chats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samdickson22](https://clawhub.ai/user/samdickson22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to convert exported ChatGPT conversations into Markdown, embed them into an OpenClaw-compatible SQLite memory database, and configure OpenClaw to search that archive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private ChatGPT conversation data and sends conversation text to OpenAI for embeddings. <br>
Mitigation: Review and remove secrets, personal data, regulated content, or confidential business material before embedding. <br>
Risk: Embedding requires an OpenAI API key and may incur API cost. <br>
Mitigation: Use a limited API key where possible, estimate cost before running large imports, and protect key material outside the generated database. <br>
Risk: Exported conversation files and the generated SQLite database may contain sensitive historical chat content. <br>
Mitigation: Protect, back up, or delete exported files and generated databases according to the user's privacy and retention requirements. <br>


## Reference(s): <br>
- [How to Export Your ChatGPT Data](references/export-guide.md) <br>
- [ChatGPT export portal](https://chat.openai.com) <br>
- [OpenAI embeddings API endpoint](https://api.openai.com/v1/embeddings) <br>
- [ClawHub release page](https://clawhub.ai/samdickson22/chatgpt-import) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration, Files] <br>
**Output Format:** [Markdown guidance with bash and YAML examples; generated Markdown files and an SQLite database] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ChatGPT conversations.json export and an OpenAI API key; sends conversation text to the OpenAI embeddings API and refuses to overwrite an existing output database.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
