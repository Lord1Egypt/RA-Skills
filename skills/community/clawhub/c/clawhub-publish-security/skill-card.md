## Description:

Automated pre-publish scanner that detects and blocks sensitive data like credentials, tokens, emails, and personal paths in ClawHub skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vilda007](https://clawhub.ai/user/vilda007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill before ClawHub publication to scan local skill directories for sensitive values and receive remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can print detected secrets or personal values in terminal output.

Mitigation: Run it locally, avoid shared CI logs for real secrets, redact output before sharing, and rotate any secret that may have been printed.

Risk: A clean scan can create an overconfident safety signal because scanning rules are incomplete.

Mitigation: Manually review configuration files, documentation examples, and generated artifacts before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vilda007/skills/clawhub-publish-security)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [VETTING_REPORT.md](artifact/VETTING_REPORT.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and scanner console output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scanner output may include matched sensitive values when findings are printed.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
