## Description:

Provides physics-based, data-grounded Earth science reasoning with explicit uncertainty for geology, wells, seismic, petrophysics, and subsurface analyses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ariffazil](https://clawhub.ai/user/ariffazil)

### License/Terms of Use:

MIT-0

## Use Case:

Geoscience analysts, developers, and agents use this skill to ground geology, wells, seismic, petrophysics, and subsurface reasoning in observations, derived data, explicit interpretation labels, and uncertainty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation terms such as pressure, depth, formation, or structure may influence unrelated answers.

Mitigation: Narrow routing or confirm geoscience context before applying the skill when terms are ambiguous.

Risk: Subsurface interpretations can be misleading when observations, derived values, interpretations, and speculation are mixed together.

Mitigation: Use the skill's OBS, DER, INT, and SPEC labels and preserve uncertainty bands for quantitative claims.

Risk: Safety-critical geoscience topics such as HPHT wells, unknown pressure regimes, H2S, or CO2 storage require extra review.

Mitigation: Apply the documented hold conditions and pause before making operational recommendations when safety-critical conditions are present.

## Reference(s):

- [GEOX Epistemic Labels Usage Guide](references/epistemic-labels.md)
- [GEOX Hold Conditions](references/hold-conditions.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text guidance with OBS, DER, INT, and SPEC labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution or data access; responses should preserve uncertainty and apply hold conditions for under-supported or safety-critical geoscience conclusions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
