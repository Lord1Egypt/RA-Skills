## Description:

AI Rebirth loads conversation history from a previous CodeBuddy session into the current session so users can resume, reference, or continue prior work with project-based listing, summary, full, and tail output modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxinli001](https://clawhub.ai/user/chenxinli001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to inspect and load prior CodeBuddy session history when continuing interrupted work or importing previous session context. It can list sessions for a project and print summaries, full transcripts, or the last N conversation turns as Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can print prior CodeBuddy conversation logs that may contain secrets or sensitive project context.

Mitigation: Use summary or tail modes before full-history output, avoid loading sessions likely to contain secrets, and review output before sharing it.

Risk: Session lookup can expose history across projects or from unexpected session identifiers.

Mitigation: Prefer project-scoped listing, load only known session IDs, and confirm the selected session before displaying transcript content.

## Reference(s):

- [AI Rebirth ClawHub release](https://clawhub.ai/chenxinli001/skills/ai-rebirth)
- [Publisher profile](https://clawhub.ai/user/chenxinli001)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown text with command-line examples and session-history summaries or transcripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only session inspection; output may include sensitive prior conversation content.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
