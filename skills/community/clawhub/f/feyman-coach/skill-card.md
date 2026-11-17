## Description:

A personal knowledge coach based on the Feynman technique that helps users review concepts, diagnose weak points, receive study suggestions, and optionally schedule daily reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lewisbase](https://clawhub.ai/user/lewisbase)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to run Feynman-technique study reviews over a Markdown note vault, generate diagnostic reports, practice weak points, and create review tasks or flashcards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can scan a Markdown note vault and write generated review files.

Mitigation: Use a narrow vault path, run with dry-run or manual review first, and confirm where generated notes will be written before enabling routine use.

Risk: The documentation recommends persistent automation through scheduled tasks and GitHub Actions.

Mitigation: Do not enable scheduled tasks, repository pushes, or third-party sync until the exact command, target path, and write behavior have been reviewed.

Risk: The setup guidance includes administrator PowerShell usage that may be unnecessary for normal operation.

Mitigation: Prefer non-administrator manual execution where possible and avoid elevated setup unless the environment requires it.

## Reference(s):

- [Published ClawHub skill page](https://clawhub.ai/lewisbase/skills/feyman-coach)
- [Feynman Technique reference](https://fs.blog/feyman-technique/)
- [Obsidian Spaced Repetition plugin](https://github.com/st3v3nmw/obsidian-spaced-repetition)
- [Anki flashcards](https://apps.ankiweb.net/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate Markdown review tasks, diagnostic reports, study suggestions, and flashcard-style review content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
