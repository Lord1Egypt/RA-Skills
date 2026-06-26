## Description: <br>
Generates an executive risk committee brief for Mexican banking indicators, accepting CNBV metrics and market context through Telegram and returning a structured PDF. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricardo-mendoza-rodriguez](https://clawhub.ai/user/ricardo-mendoza-rodriguez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Bank risk, compliance, and committee support teams use this skill to collect key CNBV indicators and market context, then generate a PDF-ready executive brief for a Mexico banking risk committee. It is intended to support internal preparation and review, not replace formal regulatory or legal analysis. <br>

### Deployment Geography for Use: <br>
Mexico <br>

## Known Risks and Mitigations: <br>
Risk: The Telegram bot collects banking indicators and market context, which may include confidential business information. <br>
Mitigation: Install only where Telegram is an approved channel, restrict bot access, and avoid sending confidential material to unauthorized chats. <br>
Risk: A Telegram bot token is required and could allow unauthorized bot control if exposed. <br>
Mitigation: Store TELEGRAM_BOT_TOKEN securely, rotate it if exposure is suspected, and run the skill in a controlled virtual environment or container. <br>
Risk: Generated risk committee PDFs are written to /tmp and may persist after use. <br>
Mitigation: Delete generated PDFs from /tmp after sending or reviewing them, especially when they contain confidential banking information. <br>
Risk: The PDF uses embedded threshold logic for CNBV and Basel III Mexico references that may not reflect the latest institution-specific or regulatory interpretation. <br>
Mitigation: Have qualified risk, compliance, or legal reviewers verify thresholds, signals, and recommendations before committee use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ricardo-mendoza-rodriguez/banking-committee-brief-mx) <br>


## Skill Output: <br>
**Output Type(s):** [text, pdf, shell commands, configuration] <br>
**Output Format:** [Telegram conversation that returns a generated PDF brief; local setup uses shell commands and environment configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TELEGRAM_BOT_TOKEN and writes generated PDFs under /tmp.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
