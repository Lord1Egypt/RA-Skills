## Description: <br>
AI-powered DP Platform Operations Advisor monitors, diagnoses, and advises on DP Data Processing Platform job operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hxp365](https://clawhub.ai/user/hxp365) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to check DP platform job health, analyze throughput and stalls, diagnose failures, recommend fixes, and prepare incident summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles DP_API_KEY credentials and calls a DP platform endpoint. <br>
Mitigation: Install only for trusted DP platform endpoints, use HTTPS, and provide a least-privilege DP_API_KEY. <br>
Risk: Operational workflows may include restart or other state-changing actions. <br>
Mitigation: Require explicit user confirmation with the exact job ID before any restart or state-changing action. <br>
Risk: Authentication fallback or re-login behavior could broaden access beyond the intended API-key boundary. <br>
Mitigation: Use DP_API_KEY authentication only and do not allow the agent to attempt re-login or alternate authentication methods. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hxp365/dp-ops-advisor) <br>
- [Publisher profile](https://clawhub.ai/user/hxp365) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured operations sections and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DP_SERVER_URL and a least-privilege DP_API_KEY; may propose DP platform API calls and state-changing actions that require explicit confirmation.] <br>

## Skill Version(s): <br>
2.0.1 (source: server-resolved release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
