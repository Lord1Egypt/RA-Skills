## Description:

Query Feishu Bitable (多维表格) with server-side filter, sort, field selection, and multiple output formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadblue22](https://clawhub.ai/user/deadblue22)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to query Feishu Bitable records with server-side filters, sorting, pagination, selected fields, and compact output when built-in record listing is too broad or inefficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve organizational Feishu Bitable data using locally stored Feishu app credentials.

Mitigation: Install and run it only in environments authorized to use those credentials, and treat returned records as organizational data.

Risk: Broad queries or full pagination can retrieve more records or fields than needed.

Mitigation: Use explicit app tokens, table IDs, filters, view IDs, field selections, compact fields, and count mode to limit data retrieval to the required records.

Risk: Local time filtering runs after records are fetched, so it may still pull records before narrowing the result set.

Mitigation: Prefer server-side filters where possible, especially structured JSON filters for date ranges, and reserve local time filters for cases where Feishu API filter behavior requires them.

## Reference(s):

- [Feishu Bitable Filter Syntax Reference](references/filter-syntax.md)
- [ClawHub skill page](https://clawhub.ai/deadblue22/skills/feishu-bitable-query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, JSONL, TSV]

**Output Format:** [Markdown guidance with bash examples; the helper script can emit JSON, JSONL, or TSV query results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Feishu app credentials from ~/.openclaw/openclaw.json and writes progress to stderr while keeping query results on stdout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
