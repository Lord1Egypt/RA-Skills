## Description:

Conducts a Chinese-language six-step departmental budget execution audit workflow covering budget overview, revenue and expenditure analysis, execution progress, public expenses, project spending, and report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rc17777](https://clawhub.ai/user/rc17777)

### License/Terms of Use:

MIT-0

## Use Case:

Audit teams and agents use this skill to coordinate departmental budget execution reviews, including budget execution rates, public expenses, carryover balances, project spending, and audit report preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive government or financial records may be included when using the workflow.

Mitigation: Review data handling requirements before use and limit workflow inputs to records approved for the target audit environment.

Risk: The workflow relies on connected helper skills for data analysis, fraud detection, procurement review, report writing, and document formatting.

Mitigation: Review and approve the connected helper skills before deployment, especially when they process financial or government records.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rc17777/skills/audit-budget-execution)
- [Skill Usage Documentation](artifact/SKILL.md)
- [Workflow Definition](artifact/workflow.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with workflow YAML and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language audit workflow template that depends on pipeline_engine.py and named audit helper skills.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
