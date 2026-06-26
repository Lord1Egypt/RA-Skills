## Description: <br>
商业捡漏预警虾 helps agents define and run multi-platform deal-monitoring rules for discounted goods, real estate, auctions, and procurement opportunities, with valuation and risk-screening guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business operators use this skill to express monitoring criteria, generate rule JSON, run marketplace or procurement scans, and review candidate opportunities before acting. It is most useful for alerting workflows that compare listed prices against valuation references and attach risk notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring scraping-style monitoring can conflict with target platform rules, especially when login-state or anti-bot collection techniques are used. <br>
Mitigation: Confirm each target platform permits automation, avoid logged-in sessions unless clearly authorized, and keep collection frequency conservative and inspectable. <br>
Risk: Listing data, contact details, and alert logs may be retained locally longer than intended. <br>
Mitigation: Collect only necessary fields, decide whether contact details should be collected at all, and keep the data directory and scheduled jobs easy to inspect and delete. <br>
Risk: The bundled collector is an example implementation that returns simulated results until real platform collectors are added. <br>
Mitigation: Treat example output as non-authoritative and validate any real collector, valuation logic, and risk filter before relying on alerts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tujinsama/deal-hunter-alert-claw) <br>
- [Platform collection rules](references/platform-rules.md) <br>
- [Risk signal library](references/risk-signals.md) <br>
- [Valuation model library](references/valuation-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON monitoring rules; the bundled monitor can print JSON results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The monitor script may create local seen-ID and alert-log files in the configured deal-hunter data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
