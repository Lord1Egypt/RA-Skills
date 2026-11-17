## Description:

Generate ASCII bar, line, pie, and scatter charts from CSV or inline data in a terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and command-line users use this skill to quickly visualize small datasets, trends, comparisons, and distributions as terminal ASCII charts without opening a spreadsheet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local data files may contain sensitive or unintended information before charting.

Mitigation: Review local CSV or data files before passing them to the chart command.

Risk: Scatter plots require numeric coordinate data and may not represent arbitrary label/value categories correctly.

Mitigation: Use scatter charts only with numeric x,y coordinate data; use bar, line, or pie charts for label/value categories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/bytesagain-chart-generator)
- [Publisher profile](https://clawhub.ai/user/loutai0307-prog)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with terminal commands and ASCII chart output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces terminal-rendered bar, line, pie, scatter, and demo chart output from inline data or CSV-style files.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
