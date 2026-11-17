## Description:

Micro-tier governance skill for small AI agent organizations (1-3 agents). Consolidates 18 enterprise function blocks into two departments, governance-and-delivery and engineering-and-safety, covering strategy, risk, compliance, architecture, safety, and delivery. Ships ten harness code templates, three prompt frameworks, a full error-code catalog, and a scaling specification. Provides two self-contained human-paste prompts (method implementation, robustness checks) usable in any AI chat window. Source files are authored in English; runtime output follows the user's language per the language policy, with English fallback. Includes propose-only self-scaling that evaluates scaling thresholds and proposes tier upgrades up to group. Use when a small team needs enterprise-grade governance, engineering harnesses, PII masking, AIGC disclosure, or tier-upgrade assessment for its agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsmithfan](https://clawhub.ai/user/johnsmithfan)

### License/Terms of Use:

GPL-3.0

## Use Case:

Developers, operators, and small AI agent teams use this skill to route governance, delivery, engineering, safety, compliance, PII masking, audit-trace, and tier-upgrade assessment work across a micro-tier agent organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports broad workspace read/write and agent-session/subagent permissions with under-disclosed side effects.

Mitigation: Install only in workspaces where those authorities are acceptable, and review expected state-file updates and generated upgrade packages before use.

Risk: Self-scaling actions can create tier-upgrade proposals and alter operational state.

Mitigation: Run self-scaling actions manually after review; keep tier changes human-approved and inspect generated upgrade packages before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnsmithfan/skills/ai-company)
- [Server-resolved GitHub source](https://github.com/JohnSmithfan/AI-Company)
- [Governance and Delivery Department](references/departments/governance-and-delivery.md)
- [Engineering and Safety Department](references/departments/engineering-and-safety.md)
- [Method Patterns](references/method-patterns.md)
- [Error Codes](references/error-codes.md)
- [Self-Scaling Governance Reference](references/scaling.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured text with optional code, command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime output follows the user's requested language when provided, with English fallback; immutable identifiers such as slugs, error codes, file paths, and function names remain untranslated.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, CHANGELOG, and artifact _meta.json; server release metadata reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
