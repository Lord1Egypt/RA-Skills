## Description:

ChatBI Skill Test lets an agent call a ChatBI command-line client to run natural-language data queries, stream progress, and extract intent, table selection, SQL, and final answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyukun230](https://clawhub.ai/user/zhangyukun230)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to query registered ChatBI data tables with natural language and receive intent analysis, selected tables, generated SQL, query results, and a final natural-language answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, generated SQL, metadata, and result data may be sent to a default cleartext HTTP endpoint.

Mitigation: Configure a trusted HTTPS ChatBI endpoint before use, and avoid submitting confidential prompts or database results unless the service and transport are approved.

Risk: Built-in account, workspace, room, and table identifiers may point to an unintended environment.

Mitigation: Review and override the ChatBI environment variables or command-line endpoint for the intended workspace before running the skill.

Risk: Raw event exports can contain sensitive prompts, SQL, metadata, and result data.

Mitigation: Use --save-raw only for approved debugging, store those files securely, and delete them when they are no longer needed.

## Reference(s):

- [ChatBI Agent CLI command reference](artifact/references/COMMANDS.md)
- [ClawHub skill page](https://clawhub.ai/zhangyukun230/skills/chatbi-skil-test)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Streaming terminal text with SQL snippets, optional ASCII tables, and optional raw JSON event files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI supports summary, detail, sql-only, and raw output modes; raw event files can include prompts, SQL, metadata, and result data.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
