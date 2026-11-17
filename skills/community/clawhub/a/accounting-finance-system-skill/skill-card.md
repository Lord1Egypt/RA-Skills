## Description:

Research and solve "how do I do this?" questions inside accounting and finance software systems (ERP, GL, AP/AR, billing, close, and reporting tools). Use when a user needs operational steps, setup guidance, or troubleshooting help in a specific system and wants the result documented as a quick memo or simple Q-and-A DOCX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chipmunkrpa](https://clawhub.ai/user/chipmunkrpa)

### License/Terms of Use:

MIT-0

## Use Case:

Finance operations users, consultants, and developers use this skill to research accounting or finance system how-to and troubleshooting questions, confirm assumptions, and produce a cited DOCX memo or Q&A deliverable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned local dependency installation can make DOCX generation vary across environments.

Mitigation: Use a virtual environment and pin python-docx before running the generator.

Risk: Accounting system guidance may affect production finance workflows if assumptions or sources are wrong.

Mitigation: Review assumptions, cited source links, permissions, and validation checks before applying steps in production systems.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chipmunkrpa/skills/accounting-finance-system-skill)
- [Publisher Profile](https://clawhub.ai/user/chipmunkrpa)
- [Clarification Question Bank](references/clarification-question-bank.md)
- [Source Priority And Evidence Rules](references/source-priority.md)
- [Report JSON Schema](references/report-json-schema.md)
- [Example Report Input](references/example_report_input.json)
- [Oracle NetSuite Documentation](https://docs.oracle.com/en/cloud/saas/netsuite)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with structured JSON input and generated DOCX deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before web research; DOCX generation depends on python-docx.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
