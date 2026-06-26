## Description: <br>
Gate platform activity and campaign hub skill for activity recommendations, airdrops, trading competitions, and enrolled activity lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents with a configured Gate MCP session use this skill to find Gate campaigns, filter activities by type or scenario, and open their enrolled activity entry. The workflow is read-only and requires Gate API credentials with Activity:Read permission. <br>

### Deployment Geography for Use: <br>
Global, subject to Gate activity availability and user region restrictions. <br>

## Known Risks and Mitigations: <br>
Risk: Generic prompts such as "my activities" or "what activities" can unexpectedly invoke a configured Gate exchange API session for activity lookups. <br>
Mitigation: Clarify ambiguous short prompts before invoking the skill and frame results as Gate activity-center data. <br>
Risk: A broad or reused Gate API key could expose more account capability than this read-only workflow needs. <br>
Mitigation: Use a dedicated Gate API key limited to Activity:Read and keep GATE_API_KEY and GATE_API_SECRET in the local MCP configuration, not chat. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gate-exchange/gate-exchange-activitycenter) <br>
- [OpenClaw metadata homepage](https://github.com/gate/gate-skills) <br>
- [Gate runtime rules](references/gate-runtime-rules.md) <br>
- [Gate ActivityCenter MCP specification](references/mcp.md) <br>
- [Activity scenarios and prompt examples](references/scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown activity cards, tables, links, and short status or setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Gate activity-center queries; activity list responses are limited to 3 activities per request.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact SKILL.md version 2026.4.3-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
