## Description:

Screens and analyzes mutual funds using a five-dimension framework for performance, managers, style, holdings, and institutional flows, then supports portfolio construction and DCA tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cr330326](https://clawhub.ai/user/cr330326)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agent operators use this skill to screen Chinese mutual funds, compare individual funds, build fund portfolios, and track DCA execution. Outputs should be treated as informational and reviewed before investment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fund screening outputs may be mistaken for personalized financial advice.

Mitigation: Treat recommendations as informational only, review them independently, and include the required disclaimer when discussing specific funds.

Risk: The skill can save or update local Markdown or XLSX investment records.

Mitigation: Confirm before allowing writes or updates to local investment records and keep generated files in the documented results location.

Risk: Processing XLSX files introduces dependency and file-handling risk.

Mitigation: Use a locked or sandboxed Python environment when opening XLSX files.

## Reference(s):

- [Five-Dimension Analysis Standard](artifact/references/five-dimensions.md)
- [ClawHub Skill Page](https://clawhub.ai/cr330326/skills/fund-screening)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Chinese Markdown with tables and scorecards, optional XLSX files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Specific fund recommendations must include an informational-only investment disclaimer; saved result files use Markdown or XLSX formats with YYYYMMDD dates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
