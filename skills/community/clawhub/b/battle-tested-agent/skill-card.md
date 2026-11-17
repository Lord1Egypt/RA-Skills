## Description:

Provides 19 production-hardened patterns and an audit script for hardening SKILL.md-based agents against memory loss, hallucination, weak handoffs, stale delegated work, and unreliable verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit and harden SKILL.md-based agent workspaces by adding reliability, verification, memory, delegation, and recovery patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory, WAL, and learning templates can retain sensitive user content, secrets, or private links if copied into a real workspace without controls.

Mitigation: Require explicit user approval before retaining personal or sensitive information, redact secrets and private links, and define retention and deletion rules before enabling persistent memory patterns.

Risk: Self-improvement and auto-promotion guidance can turn transient mistakes into persistent agent rules without enough review.

Mitigation: Make all SOUL.md, AGENTS.md, and recurring-rule changes human-reviewed, and treat templates as proposals rather than automatic updates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zurbrick/skills/battle-tested-agent)
- [Starter Patterns](references/starter-patterns.md)
- [Intermediate Patterns](references/intermediate-patterns.md)
- [Advanced Patterns](references/advanced-patterns.md)
- [Audit Usage](references/audit-usage.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples and reusable workspace templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an audit shell script and optional workspace templates; requires bash, grep, find, and wc.]

## Skill Version(s):

1.5.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
