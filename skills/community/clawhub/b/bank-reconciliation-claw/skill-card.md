## Description: <br>
银行流水对账虾 reconciles bank statement, order, and invoice data locally and generates match summaries, detail sheets, and exception reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance operators and agents use this skill to reconcile uploaded Excel or CSV bank statements against order and invoice exports, identify unmatched records, duplicates, amount differences, and date offsets, and generate a local reconciliation report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The preview command can print raw financial rows to the terminal or agent transcript. <br>
Mitigation: Use preview only on files whose contents are acceptable to expose in the local terminal session, and avoid it for highly sensitive datasets. <br>
Risk: Generated reconciliation reports may contain financial records and exception details. <br>
Mitigation: Review reports before sharing or exporting them, and apply the documented desensitization rules where display or collaboration copies are needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tujinsama/bank-reconciliation-claw) <br>
- [Reconciliation rules](references/reconciliation-rules.md) <br>
- [Field mapping](references/field-mapping.md) <br>
- [Desensitization rules](references/desensitization-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files] <br>
**Output Format:** [Markdown guidance with shell commands, terminal summaries, and generated Excel reconciliation reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local Excel/CSV inputs; preview output can print raw financial rows to the terminal.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
