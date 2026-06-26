## Description: <br>
Anti Cheating Assistant helps model business workflows, analyze fraud and business-security risks, and propose risk-control solutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jshdcn](https://clawhub.ai/user/jshdcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business, risk, and security teams use this skill to clarify business flows, create three-flow business models, identify possible cheating or fraud risks, and request targeted risk-control recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Business names and workflow details may be embedded in external visualization URLs. <br>
Mitigation: Avoid entering confidential processes, customer data, trade secrets, or regulated business information unless diagrams are generated locally or the user explicitly consents to external link creation. <br>
Risk: The solution workflow may require an external MCP/API service and an API key. <br>
Mitigation: Confirm the endpoint and credential handling with the publisher before use, and provide general guidance when the knowledge retrieval service is unavailable or unauthorized. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jshdcn/anti-cheating-assistant) <br>
- [Risk problems table](references/risk-problems-table.md) <br>
- [Solution MCP interface](references/solution-list.md) <br>
- [Three-flow graph analysis workflow](scripts/three_flow_graph_analysis.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown responses with structured questions, business-flow summaries, risk findings, solution recommendations, diagram links, and tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include external visualization links and MCP/API examples when relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
