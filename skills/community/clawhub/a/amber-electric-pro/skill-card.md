## Description: <br>
Access real-time electricity prices, 24-hour forecasts, and site details from Amber Electric. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingmaxmmxweisun](https://clawhub.ai/user/kingmaxmmxweisun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to read Amber Electric account sites, current electricity prices, and 24-hour price forecasts for energy-aware decisions. <br>

### Deployment Geography for Use: <br>
Australia <br>

## Known Risks and Mitigations: <br>
Risk: The configured Amber API key allows the skill to read Amber site identifiers and electricity pricing data. <br>
Mitigation: Configure AMBER_API_KEY only in trusted agent environments and rotate or revoke the key if the environment is no longer trusted. <br>
Risk: Server evidence reports unavailable source provenance and a minor version mismatch between release evidence and artifact metadata. <br>
Mitigation: Verify the publisher profile and package version before installing when source provenance is important. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingmaxmmxweisun/amber-electric-pro) <br>
- [Amber Electric API base endpoint](https://api.amber.com.au/v1) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Configuration] <br>
**Output Format:** [JSON responses from Amber Electric API endpoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMBER_API_KEY; site_id is required for current price and forecast actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact _meta.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
