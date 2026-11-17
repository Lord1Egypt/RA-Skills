## Description:

Master the art of spawning and managing sub-agents. Write prompts that actually work, track running agents, and learn from every outcome.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to structure prompts for delegated research, build, and review work, track active sub-agents, and capture lessons from agent outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes optional routing of prompt messages to a third-party API endpoint.

Mitigation: Do not send private code, business documents, regulated data, secrets, or sensitive workspace content to that endpoint without approval and redaction rules.

Risk: The local agent-tracking workflow may leave persistent notes in the workspace.

Mitigation: Store tracking notes in approved locations and review them for sensitive task details before sharing or committing.

Risk: The security verdict is suspicious because the skill requires a third-party API key and lacks clear safeguards for full prompt payloads.

Mitigation: Review the skill before installation and treat remote API usage as optional unless the deployment has explicit data-handling approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abeltennyson/skills/abel-agent-orchestration)
- [Publisher Profile](https://clawhub.ai/user/abeltennyson)
- [Complete Setup Guide](https://skillboss.co/skill.md)
- [Active Agents Tracking Template](artifact/examples/active-agents.md)
- [Builder Agent Template](artifact/templates/builder-agent.md)
- [Research Agent Template](artifact/templates/research-agent.md)
- [Review Agent Template](artifact/templates/review-agent.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with prompt templates, command snippets, and example code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY only when using the optional SkillBoss API Hub example.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
