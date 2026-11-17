## Description:

A native UI asset and color toolset for OpenClaw and other AI Agents. Generate SVG placeholders, animated gradients, theme-based palettes, and perform color conversions without hallucination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[douxc](https://clawhub.ai/user/douxc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate SVG placeholders, animated gradients, theme palettes, random colors, and color conversions for UI mockups and frontend assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated asset URLs and API requests may send placeholder text, color choices, or query parameters to the third-party colors-cc.top service.

Mitigation: Do not include secrets, private client names, unreleased product names, or sensitive internal labels in placeholder text or query parameters.

Risk: Generated assets rely on availability and behavior of an external third-party web service.

Mitigation: Use local or static alternatives for private, offline, or high-availability workflows.

Risk: SVG placeholders may be embedded directly into user-facing pages.

Mitigation: Review generated URLs, dimensions, text, attribution settings, and rendered assets before publication.

## Reference(s):

- [Colors CC ClawHub Skill Page](https://clawhub.ai/douxc/skills/colors-cc-skill)
- [Colors CC Live Site](https://colors-cc.top/)
- [LLM-Optimized Documentation](https://colors-cc.top/llms.txt)
- [OpenAPI Specification](https://colors-cc.top/openapi.json)
- [Placeholder Generator](https://colors-cc.top/)
- [Universal Color Converter](https://colors-cc.top/tools/converter)
- [Random Palette Generator](https://colors-cc.top/tools/random-palette)
- [CSS Color Names Reference](https://colors-cc.top/tools/color-names)

## Skill Output:

**Output Type(s):** [text, markdown, code, API calls, guidance]

**Output Format:** [Markdown with inline HTML, JavaScript examples, API URLs, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated SVG placeholders may include a colors-cc.top attribution watermark unless disabled with the documented attribution parameter.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
