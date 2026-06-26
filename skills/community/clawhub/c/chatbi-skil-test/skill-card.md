## Description: <br>
ChatBI Agent Skill lets an agent call a ChatBI streaming endpoint from the command line to ask natural-language questions over registered enterprise data tables and extract intent, table selection, SQL, execution details, and final answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyukun230](https://clawhub.ai/user/zhangyukun230) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data analysts use this skill to run ChatBI natural-language data queries from an agent workflow, monitor the streaming execution path, and retrieve selected tables, generated SQL, data previews, and final natural-language answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send enterprise questions and embedded workspace or account context to a configured ChatBI service endpoint. <br>
Mitigation: Install only when the ChatBI service is trusted, use an approved HTTPS endpoint where possible, and configure authorized account and workspace variables before querying data. <br>
Risk: Raw mode and saved raw event logs can contain sensitive query, SQL, table, or result details. <br>
Mitigation: Use raw mode and --save-raw only for approved debugging, protect generated files, and clean them up after use. <br>
Risk: The default configuration includes a production HTTP endpoint and embedded workspace identifiers. <br>
Mitigation: Review and override CHATBI_API_URL, CHATBI_UIN, CHATBI_OWNER_UIN, CHATBI_APP_ID, CHATBI_WORKSPACE_ID, and CHATBI_ROOM_KEY for the intended deployment. <br>


## Reference(s): <br>
- [ChatBI Agent CLI command reference](artifact/references/COMMANDS.md) <br>
- [ClawHub skill page](https://clawhub.ai/zhangyukun230/chatbi-skil-test) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or terminal text with optional SQL and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports summary, detail, sql-only, and raw output modes; streaming usage expects incremental stdout.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
