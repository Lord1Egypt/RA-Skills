## Description:

Memory file maintenance and optimization system that moves factual content from MEMORY.md into dedicated facts files while preserving core rules, indexes, and agent capability information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[webray1983](https://clawhub.ai/user/webray1983)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to reorganize long-term agent memory when factual project, portfolio, preference, or event information accumulates in MEMORY.md. It creates a facts directory, updates a Quick Index, and preserves core behavior and capability information in the primary memory file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can rewrite persistent memory files and move content between MEMORY.md and memory/facts files.

Mitigation: Create a timestamped backup of MEMORY.md and memory/facts before migration, then verify that core rules, tool descriptions, installed skills, and capability definitions remain intact.

Risk: The skill includes deletion guidance for redundant, outdated, or duplicate memory entries.

Mitigation: Require an itemized dry-run list of every keep, move, rewrite, and delete action, and obtain separate approval before deleting any content.

## Reference(s):

- [Clear-Mind Skill on ClawHub](https://clawhub.ai/webray1983/skills/clear-mind)
- [Publisher profile: webray1983](https://clawhub.ai/user/webray1983)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files, Configuration]

**Output Format:** [Markdown guidance with file-organization plans and memory file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or modify MEMORY.md and memory/facts files after user review.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
