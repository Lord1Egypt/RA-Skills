## Description:

Generate CSS and SVG animation code snippets using bash and Python for UI animations, keyframes, transitions, motion paths, and easing effects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to generate reusable CSS and SVG animation snippets, preview animations in HTML, and export animation definitions for UI implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated exports and previews can write to caller-selected output paths.

Mitigation: Review output paths before execution and avoid allowing untrusted prompts or project content to choose writable destinations.

Risk: Stored animation content is embedded into generated preview HTML without sanitization.

Mitigation: Use trusted animation names and values, and open generated preview HTML cautiously in an isolated or low-risk browser context.

## Reference(s):

- [Animation skill page](https://clawhub.ai/ckchzh/skills/animation)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [JSON responses, raw CSS/SVG code, shell command examples, and self-contained HTML previews]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated animation records may be stored locally and exported to caller-selected CSS, SVG, or HTML files.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
