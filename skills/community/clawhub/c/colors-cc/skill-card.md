## Description:

A native UI asset and color toolset for OpenClaw and other AI Agents. Generate SVG placeholders, animated gradients, theme-based palettes, and perform color conversions without hallucination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[douxc](https://clawhub.ai/user/douxc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agents use Colors CC to create SVG placeholders, animated gradients, theme palettes, color conversions, and CSS color-name lookups for UI mockups and generated application assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated placeholder and API URLs contact a third-party remote service and may expose URL text or internal identifiers.

Mitigation: Do not include confidential text or internal identifiers in placeholder URLs.

Risk: Remote placeholders may be unsuitable when output integrity, privacy, or offline use is required.

Mitigation: Disable attribution where appropriate and use local or self-hosted assets for privacy-sensitive or offline workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/douxc/skills/colors-cc)
- [Colors CC live site](https://colors-cc.top/)
- [LLM-optimized documentation](https://colors-cc.top/llms.txt)
- [OpenAPI specification](https://colors-cc.top/openapi.json)
- [Universal Color Converter](https://colors-cc.top/tools/converter)
- [Random Palette Generator](https://colors-cc.top/tools/random-palette)
- [CSS Color Names Reference](https://colors-cc.top/tools/color-names)
- [Fluid Gradient Placeholder](https://colors-cc.top/tools/fluid-placeholder)

## Skill Output:

**Output Type(s):** [Markdown, Code, API calls, Guidance]

**Output Format:** [Markdown with inline HTML, JavaScript examples, API URLs, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include third-party service URLs; placeholder dimensions are clamped and placeholder text is truncated by the service.]

## Skill Version(s):

0.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
