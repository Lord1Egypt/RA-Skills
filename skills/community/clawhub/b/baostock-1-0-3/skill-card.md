## Description:

BaoStock helps agents query free China A-share market data, including K-line history, financial data, industry classifications, trading calendars, dividends, index constituents, and basic stock information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kernelh](https://clawhub.ai/user/kernelh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to guide BaoStock installation and Python API usage for A-share data collection, financial analysis, and educational backtesting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Python dependencies are specified with lower bounds rather than pinned versions, which can reduce reproducibility.

Mitigation: Install in a virtual environment or container and pin reviewed versions of baostock and pandas for controlled deployments.

Risk: Financial analysis and backtesting examples can be misread as trading advice.

Mitigation: Treat outputs as educational data workflows and require human financial review before acting on any market signal.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kernelh/skills/baostock-1-0-3)
- [Publisher Profile](https://clawhub.ai/user/kernelh)
- [BaoStock Homepage](https://www.baostock.com)
- [BaoStock API Documentation](https://www.baostock.com/baostock/index.php/Python_API%E6%96%87%E6%A1%A3)
- [BaoStock Documentation Index](https://www.baostock.com/baostock/index.php)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are instructional and may include BaoStock API examples, pandas data workflows, CSV export steps, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json reports package version 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
