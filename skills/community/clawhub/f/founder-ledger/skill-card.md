## Description:

A one-file income ledger and milestone registry for solo founders tracking their way to their first $1,000, using stdlib-only Python and one local JSON file for data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulscode](https://clawhub.ai/user/paulscode)

### License/Terms of Use:

MIT

## Use Case:

Solo founders and developers use this skill to record early revenue entries, inspect progress toward the first $1,000, and keep a permanent milestone registry from a local command-line ledger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Revenue entries are stored in a local plaintext JSON file.

Mitigation: Keep real ledgers in a private directory and use --file or LEDGER_FILE to separate test ledgers from real data.

Risk: Undo removes the latest ledger entry but does not erase milestones that were already recorded.

Mitigation: Treat the milestone registry as a permanent history and review ledger behavior before using it for reversible or audited accounting workflows.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/paulscode/skills/founder-ledger)
- [README](README.md)
- [LICENSE](LICENSE)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and CLI text or JSON output from the included Python ledger tool]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The ledger writes to a local JSON file selected by --file, LEDGER_FILE, or the default ledger.json path.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
