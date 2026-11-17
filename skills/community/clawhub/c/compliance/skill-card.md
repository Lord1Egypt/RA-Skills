## Description:

Track compliance requirements and generate audit trail reports for audits, policy checks, and audit trail generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security teams, and compliance reviewers use this skill to record timestamped compliance activities, search prior entries, check status, and export local audit records for reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext compliance logs and exports may contain sensitive operational, policy, or audit information.

Mitigation: Do not enter secrets, credentials, tokens, private keys, regulated personal data, or authoritative audit evidence unless the local files under ~/.local/share/compliance/ are managed appropriately.

Risk: Exported CSV, JSON, or TXT files may include all logged data and may not be safe to share as-is.

Mitigation: Review exported files before sharing and treat them as sensitive records.

## Reference(s):

- [Compliance on ClawHub](https://clawhub.ai/bytesagain-lab/skills/compliance)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, JSON, CSV]

**Output Format:** [CLI text with local plaintext log files and JSON, CSV, or TXT exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores compliance records under ~/.local/share/compliance/.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
