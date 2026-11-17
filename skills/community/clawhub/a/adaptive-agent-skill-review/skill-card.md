## Description:

Reviews skills for staleness, missing gotchas, and improvement opportunities so procedural memory stays accurate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[truenorth-lj](https://clawhub.ai/user/truenorth-lj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to audit skill files, identify stale guidance or missing lessons, and produce reviewed maintenance updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read memory and skill files, edit multiple skill instructions, and commit persistent agent-behavior changes.

Mitigation: Use it only in a controlled skills repository, require a read-only audit first, review diffs before applying them, and require explicit approval before edits, staging, commits, or delegated agent work.

Risk: Memory inputs may contain sensitive or unapproved feedback that should not be incorporated into shared skill instructions.

Mitigation: Restrict memory review to approved non-sensitive feedback files and exclude secrets or private user data from skill updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/truenorth-lj/skills/adaptive-agent-skill-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with summary tables, shell commands, and proposed file edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or apply skill documentation updates when authorized.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
