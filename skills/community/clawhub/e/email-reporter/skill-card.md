## Description: <br>
Generic email reporting tool for OpenClaw agents that auto-converts Markdown reports to PDF and sends them as attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dirkcaiusa](https://clawhub.ai/user/dirkcaiusa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent users use this skill to send generated reports by email, with Markdown reports converted to PDF when images or large files make attachment delivery more appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe command execution may affect the msmtp email path. <br>
Mitigation: Avoid msmtp mode until reviewed or patched; prefer the SMTP backend with validated recipient and subject values. <br>
Risk: SMTP credentials can be handled through local configuration. <br>
Mitigation: Prefer environment variables or a secret manager, use app-specific SMTP credentials, and avoid storing long-lived secrets in plaintext config files. <br>
Risk: The skill can email generated report contents to a configured recipient. <br>
Mitigation: Check the recipient, subject, and report contents before execution, especially for sensitive reports or attachments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dirkcaiusa/email-reporter) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, PDF, Files, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown report files, generated PDF files, and email attachments configured through environment variables, config file values, or command-line arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; optional Python packages include markdown and weasyprint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
