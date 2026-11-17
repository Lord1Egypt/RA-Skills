## Description:

Generates zero-dependency HTML presentations with 21 design presets, visual style exploration, presentation and speaker modes, and support for pitch decks, product launches, and technical talks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaisersong](https://clawhub.ai/user/kaisersong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, presenters, and content creators use this skill to plan, generate, review, and refine browser-based HTML slide decks from prompts, notes, existing plans, or PowerPoint content. It supports quick drafts, deeper narrative planning, style selection, speaker mode, and in-browser editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated decks may include a Ctrl/Cmd+S save behavior that can upload the edited presentation back to the hosting path.

Mitigation: Review the generated HTML before hosting and remove or replace the PUT save behavior with local download-only saving.

Risk: Optional Python package installation for PowerPoint extraction introduces normal third-party package risk.

Mitigation: Pin package versions and use a disposable virtual environment when installing optional dependencies.

Risk: Generated decks include a kai-slide-creator watermark by default.

Mitigation: Confirm that the watermark is acceptable for the intended audience before distribution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaisersong/skills/genppt)
- [Project Homepage](https://github.com/kaisersong/slide-creator)
- [Live Demo](https://kaisersong.github.io/slide-creator/demos/blue-sky-en.html)
- [Workflow Reference](artifact/references/workflow.md)
- [HTML Template Reference](artifact/references/html-template.md)
- [Review Checklist](artifact/references/review-checklist.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions and generated zero-dependency HTML presentation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated decks can include presenter mode, editable slide content, speaker notes, preset-specific CSS, and a kai-slide-creator watermark.]

## Skill Version(s):

2.14.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
