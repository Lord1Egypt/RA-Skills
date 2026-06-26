## Description: <br>
The fast auto-invest function of Gate Exchange Earn for creating, updating, stopping, and topping up invest plans and querying supported coins, minimum amounts, records, orders, and plan detail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Gate Exchange users and agents use this skill to manage Gate Earn auto-invest, dollar-cost averaging plans, including lifecycle actions, plan and order queries, balance context, and compliance-facing rule checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial write actions can create, update, stop, or top up Gate auto-invest plans. <br>
Mitigation: Require an Action Draft and explicit user confirmation before write tools are called. <br>
Risk: A repeated top-up call can duplicate deductions. <br>
Mitigation: Call the add-position tool exactly once for each confirmed top-up request. <br>
Risk: Incorrect time-zone handling can schedule an auto-invest plan at the wrong hour. <br>
Mitigation: Convert local execution times to UTC and show both UTC and local time in confirmations. <br>
Risk: The skill can read account balances, plan details, and trading history through Gate MCP tools. <br>
Mitigation: Limit execution to the named Gate MCP tools and preserve the documented user confirmation and privacy notices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gate-exchange/gate-exchange-autoinvest) <br>
- [Gate Auto-Invest scenario index](references/scenarios.md) <br>
- [Gate Auto-Invest plan lifecycle workflows](references/autoinvest-plans.md) <br>
- [Gate Auto-Invest rules, compliance, and funding source](references/autoinvest-compliance.md) <br>
- [Gate exchange runtime rules](https://github.com/gate/gate-skills/blob/master/skills/exchange-runtime-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown and structured MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before financial write actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact version 2026.4.2-3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
