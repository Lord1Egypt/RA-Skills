## Description:

File-integrity helps agents compute and compare checksums, verify copied or downloaded files, and create or check checksum manifests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zd200572](https://clawhub.ai/user/zd200572)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to verify file integrity after copy, download, backup, restore, or dataset transfer workflows. It supports single-file hashing, expected-hash comparison, copy/download verification, and manifest generation or checking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read files selected for hashing or manifest checks.

Mitigation: Run it only on intended files and directories, and avoid pointing it at sensitive paths unless checksum verification requires that access.

Risk: The skill can write copied files, downloaded files, partial downloads, and checksum manifests to user-provided paths.

Mitigation: Review destination paths before execution and keep outputs in expected working directories.

Risk: Downloaded content may be untrusted if no expected checksum is supplied.

Mitigation: Prefer a trusted SHA-256 or stronger checksum from the original publisher when using download verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zd200572/skills/file-integrity)
- [Publisher profile](https://clawhub.ai/user/zd200572)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supported subcommands can emit JSON with --json; verification results use exit codes 0, 1, and 2.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
