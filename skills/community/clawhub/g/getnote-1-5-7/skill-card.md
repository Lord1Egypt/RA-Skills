## Description: <br>
Getnote helps an agent save, search, and manage personal notes and knowledge bases through Get笔记. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackie2010](https://clawhub.ai/user/jackie2010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to let an agent capture links, images, and text as notes, search saved notes semantically, and organize notes with knowledge bases and tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access privacy-sensitive remote note content, links, images, and searches through biji.com. <br>
Mitigation: Install only when the user trusts Get笔记/biji.com with that data, avoid showing private note content in shared chats, and configure GETNOTE_OWNER_ID in shared contexts. <br>
Risk: The skill can perform sensitive note-management actions such as deleting, moving, or changing notes. <br>
Mitigation: Use explicit /note commands for sensitive operations and confirm destructive or reorganizing changes before executing them. <br>
Risk: Stored API credentials authorize access to the user's notes. <br>
Mitigation: Store credentials in configuration or environment variables rather than chat, and revoke the provider API key when the skill is no longer used. <br>


## Reference(s): <br>
- [Getnote ClawHub Page](https://clawhub.ai/jackie2010/getnote-1-5-7) <br>
- [Get笔记 Homepage](https://biji.com) <br>
- [Get笔记 Open Platform](https://www.biji.com/openapi) <br>
- [Get笔记 API Details](references/api-details.md) <br>
- [OAuth Authorization Configuration](references/oauth.md) <br>
- [Save Notes](references/save.md) <br>
- [Semantic Search](references/search.md) <br>
- [Note Lists and Details](references/list.md) <br>
- [Knowledge Base Management](references/knowledge.md) <br>
- [Tag Management](references/tags.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with API request guidance and occasional shell or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Getnote API credentials and may return or modify user note data through biji.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata); package version 1.5.7 (source: package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
