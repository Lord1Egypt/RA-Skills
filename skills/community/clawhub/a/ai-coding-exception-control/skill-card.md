## Description:

Chinese-language coding workflow that guides agents through research, requirements, design, exception-first implementation, testing, review, and lesson capture to reduce missing error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llimage](https://clawhub.ai/user/llimage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to structure AI-assisted software work around failure scenarios, exception handling, automated testing, audit handoff, and post-task lesson capture. It is most useful for non-trivial feature work where requirements, design, implementation, tests, and review need explicit quality gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly auto-activates on generic coding, design, test, review, and refactoring requests.

Mitigation: Install it only in contexts that intentionally use this heavyweight workflow, or narrow the trigger phrases before deployment.

Risk: The workflow directs agents to write persistent lessons and modify skill or SOP files.

Mitigation: Require explicit user approval for persistent writes and review diffs before accepting skill, SOP, or memory changes.

Risk: The workflow mandates web research and may encourage logging raw request context.

Mitigation: Redact confidential project, customer, credential, and personal data before searches or logs, and disable web research where policy requires offline work.

Risk: The testing guidance includes chaos-test actions against containers and services.

Mitigation: Run chaos tests only in isolated mock or staging environments with explicit approval, never against production or shared infrastructure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/llimage/skills/ai-coding-exception-control)
- [README](README.md)
- [Requirements and design SOP](references/requirements-design-sop.md)
- [Coding SOP](references/coding-sop.md)
- [Testing SOP](references/testing-sop.md)
- [Lessons feedback loop SOP](references/lessons-feedback-loop.md)
- [Audit-Ledger handoff specification](references/audit-ledger-spec.md)
- [Template collection](references/templates.md)
- [OPC development suite overview](references/OPC-DEVELOPMENT-SUITE.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Chinese-language Markdown guidance with checklists, templates, code snippets, and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent lesson records, skill/SOP edits, web research, and chaos-test commands; review before execution.]

## Skill Version(s):

1.7.0 (source: SKILL.md frontmatter and server release metadata, released 2026-07-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
