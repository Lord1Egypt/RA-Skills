## Description: <br>
Explains how to call Facebook Graph API endpoints through baiz.ai's proxy using a BAIZ_API_TOKEN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evte](https://clawhub.ai/user/evte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure agents or workflows that route Facebook Graph API requests through baiz.ai with a baiz.ai bearer token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes Facebook Graph API activity through baiz.ai and may expose broad Facebook asset access through the proxy token. <br>
Mitigation: Use only Baiz and Facebook accounts you control, verify token scope before use, and prefer least-privilege test accounts. <br>
Risk: Write, delete, budget, campaign, account, or bulk operations can affect live Facebook advertising resources. <br>
Mitigation: Require explicit human approval before any state-changing or spend-related operation. <br>
Risk: Uploads or request bodies may contain sensitive campaign or asset data handled by a third-party service. <br>
Mitigation: Avoid sensitive uploads unless baiz.ai's data handling is trusted and approved for the intended use. <br>


## Reference(s): <br>
- [baiz.ai homepage](https://baiz.ai) <br>
- [ClawHub skill page](https://clawhub.ai/evte/fb-graph-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls] <br>
**Output Format:** [Markdown with HTTP request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a sensitive BAIZ_API_TOKEN and uses baiz.ai as a third-party proxy for Facebook Graph API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
