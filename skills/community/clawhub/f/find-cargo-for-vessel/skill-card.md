## Description: <br>
Recommends domestic or international cargo listings for shipowners from current port, destination port, and vessel capacity, then records the completed cargo-search demand. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linyihuang1992-ops](https://clawhub.ai/user/linyihuang1992-ops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shipping and chartering users use this skill to find cargo opportunities that match a vessel's current port, planned destination port, and available tonnage. The agent presents ranked cargo recommendations, clickable detail links, and contact details that are publicly available from the cargo source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically record and send shipowner demand data after successful cargo searches. <br>
Mitigation: Install only when demand recording is intended, configure API_BASE_URL and CARGO_DEMAND_API_PATH deliberately, and protect ADMIN_API_KEY or ADMIN_TOKEN. <br>
Risk: If backend sync is unavailable or disabled, demand records may be queued locally. <br>
Mitigation: Monitor or clear the local demand_outbox.jsonl queue when backend synchronization is disabled or failing. <br>
Risk: The FastAPI service does not define its own access controls. <br>
Mitigation: Deploy the service behind authentication or an internal gateway and restrict access to intended users. <br>


## Reference(s): <br>
- [ShippingClaw backend demand API](references/backend-api.md) <br>
- [航运在线 cargo listings](https://chartering.sol.com.cn) <br>
- [UN/LOCODE dataset](https://raw.githubusercontent.com/datasets/un-locode/main/data/code-list.csv) <br>
- [World Port Index query service](https://services9.arcgis.com/j1CY4yzWfwptbTWN/arcgis/rest/services/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown cargo recommendations with clickable links, plus JSON outputs from supporting scripts and service endpoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search requires current port, destination port, vessel capacity in tons, and user ID; successful searches may record demand data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
