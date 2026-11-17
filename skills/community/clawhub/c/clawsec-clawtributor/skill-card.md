## Description:

Clawtributor helps AI agents prepare approval-gated community incident reports about malicious prompts, vulnerable skills, and tampering attempts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

AGPL-3.0-or-later

## Use Case:

Developers and security-minded agent users use this skill to draft local, structured reports for malicious prompts, vulnerable skills or plugins, and tampering attempts. The workflow keeps reporting approval-gated and asks the user to review and sanitize evidence before manual submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npx install examples can create supply-chain ambiguity before installation.

Mitigation: Prefer the signed release verification workflow or a version-pinned installer before trusting release files.

Risk: Manual report submission can disclose sensitive host, user, or conversation data if evidence is not sanitized.

Mitigation: Review the exact payload with the user and remove personal data, credentials, secrets, and confidential details before approval.

Risk: Local incident reports and state files may contain sensitive security observations.

Mitigation: Store report files under the documented local path with private file permissions such as chmod 600.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davida-ps/skills/clawsec-clawtributor)
- [ClawSec Homepage](https://clawsec.prompt.security)
- [Prompt Security](https://prompt.security)
- [Security Incident Report Form](https://github.com/prompt-security/clawsec/issues/new?template=security_incident_report.md)
- [Reporting Guide](artifact/reporting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON report templates and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local report drafts and approval prompts; report submission remains manual and user-approved.]

## Skill Version(s):

0.0.9 (source: frontmatter, skill.json, changelog, released 2026-06-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
