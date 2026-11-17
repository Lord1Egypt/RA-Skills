## Description:

Search codebase contents, filenames, and directory structures using ripgrep, fd, and tree with filters for file types, context, depth, and result limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanxingang](https://clawhub.ai/user/yanxingang)

### License/Terms of Use:


## Use Case:

Developers and coding agents use this skill to inspect unfamiliar codebases, find definitions and usages, locate files, and summarize project structure without modifying files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback installation guidance downloads CLI archives and copies binaries into /usr/local/bin without documented checksum or signature verification.

Mitigation: Prefer OS package-manager installs for rg, fd, and tree; if manual binary installation is required, independently verify checksums or signatures before installing system-wide.

Risk: The skill reads files under user-provided search paths.

Mitigation: Run searches only against codebases and directories the operator is authorized to inspect, and avoid broad searches over sensitive local paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanxingang/skills/code-search)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Structured plain text with delimited result sections and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only search, filename, directory tree, dependency-check, error, and truncation outputs; grep defaults to 100 results, glob defaults to 200 results, and tree defaults to depth 3.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
