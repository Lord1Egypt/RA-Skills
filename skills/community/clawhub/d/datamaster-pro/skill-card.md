## Description:

DataMaster Pro helps agents fetch, clean, visualize, and report on tabular data for data analysts and operations teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gdp6539](https://clawhub.ai/user/gdp6539)

### License/Terms of Use:

MIT

## Use Case:

Data analysts, operations teams, and business users can use this skill to collect data from supported sources, clean structured datasets, generate charts, and draft analysis reports. It is intended for normal ClawHub release use with reviewer attention to the security findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network and API inputs may fetch untrusted content or unexpected endpoints.

Mitigation: Use the skill only with trusted datasets and trusted URLs, and prefer HTTPS-only public endpoints.

Risk: Command-line headers or connection strings may expose secrets in shell history, logs, or process listings.

Mitigation: Avoid passing secrets in command-line headers; use controlled environment variables or a secret manager when credentials are required.

Risk: Generated reports and extracted datasets may contain sensitive data.

Mitigation: Store generated files in a controlled directory and review reports before sharing or publishing them.

Risk: PDF generation and report names can introduce unsafe file-output behavior when inputs are untrusted.

Mitigation: Do not run PDF generation with untrusted report names, and review output paths before execution.

Risk: The skill documentation overstates some capabilities relative to the provided scripts.

Mitigation: Review the skill manually before installation and test the intended workflow on non-sensitive sample data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gdp6539/skills/datamaster-pro)
- [DataMaster Pro README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration; generated artifacts may include CSV, JSON, SVG, HTML, Markdown, or PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local datasets, fetch trusted URLs or APIs, and write generated charts or reports to local output paths.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
