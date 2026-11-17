## Description:

Data Chart Builder helps agents create publication-ready line, bar, scatter, fill, indexed-series, annotated, and multi-series charts from CSV, JSON, FRED, or inline data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratyushchauhan](https://clawhub.ai/user/pratyushchauhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to turn local, remote, FRED, or inline datasets into reusable chart configurations and saved plot files for time-series comparison, trend analysis, and annotated data visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted chart configurations can fetch chart data from arbitrary URLs.

Mitigation: Use trusted configurations and vetted data URLs; prefer local files or known data providers when possible.

Risk: Chart configurations can write output files to caller-specified paths.

Mitigation: Review the output path before execution and run the skill with a restricted output directory for shared or automated environments.

## Reference(s):

- [Data Chart Builder on ClawHub](https://clawhub.ai/pratyushchauhan/skills/data-chart-builder)
- [FRED](https://fred.stlouisfed.org)

## Skill Output:

**Output Type(s):** [configuration, shell commands, code, guidance, files]

**Output Format:** [Markdown guidance with JSON configuration examples and bash commands; generated charts are written as image files by the script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chart files are saved to configured local output paths, defaulting to /tmp/chart.png.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
