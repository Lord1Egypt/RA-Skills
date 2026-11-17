## Description:

byted-livesaas-master helps agents operate Volcengine Enterprise Live / LiveSaaS workflows through the bytedlive CLI, including live room lifecycle management, comments, system messages, audience controls, product-card operations, analytics, account queries, media maintenance, and OpenAPI fallback calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcvneomnistreambot](https://clawhub.ai/user/volcvneomnistreambot)

### License/Terms of Use:

MIT-0

## Use Case:

External LiveSaaS operators, support agents, and developers use this skill to configure and manage Volcengine Enterprise Live rooms, comments, audience moderation, product cards, analytics, and related OpenAPI actions from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install global npm tools.

Mitigation: Use it only where global npm installs are acceptable, and prefer preinstalling a vetted pinned CLI from a trusted HTTPS source.

Risk: The skill uses cached LiveSaaS account credentials for account-control actions.

Mitigation: Avoid broad credentials on machines with unrelated sensitive data, and use credentials appropriate to the intended LiveSaaS operations.

Risk: The skill sends startup telemetry by default.

Mitigation: Disable telemetry when policy requires it before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcvneomnistreambot/skills/byted-livesaas-master)
- [Volcengine Enterprise Live documentation center](https://www.volcengine.com/docs)
- [Volcengine Enterprise Live API reference](https://www.volcengine.com/docs/3019/66792?lang=zh)
- [Volcengine Enterprise Live release history](https://www.volcengine.com/docs/3019/129183?lang=zh)
- [OpenAPI action version reference](references/data/openapiActionVersions.json)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown]

**Output Format:** [Markdown responses with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute or propose bytedlive / bytedlive-b CLI commands and OpenAPI calls after credential checks and safety gating.]

## Skill Version(s):

1.1.4 (source: frontmatter; release metadata version 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
