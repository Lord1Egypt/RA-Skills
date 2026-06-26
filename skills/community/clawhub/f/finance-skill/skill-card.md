## Description: <br>
Finance Skill helps an agent parse bank statements, store local transaction records, and answer natural-language spending questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[safaiyeh](https://clawhub.ai/user/safaiyeh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Individuals and agents use this skill to maintain a local personal finance memory layer from bank statements, then query spending by category, merchant, date range, or summary. It is intended for local workflows where the user reviews parsed transaction data before relying on financial summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive bank statements and transaction history on local disk. <br>
Mitigation: Protect the local workspace with normal machine safeguards, review retained data periodically, delete records or statements no longer needed, and use disk encryption where appropriate. <br>
Risk: Parsed financial transactions or summaries may be incomplete or inaccurate if statement extraction misses pages or totals do not match. <br>
Mitigation: Extract full PDFs before parsing, compare imported transaction totals with the statement total, and review parsed transactions before relying on summaries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/safaiyeh/finance-skill) <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON transaction records and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores transaction data and raw statements under ~/.openclaw/workspace/finance when used as documented.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
