## Description: <br>
AI PPT creation skill with structured 5-stage generation, machine-readable QA gates, checkpoint recovery, experience accumulation, native charts, visual QA, automated gate checks, and multi-canvas output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simon2256928](https://clawhub.ai/user/simon2256928) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and presentation authors use DeckCraft to create editable PowerPoint decks from briefs, outlines, source documents, and structured content while preserving machine-readable QA checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted PDFs, DOCX files, images, or fetched web content may exercise document and image parsing dependencies. <br>
Mitigation: Keep Python dependencies current or pinned through a lockfile, and process untrusted inputs in an isolated workspace before using generated deck outputs. <br>
Risk: Generated presentation content or layout diagnostics may still contain incorrect, misleading, or unsuitable material. <br>
Mitigation: Review the deck, inspect rendered previews when available, and rely on machine-readable gate JSON rather than verbal pass/fail claims before delivery. <br>


## Reference(s): <br>
- [DeckCraft README](README.md) <br>
- [DeckCraft Skill Specification](SKILL.md) <br>
- [DeckCraft Changelog](CHANGELOG.md) <br>
- [DeckCraft Migration Guide](MIGRATION.md) <br>
- [Design Spec Template](templates/design_spec.md) <br>
- [DeckCraft on ClawHub](https://clawhub.ai/simon2256928/deckcraft) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [PPTX files, JSON gate reports, Markdown plans or reports, and Python or shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces editable PowerPoint content through python-pptx and machine-readable QA outputs for content and render gates.] <br>

## Skill Version(s): <br>
6.0.0 (source: changelog, released 2026-06-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
