## Description: <br>
Check AI token usage, quotas, and costs across Anthropic and other providers using Anthropic OAuth API and OpenClaw session logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bshandley](https://clawhub.ai/user/bshandley) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Anthropic quota utilization, OpenClaw session token counts, request counts, and AI cost signals for local monitoring or reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Claude Code credentials and OpenClaw session logs to report AI usage. <br>
Mitigation: Install only when that access is acceptable, review the script before scheduling it, and keep cron or dashboard use under the user's control. <br>
Risk: Usage reports may expose provider, model, token, request, quota, or cost data. <br>
Mitigation: Avoid sharing generated reports when those usage details are private or sensitive. <br>


## Reference(s): <br>
- [AI Usage on ClawHub](https://clawhub.ai/bshandley/ai-usage) <br>
- [Anthropic OAuth usage API endpoint](https://api.anthropic.com/api/oauth/usage) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text report or JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No pip dependencies; requires local Claude Code authentication for Anthropic quota data and OpenClaw session logs for provider usage statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
