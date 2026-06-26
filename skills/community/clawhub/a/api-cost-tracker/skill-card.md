## Description: <br>
Track AI API costs across OpenAI, Anthropic, Google AI with budget alerts, analytics, and optimization tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k5rs4n](https://clawhub.ai/user/k5rs4n) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use this skill to monitor AI API spending, review budget status, generate cost reports, and compare provider/model usage across OpenAI, Anthropic, and Google AI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal CLI usage records demo API spend, so generated reports and budget alerts can be misleading. <br>
Mitigation: Remove or explicitly gate demo data before relying on reports, scheduled runs, or budget alerts. <br>
Risk: Automated monitoring can amplify misleading cost data if scheduled before real provider collection is clear. <br>
Mitigation: Validate the real usage collection path and review generated cost files before adding scheduled runs or alert webhooks. <br>
Risk: Provider API keys and alert webhooks may be configured for normal use. <br>
Mitigation: Use environment variables for credentials and avoid providing webhooks until the data source and alert behavior have been reviewed. <br>


## Reference(s): <br>
- [API Cost Tracker on ClawHub](https://clawhub.ai/k5rs4n/api-cost-tracker) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output, Markdown reports, JSON reports, CSV reports, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local cost history under the configured data directory when tracking runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
