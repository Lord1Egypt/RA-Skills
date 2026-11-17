## Description:

Designs single-image posters, banners, and infographics as production-ready PNG files using HTML canvas, multi-resolution export, topic-driven palettes, reference-image color extraction, and browser-based visual QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fsyj123](https://clawhub.ai/user/fsyj123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content-producing agents use this skill to create static poster, banner, and infographic deliverables as canvas-based HTML with high-resolution PNG exports. It is most appropriate when the deliverable is a single image rather than a chart, slide deck, or multi-page document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be misapplied to charts, slide decks, multi-page documents, or language-sensitive templates where a single static canvas poster workflow is not the right fit.

Mitigation: Confirm that the requested deliverable is a static single-image poster or banner; choose a charting, presentation, document, or localization-focused tool when the task falls outside that scope.

Risk: High-resolution canvas exports can appear valid while still being blank, incorrectly scaled, or visually incomplete.

Mitigation: Run browser render checks, PNG signature checks, pixel-zone sampling with the bundled QA script, and text-presence checks before delivering exported poster images.

## Reference(s):

- [Canvas Poster Kit on ClawHub](https://clawhub.ai/fsyj123/skills/canvas-poster-kit)
- [Design Patterns - Topic-Driven Palettes and Layout Blocks](references/design-patterns.md)
- [Browser-Based Visual QA](references/browser-qa.md)
- [Multi-Resolution Canvas Export - Deep Dive](references/multi-resolution.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Files, Shell commands]

**Output Format:** [Markdown guidance with HTML/JavaScript canvas code, Python QA commands, and PNG export instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces static single-image poster workflows with 1x, 2K, and 4K PNG export patterns.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
