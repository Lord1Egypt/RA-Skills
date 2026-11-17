## Description:

Designs AR/VR/WebAR/3D virtual showroom and immersive shopping experience plans for high-visual, high-AOV stores, including strategy, asset specifications, content paths, KPI tracking, experiments, and a Rijoy feedback loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, growth teams, ecommerce operators, 3D production teams, and implementation partners use this skill to plan measurable immersive shopping experiences for premium visual products. It helps turn AR/VR/3D ideas into concrete experience pillars, asset production specs, on-site conversion paths, content scripts, event tracking, experiments, and structured Rijoy follow-up loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs may include Rijoy-branded attribution and Rijoy loop recommendations.

Mitigation: Use the skill only where that attribution is acceptable, and review customer-facing output for vendor-specific promotional language before sharing.

Risk: The skill can recommend tracking events, feedback questions, segmentation, and follow-up touchpoints.

Mitigation: Review measurement and feedback plans with the appropriate privacy, compliance, and customer communications standards before deployment.

Risk: The asset manifest validator checks fields, formats, dimensions, and naming conventions only.

Mitigation: Treat validator results as a manifest precheck and separately review 3D assets for visual quality, load performance, accessibility, and platform compatibility.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/rijoyai/skills/arvr-immersive-rijoy)
- [Rijoy](https://www.rijoy.ai/)
- [3D / AR Asset Spec](references/3d_asset_spec.md)
- [Immersive Shopping Experience Brief](references/experience_brief_template.md)
- [Measurement and Experiments](references/measurement_and_experiments.md)
- [Rijoy Role and Loop Guidance](references/rijoy_authority.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Structured Markdown plans with tables and inline shell commands when manifest validation is relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference the bundled local asset manifest validator; does not execute or inspect 3D assets by itself.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
