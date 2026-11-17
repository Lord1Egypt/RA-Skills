## Description:

Extracts pile IDs, coordinates, diameters, top elevations, and optional rock-surface interpolation results from pile foundation DXF drawings into Excel summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxp1941](https://clawhub.ai/user/sxp1941)

### License/Terms of Use:

MIT-0

## Use Case:

Civil, geotechnical, and estimating teams use this skill to extract pile-foundation parameters from DXF drawings, summarize quantities in Excel, interpolate weathered rock elevations from contour layers, calculate rock embedment depths, and optionally label piles back into DXF output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The interpolation step updates the provided Excel workbook directly.

Mitigation: Run the workflow on copies of important DXF and Excel files before using the results operationally.

Risk: DXF layer conventions, contour coverage, and elevation datum assumptions can affect extracted coordinates, pile elevations, and embedment-depth calculations.

Mitigation: Review the DXF structure analysis, confirm the datum and target layers, and manually check edge cases such as incomplete contour coverage or negative layer thickness.

## Reference(s):

- [DXF pile drawing patterns](references/dxf_pile_patterns.md)
- [ClawHub skill page](https://clawhub.ai/sxp1941/skills/dxf-pile-extraction)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands; scripts produce Excel workbooks, console analysis, and optional DXF output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Works with user-provided DXF drawings and Excel workbooks; interpolation updates the provided workbook in place.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
