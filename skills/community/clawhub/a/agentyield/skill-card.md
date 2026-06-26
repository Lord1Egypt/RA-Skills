## Description: <br>
Automatic waste detection and cost optimization for every LLM and tool call. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[philg](https://clawhub.ai/user/philg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use AgentYield.co to observe LLM and tool-call activity, send redacted telemetry to AgentYield, and identify waste or cost-optimization opportunities without transmitting raw prompts, model outputs, tool inputs, or tool outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends redacted OpenClaw usage telemetry to AgentYield's service for cost analysis. <br>
Mitigation: Install only when that telemetry flow is intended, review retention and deletion controls, and use a test key for evaluation. <br>
Risk: The skill requires an AgentYield API key scoped to a user account. <br>
Mitigation: Keep AGENTYIELD_API_KEY in the environment, prefer ay_test_ keys during evaluation, and revoke unused or exposed keys from AgentYield settings. <br>


## Reference(s): <br>
- [AgentYield homepage](https://agentyield.co) <br>
- [AgentYield skill source](https://agentyield.co/skills/agentyield.md) <br>
- [AgentYield developer SDK](https://agentyield.co/developer/sdk) <br>
- [AgentYield retention and privacy controls](https://agentyield.co/privacy) <br>
- [AgentYield data deletion documentation](https://agentyield.co/docs#data-deletion) <br>
- [ClawHub skill page](https://clawhub.ai/philg/agentyield) <br>
- [Publisher profile](https://clawhub.ai/user/philg) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API Calls, Telemetry] <br>
**Output Format:** [Markdown guidance with JSON event schemas and HTTPS API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENTYIELD_API_KEY; sends limited, redacted usage telemetry to AgentYield for cost analysis.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter version 0.6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
