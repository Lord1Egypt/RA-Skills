## Description:

Use this skill when the user wants to extract a webpage's design language into a reusable HTML style reference file, including typography, colors, spacing, surfaces, components, states, themes, motion, code-block styles, background atmosphere, decorative motifs, and art direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vintlin](https://clawhub.ai/user/vintlin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to extract a webpage's visual system into reusable design tokens, component archetypes, JSON manifests, and style specimen HTML that can guide future AI-generated pages without cloning the original page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser-based webpage access, which can expose an agent environment to untrusted, private-network, localhost, or cloud metadata URLs if pointed at them.

Mitigation: Run it in an isolated project or virtual environment, prefer public and trusted target URLs, and avoid localhost, private network, cloud metadata, or sensitive internal pages.

Risk: Generated output paths can place intermediate or extracted design files outside the intended skill asset area if the operator intentionally overrides them.

Mitigation: Keep output under the skill's assets/theme directory unless a separate intermediate file location is intentionally reviewed.

Risk: The workflow depends on Playwright and some sample HTML specimens may load external fonts when opened.

Mitigation: Pin Playwright in controlled environments and review whether external font loading is acceptable before opening or distributing specimens.

## Reference(s):

- [Extract Design ClawHub release](https://clawhub.ai/vintlin/skills/extract-design)
- [Extraction checklist](references/extraction-checklist.md)
- [Style specimen template](references/style-specimen.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, HTML]

**Output Format:** [Concise extraction summary plus generated JSON style manifest and self-contained HTML style specimen files; may include shell commands for Playwright-based extraction.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are normally saved under the skill's assets/theme directory with source-specific filenames.]

## Skill Version(s):

1.0.1 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
