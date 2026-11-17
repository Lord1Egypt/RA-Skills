## Description:

Checks npm projects and systems for the March 2026 axios supply-chain compromise involving axios@1.14.1, axios@0.30.4, and plain-crypto-js@4.2.1, then produces detection and remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vjumpkung](https://clawhub.ai/user/vjumpkung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security engineers, and CI/CD maintainers use this skill to assess whether a project or build environment was exposed to the March 2026 axios compromise and to choose appropriate remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remediation guidance includes elevated hosts-file and firewall commands that can affect the whole system.

Mitigation: Confirm indicators match the environment, review package files first, and treat sudo-level network blocking changes as manual changes that may need reversal.

Risk: Confirmed dropper execution or RAT artifacts indicate the affected machine or CI job may have exposed credentials.

Mitigation: Rebuild from a known-good state and rotate credentials that were accessible at install time, including npm tokens, cloud keys, SSH keys, environment secrets, and CI/CD secrets.

## Reference(s):

- [StepSecurity Harden-Runner](https://github.com/step-security/harden-runner)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown security check report with shell command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes project and system findings, a clean/exposed/compromised verdict, and recommended remediation actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
