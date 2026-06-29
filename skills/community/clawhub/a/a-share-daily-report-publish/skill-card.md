## Description: <br>
This skill guides agents through collecting A-share market data from Tongdaxin MCP and Tonghuashun iWencai, then generating a 25-module local HTML recap report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinfa77-svg](https://clawhub.ai/user/jinfa77-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to collect daily A-share market data, assemble a structured report_data.json file, and generate an HTML recap for market review workflows. The report is informational and should not be treated as personalized investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated strategy, position-size, or stop-loss sections could be mistaken for personalized or professional investment advice. <br>
Mitigation: Treat the report as informational, verify market data independently, and apply qualified human review before making financial decisions. <br>
Risk: The workflow queries external market-data integrations and may run unintentionally if broad trigger phrases are used. <br>
Mitigation: Use explicit prompts, configure only trusted Tongdaxin and iWencai integrations, and protect any required API credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinfa77-svg/a-share-daily-report-publish) <br>


## Skill Output: <br>
**Output Type(s):** [text, html, shell commands, configuration, guidance] <br>
**Output Format:** [HTML report generated from JSON data, with workflow guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a-share-report-YYYY-MM-DD.html from report_data.json and a bundled HTML template.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
