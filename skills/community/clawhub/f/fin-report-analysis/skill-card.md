## Description: <br>
Analyzes Excel financial statements and produces a Markdown financial analysis report covering line-item changes, balance-sheet and income-statement structure, financial ratios, and expert summary recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinfeihaaaaaaaaaaa](https://clawhub.ai/user/yinfeihaaaaaaaaaaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance teams, analysts, and business reviewers use this skill to analyze uploaded Excel financial statements and generate a structured Markdown report for due diligence, annual review, operational health checks, and management discussion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The analysis script may attempt to install pandas and openpyxl automatically during execution. <br>
Mitigation: Use a controlled or sandboxed Python environment and preinstall dependencies before running the skill in sensitive or locked-down environments. <br>
Risk: Generated reports may contain confidential financial data from the source workbook. <br>
Mitigation: Review the Markdown report before sharing it and apply the same handling controls used for the original financial workbook. <br>
Risk: Financial conclusions can be incomplete or misleading when workbook structure, sheet names, units, or periods are not detected correctly. <br>
Mitigation: Check unmatched-sheet and data-insufficiency notes in the report, verify units and period columns, and have a qualified reviewer confirm material conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinfeihaaaaaaaaaaa/fin-report-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown report with tabular financial analysis and summary guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a Markdown report file next to the source workbook and may include financial data from the uploaded workbook.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
