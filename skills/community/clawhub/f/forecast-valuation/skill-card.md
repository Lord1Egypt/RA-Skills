## Description: <br>
A financial forecasting and valuation model generator that creates spreadsheet-based forecasts, DCF valuation, comparable-company analysis, sensitivity analysis, and a football-field valuation range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate a local Excel valuation workbook for a named company and stock code. The workbook is useful as a financial-model template, but outputs should be independently reviewed before any business or investment use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated valuation outputs may be misleading if treated as decision-grade financial analysis. <br>
Mitigation: Use the workbook as a template and independently verify all assumptions, comparable-company selections, sensitivity tables, and target prices before business or investment use. <br>
Risk: API credentials entered during configuration are stored in plaintext config.json. <br>
Mitigation: Avoid entering real credentials unless plaintext local storage is acceptable; rotate any credentials that were entered unintentionally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cgxxxxxxxxxxxx/forecast-valuation) <br>
- [Artifact README](docs/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration, guidance] <br>
**Output Format:** [Excel workbook plus command-line and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a local .xlsx valuation workbook and may write local config.json settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
