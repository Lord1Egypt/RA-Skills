## Description:

Helps knowledge workers, content teams, consultants, and creators organize local files, web research, and AI-HIVE generation work into supervised Claude Cowork projects with plans, permission boundaries, media tasks, and result indexes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to turn Claude Cowork and AI-HIVE tasks into auditable project workflows. It is intended for planning model routing, cost and speed tradeoffs, permission gates, media generation tasks, and final acceptance records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An API key can be sent to an environment-configured endpoint.

Mitigation: Keep AI_HIVE_API_KEY in a secure local credential source and set AI_HIVE_BASE_URL only when the endpoint is fully trusted.

Risk: Broad implicit invocation can start planning in contexts where the user did not clearly choose this skill.

Mitigation: Prefer explicit invocation and review the plan before installing or executing the skill.

Risk: Paid, bulk, publishing, deletion, or account-access actions may have external or irreversible effects.

Mitigation: Require manual confirmation before any paid, bulk, publishing, deletion, or account-access action.

## Reference(s):

- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [Claude Cowork Product Guide](https://claude.com/blog/the-claude-cowork-product-guide)
- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ai-model-expert-hot-claude-cowork-desktop)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON plans and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project directories, permission boundaries, work plans, media task ledgers, and result indexes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
