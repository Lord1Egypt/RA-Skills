## Description: <br>
Build Protocol Decision guides agents through rigorous, auditable workflows for high-stakes decisions such as investments, major purchases, technology selection, supplier choice, and other hard-to-reverse commitments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[christianye](https://clawhub.ai/user/christianye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users use this skill to structure, compare, audit, and document consequential choices before committing money, time, or operational effort. It is especially oriented toward financial decisions, purchases, vendor selection, and buy-versus-build tradeoffs that require live data, explicit methodology, risk limits, and post-decision tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports consequential financial and operational decisions, so agent output could influence investment, purchase, vendor, or technology commitments. <br>
Mitigation: Use independent judgment, review assumptions, and treat the workflow as decision support rather than an authority to commit funds or execute trades. <br>
Risk: Market prices, vendor pricing, product listings, and other decision inputs can become stale quickly. <br>
Mitigation: Fetch current data from live sources, record timestamps, and explicitly mark data as unavailable rather than substituting document or chat-history prices. <br>
Risk: The optional audit script reads the decision document path supplied by the user and may surface sensitive decision details in local output. <br>
Mitigation: Run the script only on intended local documents and review files for sensitive content before sharing audit output. <br>
Risk: False precision can make estimates appear more reliable than the underlying data supports. <br>
Mitigation: Label estimates, round uncertain numbers appropriately, show methodology, and include downside cases and exit conditions. <br>


## Reference(s): <br>
- [Decision Workflow](references/decision-workflow.md) <br>
- [Investment Playbook Template](references/investment-playbook-template.md) <br>
- [Decision Audit Script](references/audit-script-decision.sh) <br>
- [ClawHub Skill Page](https://clawhub.ai/christianye/build-protocol-decision) <br>
- [Stooq Quote CSV Endpoint](https://stooq.com/q/l/?s=SYMBOL.us&f=sd2t2ohlcv&h&e=csv) <br>
- [Yahoo Finance Chart Endpoint](https://query1.finance.yahoo.com/v8/finance/chart/SYMBOL) <br>
- [CoinGecko Simple Price API](https://api.coingecko.com/api/v3/simple/price) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code] <br>
**Output Format:** [Markdown guidance with checklists, decision matrices, templates, and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live data fetch commands, decision records, audit findings, risk controls, stop-loss rules, and P/L tracking templates.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
