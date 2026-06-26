## Description: <br>
Query Anthropic Admin API for token usage reports (daily, weekly, monthly) with model breakdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leaofelipe](https://clawhub.ai/user/leaofelipe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering managers, and Anthropic organization administrators use this skill to inspect Anthropic token usage across daily, weekly, and monthly windows, including optional per-model breakdowns and cost estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to an Anthropic Admin API key and organization usage data. <br>
Mitigation: Install only when that access is intended, configure the key through the OpenClaw API key field or direct config entry, and do not paste the Admin API key into chat. <br>
Risk: The skill makes external requests to api.anthropic.com and may fetch anthropic.com/pricing for cost estimates. <br>
Mitigation: Review and approve those network destinations before use in restricted environments. <br>
Risk: The security summary reports that one script error path asks users to paste the key into chat. <br>
Mitigation: Before installation or publication, revise that guidance so all key handling uses the OpenClaw key field or local config only. <br>


## Reference(s): <br>
- [ClawHub Anthropic Usage skill page](https://clawhub.ai/leaofelipe/anthropic-usage) <br>
- [OpenClaw](https://openclaw.dev) <br>
- [Anthropic pricing](https://www.anthropic.com/pricing) <br>
- [Anthropic usage report API endpoint](https://api.anthropic.com/v1/organizations/usage_report/messages) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown tables and concise explanatory text, with shell commands when invoking or checking the usage script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and ANTHROPIC_ADMIN_API_KEY; cost estimates may use current rates from anthropic.com/pricing.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence and target metadata; artifact _meta.json reports 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
