## Description:

Coding style memory that adapts to your preferences, conventions, and patterns for consistent coding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chayjan](https://clawhub.ai/user/chayjan)

### License/Terms of Use:


## Use Case:

Developers and coding agents use this skill to remember explicit coding preferences, apply them in future code work, and manage local preference memory on request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent coding preferences may be written across sessions without enough user clarity.

Mitigation: Require explicit confirmation before each write to ~/coding/memory.md and show the exact preference that will be stored.

Risk: Runtime resources could be confused with writable skill state.

Mitigation: Treat SKILL.md, criteria.md, dimensions.md, and memory-template.md as read-only references; store mutable memory only under ~/coding.

Risk: Stored preferences may become stale, vague, or inconsistent.

Mitigation: Keep entries short, allow users to inspect or forget preferences, and archive or merge old entries when memory approaches the documented limit.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chayjan/skills/coding-1-0-3)
- [Skill Homepage](https://clawic.com/skills/coding)
- [Preference Criteria](criteria.md)
- [Code Preference Dimensions](dimensions.md)
- [Memory Templates](memory-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with concise text and inline shell commands when local memory setup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local preference memory files under ~/coding after explicit user confirmation.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter and artifact/_meta.json); server release version 1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
