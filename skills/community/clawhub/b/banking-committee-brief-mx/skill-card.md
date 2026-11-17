## Description:

Generates an executive banking risk committee brief for Mexico from CNBV indicators and market context received through Telegram, returning a structured PDF ready for committee review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardo-mendoza-rodriguez](https://clawhub.ai/user/ricardo-mendoza-rodriguez)

### License/Terms of Use:

MIT-0

## Use Case:

Banking risk, compliance, and committee support teams use this skill to convert CNBV-style risk indicators and market notes into a structured Spanish-language PDF brief for a Mexican bank risk committee.

### Deployment Geography for Use:

Mexico

## Known Risks and Mitigations:

Risk: Banking indicators and market context may include customer, confidential, or regulated nonpublic data sent through Telegram.

Mitigation: Deploy only after internal approval for Telegram data handling, restrict bot access to authorized users, and avoid sending regulated nonpublic data unless explicitly permitted.

Risk: User-provided text is incorporated into generated PDFs, which may create misleading content or formatting issues if not reviewed.

Mitigation: Validate and escape user-provided text before PDF generation and require human review before committee distribution.

Risk: Generated PDFs are written to temporary storage and may remain accessible after use.

Mitigation: Use secure temporary file handling with cleanup after delivery and run the bot in a controlled environment.

Risk: Unpinned dependencies may change behavior or introduce vulnerable versions.

Mitigation: Pin ReportLab and python-telegram-bot dependencies in a virtual environment or container before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ricardo-mendoza-rodriguez/skills/banking-committee-brief-mx)
- [Publisher profile](https://clawhub.ai/user/ricardo-mendoza-rodriguez)

## Skill Output:

**Output Type(s):** [text, PDF, shell commands, configuration]

**Output Format:** [Telegram conversation responses and a generated PDF document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TELEGRAM_BOT_TOKEN environment variable and writes generated PDF files to temporary storage.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
