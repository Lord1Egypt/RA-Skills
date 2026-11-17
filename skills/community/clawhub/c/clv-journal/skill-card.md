## Description:

Log bets with entry + closing odds, compute closing-line value (CLV) in odds pts and implied-prob pts, and roll up beat-close rate by sport/book/market.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianalloway](https://clawhub.ai/user/ianalloway)

### License/Terms of Use:

MIT-0

## Use Case:

External users who track sports wagers can record entry and closing prices, calculate closing-line value, and review beat-close rates by sport, book, or market.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example values in the commands could be recorded by mistake.

Mitigation: Replace example values with the intended bet details before running commands.

Risk: The journal contains plaintext betting records.

Mitigation: Protect access to the local CSV journal and its backups.

Risk: Updating an existing record rewrites the journal file.

Mitigation: Keep a backup before updating existing records.

## Reference(s):

- [ClawHub release](https://clawhub.ai/ianalloway/skills/clv-journal)

## Skill Output:

**Output Type(s):** [CSV files, Text analysis, Python code, Shell commands]

**Output Format:** [Markdown guidance with inline Python shell commands; CSV journal and text rollups]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands create or update a local CSV journal and print CLV summaries.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
