## Description: <br>
Helps agents reproduce A-share quantitative research reports by identifying the research pattern, selecting an appropriate stock universe, running a standardized Python backtest when applicable, and presenting report-style results with tables and figures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x2hacks](https://clawhub.ai/user/0x2hacks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to turn an A-share quantitative or financial-engineering report into a structured replication workflow, including research classification, factor or rule definition, dataset selection, backtest execution, and report-style interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled workflow may run a local Python backtest that contacts external market-data providers and writes report artifacts locally. <br>
Mitigation: Run it in a virtual environment, install dependencies from trusted sources, and set output and download limits such as OUT_DIR or TARGET_DOWNLOAD_STOCKS before execution. <br>
Risk: Backtest conclusions can be sensitive to stock-universe selection, data availability, transaction-cost assumptions, and whether the original report disclosed enough detail for strict replication. <br>
Mitigation: Review the reported sample size, filtering rules, cost assumptions, and any proxy-replication notes before relying on the generated conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0x2hacks/a-share-quant-report) <br>
- [OpenClaw skill format](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with tables, inline image references, Python code or commands when execution is needed, and explanatory guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local backtest outputs and figures when the agent executes the provided Python workflow.] <br>

## Skill Version(s): <br>
1.0.2 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
