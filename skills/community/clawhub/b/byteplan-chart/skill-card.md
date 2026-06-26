## Description: <br>
BytePlan Chat generates BytePlan AI data visualizations from user queries and supports 12 chart types, including line, bar, pie, heatmap, table, and dual-axis charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshuaiitr-ai](https://clawhub.ai/user/wangshuaiitr-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data analysts use this skill inside an agent to ask BytePlan business-data questions and receive generated visualizations across supported chart types. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores BytePlan credentials and uses them to request access tokens. <br>
Mitigation: Keep .env private, rotate credentials regularly, and use a limited or read-only BytePlan account where possible. <br>
Risk: Credential-backed requests are sent to the configured BYTEPLAN_BASE_URL. <br>
Mitigation: Verify BYTEPLAN_BASE_URL points to the intended BytePlan host before running the skill. <br>
Risk: The default documented scope is write, which may be broader than needed for chart generation. <br>
Mitigation: Avoid write scope unless required for the deployment and prefer the narrowest available account permissions. <br>
Risk: Business queries and resulting data may be sent to BytePlan's configured API endpoint. <br>
Mitigation: Avoid sensitive business queries unless the endpoint, account, and data handling expectations have been approved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangshuaiitr-ai/byteplan-chart) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [RELEASE-NOTES.md](artifact/RELEASE-NOTES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Console text plus generated PNG chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates timestamped chart images under the configured chart output directory after credential-backed BytePlan API calls.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence and RELEASE-NOTES.md; package.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
