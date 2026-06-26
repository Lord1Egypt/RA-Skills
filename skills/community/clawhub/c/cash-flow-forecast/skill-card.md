## Description: <br>
Build a 13-week rolling cash flow forecast from QBO data with 3-scenario modeling (base, upside, downside). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, accounting, and advisory users can generate a 13-week cash-flow forecast from QuickBooks Online data, including scenario comparisons, burn-rate analysis, runway estimates, assumptions, and forecast accuracy tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated Excel reports and CDC cache may contain sensitive cash, runway, burn-rate, and client financial information. <br>
Mitigation: Use only authorized client data, restrict access to report and cache locations, and handle generated files as sensitive financial records. <br>
Risk: QuickBooks Online access can expose client accounting records beyond what is needed for a forecast. <br>
Mitigation: Prefer sandbox or least-privilege read-only QBO access where available, and verify the selected company slug before running the forecast. <br>
Risk: Scenario forecasts can be misleading if inputs, thresholds, or client SOP assumptions are incorrect. <br>
Mitigation: Review SOP-driven assumptions, low-cash thresholds, and forecast outputs before using them for advisory or operating decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/cash-flow-forecast) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI examples and Excel report descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for generating an Excel workbook with Summary, Weekly Detail, Scenarios, Burn Rate, Assumptions, and CDC Log tabs.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
