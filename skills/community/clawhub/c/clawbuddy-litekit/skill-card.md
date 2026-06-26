## Description: <br>
Open the ClawBuddy LiteKit mission-control dashboard for AI agents with live OpenClaw Gateway status, agent profiles, task boards, meeting intelligence, council debates, and AI logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevekaplanai](https://clawhub.ai/user/stevekaplanai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to open a hosted mission-control dashboard, check Gateway connection status, inspect agent activity, and walk through OpenClaw setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a hosted ClawBuddy dashboard and Lovable/Supabase service with the user's OpenClaw environment. <br>
Mitigation: Install only if that hosted service is acceptable for the environment and review the dashboard and status endpoints before use. <br>
Risk: OpenClaw setup requires OPENCLAW_API_KEY, which is sensitive. <br>
Mitigation: Use a scoped or revocable key when possible, store it only in the intended cloud secret manager, and rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/stevekaplanai/clawbuddy-litekit) <br>
- [Live ClawBuddy dashboard](https://agentcommander.lovable.app) <br>
- [OpenClaw integration reference](references/openclaw.md) <br>
- [OpenClaw Gateway docs](https://openclaw-openclaw.mintlify.app/concepts/gateway) <br>
- [OpenResponses HTTP API](https://documentation.openclaw.ai/gateway/openresponses-http-api) <br>
- [OpenClaw Agent Protocol](https://openclaw-openclaw.mintlify.app/api/agent-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open a hosted dashboard or return dashboard and status URLs; the status command emits the hosted OpenClaw status response.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
