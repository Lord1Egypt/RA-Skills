## Description:

DeckLingo for PPTX helps agents translate editable PowerPoint decks across languages while preserving layout, glossary consistency, speaker notes, and editability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neabigmo](https://clawhub.ai/user/neabigmo)

### License/Terms of Use:

MIT

## Use Case:

Developers, localization teams, and presentation authors use this skill to scan and translate editable PPTX slides, speaker notes, layouts, or masters while applying glossaries and checking for remaining source-language text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected deck text can be sent to Google through deep-translator.

Mitigation: Review before installing on confidential decks and use only when sending selected PPTX text to Google is acceptable.

Risk: The security summary reports world-writable presentation files.

Mitigation: Run the skill in a private or isolated directory and adjust output file permissions before sharing translated decks.

Risk: Untrusted PPTX files are processed locally as ZIP/XML containers.

Mitigation: Avoid untrusted PPTX inputs or inspect them in an isolated environment before translating.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/neabigmo/skills/decklingo-pptx)
- [Project Homepage](https://github.com/Neabigmo/DeckLingo-for-PPTX)
- [Glossary Schema](references/glossary-schema.md)
- [Translation Modes](references/translation-modes.md)
- [Platform Compatibility](references/platform-compatibility.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands, translated PPTX files, and optional JSON scan or translation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write output decks, backup files, and report files when the bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
