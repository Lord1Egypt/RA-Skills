## Description: <br>
Official Easyship Integration. Ship, label, track & pickup across 550+ couriers in 200+ countries. Connects to mcp.easyship.com - no install required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulld](https://clawhub.ai/user/paulld) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to compare shipping rates, create and manage Easyship shipments, buy labels, track packages, schedule pickups, review billing history, validate addresses, and summarize shipping analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage shipments, buy shipping labels, schedule or cancel pickups, cancel or delete shipments, and query billing history through an Easyship account. <br>
Mitigation: Use the least-privileged Easyship token available and require user review before purchases, pickup scheduling, shipment cancellation or deletion, and billing queries. <br>
Risk: Shipping rates, customs values, addresses, and delivery estimates can be wrong when required details are missing or assumed. <br>
Mitigation: Confirm complete origin, destination, parcel, and customs details before acting, and label rate results as estimates when assumptions were used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paulld/easyship-official) <br>
- [Easyship MCP server](https://mcp.easyship.com) <br>
- [Easyship API token setup](https://app.easyship.com/connect) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown] <br>
**Output Format:** [Markdown responses with comparison tables, clickable document links, status summaries, pickup options, billing details, and analytics summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Easyship API access token in EASYSHIP_API_ACCESS_TOKEN.] <br>

## Skill Version(s): <br>
0.1.7 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
