## Description: <br>
Transform your agent from chatbot to copilot with context persistence, proactive anticipation, and opinionated help across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents used by developers, knowledge workers, creative workers, and operators use this skill to maintain local work context, anticipate relevant follow-ups, and provide opinionated help across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages persistent local memory that may capture sensitive work context. <br>
Mitigation: Require explicit user opt-in before creating or updating copilot state files, avoid storing secrets or regulated data, and periodically review or delete saved files. <br>
Risk: The skill may encourage broad proactive inspection of work tools such as screenshots, Slack, email, calendar, deployment monitoring, or production systems. <br>
Mitigation: Require explicit user consent before using screenshots, messaging, email, calendar, deployment monitoring, or production actions, and keep production actions behind confirmation. <br>
Risk: Proactive recommendations can interrupt users or act on stale context. <br>
Mitigation: Read current state before responding, stay silent on routine heartbeats when there is no useful update, and ask a clarifying question when context is stale. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/copilot) <br>
- [Context-Specific Behaviors](artifact/contexts.md) <br>
- [Implementation Details](artifact/implementation.md) <br>
- [State File Templates](artifact/templates.md) <br>
- [Copilot Interaction Examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with state-file templates and suggested interaction commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to read and update local context files and to ask for confirmation before higher-risk actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
