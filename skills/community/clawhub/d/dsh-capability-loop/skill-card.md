## Description:

A governance workflow for auditing, improving, validating, and iterating DSH skills, plugins, projects, and handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linboomboom](https://clawhub.ai/user/linboomboom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using DSH use this skill to audit and improve their environment, guide projects from intake through acceptance, and prepare checked handoff materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious for risky command execution, injected agent instructions, and state-changing actions. Scan coverage was partial: 54 of 63 components were fully inspected, and some content could not be fully parsed.

Mitigation: Consider avoiding installation until the command-execution path, instruction injection, state-changing actions, and antivirus guidance have been reviewed. Treat the partially inspected content as unevaluated.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/linboomboom/skills/dsh-capability-loop)
- [Project takeover and state guidance](references/02-takeover.md)
- [Audit guidance](references/10-audit.md)
- [Handoff guidance](references/60-handoff.md)
- [Review and evolution guidance](references/75-grill.md)
- [Store publishing guidance](references/95-store-publish.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown reports and checklists, shell commands, code examples, and JSON or YAML templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include audit findings, gate criteria, and handoff materials.]

## Skill Version(s):

2.15.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
