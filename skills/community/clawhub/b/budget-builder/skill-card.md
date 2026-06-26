## Description: <br>
Dual-mode budget pipeline for FP&A-quality budget management: it builds annual budgets from QBO history and compares YTD actuals against saved budgets with variance flags, commentary stubs, rolling forecasts, and Excel workbook outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, accounting, and FP&A users use this skill to build annual operating budgets, run monthly budget-vs-actual close, generate board-ready variance workbooks, and track budget accuracy over time for QBO-connected clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill works with QuickBooks financial data and saves budget and CDC files locally. <br>
Mitigation: Use least-privilege QBO access where possible, keep generated Excel and .cache/budget-builder files out of shared or synced locations, and delete cached files when no longer needed. <br>
Risk: Budget assumptions, overrides, and generated commentary may affect financial planning decisions. <br>
Mitigation: Review assumptions, overrides, material variance flags, and commentary before sharing reports or using them for management decisions. <br>


## Reference(s): <br>
- [Budget Builder ClawHub Release](https://clawhub.ai/samledger67-dotcom/budget-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with bash, JSON, and CSV examples; generated artifacts are Excel workbooks and local JSON cache files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Build workbooks with 4 tabs or Compare workbooks with 6 tabs, plus local budget and CDC JSON cache files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
