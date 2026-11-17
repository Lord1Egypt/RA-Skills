## Description:

Computerized maintenance management system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Maintenance teams and developers can use this skill to run a local CMMS command-line workflow for adding, listing, searching, removing, exporting, and summarizing maintenance entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration updates can allow shell injection through unsafe sed-based rewriting.

Mitigation: Review or patch the shell script before installing; validate configuration keys and replace sed-based updates with data-safe file rewriting.

Risk: Entry and export handling uses weak JSON and CSV encoding.

Mitigation: Encode JSON with a real JSON encoder, quote CSV fields correctly, and handle exported CSV files from untrusted entries carefully.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain-lab/skills/cmms)
- [Publisher profile](https://clawhub.ai/user/bytesagain-lab)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output with JSONL data storage and optional JSONL or CSV export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses stdout for status and command results, stores entries under CMMS_DIR or ~/.cmms, and exits 0 on success or 1 on error.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
