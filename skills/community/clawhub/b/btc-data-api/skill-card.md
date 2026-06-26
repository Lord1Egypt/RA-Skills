## Description: <br>
查询比特币链上结构数据（UTXO、大额流出、筹码分布、持仓结构、链上指标等）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengcheche-0](https://clawhub.ai/user/fengcheche-0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to query Bitcoin on-chain structure and metric tables from a command-line API helper. It supports latest-record, recent-limit, date-based, field, field-limit, and field-date queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill calls a disclosed HTTP API endpoint without transport encryption. <br>
Mitigation: Use it only when you trust and intend to use the API at 10.168.1.162:9000, and avoid passing unrelated sensitive values in query arguments. <br>
Risk: The helper depends on the Python requests package being available. <br>
Mitigation: Confirm the runtime has python3 and requests installed before relying on the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengcheche-0/btc-data-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; API helper prints JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the Python requests package; calls a disclosed HTTP API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
