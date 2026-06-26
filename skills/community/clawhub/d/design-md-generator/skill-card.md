## Description: <br>
Generate DESIGN.md files from any website URL, extracting colors, typography, spacing, components, and shadows into structured Markdown that AI coding agents can use to build visually consistent UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wavmson](https://clawhub.ai/user/wavmson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and design-focused agents use this skill to inspect a public or authorized website and turn its visual system into a reusable DESIGN.md file. The output helps downstream coding agents reproduce the target site's look with matching colors, typography, layout rules, component states, and prompt guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens user-provided websites and extracts visual design information, which can expose page content or browsing context. <br>
Mitigation: Use public or authorized URLs, avoid authenticated or sensitive pages unless intentional, and review generated DESIGN.md files before reusing them as agent context. <br>
Risk: Browser-based analysis of untrusted sites can carry browser sandbox and content-execution risk. <br>
Mitigation: Prefer an isolated environment when inspecting untrusted URLs and keep browser tooling current. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wavmson/design-md-generator) <br>
- [DESIGN.md Format Specification](references/format-spec.md) <br>
- [Linear DESIGN.md Example](references/example-linear.md) <br>
- [Google Stitch DESIGN.md Format](https://stitch.withgoogle.com/docs/design-md/format/) <br>
- [Google Stitch DESIGN.md Overview](https://stitch.withgoogle.com/docs/design-md/overview/) <br>
- [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Guidance] <br>
**Output Format:** [Markdown DESIGN.md with optional HTML previews and JSON token extraction output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated DESIGN.md files follow a 9-section visual design system format and may include local preview files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
