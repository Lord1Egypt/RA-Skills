## Description:

Generate visually unified image-based PPT/PPTX decks from articles, reports, papers, notes, or outlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ningzimu](https://clawhub.ai/user/ningzimu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to turn source material into visually unified, image-based PowerPoint decks with slide images, speaker notes, and assembly guidance. It is best suited for decks where full-slide generated images are acceptable rather than separately editable text boxes, charts, and shapes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional API fallback and shared local runtime can store API credentials and send presentation text or selected images to an image provider.

Mitigation: Prefer the built-in image tool when available, avoid untrusted OPENAI_BASE_URL values, and do not place real API keys directly in command lines.

Risk: Persistent saved styles under the local Codex PPT home can be reused in later deck generation.

Mitigation: Review files under ~/.codex-ppt-skill/references before allowing the skill to reuse saved styles.

Risk: The security verdict is suspicious because credential and data-handling behavior need review before installation.

Mitigation: Review the skill and its runtime configuration before deployment, especially API provider settings and any content sent for image generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ningzimu/skills/codex-ppt)
- [Project homepage](https://github.com/ningzimu/codex-ppt-skill)
- [Backend selection](docs/backend-selection.md)
- [CLI/API fallback](docs/cli-api-fallback.md)
- [Project assembly and reporting](docs/project-assembly-and-reporting.md)
- [Slide generation and subagents](docs/slide-generation-and-subagents.md)
- [User-supplied assets](docs/user-supplied-assets.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON job files, PNG slide images, speaker notes, and PPTX deck files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces full-slide 16:9 image pages and assembled PPTX decks; optional CLI/API fallback may use local configuration and external image providers.]

## Skill Version(s):

0.6.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
