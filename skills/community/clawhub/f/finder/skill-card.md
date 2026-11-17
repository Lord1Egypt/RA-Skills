## Description:

Find files by name, size, date, and type with deduplication. Use when searching filesystems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Finder to locate files during filesystem inspection by name pattern, minimum size, recency, extension, emptiness, or largest size.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted patterns, paths, sizes, extensions, day values, or counts can be interpreted as command syntax during local file searches.

Mitigation: Use only trusted inputs until the script corrects argument indexing, quotes expansions, and validates each command parameter.

Risk: Recursive filesystem scans may traverse sensitive or unexpectedly large directory trees.

Mitigation: Limit searches to intended directories and document recursive scan behavior before deploying the skill.

## Reference(s):

- [Finder on ClawHub](https://clawhub.ai/bytesagain3/skills/finder)
- [Publisher profile: bytesagain3](https://clawhub.ai/user/bytesagain3)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash command examples and shell output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Most commands print up to 20 matching paths; the largest-file command prints a requested count.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
