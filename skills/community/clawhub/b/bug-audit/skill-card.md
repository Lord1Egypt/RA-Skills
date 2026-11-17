## Description:

Comprehensive bug audit for Node.js web projects that guides an agent to dissect project code into audit tables, verify each item, run adversarial checks, and report concrete bugs and fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abczsl520](https://clawhub.ai/user/abczsl520)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to audit Node.js web projects, including games, dashboards, API services, bots, WeChat apps, and data tools. It helps an agent build project-specific check matrices, verify security and logic risks, and produce actionable bug reports with fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit procedures can include network, load, authentication-bypass, SSRF, upload, or data-exposure testing that may disrupt systems or access sensitive data.

Mitigation: Use the skill only for authorized audits of systems you own or are approved to test, preferably in local or staging environments, and require explicit approval before disruptive or intrusive tests.

Risk: Debug logging and debug panel snippets in the artifact could expose sensitive data or unsafe DOM rendering if copied into production as-is.

Mitigation: Do not deploy those snippets to production without authentication, redaction, rate limits, retention limits, and safe DOM rendering.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abczsl520/skills/bug-audit)
- [Audit Modules](references/modules.md)
- [Pitfall Lookup Table](references/pitfalls.md)
- [Red Team / Blue Team Playbook](references/redblue.md)
- [Bug Audit Skill Wiki](https://github.com/abczsl520/bug-audit-skill/wiki)
- [Dissection Workflow Details](https://github.com/abczsl520/bug-audit-skill/wiki/解剖流程详解)
- [Audit Module Overview](https://github.com/abczsl520/bug-audit-skill/wiki/排查模块一览)
- [Practical Pitfall Reference](https://github.com/abczsl520/bug-audit-skill/wiki/实战踩坑速查)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown audit findings with tables, severity labels, file references, fixes, and optional code or shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be based on the target project's actual code and should distinguish verified findings from items checked as OK.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
