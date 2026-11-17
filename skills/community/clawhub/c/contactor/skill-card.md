## Description:

Contactor and starter selection tool. Use when json contactor tasks, csv contactor tasks, checking contactor status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can invoke this skill to manage local contactor-related records through shell commands for status checks, listing, searching, export, and configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores, mutates, removes, and exports arbitrary local records.

Mitigation: Review stored data before use, avoid storing secrets, and run it only in a controlled local data directory.

Risk: A configuration bug may allow crafted input to run local commands.

Mitigation: Avoid untrusted configuration values and prefer a fixed version with input validation and safe serialization before operational use.

Risk: Exported CSV files may carry unsafe user-controlled content into spreadsheet software.

Mitigation: Treat exported CSVs as untrusted and inspect or sanitize them before opening in spreadsheet tools.

Risk: The skill's documented contactor-selection purpose is broader than the observed record-management behavior.

Mitigation: Validate that the implemented commands match the intended electrical contactor workflow before relying on outputs.

## Reference(s):

- [Contactor ClawHub Page](https://clawhub.ai/xueyetianya/skills/contactor)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, mutate, remove, and export local JSONL or CSV records through the bundled shell script.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
