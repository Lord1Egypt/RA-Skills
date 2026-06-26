## Description: <br>
Query and manage GPS travel data from Geomanic, a privacy-first GPS tracking platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weltspion](https://clawhub.ai/user/weltspion) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to connect OpenClaw to a Geomanic account, query travel statistics, inspect location history, and create, update, or delete GPS waypoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive GPS location history through a Geomanic account token. <br>
Mitigation: Store GEOMANIC_TOKEN as a secret, revoke or regenerate it when needed, and install the skill only when Geomanic location access is intended. <br>
Risk: Create, update, and delete waypoint actions can modify or remove GPS records. <br>
Mitigation: Verify waypoint IDs and keep query or edit ranges as narrow as practical before executing modifying actions. <br>


## Reference(s): <br>
- [Geomanic](https://geomanic.com) <br>
- [Geomanic API Key Management](https://geomanic.com/data) <br>
- [ClawHub Skill Page](https://clawhub.ai/weltspion/geomanic) <br>
- [OpenClaw](https://www.getopenclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with curl examples, configuration snippets, and JSON-RPC responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEOMANIC_TOKEN and uses ISO 8601 time ranges for waypoint and statistics queries.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
