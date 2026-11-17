## Description:

Scans files, repos, and directories for leaked secrets, including API keys, tokens, passwords, connection strings, private keys, and credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nirwandogra](https://clawhub.ai/user/nirwandogra)

### License/Terms of Use:

MIT

## Use Case:

Developers and security reviewers use this skill to audit files, directories, and repositories for exposed credentials before committing, publishing, or deploying code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner reports may contain sensitive secret evidence, including previews and contextual lines.

Mitigation: Treat Markdown and JSON reports as sensitive artifacts, restrict sharing, and manually review reports before publishing or uploading them.

Risk: Directory scans may follow symlinks outside the intended scan folder.

Mitigation: Avoid running the scanner on untrusted repositories and inspect or remove symlinks before scanning until symlink handling is fixed.

## Reference(s):

- [Credential Scanner on ClawHub](https://clawhub.ai/nirwandogra/skills/credential-scanner)
- [Publisher profile](https://clawhub.ai/user/nirwandogra)

## Skill Output:

**Output Type(s):** [analysis, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown report or JSON with finding summaries, severity counts, file paths, line numbers, masked secret previews, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI output can be printed to stdout or saved to a report file; exit codes distinguish clean, high-severity, and critical findings.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
