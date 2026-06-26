## Description: <br>
检索日记与会话内容，支持中文分词、BM25搜索、时间衰减排序。可搜索日记、查找历史对话（含归档）、导出会话记录（自动过滤噪音，3天后自动清理）、查询定时任务运行记录。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebrinass](https://clawhub.ai/user/sebrinass) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to search diary files, historical conversation sessions, exported conversations, and cron run records across local OpenClaw data. It is intended for personal knowledge retrieval and session review where the user controls access to the underlying memory and session directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads private diary files, historical session transcripts, cron run records, and OpenClaw configuration paths. <br>
Mitigation: Install it only in environments where the user is comfortable granting access to those local OpenClaw files and directories. <br>
Risk: The cleanup tool can delete checkpoint backup files from session directories when run with deletion enabled. <br>
Mitigation: Review the dry-run output first and proceed with deletion only after explicit user confirmation. <br>
Risk: Exported session records may contain sensitive conversation content. <br>
Mitigation: Store exported markdown files in the intended exports directory and rely on the documented automatic cleanup period or remove them manually when no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sebrinass/diary-search) <br>
- [npm package: diary-search](https://www.npmjs.com/package/diary-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with optional shell commands and exported markdown session files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include diary entries, session excerpts, cron run summaries, statistics, or cleanup previews depending on the selected tool.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
