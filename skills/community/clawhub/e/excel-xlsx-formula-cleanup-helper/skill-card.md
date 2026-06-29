## Description: <br>
Diagnoses and helps fix Microsoft Excel XLSX workbook issues involving formulas, named ranges, Power Query refreshes, pivot tables, VBA/macro preservation, workbook corruption, and repeatable data cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, finance and operations teams, spreadsheet-heavy small businesses, and developers use this skill to diagnose Excel workbook failures and plan non-destructive repairs for formulas, ranges, Power Query, pivots, macros, corruption, and recurring data cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive financial or business spreadsheets could be changed incorrectly if originals are edited directly. <br>
Mitigation: Work on copies, review proposed changes, and validate repaired workbooks before replacing originals. <br>
Risk: Broad trigger wording could cause the skill to be invoked for spreadsheet tasks where workbook repair guidance is not intended. <br>
Mitigation: Narrow the trigger wording before deployment or invoke the skill explicitly for Excel workbook inspection and repair tasks. <br>
Risk: Formula, pivot, macro, or query changes can alter workbook business logic. <br>
Mitigation: Keep formulas and package structures intact where possible, preserve macros unless removal is requested, and verify sheets, ranges, tables, pivots, and recalculation requirements. <br>


## Reference(s): <br>
- [Requirement Plan](artifact/references/requirement-plan.md) <br>
- [Excel SQL Query Discussion](https://segmentfault.com/q/1010000042660742/a-1020000042660744) <br>
- [Power Query Multi-Table Connection Guide](https://segmentfault.com/a/1190000046365752) <br>
- [Excel Reading with Qt C++ Discussion](https://segmentfault.com/q/1010000009431251/a-1020000009437423) <br>
- [openpyxl Column Count Discussion](https://segmentfault.com/q/1010000023905216/a-1020000023905711) <br>
- [openpyxl Strikethrough Reading Discussion](https://segmentfault.com/q/1010000020612541/a-1020000020616533) <br>
- [openpyxl 3.0.3 Chinese Manual](https://segmentfault.com/a/1190000022195748) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with optional code blocks, shell commands, and validation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include workbook diagnoses, non-destructive repair plans, automation snippets, and validation checklists.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
