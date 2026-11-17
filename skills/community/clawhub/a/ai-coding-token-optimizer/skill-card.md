## Description:

Helps coding agents reduce always-loaded project instructions and build task-focused documentation maps without changing application behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asif2bd](https://clawhub.ai/user/asif2bd)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to slim coding-agent instruction files, create navigable project documentation, and verify that required rules and links remain intact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Edits to AGENTS.md or CLAUDE.md can change how agents behave on later tasks.

Mitigation: Review the documentation diff and preserve mandatory instructions and release gates before keeping the changes.

Risk: Project details or secrets could be exposed in an optional feedback report.

Mitigation: Remove sensitive details, let the user review the redacted report, and never submit it automatically.

Risk: Documentation mapping could overstep into application changes or release actions.

Mitigation: Limit changes to documentation and do not commit, push, or deploy unless separately requested.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/asif2bd/skills/ai-coding-token-optimizer)
- [ProSkills skill homepage](https://proskills.md/skills/coding/ai-coding-token-optimizer)
- [Adoption guide](artifact/references/adoption.md)
- [Verification guide](artifact/references/verification.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Project instruction files, documentation maps, and a Markdown validation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports per-agent before/after instruction sizes and approximate token counts; feedback is optional and never sent automatically.]

## Skill Version(s):

1.2.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
