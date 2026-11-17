## Description:

BaoStock helps agents query free China A-share market data, including K-line, financial, trading-calendar, industry, and index-constituent data without registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderwpf](https://clawhub.ai/user/coderwpf)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and agent builders use this skill to install BaoStock, call its Python APIs, and retrieve China A-share securities, price history, financial metrics, industry classifications, and index constituent data for analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package installation can introduce unreviewed dependency changes.

Mitigation: Install the skill dependencies in a virtual environment and pin reviewed versions of baostock and pandas before use.

Risk: Sample scripts contact BaoStock services and examples may create or overwrite CSV files with the shown filenames.

Mitigation: Review scripts before execution, confirm outbound network access is acceptable, and choose explicit output paths for generated CSV files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/coderwpf/skills/baostock)
- [BaoStock Homepage](https://www.baostock.com)
- [BaoStock Python API Documentation](http://baostock.com/baostock/index.php/Python_API%E6%96%87%E6%A1%A3)
- [BaoStock API Manual](https://www.baostock.com/baostock/index.php/Python_API%E6%96%87%E6%A1%A3)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to run Python package installation, query remote BaoStock services, and write CSV outputs.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
