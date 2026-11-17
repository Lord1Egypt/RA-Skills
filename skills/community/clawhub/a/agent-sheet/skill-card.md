## Description:

Shell-native spreadsheet CLI for agent work, used for workbook inspection, sheet and range reads, precise writes, import/export handoff, review-table construction, formula analysis, and bounded workbook-native scripting with verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangluoshen](https://clawhub.ai/user/yangluoshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect, transform, write, import, export, and verify spreadsheet workbooks through the local agent-sheet CLI while keeping workbook targets explicit and changes bounded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The npm installation target uses agent-sheet@latest, so future package changes could alter behavior.

Mitigation: Install only when the package and publisher are trusted, or pin an audited agent-sheet version before deployment.

Risk: Write, delete, clear, import/export, and script js commands can make real changes to workbook or filesystem state.

Mitigation: Confirm the target entryId, sheet, range, and path before execution, keep mutations bounded, and run the documented verification steps after changes.

Risk: Shell roundtrips can preserve row counts while shifting headers or key columns.

Mitigation: Verify the header row, first sample rows, key columns, and total row count before treating writeback as successful.

## Reference(s):

- [Repository](https://github.com/dream-num/skills)
- [Documentation](https://github.com/dream-num/skills)
- [Command Selection Matrix](artifact/references/command-selection-matrix.md)
- [Gotchas Reference](artifact/references/gotchas.md)
- [Shell Patterns Reference](artifact/references/shell-patterns.md)
- [JS API Minimal Reference](artifact/references/js-api-minimal.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce bounded previews, file paths, stream output, verification summaries, and small helper-script invocations.]

## Skill Version(s):

0.1.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
