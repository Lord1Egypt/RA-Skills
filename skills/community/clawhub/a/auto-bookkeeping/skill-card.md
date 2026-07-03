## Description: <br>
智能自动记账 helps an agent parse natural-language bookkeeping requests, store local SQLite ledger entries, query records, and generate monthly HTML spending reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and agents use this skill to turn short expense or income phrases into structured bookkeeping records, review monthly ledger summaries, search entries, delete mistaken records, and create local visual reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can record, reveal, report, and delete personal financial data from broad conversational triggers. <br>
Mitigation: Use explicit bookkeeping commands, review parsed entries before saving, and confirm delete or report actions before executing them. <br>
Risk: Automatically saved entries may be incorrect when amount, date, category, or transaction type parsing is uncertain. <br>
Mitigation: Show the parsed entry to the user and require confirmation whenever confidence is low or any required value is missing. <br>
Risk: The artifact references Python scripts that are not included, so bookkeeping, deletion, and report flows may fail or behave differently after local repair. <br>
Mitigation: Verify the installed files before use and add backups or dry-run checks before relying on delete and report workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, files] <br>
**Output Format:** [Markdown responses with shell commands, JSON parser results, SQLite-backed ledger data, and generated local HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python. The release artifact references parser, bookkeeping, and reporter scripts that were not included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
