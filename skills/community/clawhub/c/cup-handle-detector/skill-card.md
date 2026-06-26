## Description: <br>
Detects cup-and-handle technical analysis patterns in stock daily price data and generates annotated pattern charts when a match is found. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laigen](https://clawhub.ai/user/laigen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to check individual stocks or SQLite-backed stock datasets for recent cup-and-handle patterns and to produce local charts and reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live single-stock analysis requires a Tushare token. <br>
Mitigation: Provide TUSHARE_TOKEN only when live Tushare data is needed. <br>
Risk: Batch mode scans every table in the selected SQLite database and writes chart and report files. <br>
Mitigation: Point batch mode only at SQLite databases and output directories intended for this analysis. <br>
Risk: Cup-and-handle detection is a technical analysis aid and can be subjective or wrong. <br>
Mitigation: Review the generated score, chart, and source market data before using results in any financial workflow. <br>


## Reference(s): <br>
- [Cup-and-handle recognition algorithm](references/algorithm.md) <br>
- [ClawHub skill page](https://clawhub.ai/laigen/cup-handle-detector) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Console text with optional Markdown scan report and PNG chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-stock mode can use live Tushare data with TUSHARE_TOKEN; batch mode reads SQLite tables and writes charts plus a report to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
