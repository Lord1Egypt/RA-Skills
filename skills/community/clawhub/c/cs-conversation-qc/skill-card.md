## Description:

客服会话质检 is a Chinese customer-service conversation QC skill that analyzes exported chat logs, applies configurable scoring rules, masks sensitive data, and produces QC reports with deduction evidence and manual-review items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenobiazizi](https://clawhub.ai/user/zenobiazizi)

### License/Terms of Use:

MIT-0

## Use Case:

Customer-service supervisors, QA reviewers, and operations teams use this skill to review Chinese customer-service conversations from CSV, Excel, or text exports. It helps score conversations against configurable rules, summarize deductions, and separate uncertain findings for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer chat logs may contain private or sensitive personal data.

Mitigation: Process data locally where possible, mask personal data in reports, and avoid sending private conversation content through public feedback channels.

Risk: Automated QC scores may be mistaken for final employee-performance decisions.

Mitigation: Review generated reports before using them for employee assessment, with particular attention to manual-review items and semantic judgments.

Risk: Conversation export formats or ambiguous column meanings can lead to incomplete parsing.

Mitigation: Confirm uncertain column mappings with the user and place unparseable conversations in an unprocessed list instead of scoring them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zenobiazizi/skills/cs-conversation-qc)
- [Default Customer-Service QC Rules](references/rules-default.md)
- [Custom QC Rules Guide](references/rules-guide.md)
- [Sample QC Report](examples/sample-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown report or Excel-style tables with masked evidence and manual-review sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce an Excel workbook when the agent environment supports it; otherwise uses Markdown tables.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
