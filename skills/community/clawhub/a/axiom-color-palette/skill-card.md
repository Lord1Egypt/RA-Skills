## Description: <br>
Axiom Color Palette generates harmonious color palettes from a provided hex color and can format them as text, JSON, or CSS custom properties. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers can use this skill to generate complementary, analogous, triadic, tetradic, split-complementary, or monochromatic color palettes from a base hex color for design exploration and CSS output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as an image color extractor, but the security evidence says the actual code is a hex-color harmony generator. <br>
Mitigation: Use it only for hex-color harmony generation, or wait for the publisher to align the metadata, documentation, and implementation before relying on image extraction. <br>
Risk: The release license is inconsistent across evidence sources. <br>
Mitigation: Confirm the authoritative license before redistribution or commercial deployment. <br>
Risk: Generated palettes do not include alpha handling or WCAG accessibility scoring. <br>
Mitigation: Run separate contrast and accessibility checks before using generated palettes in production interfaces. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kofna3369/axiom-color-palette) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Implementation summary](artifact/axiom_color_palette.py.auto.md) <br>
- [Test summary](artifact/test_axiom_color_palette.py.auto.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands, guidance] <br>
**Output Format:** [Plain text, JSON, or CSS custom properties] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deterministic local output from a hex color input; no external API calls are indicated.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
