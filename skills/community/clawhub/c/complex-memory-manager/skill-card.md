## Description:

Privacy-aware structured memory management for AI agents using a three-tier model for public, internal, and private memory handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bustes01](https://clawhub.ai/user/bustes01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to define persistent cross-session memory practices, including public usage statistics, internal agent memory entries, private data exclusions, and periodic cleanup routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tier 2 memory uses XOR plus Base64, which should not be treated as strong protection for sensitive information.

Mitigation: Treat Tier 2 entries as readable by anyone with file access and do not store secrets, personal data, or regulated information through this skill.

Risk: The cleanup protocol can delete, merge, or archive persistent memory entries.

Mitigation: Require manual approval or a dry run before cleanup actions modify stored memory.

## Reference(s):

- [ClawHub skill homepage](https://clawhub.ai/BusTes01/complex-memory-manager)
- [ClawHub skill page](https://clawhub.ai/bustes01/skills/complex-memory-manager)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON examples, Python snippets, file path conventions, and procedural cleanup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory handling conventions rather than executable enforcement; cleanup actions require agent or user execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
