## Description: <br>
Research and solve "how do I do this?" questions inside accounting and finance software systems (ERP, GL, AP/AR, billing, close, and reporting tools). Use when a user needs operational steps, setup guidance, or troubleshooting help in a specific system and wants the result documented as a quick memo or simple Q-and-A DOCX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChipmunkRPA](https://clawhub.ai/user/ChipmunkRPA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance operations users, consultants, and system administrators use this skill to research how-to and troubleshooting questions in accounting and finance systems, then document source-backed operational steps as a quick memo or simple Q-and-A DOCX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Accounting-system guidance may be incorrect, stale, or mismatched to the user's exact system version and permissions. <br>
Mitigation: Prefer current official vendor documentation, capture accessed dates, separate assumptions from source-backed guidance, and review cited sources before applying recommendations. <br>
Risk: Applying recommendations directly in production finance systems can affect accounting records, workflows, approvals, or reporting. <br>
Mitigation: Use the skill as research and documentation support, not as authority to make live accounting changes; obtain appropriate finance or system-administrator approval before implementation. <br>
Risk: Users may expose credentials, sensitive transaction details, or other confidential finance data during troubleshooting. <br>
Mitigation: Avoid giving the agent credentials or sensitive transaction details; use sanitized examples and only the minimum context needed to answer the workflow question. <br>
Risk: The optional DOCX generator depends on an external Python package. <br>
Mitigation: Install python-docx only from a trusted package source and inspect generated documents before distribution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ChipmunkRPA/accounting-finance-system-skill) <br>
- [Clarification Question Bank](artifact/references/clarification-question-bank.md) <br>
- [Source Priority And Evidence Rules](artifact/references/source-priority.md) <br>
- [Report JSON Schema](artifact/references/report-json-schema.md) <br>
- [Example Report Payload](artifact/references/example_report_input.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance and structured JSON used to generate a DOCX report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports quick memo and simple Q-and-A deliverables; DOCX generation requires python-docx from a trusted package source.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
