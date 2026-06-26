## Description: <br>
Create publication-ready economic comparison charts from Federal Reserve Economic Data (FRED). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pratyushchauhan](https://clawhub.ai/user/pratyushchauhan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and economic researchers use this skill to configure and generate indexed comparison charts for FRED time series such as GDP, wages, inflation, employment, and corporate profits. It supports annotated timelines and gap visualization for economic comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper contacts FRED over the network and depends on remote FRED responses for chart data. <br>
Mitigation: Review the requested FRED series IDs and date ranges, and confirm the retrieved data source before using generated charts in decisions or publications. <br>
Risk: The helper writes to the user-provided output path and may overwrite an existing file at that location. <br>
Mitigation: Choose a new or disposable output path unless overwriting an existing chart is intentional. <br>
Risk: The helper requires pandas and matplotlib in the execution environment. <br>
Mitigation: Install and verify these dependencies in an isolated environment before running the script. <br>


## Reference(s): <br>
- [FRED](https://fred.stlouisfed.org) <br>
- [FRED CSV graph endpoint](https://fred.stlouisfed.org/graph/fredgraph.csv) <br>
- [ClawHub skill page](https://clawhub.ai/pratyushchauhan/fred-data-viz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell commands; the helper script produces chart image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided FRED series IDs, date ranges, labels, colors, annotations, and output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
