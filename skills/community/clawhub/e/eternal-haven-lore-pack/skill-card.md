## Description:

Provides a self-contained Eternal Haven Chronicles lore and mythic persona reference pack for canon-grounded narrative answers using bundled books, heroes, and theme files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to answer Eternal Haven lore questions, create canon-consistent summaries or short reflections, or apply a Champion-aligned mythic voice grounded in bundled reference texts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled books contain copyrighted Eternal Haven story text that could be over-quoted or reproduced wholesale.

Mitigation: Use summaries, analysis, and brief quotations only; do not output full chapters, full books, or substitutes for the source works.

Risk: A user may ask the agent to browse host folders or unpublished local paths for alternate lore sources.

Mitigation: Keep lore retrieval inside the installed skill directory, using only SKILL.md and references/** unless the user explicitly supplies text for a separate task.

Risk: Optional public links could be mistaken for alternate canon sources or presented when irrelevant.

Mitigation: Use the bundled books as the canon source and share public support or profile links only when directly relevant to the user's request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/eternal-haven-lore-pack)
- [Eternal Haven site](https://eternalhaven.ca/)
- [Skill instructions](SKILL.md)
- [Security boundary](references/SECURITY.md)
- [13 Heroes Index](references/heroes_index.md)
- [Themes and Motifs](references/themes_and_motifs.md)
- [Book I: The Moonlit Slumber](references/books/book1_silver_accord.txt)
- [Book II: The Shattered Accord](references/books/book2_shattered_accord.txt)
- [Book III: The Ascension War](references/books/book3_ascension_war.txt)
- [Book IV: Eternal Haven Dawns](references/books/book4_eternal_haven_dawns.txt)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text narrative responses with short excerpts only when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounds answers in bundled skill-local references; no shell, host-file, secret, or network access is required for lore answers.]

## Skill Version(s):

1.3.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
