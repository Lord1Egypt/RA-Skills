## Description: <br>
Helps agents configure Feishu/Lark credentials and bot routing, then read, create, append, and edit Docx, Sheets, Base, Wiki, Drive, and IM content through Feishu OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luz404](https://clawhub.ai/user/luz404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an OpenClaw agent to Feishu/Lark, manage app and OAuth credentials, and perform document, spreadsheet, Base, Wiki, Drive, and IM operations through API-backed tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Feishu/Lark app credentials and OAuth tokens that can access or modify cloud content. <br>
Mitigation: Use minimum required Feishu scopes, keep .env and token files private, and avoid storing tokens inside shared project folders. <br>
Risk: Write operations can change documents, sheets, Base records, wiki/drive content, or IM messages. <br>
Mitigation: Require explicit confirmation before replace, delete-like, Base schema or record, and message-sending actions; read before writing and verify after writing. <br>
Risk: User refresh tokens are single-use and can be invalidated if refreshed incorrectly. <br>
Mitigation: Persist both the new user access token and new refresh token immediately after refresh, using Feishu response expiry fields as the source of truth. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/luz404/feishu-clouddoc-api) <br>
- [Audited Interfaces](references/interfaces.md) <br>
- [Operations](references/operations.md) <br>
- [Setup](references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Feishu/Lark app credentials and optional user OAuth tokens supplied outside the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
