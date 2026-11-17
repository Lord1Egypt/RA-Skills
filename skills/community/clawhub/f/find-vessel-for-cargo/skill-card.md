## Description: <br>
Finds domestic or international empty vessels for cargo owners using loading port, discharge port, cargo name, tonnage, and expected loading date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linyihuang1992-ops](https://clawhub.ai/user/linyihuang1992-ops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Shipping and chartering users use this skill to match cargo demand against available domestic or international empty vessels, review ranked candidates, and open structured vessel details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cargo demand details may be sent to a configured backend endpoint or queued locally when the endpoint is unavailable. <br>
Mitigation: Configure the endpoint deliberately, inform users about demand submission and local queuing, and protect or clean the outbox and cache directories. <br>
Risk: The local uvicorn service can expose vessel search and detail endpoints if bound to an untrusted network. <br>
Mitigation: Run the service on localhost or a trusted network unless authentication and network controls are in place. <br>
Risk: Vessel details can include public contact information. <br>
Mitigation: Use only returned public data, avoid bypassing access controls, and review contact handling before shared or production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linyihuang1992-ops/skills/find-vessel-for-cargo) <br>
- [Backend API reference](references/backend-api.md) <br>
- [航运在线空船数据源](https://chartering.sol.com.cn) <br>
- [UN/LOCODE dataset](https://raw.githubusercontent.com/datasets/un-locode/main/data/code-list.csv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or text summaries with detail actions, plus JSON service responses when used through the local API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are limited to returned source data and mark uncertain tonnage, open-port, or open-date fields for manual confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
