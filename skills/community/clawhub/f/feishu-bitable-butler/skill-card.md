## Description: <br>
飞书多维表格 AI 管家自动化飞书 Bitable 的数据清洗、批量录入、报表生成、字段管理和智能摘要。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[young-joey](https://clawhub.ai/user/young-joey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to inspect Feishu Bitable structure, batch read or write records, clean table data, generate reports, and manage fields. It is suited for business tables such as customer follow-up, weekly reports, sales funnels, and employee information workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad read/write access to Feishu Bitable can expose or alter business, customer, or employee data. <br>
Mitigation: Limit the Feishu app to the required bases and tables, preview bulk reads/writes and field changes, and require explicit approval before modifying production data. <br>
Risk: Generated summaries or reports may disclose sensitive table contents in chat channels. <br>
Mitigation: Confirm the audience and destination before sharing summaries, and avoid sending customer or employee data unless explicitly approved. <br>
Risk: Incorrect app_token, table_id, or field mapping can write to the wrong table or corrupt records. <br>
Mitigation: Follow the skill's structure-first workflow: parse metadata, list fields, sample records, and verify writes with record lookups. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/young-joey/feishu-bitable-butler) <br>
- [Field types reference](references/field-types.md) <br>
- [Common scenarios examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, API Calls] <br>
**Output Format:** [Markdown guidance with Feishu Bitable tool-call sequences, structured summaries, and report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct agents to read, create, update, and summarize Feishu Bitable records after confirming table structure.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
