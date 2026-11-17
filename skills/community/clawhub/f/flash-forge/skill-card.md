## Description:

Generate flashcards from any content. Paste notes, articles, or textbook pages. Get study-ready cards with spaced repetition scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

External users and learners use this skill to turn notes, articles, or textbook material into study-ready flashcards, then review them with spaced repetition and progress tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flashcard content, tags, and review history may be saved locally in a JSON deck file.

Mitigation: Avoid entering highly sensitive study material unless the local storage location and backup practices are acceptable for the user's environment.

Risk: Generated cards may omit context or introduce inaccurate study prompts from the source material.

Mitigation: Review generated flashcards against the original notes before relying on them for study or assessment preparation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/flash-forge)
- [README](README.md)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown study prompts, local JSON deck data, and tab-separated Anki-compatible export text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores flashcard fronts, backs, tags, and review history locally when used with the bundled JavaScript helper.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
