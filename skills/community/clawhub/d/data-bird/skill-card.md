## Description:

Data Bird is a lightweight data-analysis agent that analyzes workspace CSV/Excel files or downloaded HTTP(S) CSV/Excel files and produces ECharts charts with written insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niu001007](https://clawhub.ai/user/niu001007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Data Bird to turn tabular business data into quick charts, summaries, and short reports from natural-language questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch HTTP(S) data sources, including localhost or private-network URLs.

Mitigation: Allow downloads only from trusted sources and block localhost or private-network downloads unless the deployment explicitly requires them.

Risk: MySQL support can expose production credentials or unrestricted SQL when enabled.

Mitigation: Keep MySQL disabled for the free release unless explicitly authorized, and use restricted read-only credentials with bounded queries when enabled.

Risk: Report generation can write files outside the expected workspace when output paths are not constrained.

Mitigation: Force report output into a controlled workspace directory and review generated HTML reports from untrusted datasets before opening or sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niu001007/skills/data-bird)
- [Publisher profile](https://clawhub.ai/user/niu001007)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON containing ECharts options, insights, Markdown report text, summary metadata, and report artifact paths or URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The free configuration limits analysis to files up to 10 MB, up to 10,000 rows, and up to 5 charts per run.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
