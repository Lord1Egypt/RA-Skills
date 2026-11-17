## Description:

Dev Setup helps agents and developers record, search, summarize, and export timestamped notes about macOS development environment setup tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Dev Setup to keep a local, searchable history of macOS development setup activities, tool installation notes, configuration changes, and onboarding records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the skill as an automated macOS provisioning tool even though the artifact behaves as a local setup-note logger.

Mitigation: Review before installing and use it for recording setup notes rather than unattended provisioning.

Risk: Setup notes can include secrets, tokens, passwords, private host details, or credential-bearing commands, and entries are stored verbatim in the user's home directory.

Mitigation: Do not record sensitive values; review local logs and exported files before sharing or committing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/dev-setup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks and command-line text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external services, databases, or API keys are required; the artifact stores log and export files locally under ~/.local/share/dev-setup/.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
