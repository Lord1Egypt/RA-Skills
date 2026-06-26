## Description: <br>
Guides an agent to manage personal finances by recording income and expenses, processing statements and card bills, preventing duplicates, and generating monthly and annual summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evandrotho](https://clawhub.ai/user/evandrotho) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual users use this skill to let an agent maintain local personal finance Markdown files, interpret natural-language finance requests, process bank statements or card bills, and produce financial summaries after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal finance records may be stored under workspace/financas. <br>
Mitigation: Install only in workspaces where keeping personal finance records is acceptable. <br>
Risk: Broad finance-related activation triggers may load the skill during unrelated tasks. <br>
Mitigation: Narrow activation triggers if common words such as conta, total, banco, or month names often appear outside finance tasks. <br>
Risk: Parsed statement or card-bill transactions may be misclassified or duplicated. <br>
Mitigation: Review interpreted transactions before confirming and use the skill's duplicate checks based on value, date, and month. <br>


## Reference(s): <br>
- [Finanças Template on ClawHub](https://clawhub.ai/evandrotho/financas-template) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown guidance, finance tables, and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Intended to update local workspace finance records only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
