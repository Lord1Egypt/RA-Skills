## Description: <br>
Generate color palettes and get color suggestions via the Colormind.io API, including listing models and generating palettes with optional locked colors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boilerrat](https://clawhub.ai/user/boilerrat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and agents use this skill to list Colormind models, generate five-color palettes, lock selected RGB colors, and derive a palette from sampled image colors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Palette colors and image-derived RGB values are sent to colormind.io over unencrypted HTTP. <br>
Mitigation: Use this skill only for non-sensitive palettes and avoid private photos, confidential design work, and proprietary brand colors. <br>
Risk: Image sampling depends on ImageMagick and may process local image files. <br>
Mitigation: Keep ImageMagick patched, process only trusted images, and use sandboxing for automated or higher-risk workflows. <br>


## Reference(s): <br>
- [Colormind API endpoint](http://colormind.io/api/) <br>
- [Colormind model list endpoint](http://colormind.io/list/) <br>
- [ClawHub release page](https://clawhub.ai/boilerrat/colormind) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON with optional Markdown palette summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Palette output includes RGB arrays and may include hex color summaries when pretty output is requested.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
