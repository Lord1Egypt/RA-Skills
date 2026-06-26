## Description: <br>
Get笔记 helps an agent save, search, and manage a user's personal notes, tags, and knowledge bases through the Getnote API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horisony](https://clawhub.ai/user/horisony) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to save links, images, and text as Getnote notes; search private notes or knowledge bases; and manage note metadata such as tags and collections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to private notes and supports delete and public-share actions without strong confirmation safeguards. <br>
Mitigation: Install only when the publisher and Getnote are trusted, and require confirmation of the exact note title or ID before updates, deletion, image upload, or public share-link creation. <br>
Risk: The skill uses sensitive Getnote credentials and may be used in shared or group contexts. <br>
Mitigation: Configure GETNOTE_OWNER_ID where multiple users may interact with the agent, and deny note operations when the sender does not match the configured owner. <br>


## Reference(s): <br>
- [Getnote Homepage](https://biji.com) <br>
- [Getnote OpenAPI Base URL](https://openapi.biji.com) <br>
- [Getnote API Details](references/api-details.md) <br>
- [Save Notes](references/save.md) <br>
- [Search Notes](references/search.md) <br>
- [List and Manage Notes](references/list.md) <br>
- [Tags](references/tags.md) <br>
- [OAuth Configuration](references/oauth.md) <br>
- [Knowledge Base Management](references/knowledge.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with API request details and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Getnote note IDs, search results, update confirmations, deletion confirmations, upload steps, or share-link results depending on the user request.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
