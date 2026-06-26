## Description: <br>
Excel Master helps an agent open user-named Excel workbooks, inspect sheet data, filter rows, compute basic column statistics, summarize table dimensions, and save explicit workbook changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zywss](https://clawhub.ai/user/zywss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users working with spreadsheets can use this skill to inspect Excel data, run simple filters and statistics, and write changes back only after an explicit save command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can display spreadsheet contents in the agent conversation. <br>
Mitigation: Open only spreadsheets whose contents are appropriate to share in the current agent session. <br>
Risk: The save command writes changes back to the opened workbook. <br>
Mitigation: Confirm the target file before saving and keep a backup for important workbooks. <br>
Risk: Advertised chart, PDF export, sheet switching, and AI-analysis capabilities are not supported by the reviewed behavior. <br>
Mitigation: Rely only on documented read, filter, statistic, simple analysis, and save behavior until the publisher implements and documents additional features. <br>


## Reference(s): <br>
- [Artifact README](README.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zywss/excel-master) <br>


## Skill Output: <br>
**Output Type(s):** [text, structured data summaries, spreadsheet file writes, guidance] <br>
**Output Format:** [Plain text responses with JSON-formatted table excerpts and summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads spreadsheet files named by the user and writes back to the opened workbook only when save is explicitly requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
