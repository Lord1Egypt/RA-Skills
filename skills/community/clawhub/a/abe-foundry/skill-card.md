## Description:

Self-writing meta-extension that researches documentation, writes OpenClaw extensions, tools, hooks, and skills, and can learn from prior activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to research OpenClaw documentation and generate OpenClaw-compatible extensions, hooks, tools, and skill packages. It is intended for agent-assisted capability development that remains subject to human review before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and modify OpenClaw capabilities and learn from activity across sessions.

Mitigation: Use a pinned, reviewed plugin version; keep auto-learning and publishing disabled unless needed; review generated diffs before enabling them.

Risk: Task content may be sent to SkillBoss API Hub for LLM, search, and scraping functions.

Mitigation: Avoid using the skill with secrets or private code unless the provider and retention controls are acceptable.

Risk: The security summary flags mutable third-party code with powerful meta-programming behavior and limited scoping detail.

Mitigation: Install only when this behavior is acceptable for the workspace and review generated changes before deployment.

## Reference(s):

- [Foundry homepage](https://getfoundry.app)
- [SkillBoss API Hub](https://api.heybossai.com/v1/pilot)
- [Foundry Marketplace](https://api.claw.getfoundry.app)
- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/abe-foundry)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or generate OpenClaw extensions, hooks, tools, skills, and configuration changes for review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
