## Description:

Transform reference photographs and visually dense images into sparse, recognizable, high-saturation flat-vector-style illustrations through semantic compression rather than literal tracing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[createlafont](https://clawhub.ai/user/createlafont)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to convert supplied reference images into clean, low-complexity flat illustrations while preserving recognizable identity, composition, and spatial relationships.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided images may be sent to the configured image-generation provider.

Mitigation: Use the skill only when that provider data flow is acceptable, and avoid submitting sensitive or restricted images unless approved.

Risk: The output is vector-style raster artwork and may be mistaken for an editable SVG or true vector file.

Mitigation: Use an SVG-capable workflow when editable vector output is required, or present the result as vector-style raster output.

Risk: Generated illustrations may retain unwanted source text, logos, watermarks, UI elements, or excessive detail.

Mitigation: Apply the artifact's source-cleanup and visual-validation checks before delivery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/createlafont/skills/dnr-flat-pic)
- [Canonical Rendering Contract](references/generation-spec.md)
- [Human-Perceived Semantic Complexity and Budget](references/semantic-complexity.md)
- [Aspect-Ratio Adaptation and Square Icon Conversion](references/aspect-ratio-adaptation.md)
- [Calibration Examples and Failure Modes](references/examples-and-failures.md)

## Skill Output:

**Output Type(s):** [image, guidance]

**Output Format:** [Raster image artifact with minimal text unless the user asks for analysis]

**Output Parameters:** [2D image]

**Other Properties Related to Output:** [Preserves the reference aspect ratio unless another ratio is requested; defaults to semantic complexity 6 out of 10 or lower with solid flat-color fills.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
