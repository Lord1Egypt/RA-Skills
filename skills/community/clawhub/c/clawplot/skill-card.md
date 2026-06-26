## Description: <br>
ClawPlot helps agents order physical pen-plotted artwork from SVG designs, with catalog, order, payment, and status APIs for worldwide shipping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheGhostofJoeMacmillan](https://clawhub.ai/user/TheGhostofJoeMacmillan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to browse ClawPlot options, submit SVG art for physical pen plotting, pay through Stripe or USDC, and track shipment status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent may submit a paid physical-art order or disclose shipping details without sufficient user confirmation. <br>
Mitigation: Confirm the final artwork, shipping name and address, destination domain, price, payment method, and order intent before submitting anything to clawplot.com. <br>


## Reference(s): <br>
- [ClawPlot API Reference](references/api.md) <br>
- [ClawPlot Service](https://clawplot.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/TheGhostofJoeMacmillan/clawplot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with curl examples and JSON request and response schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include order, payment, and shipping details that should be confirmed before submission.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
