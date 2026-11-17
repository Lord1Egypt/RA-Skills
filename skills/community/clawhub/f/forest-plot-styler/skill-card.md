## Description:

Beautifies meta-analysis forest plots with customizable odds ratio points and confidence intervals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, clinicians, data analysts, and developers use this skill to generate publication-ready forest plots from CSV or Excel meta-analysis data with configurable odds-ratio markers, confidence intervals, subgroup summaries, and PNG/PDF/SVG outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependencies can change behavior or introduce vulnerable versions over time.

Mitigation: Install the skill in a virtual environment or sandbox and pin and audit matplotlib, numpy, and pandas before repeated or sensitive use.

Risk: The script reads and writes local paths supplied on the command line.

Mitigation: Use trusted input files and choose output paths deliberately, preferably within a controlled workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/forest-plot-styler)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with command-line examples; generated plot files may be PNG, PDF, or SVG.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided CSV or Excel input and writes plots to a user-selected output path.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
