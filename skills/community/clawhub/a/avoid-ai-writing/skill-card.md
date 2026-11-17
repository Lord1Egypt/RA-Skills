## Description:

Audits and rewrites prose to remove AI-writing patterns, with detect-only, edit-in-place, voice-profile, and convergence modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conorbronsdon](https://clawhub.ai/user/conorbronsdon)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, marketers, and developers use this skill to audit drafts for AI-like phrasing, rewrite editable passages, or make targeted file edits while preserving quoted, code, table, and attributed content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-writing signals can produce false positives and should not be treated as proof of authorship.

Mitigation: Use the skill as a writing-quality aid, review the cited flags in context, and avoid consequential authorship judgments based only on its output.

Risk: Edit-in-place mode can change user files.

Mitigation: Review edits before accepting them and keep changes minimal, preserving quoted material, code blocks, tables, and attributed text.

Risk: Rewrites can accidentally add facts, stance, or voice that were not present in the source.

Mitigation: Limit edits to subtraction, clarification, and sharpening of source material; do not add unsourced specifics or invented author persona.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/conorbronsdon/skills/avoid-ai-writing)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)
- [brandonwise/humanizer](https://github.com/brandonwise/humanizer)
- [blader/humanizer](https://github.com/blader/humanizer)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Pangram Labs](https://www.pangram.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown audit reports, rewritten prose, edit summaries, and targeted file edits when edit mode is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Detect, rewrite, and edit modes; optional voice profiles; second-pass audit for rewrite convergence.]

## Skill Version(s):

3.22.3 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
