## Description:

企业级沟通智能系统，支持跨渠道消息管理、情感分析、关系图谱与沟通策略优化，并为沟通协作场景提供标准化流程和配置参考。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, enterprise teams, and developers use this skill to draft, review, and structure workplace communications, customer replies, and team communication workflows. It also describes batch operations, audit logging, webhook notifications, and configuration patterns for communication automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence rates the skill as suspicious because it requests broad file, shell, and external integration behavior that is not consistently scoped.

Mitigation: Install and run it only with least-privilege tools, and require explicit confirmation before command execution, API calls, webhook notifications, exports, or batch operations.

Risk: Communication content may include sensitive business, customer, or employee information, and some documented workflows involve external APIs or callbacks.

Mitigation: Avoid sensitive message content unless external transfer is acceptable, redact secrets and personal data where possible, and verify callback URLs before use.

Risk: Generated communication drafts or strategy suggestions may be incomplete, inaccurate, or inappropriate for high-stakes decisions.

Mitigation: Treat outputs as drafts, require human review before sending messages, and avoid using the skill for decisions requiring deterministic or legally binding outcomes.

Risk: Batch operations, retries, and webhook notifications can amplify mistakes across many recipients or systems.

Mitigation: Test with a small scope first, apply rate limits, review operation logs, and confirm target lists and notification endpoints before full-scale use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/comm-skill-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with text examples, JSON configuration snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended as drafts, operational guidance, and configuration examples that should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
