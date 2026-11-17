## Description:

Multi-target parallel file copy CLI that reads a source once into memory and writes to multiple USB drives concurrently.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and automation agents use this skill to install and invoke fastcp for copying one source directory to multiple removable drives or target directories, with optional verification, incremental copy, dry-run previews, concurrency control, and JSON output for scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A normal fastcp command writes to every listed target path, so a mistaken drive letter or mount point could copy files to the wrong destination.

Mitigation: Run fastcp with --dry-run first and confirm each drive letter or mount point before executing a real copy.

Risk: Installing from a moving external source can retrieve code that differs from a previously reviewed release.

Mitigation: Prefer a pinned reviewed version or verify the release checksum before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dongsheng123132/skills/fastcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, json]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend dry-run, verification, quiet, verbose, concurrency, buffer-size, incremental, preload, and JSON-output flags.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
