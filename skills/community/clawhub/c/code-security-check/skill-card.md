## Description:

Audit the current project for sensitive information leaks before pushing to public repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mate-matt](https://clawhub.ai/user/mate-matt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to check a working tree for exposed credentials, weak .gitignore coverage, and sensitive files before pushing or open-sourcing a repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect highly sensitive files in the current workspace, including credential and private key files.

Mitigation: Use it only in repositories where agent access to potential secrets is acceptable, and prefer confirmation or metadata-only handling before opening private keys or production credential files.

Risk: The skill may falsely skip scans for local or private repositories after its exposure gate.

Mitigation: Do not rely on a no-risk result for local or private repositories when sensitive files still need internal review.

Risk: The skill proposes remediation actions that can change repository ignore rules or tracking state.

Mitigation: Review the findings first and require explicit user confirmation before applying file or git changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown security audit report with findings, redacted examples, and optional remediation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Redacts full secrets and requires user confirmation before modifying files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
