## Description: <br>
Fetch and compare mainstream coffee prices (latte, americano, etc.) from major chains like Starbucks, Luckin, and Cotti for a given Chinese city and output them as a table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Realank](https://clawhub.ai/user/Realank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and agents use this skill to estimate and compare common coffee prices across Starbucks, Luckin, and Cotti for Chinese cities. It is suited for quick pricing benchmarks and brand comparisons where reference prices are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides rough reference prices that may differ from official store, app, promotion, or reimbursement prices. <br>
Mitigation: Use the generated table for benchmarking only and verify official app or ordering mini-program prices for financial or reimbursement decisions. <br>
Risk: When no city is provided, the script may contact ipinfo.io to infer location from IP data. <br>
Mitigation: Pass --city explicitly or set OPENCLAW_CITY when location lookup is not desired. <br>
Risk: The requests dependency is declared with a minimum version rather than an exact pin. <br>
Mitigation: Pin dependencies before installation in sensitive or reproducible environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Realank/coffee-prices) <br>
- [ipinfo.io city lookup endpoint](https://ipinfo.io/json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, shell commands, guidance] <br>
**Output Format:** [Markdown table by default, with optional JSON or CSV output from the CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CNY reference prices by city, brand, and drink; prices are estimates rather than authoritative menu prices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
