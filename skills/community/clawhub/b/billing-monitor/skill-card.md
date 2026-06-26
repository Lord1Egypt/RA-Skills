## Description: <br>
Monitors API billing errors, alerts owner and admin contacts, and guides fallback model switching when provider billing failures affect an agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent operators use this skill to detect provider billing failures, notify the owner and admin, log the incident, and switch to a configured fallback model when service continuity is affected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Silent scheduled checks can use provider API keys and write billing status without direct user visibility. <br>
Mitigation: Limit deployment to trusted environments, protect local context files, and review logs and cron schedules before enabling automated checks. <br>
Risk: Automatic fallback model changes can alter agent behavior or cost profile. <br>
Mitigation: Validate fallback model configuration in advance and require human approval before persistent model switching. <br>
Risk: Peer-agent billing reports could trigger escalation or operational changes without direct provider confirmation. <br>
Mitigation: Treat peer reports as signals for admin review and confirm billing status with provider checks before lasting changes. <br>


## Reference(s): <br>
- [Billing Monitor on ClawHub](https://clawhub.ai/netanel-abergel/billing-monitor) <br>
- [Anthropic Messages API](https://api.anthropic.com/v1/messages) <br>
- [OpenAI Chat Completions API](https://api.openai.com/v1/chat/completions) <br>
- [Google Generative Language Models API](https://generativelanguage.googleapis.com/v1beta/models) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes alert text, logging commands, health-check logic, and fallback configuration guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
