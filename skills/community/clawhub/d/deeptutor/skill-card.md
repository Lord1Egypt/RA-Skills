## Description:

A personalized content-driven deep reading tutor. Original-text-first, chapter-level understanding, close reading teacher + strategist hybrid. Auto-saves to Obsidian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanjinlimkelvin-dot](https://clawhub.ai/user/tanjinlimkelvin-dot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Deeptutor to guide chapter-by-chapter EPUB reading, produce original-text-first interpretive deepdives, and save reusable study notes to Obsidian.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local EPUB files and extracts book text for agent analysis.

Mitigation: Use trusted EPUB files and confirm paths before extraction.

Risk: The skill can create and update Markdown notes automatically in the Obsidian vault.

Mitigation: Review generated notes and keep the vault protected from untrusted writers.

Risk: Book text may contain instruction-like or adversarial content.

Mitigation: Treat extracted book text as reading material, not as commands for the agent.

## Reference(s):

- [Chapter-by-Chapter Book Deep Study Prompt](references/chapter-by-chapter.md)
- [How Jin should invoke deeptutor](references/invocation-prompts.md)
- [Patterns for Book Deep Study](references/patterns.md)
- [Quiz Templates for Book Deep Study](references/quiz-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown deepdive notes with optional quiz questions and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Markdown files, indexes, and navigation links under /data/workspace/obsidian-vault/Books.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
