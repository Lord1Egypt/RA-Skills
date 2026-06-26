## Description: <br>
Turns conversations into polished visual summary cards by extracting key ideas, action items, and next steps with Mew.Design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuminliu026](https://clawhub.ai/user/shuminliu026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to condense user-agent conversations into readable visual recap cards for status updates, decisions, takeaways, and next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Mew.Design API key. <br>
Mitigation: Use a dedicated revocable key and replace it if validation or generation behavior looks unexpected. <br>
Risk: Summarized conversation content is sent to Mew.Design for image generation. <br>
Mitigation: Avoid confidential chats unless Mew.Design's data handling is acceptable for the intended use. <br>
Risk: Temporary request JSON may contain summary text. <br>
Mitigation: Keep generated request files in temporary paths and remove them when the workflow is complete. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shuminliu026/chat-summary-card) <br>
- [Chat Summary Image Patterns](references/patterns.md) <br>
- [Mew.Design login](https://mew.design/login) <br>
- [Mew.Design design generation API](https://api.mew.design/open/api/design/generate) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown image link with one-sentence summary; helper scripts also produce JSON request bodies.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Mew.Design API key, validates the key before generation, and sends summarized conversation content to Mew.Design.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
