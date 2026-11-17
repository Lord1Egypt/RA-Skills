## Description:

Automatically installs ClawHub skills with retry logic, automatic confirmation, and a 30-minute timeout when a user provides a skill name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z448577223](https://clawhub.ai/user/z448577223)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install named ClawHub skills through an automated shell script that retries rate limits and forced installs. Use it only when the user intentionally wants prompt-bypassing installation behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer bypasses ClawHub install confirmations and continues retrying even when a skill is flagged as suspicious.

Mitigation: Use only for trusted skills after reviewing the publisher, version, permissions, warnings, and security findings.

Risk: Automated retries can repeatedly attempt an unintended or failing install for up to 30 minutes.

Mitigation: Confirm the exact skill name before use and stop to review unexpected failures or suspicious package warnings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/z448577223/skills/clawhub-skill-install)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with bash command examples and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs clawhub install with --force, retries every 10 seconds, and stops after 30 minutes.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
