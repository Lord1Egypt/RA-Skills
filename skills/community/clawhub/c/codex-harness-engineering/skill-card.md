## Description:

基于 OpenAI《Harness Engineering》实践的 Codex 工作规范。强调环境能力补齐、仓库即记录系统、严格分层架构、可观测可验证闭环、持续防漂移治理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmypeng4ios](https://clawhub.ai/user/jimmypeng4ios)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to guide Codex through multi-step repository work, PR review loops, documentation upkeep, architecture boundary enforcement, observability-driven validation, and long-term drift control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may encourage Codex to create or update repository documentation, lint rules, and pull requests.

Mitigation: Use normal code review, CI, and scan controls for generated repository changes.

Risk: The skill is written as Chinese-language workflow guidance and may not fit teams that require English-only operating instructions.

Mitigation: Install it only when Chinese-language workflow guidance is suitable for the team.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimmypeng4ios/skills/codex-harness-engineering)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Natural-language guidance with Markdown structure and repository change recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to create or update repository documentation, lint rules, tests, pull requests, logs, metrics, and review artifacts.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
