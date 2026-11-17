## Description:

Use when asked to review, edit, tighten, shorten, deduplicate, clean up, or remove slop from an existing agent skill while preserving behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uncmatteth](https://clawhub.ai/user/uncmatteth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to review or edit existing agent skills while preserving behavior, trigger intent, safety boundaries, and host-compatible frontmatter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Edits to skill safety rules, routing metadata, permissions, or tool instructions could alter agent behavior in security-sensitive ways.

Mitigation: Prefer review-only mode for security-sensitive skills and inspect diffs before accepting changes.

Risk: A proposed skill rewrite could remove necessary behavior while shortening or deduplicating instructions.

Mitigation: Preserve the skill's real job, trigger intent, hard safety boundaries, paths, commands, output contracts, and known failure fixes during review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uncmatteth/skills/edit-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown summaries, edited skill text, patches, or concise verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May patch skill files directly for edit-in-repo requests after classifying the task.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
