## Description:

Calculate complex buffer recipes with precise measurements for molecular biology and biochemistry applications, including mass and volume calculations, pH considerations, and step-by-step preparation instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theresayao0614-sudo](https://clawhub.ai/user/theresayao0614-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, laboratory staff, and research teams use this skill to generate buffer preparation guidance for common molecular biology and biochemistry buffers such as PBS, RIPA, and TAE. Outputs should be independently checked before lab use because the security evidence flags calculation correctness concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recipe outputs may contain incorrect buffer calculations or ambiguous reagent forms.

Mitigation: Independently verify all masses, volumes, unit conversions, pH targets, and reagent forms against trusted laboratory protocols before preparing buffers.

Risk: Declared tool permissions are broader than the documented local calculator behavior requires.

Mitigation: Install or run only after review, and prefer a corrected release with narrower permissions.

Risk: Laboratory use can create safety or experimental quality issues if generated guidance is followed without local review.

Mitigation: Have qualified lab personnel review outputs, safety data sheets, institutional procedures, and pH or sterility requirements before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/theresayao0614-sudo/skills/buffer-calculator-2)
- [Publisher profile](https://clawhub.ai/user/theresayao0614-sudo)
- [Cold Spring Harbor Protocols](https://cshprotocols.org)
- [Thermo Fisher Buffer Reference](https://www.thermofisher.com/buffers)
- [Sigma-Aldrich Buffer Calculator](https://www.sigmaaldrich.com/biochemicals)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline Python and bash code blocks, plus command-line text output from the bundled calculator script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include buffer component masses, liquid volumes, pH notes, preparation steps, troubleshooting guidance, and calculation examples.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
