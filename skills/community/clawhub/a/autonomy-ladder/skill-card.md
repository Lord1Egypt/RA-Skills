## Description: <br>
A 3-tier decision framework that defines when your AI agent should act independently, report with detail, or ask before proceeding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeytbuilds](https://clawhub.ai/user/joeytbuilds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to define practical autonomy boundaries for agents, especially when deciding whether an agent should act immediately, report in detail, or wait for approval. It provides copy-ready guidance for MEMORY.md, SOUL.md, and HEARTBEAT.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default autonomy examples include sensitive actions such as credential rotation, production deployment, refunds, pull request merges, infrastructure scaling, and customer-facing communication. <br>
Mitigation: Customize the ladder before installation and keep sensitive actions approval-gated until explicit limits, runbooks, health checks, rollback procedures, cost caps, and audit logging are in place. <br>
Risk: A stale or overly broad ladder can grant more autonomy than the user currently intends. <br>
Mitigation: Review the ladder regularly, demote actions that cause issues, and default unclear actions to the more cautious tier. <br>


## Reference(s): <br>
- [Autonomy Ladder on ClawHub](https://clawhub.ai/joeytbuilds/autonomy-ladder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with copy-ready configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No runtime tool calls or external services are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
