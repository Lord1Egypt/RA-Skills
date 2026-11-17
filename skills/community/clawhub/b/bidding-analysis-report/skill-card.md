## Description:

Generates bidding data analysis reports with AI project share analysis, annual trends, top institution rankings, and chart-backed Word report output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[austin0208](https://clawhub.ai/user/austin0208)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and procurement analysts use this skill to analyze Excel-based bidding data for AI-related project share, annual trends, and top institution rankings, then generate a Chinese-language Word report with embedded charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes procurement and business data from local Excel files and can leave generated PNG charts in the working directory.

Mitigation: Run it from a trusted private directory and review or remove generated chart files after report creation.

Risk: Production use depends on Python packages installed from requirements.txt with broad version ranges.

Mitigation: Install dependencies in an isolated environment and pin reviewed versions for production workflows.

Risk: Documentation mentions PDF output, but the authoritative security guidance says not to rely on PDF output unless the implementation is updated.

Mitigation: Use Word output for normal operation and validate any PDF support before depending on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/austin0208/skills/bidding-analysis-report)
- [Project homepage](https://github.com/openclaw/bidding-analysis-report)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python API examples, shell command examples, generated Word documents, and PNG charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads Excel input files and writes report and chart files to the local output path.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
