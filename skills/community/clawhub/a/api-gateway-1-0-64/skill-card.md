## Description: <br>
Connect to 100+ APIs, including Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, and HubSpot, with managed OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larry-at](https://clawhub.ai/user/larry-at) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to call native third-party API endpoints and manage user-authorized service connections through Maton's OAuth-backed gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The gateway can expose broad write, delete, admin, billing, and webhook actions across connected services. <br>
Mitigation: Use least-privilege service connections and require explicit confirmation before write, delete, admin, billing, or webhook operations. <br>
Risk: Agents may use the default active connection when multiple connections exist for the same app. <br>
Mitigation: Specify the exact connection ID with the Maton-Connection header for sensitive or multi-account workflows. <br>
Risk: Connected services may include production finance, ads, identity, DNS, or legal systems. <br>
Mitigation: Avoid those systems without additional review controls and deploy only where Maton's brokered service access is trusted. <br>


## Reference(s): <br>
- [Maton homepage](https://maton.ai) <br>
- [Maton API reference](https://www.maton.ai/docs/api-reference) <br>
- [ClawHub skill page](https://clawhub.ai/larry-at/api-gateway-1-0-64) <br>
- [API Gateway skill source](artifact/SKILL.md) <br>
- [Bundled service references](artifact/references/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API request examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; third-party service access depends on user-authorized OAuth connections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata; artifact metadata version 1.0.64) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
