## Description: <br>
Agricultural Output Forecasting helps estimate crop yields and agricultural production using crop type, planted area, region, season, simulated weather factors, and market trend factors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Andyxcg](https://clawhub.ai/user/Andyxcg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Farmers, agronomists, agricultural businesses, and developers use this skill to generate decision-support forecasts for crop yield, production volume, risk level, and recommendations. It can be used through the Python API or command line, with optional CSV export and SkillPay billing after local trial usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package includes an under-disclosed long-running self-evolution daemon. <br>
Mitigation: Do not run auto-evolve-daemon.sh unless a long-running background process is intentional and has been reviewed. <br>
Risk: Privacy documentation does not fully match code behavior around local trial user records. <br>
Mitigation: Use a non-sensitive user_id and delete local trial records when they are no longer needed. <br>
Risk: Billing depends on SkillPay credentials and token charges after trial usage. <br>
Mitigation: Configure only trusted SkillPay credentials and monitor balances and charges during use. <br>


## Reference(s): <br>
- [Agricultural Forecasting Methodology](references/forecast-methodology.md) <br>
- [SkillPay Billing API Reference](references/skillpay-billing.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Andyxcg/agricultural-output-forecasting) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell examples; runtime forecast results are JSON-like dictionaries and optional CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Forecast output may include yield estimates, confidence intervals, weather and market factors, risk assessment, recommendations, billing or trial status, and optional CSV export.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
