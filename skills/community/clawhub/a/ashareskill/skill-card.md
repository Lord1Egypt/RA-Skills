## Description:

Ashareskill retrieves A-share stock K-line data from BaoStock and calculates technical indicators for single stocks, stock pools, or supported index constituents.

This skill is for research and development only.

## Publisher:

[caoyachao](https://clawhub.ai/user/caoyachao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative analysts use this skill to fetch A-share historical K-line data, calculate common technical indicators, and export the results for backtesting or analysis. The artifact states the data is for reference, learning, and research use and does not provide investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts BaoStock to retrieve market data.

Mitigation: Run it only in an environment where outbound access to BaoStock is expected and permitted.

Risk: The skill writes CSV files when export examples or output paths are used.

Mitigation: Use a controlled output directory and review the selected output path before execution.

Risk: Dependency versions are specified with lower bounds, which can reduce reproducibility over time.

Mitigation: Install in a dedicated virtual environment and pin dependency versions for reproducible deployments.

Risk: Market data and calculated indicators may be unsuitable as the sole basis for investment decisions.

Mitigation: Treat generated data as reference material and validate it independently before financial use.

## Reference(s):

- [BaoStock data source](http://baostock.com/)
- [ClawHub skill page](https://clawhub.ai/caoyachao/skills/ashareskill)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [CSV files, pandas DataFrames, and Markdown guidance with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes UTF-8 CSV output and may contact BaoStock during execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
