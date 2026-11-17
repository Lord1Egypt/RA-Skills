## Description:

Guides DSH audits and upgrades through a repeatable governance loop spanning runtime fixes, requirements, design, testing, handoffs, acceptance gates, and documented iteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linboomboom](https://clawhub.ai/user/linboomboom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and DSH operators use this skill to audit and improve a DSH environment, then coordinate project work across requirements, design, testing, handoff, and acceptance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the skill suspicious due to reported potentially destructive cleanup, unsafe package contents, and advice to weaken antivirus protection.

Mitigation: Review directory-deletion behavior and package contents and assess the antivirus guidance before installation; consider avoiding installation until those checks are complete.

Risk: Coverage was partial: 37 of 40 components were fully inspected, and the scan does not establish that all behavior is safe.

Mitigation: Review the three partially inspected components before relying on the release.

## Reference(s):

- [Quickstart](QUICKSTART.md)
- [Capability audit workflow](references/10-audit.md)
- [Runtime fixes](references/20-runtime-fix.md)
- [Design and team workflow](references/50-design-team.md)
- [Handoff workflow](references/60-handoff.md)
- [ClawHub release page](https://clawhub.ai/linboomboom/skills/dsh-capability-loop)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code]

**Output Format:** [Markdown guidance, reports, checklists, and handoff documents with PowerShell and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use the included templates and scripts; environment-specific checks require the user's DSH and project paths.]

## Skill Version(s):

2.9.5 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
