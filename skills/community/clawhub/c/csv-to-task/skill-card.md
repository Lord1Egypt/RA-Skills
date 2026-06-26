## Description: <br>
Converts CSV rows into structured, trackable task objects such as Jira-style tickets, Markdown checklists, JSON arrays, or CSV rows with task fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and project teams use this skill to turn pasted CSV or spreadsheet-style rows into one task per row with mapped fields such as title, assignee, priority, due date, status, labels, and description. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CSV input may contain internal names, emails, deadlines, or project details that become visible in generated tasks. <br>
Mitigation: Review generated tasks before importing them into Jira, Linear, Notion, or another task system, and avoid providing unnecessary sensitive columns. <br>
Risk: Incorrect column mapping could create misleading task owners, priorities, dates, or statuses. <br>
Mitigation: Check the mapped fields, row count, and generated task status before using the output as an operational task list. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/csv-to-task) <br>
- [Metadata source: MiniMax-AI skills](https://github.com/MiniMax-AI/skills) <br>
- [Reference index](references/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown checklist, Jira-style text, JSON array, or CSV with added task columns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one task per input CSV row and preserves original row data as task metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and changelog, released 2026-05-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
