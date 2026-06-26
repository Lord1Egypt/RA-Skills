## Description: <br>
Query Feishu Bitable tables with server-side filters, sorting, field selection, pagination, and JSON, JSONL, or TSV output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deadblue22](https://clawhub.ai/user/deadblue22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to query large Feishu Bitable tables efficiently when they need server-side filtering, full pagination, field selection, or pipe-friendly output formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script reads Feishu app credentials already stored in ~/.openclaw/openclaw.json. <br>
Mitigation: Install and run it only in environments where that credential use is intended, and configure the Feishu app with least-privilege permissions. <br>
Risk: Broad filters or --all-pages can export more Bitable records than intended. <br>
Mitigation: Verify each app-token, table-id, filter, and output destination before running queries, and avoid full-table pagination unless a full export is needed. <br>


## Reference(s): <br>
- [Filter Syntax Reference](references/filter-syntax.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/deadblue22/feishu-bitable-query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON, JSONL, or TSV command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports count-only output, compact field formatting, pagination progress on stderr, and query results on stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
