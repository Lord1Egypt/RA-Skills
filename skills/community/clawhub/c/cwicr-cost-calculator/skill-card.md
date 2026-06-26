## Description: <br>
Calculate construction costs using DDC CWICR resource-based methodology. Break down costs into labor, materials, equipment with transparent pricing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External construction estimators, project teams, and developers use this skill to prepare transparent resource-based cost estimates, compare options, and show labor, material, equipment, overhead, and profit components. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local quantity, cost, or pricing files may contain sensitive project data. <br>
Mitigation: Grant filesystem access only to the specific files the agent needs for the current estimate. <br>
Risk: Cost estimates can be wrong when resource norms, regional factors, or current prices are incomplete or outdated. <br>
Mitigation: Verify pricing assumptions and calculation inputs before relying on outputs for bids, budgets, or commitments. <br>
Risk: Example Python package installs may affect the local environment. <br>
Mitigation: Review package installation commands and use a controlled environment when adding dependencies such as pandas or numpy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/cwicr-cost-calculator) <br>
- [Publisher profile](https://clawhub.ai/user/datadrivenconstruction) <br>
- [Data Driven Construction homepage](https://datadrivenconstruction.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with cost breakdowns, comparisons, and concise calculation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default currency is USD unless the user requests another currency; outputs separate labor, material, equipment, overhead, profit, unit cost, and total cost when enough inputs are available.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
