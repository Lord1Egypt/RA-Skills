## Description:

Checks whether credentials and tokens are stored safely by validating file permissions, plaintext exposure, git repo contamination, log redaction coverage, and token rotation status for OpenClaw and general dotfile directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techris93](https://clawhub.ai/user/techris93)

### License/Terms of Use:


## Use Case:

Developers, engineers, and security reviewers use this skill to audit credential storage in OpenClaw and dotfile directories before setup, machine onboarding, public dotfile pushes, routine reviews, or credential rotation follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented credential scans can print full secrets into the agent session, terminal output, or logs.

Mitigation: Review before installing when live tokens may be present, run only where output is not logged or shared, prefer redacted or manual checks, and rotate any credential that appears in an agent transcript or terminal log.

## Reference(s):

- [OpenClaw threat model (T-ACCESS-003)](https://github.com/openclaw/trust)
- [OpenClaw security policy](https://github.com/openclaw/openclaw/security/policy)
- [RFC 6750 - Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and audit findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only credential hygiene review; command output may contain sensitive credential material if scans match live secrets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
