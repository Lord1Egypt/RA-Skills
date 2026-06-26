## Description: <br>
Automatically monitors AI model updates and free token offers, generates weekly deployment recommendations, and helps approve, update, or roll back OpenClaw model routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hhbb2221](https://clawhub.ai/user/hhbb2221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to track model availability, free token offers, and weekly model-routing recommendations. It can support human-approved updates to an OpenClaw fallback chain with backup and rollback commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change OpenClaw model routing through approve, reject, deploy, and rollback actions. <br>
Mitigation: Review proposed routing changes before execution, keep backups, and verify service behavior after gateway restart. <br>
Risk: Scheduled jobs perform recurring external model and news collection. <br>
Mitigation: Enable the daily and weekly schedules only when recurring external monitoring is acceptable for the deployment environment. <br>
Risk: The skill reads an OpenRouter API key and can influence model choice, cost, and availability. <br>
Mitigation: Use a least-privileged API key, protect local OpenClaw configuration, and validate recommendations before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hhbb2221/ai-model-steward) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/hhbb2221) <br>
- [OpenRouter models API](https://openrouter.ai/api/v1/models) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text, JSON status objects, Markdown weekly reports, and OpenClaw configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local cache files, weekly report files, OpenClaw routing changes, and configuration backups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact files list 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
