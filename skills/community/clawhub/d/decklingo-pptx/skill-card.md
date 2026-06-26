## Description: <br>
Translate editable PowerPoint decks into Chinese, English, Japanese, and other target languages while preserving layout, glossary consistency, and editability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neabigmo](https://clawhub.ai/user/Neabigmo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to translate editable PPTX decks while preserving layout and terminology. It is suited for presentation localization workflows that need optional speaker-note, layout, master, glossary, skip-pattern, dry-run, scan, and verification support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Editable slide text, speaker notes, layouts, or masters may be sent to a Google-backed translation dependency. <br>
Mitigation: Use only with decks approved for external translation, add an explicit consent step before translation, and avoid confidential, regulated, or customer-sensitive decks unless data handling is reviewed. <br>
Risk: Unpinned runtime dependencies may change behavior over time. <br>
Mitigation: Pin and review dependencies before deploying the skill in controlled or commercial environments. <br>
Risk: Translated output can preserve layout imperfectly or leave source-language text in inherited editable objects. <br>
Mitigation: Run the scan or dry-run workflow first, choose the required slide, note, layout, and master scope, and re-scan the translated deck before delivery. <br>


## Reference(s): <br>
- [DeckLingo for PPTX homepage](https://github.com/Neabigmo/DeckLingo-for-PPTX) <br>
- [ClawHub skill page](https://clawhub.ai/Neabigmo/decklingo-pptx) <br>
- [Glossary Schema](references/glossary-schema.md) <br>
- [Translation Modes](references/translation-modes.md) <br>
- [Platform Compatibility](references/platform-compatibility.md) <br>
- [Changelog](references/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON reports, and PPTX file outputs from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce translated PPTX files, scan summaries, dry-run output, and optional machine-readable translation reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
