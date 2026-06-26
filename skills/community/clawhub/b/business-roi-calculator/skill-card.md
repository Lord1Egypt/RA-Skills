## Description: <br>
Business ROI Calculator helps evaluate business partnerships, channels, and revenue opportunities by calculating short-term ROI, long-term ROI, expected value, and threshold-based recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdp6539](https://clawhub.ai/user/gdp6539) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users and agents use this skill to assess whether a partnership, channel campaign, consulting offer, training launch, or similar revenue opportunity is worth pursuing. It turns user-provided revenue, cost, probability, and timeframe assumptions into a structured Markdown ROI report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad questions such as whether something is worth doing, even when the request is not really about partnership, channel, or ROI evaluation. <br>
Mitigation: Confirm the request is an ROI-style business evaluation before relying on the score or recommendation. <br>
Risk: The resulting recommendation depends on user-provided revenue, cost, success-rate, and timeframe assumptions. <br>
Mitigation: Use current business data, include hidden or opportunity costs, and treat the report as decision support rather than a guaranteed financial outcome. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gdp6539/business-roi-calculator) <br>
- [README](README.md) <br>
- [Preset templates](references/templates.md) <br>
- [Calculation examples](references/examples.md) <br>
- [ROI calculation script](scripts/calculate-roi.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with optional Python CLI or JSON output when using the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include input assumptions, short-term ROI, long-term ROI, expected value, threshold-based recommendation, and optional sensitivity or break-even analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
