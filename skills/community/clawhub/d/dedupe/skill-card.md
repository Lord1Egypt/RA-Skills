## Description:

Deduplication reference - exact matching, fuzzy matching, hash-based dedup, bloom filters, and data quality for removing duplicate records, files, or data entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and operators use this skill as a concise reference for choosing and applying exact, fuzzy, file-level, SQL, command-line, and probabilistic deduplication techniques.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destructive deduplication examples could delete files or database rows if copied directly into a live environment.

Mitigation: Start with read-only detection commands, work on backups or staging copies, and review delete, auto-delete, hardlink, symlink, and SQL DELETE commands before execution.

Risk: Incorrect duplicate criteria can merge or remove legitimate distinct records.

Mitigation: Define deduplication keys and keep strategy before execution, test on a subset, log removed duplicates, and validate counts and spot checks afterward.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/dedupe)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-style reference text with command, SQL, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command-specific reference sections selected by script argument.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
